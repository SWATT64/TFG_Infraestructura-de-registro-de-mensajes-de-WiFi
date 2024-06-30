import json
import logging
from pathlib import Path
import subprocess
import zipfile
import connexion
from flask import send_from_directory
import six
import os
from swagger_server.database import db
from sqlalchemy import and_, desc
from werkzeug.utils import secure_filename

from swagger_server.models.groups import Groups  # noqa: E501
from swagger_server.models.groups_database import GroupDataBase
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response404 import InlineResponse404  # noqa: E501
from swagger_server.models.inline_response500 import InlineResponse500  # noqa: E501
from swagger_server.models.job_specification import JobSpecification  # noqa: E501
from swagger_server.models.jobs_database import JobDataBase
from swagger_server.models.network_detail import NetworkDetail
from swagger_server.models.probe import Probe  # noqa: E501
from swagger_server import util
from swagger_server.models.probe_database import ProbeDataBase
logger = logging.getLogger(__name__)  # Obtener el logger para el módulo actual

def create_job(group_id, body=None):  # noqa: E501
    """Registra el trabajo al grupo

    Registra el trabajo al grupo # noqa: E501

    :param group_id: ID del grupo a consultar
    :type group_id: int
    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2002
    """
    if connexion.request.is_json:
        body = JobSpecification.from_dict(connexion.request.get_json())
        
        # Marcar todos los trabajos anteriores activos como inactivos
        previous_jobs = JobDataBase.query.filter(
            and_(JobDataBase.group_id == group_id, JobDataBase.is_active == True)
        ).all()
        for job in previous_jobs:
            job.is_active = False

        # Crear el nuevo trabajo
        job_db = JobDataBase(
            group_id=group_id,
            Status=body.job.status,
            is_active=True  # Asume que los nuevos trabajos son activos por defecto
        )

        # Si el trabajo es "scan" asignamos los detalles adicionales
        if body.job.status == "scan":
            job_db.BSSID = body.job.bssid
            job_db.ESSID = body.job.essid
            job_db.Channel = body.job.channel
            job_db.WaveLength = body.job.wave_lenght
            job_db.Status = body.job.status
            job_db.band = body.job.band
            job_db.cswitch = body.job.cswitch
            job_db.security = body.job.security
            job_db.wildcard = body.job.wildcard
            job_db.associated_clients = body.job.associated_clients
            job_db.ChannelMode = body.job.channel_mode

        db.session.add(job_db)
        db.session.flush()  # Flush to get the JobID before committing

        # Asignar URL si es necesario y no es un trabajo 'stop'
        if body.job.status != "stop":
            job_db.URL = f"http://localhost:8080/v1/probes-groups/{group_id}/jobs/{job_db.JobID}/{job_db.Status}"

        db.session.commit()
        return InlineResponse2002(job_id=job_db.JobID)  # Asume que InlineResponse2002 puede manejar el job_id



def delete_group(group_id):  # noqa: E501
    """Eliminar un grupo de sondas

    Eliminar un grupo de sondas dado el ID # noqa: E501

    :param group_id: ID del grupo de sondas a eliminar
    :type group_id: int

    :rtype: None
    """
    group = db.session.query(GroupDataBase).filter_by(id=group_id).one_or_none()
    if not group:
        return {"error": "Group not found"}, 404

    # Desasignar todas las sondas asociadas con este grupo
    probes_in_group = db.session.query(ProbeDataBase).filter_by(group_id=group_id).all()
    for probe in probes_in_group:
        probe.group_id = None
    
    group.is_active = False  # Desactivar el grupo
    db.session.commit()
    return {"message": "Group deactivated and all assigned probes unassigned"}, 200


def get_group_job(group_id):  # noqa: E501
    """Accede a todos los trabajos realizados por el grupo

    Accede a todos los trabajos realizados por el grupo # noqa: E501

    :param group_id: ID del grupo a consultar
    :type group_id: int

    :rtype: List[JobSpecification]
    """

    # Ordena los trabajos por estado activo y fecha de creación
    jobs = JobDataBase.query.filter_by(group_id=group_id).order_by(desc(JobDataBase.is_active), desc(JobDataBase.created_at)).all()

    try:
        job_specs = [JobSpecification.from_db(job) for job in jobs]
        return job_specs
    except Exception as error:
        # handle the exception
        print("An exception occurred:", type(error).__name__)
        return None  # O maneja el error de manera que sea apropiado para tu aplicación


def get_job(group_id, job_id):  # noqa: E501
    """Accede a las especificaciones del trabajo

    Devuelve el trabajo realizado por el grupo # noqa: E501

    :param group_id: ID del grupo a consultar
    :type group_id: int
    :param job_id: ID del trabajo a gestionar
    :type job_id: int

    :rtype: JobSpecification
    """
    job = JobDataBase.query.get(job_id)
    if job and job.group_id == group_id:
        return JobSpecification.from_db(job)
    return InlineResponse404(message="Job not found")


def get_monitorize(group_id, job_id):  # noqa: E501
    """Descarga el fichero resultante o el archivo procesado de una operación monitorize

    Descarga el fichero resultante o el archivo procesado de una operación monitorize # noqa: E501

    :param group_id: ID del grupo a consultar
    :type group_id: int
    :param job_id: ID del trabajo a gestionar
    :type job_id: int

    :rtype: str
    """

    # Negociación de contenido basada en el encabezado 'Accept'
    if 'application/json' in connexion.request.headers.get('Accept', ''):
        probes = ProbeDataBase.query.filter_by(group_id=group_id, is_active=True).all()

        # Preparar la lista consolidada de redes
        network_details = []
        # Recorrer todas las sondas y acumular sus redes
        for probe in probes:
            if probe.data and 'networks' in probe.data:
                for network_data in probe.data['networks']:
                    # Crear un objeto NetworkDetail por cada entrada de red y añadirlo a la lista
                    network_detail = NetworkDetail(**network_data)
                    network_details.append(network_detail)
            else:
                continue
        return InlineResponse2004(networks=network_details)
    else:
        base_path = Path(__file__).resolve().parent.parent
        scan_folder = base_path / 'monitorize' / f'Group{group_id}Job{job_id}'

        # Verificar si la carpeta existe
        if not scan_folder.exists() or not scan_folder.is_dir():
            return InlineResponse404({"error": "Folder not found"})
        # Preparar el archivo zip
        zip_filename = f"monitorize_{group_id}_{job_id}.zip"
        zip_filepath = base_path / 'monitorize' / zip_filename

        # Crear un archivo zip con todos los archivos de la carpeta
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for root, dirs, files in os.walk(scan_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, scan_folder)
                    zipf.write(file_path, arcname)

        # Devolver el archivo zip como descarga
        return send_from_directory(directory=scan_folder.parent, path=zip_filename, as_attachment=True)


def get_probe_group_information(group_id):  # noqa: E501
    """Accede a la información del grupo de sondas

    Devuelve la información del grupo de sondas # noqa: E501

    :param group_id: ID del grupo de sondas a consultar
    :type group_id: int

    :rtype: Groups
    """
    grupo = GroupDataBase.query.get(group_id)
    if grupo:
        return Groups.from_db(grupo)
    return InlineResponse404(message="Group not found"), 404


def get_scan(group_id, job_id):  # noqa: E501
    """Descarga el archivo procesado resultante de una operación scan

    Descarga el fichero resultante de una operación scan # noqa: E501

    :param group_id: ID del grupo a consultar
    :type group_id: int
    :param job_id: ID del trabajo a gestionar
    :type job_id: int

    :rtype: str
    """
    base_path = Path(__file__).resolve().parent.parent
    scan_folder = base_path / 'scan' / f'Group{group_id}Job{job_id}'

    # Verificar si la carpeta existe
    if not scan_folder.exists() or not scan_folder.is_dir():
        return {"error": "Folder not found"}, 404

    # Preparar el archivo zip
    zip_filename = f"scan_{group_id}_{job_id}.zip"
    zip_filepath = base_path / 'scan' / zip_filename

    # Crear un archivo zip con todos los archivos de la carpeta
    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for root, dirs, files in os.walk(scan_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, scan_folder)
                zipf.write(file_path, arcname)

    # Devolver el archivo zip como descarga
    return send_from_directory(scan_folder.parent, zip_filename, as_attachment=True)


def probe_group_list(nombre=None, is_active=None):  # noqa: E501
    """Lista y filtra entre todos los grupos de sondas

    Lista todos los grupos de sondas, pudiendo filtrar por nombre para obtener un resultado más óptimo. También permite filtrar grupos por su estado activo/inactivo. # noqa: E501

    :param nombre: Nombre del grupo de sondas a devolver
    :type nombre: str
    :param is_active: Filtra los grupos por su estado activo o inactivo
    :type is_active: bool

    :rtype: List[Groups]
    """
    query = GroupDataBase.query
    if nombre:
        query = query.filter(GroupDataBase.name == nombre)
    if is_active is not None:
        query = query.filter(GroupDataBase.is_active == is_active)
    grupos = query.all()
    return [Groups.from_db(group) for group in grupos]



def probe_group_register(body, nombre):  # noqa: E501
    """Registra un nuevo grupo de sondas

    Registra un nuevo grupo de sondas # noqa: E501

    :param body: Añade un grupo de sondas
    :type body: list | bytes
    :param nombre: Nombre de la sonda a devolver
    :type nombre: str

    :rtype: InlineResponse2001
    """
    if connexion.request.is_json:
        probes = [Probe.from_dict(d) for d in connexion.request.get_json()]
        nuevo_grupo = GroupDataBase(name=nombre)
        db.session.add(nuevo_grupo)
        db.session.commit()
        for probe in probes:
            probe_db = ProbeDataBase.query.get(probe.id)
            if not probe_db or not probe_db.is_active:
                return {"error": "Probe not found or is inactive"}, 404
            if probe_db:
                probe_db.group_id = nuevo_grupo.id
        db.session.commit()
        logger.debug(f"EL ID ES {nuevo_grupo.id}")
        return InlineResponse2001(id=nuevo_grupo.id)
    return 'Invalid request'


def send_work_monitorize(body, group_id, job_id):  # noqa: E501
    """Envía el fichero resultante de una operación monitorize

    Envía el fichero resultante de una operación monitorize # noqa: E501

    :param file: 
    :type file: strstr
    :param probe_id: 
    :type probe_id: int
    :param group_id: ID del grupo a consultar
    :type group_id: int
    :param job_id: ID del trabajo a gestionar
    :type job_id: int

    :rtype: InlineResponse2003
    """

    if 'file' not in connexion.request.files or 'probeId' not in connexion.request.form:
        return {"mensaje": "Falta el archivo o el ID de la sonda"}, 400
    
    # Obtener el archivo de la solicitud
    file = connexion.request.files['file']
    if file.filename == '':
        return {"mensaje": "No se ha seleccionado ningún archivo"}, 400

    # Intentar obtener el probeId, asegurándose de que se pueda convertir a entero
    try:
        probe_id = int(connexion.request.form['probeId'])
    except ValueError:
        return {"mensaje": "El ID de la sonda debe ser un número entero"}, 400
   # Verificar que el grupo y el trabajo existen y están activos
    grupo = GroupDataBase.query.filter_by(id=group_id, is_active=True).first()
    if not grupo:
        return {"error": "Group not found or is inactive"}, 404

    trabajo = JobDataBase.query.filter(JobDataBase.JobID ==job_id).first()
    if not trabajo or trabajo.group_id != group_id:
        return {"error": "Job not found or is not associated with this group"}, 404
    
    # Ruta base del código
    base_path = Path(__file__).resolve().parent.parent
    upload_folder = base_path / 'monitorize' / f'Group{group_id}Job{job_id}'
    upload_folder.mkdir(parents=True, exist_ok=True)

    # Crear nombre de archivo seguro
    filename = secure_filename(f"monitorize_{group_id}_{job_id}_{probe_id}.csv")  # Asumiendo que el archivo es un PDF
    filepath = upload_folder / filename
    
    # Guardar archivo
    file.save(filepath)

    #Utilizamos este archivo para poder sacar los json
    base_dir = os.path.dirname(__file__)
    nombre_script = os.path.join(base_dir, '..', '..', 'NetworkRecollector.py')
    result = subprocess.run(['python3',nombre_script, str(filepath)], capture_output=True, text=True)

    if result.returncode != 0:
        return {"error": "Failed to process file"}, 500
    logger.debug(f"{result.stdout}")
    data = json.loads(result.stdout)
    probe = ProbeDataBase.query.get(probe_id)
    probe.data = data
    

    db.session.commit()
    return InlineResponse2003(mensaje="File uploaded successfully")


def send_work_scan(body, group_id, job_id):  # noqa: E501
    """Envía el fichero resultante de una operación scan

    Envía el fichero resultante de una operación scan # noqa: E501

    :param file: 
    :type file: strstr
    :param probe_id: 
    :type probe_id: int
    :param group_id: ID del grupo a consultar
    :type group_id: int
    :param job_id: ID del trabajo a gestionar
    :type job_id: int

    :rtype: InlineResponse2003
    """
    if 'file' not in connexion.request.files or 'probeId' not in connexion.request.form:
        return {"mensaje": "Falta el archivo o el ID de la sonda"}, 400
    
    # Obtener el archivo de la solicitud
    file = connexion.request.files['file']
    if file.filename == '':
        return {"mensaje": "No se ha seleccionado ningún archivo"}, 400

    # Intentar obtener el probeId, asegurándose de que se pueda convertir a entero
    try:
        probe_id = int(connexion.request.form['probeId'])
    except ValueError:
        return {"mensaje": "El ID de la sonda debe ser un número entero"}, 400
    # Verificar que el grupo y el trabajo existen y están activos
    grupo = GroupDataBase.query.filter_by(id=group_id, is_active=True).first()
    if not grupo:
        return {"error": "Group not found or is inactive"}, 404

    trabajo = JobDataBase.query.filter_by(JobID=job_id, is_active=True).first()
    if not trabajo or trabajo.group_id != group_id:
        return {"error": "Job not found or is not associated with this group"}, 404
    
    # Ruta base del código
    base_path = Path(__file__).resolve().parent.parent
    upload_folder = base_path / 'scan' / f'Group{group_id}Job{job_id}'
    upload_folder.mkdir(parents=True, exist_ok=True)

    # Crear nombre de archivo seguro
    filename = secure_filename(f"scan_{group_id}_{job_id}_{probe_id}.csv")  # Asumiendo que el archivo es un PDF
    filepath = upload_folder / filename
    
    # Guardar archivo
    file.save(filepath)
    
    return InlineResponse2003(mensaje="File uploaded successfully")


def update_group(body, group_id):  # noqa: E501
    """Actualizar un grupo de sondas existente

    Actualizar un grupo de sondas existente dado el ID # noqa: E501

    :param body: Añade un grupo de sondas
    :type body: dict | bytes
    :param group_id: ID del grupo de sondas a actualizar
    :type group_id: int

    :rtype: Groups
    """
    if connexion.request.is_json:
        body = connexion.request.get_json()
        group_data = Groups.from_dict(body)  # Asume que Groups.from_dict puede manejar la deserialización correctamente
        
        grupo_actual = GroupDataBase.query.get(group_id)
        if not grupo_actual:
            return InlineResponse404(message="Group not found")
        
        # Actualiza los detalles del grupo
        grupo_actual.name = group_data.name
        
        # Reasigna las sondas al grupo, primero desasigna todas las sondas actuales
        current_probes = ProbeDataBase.query.filter_by(group_id=group_id).all()
        for probe in current_probes:
            probe.group_id = None  # Remueve la asociación actual
        
        probe_ids = group_data.probes_id  # Asume que 'probes' es una lista de IDs de sondas
        probes = ProbeDataBase.query.filter(ProbeDataBase.id.in_(probe_ids)).all()
        if len(probes) != len(probe_ids):
            return {"error": "One or more probes not found"}, 404

        for probe in probes:
            probe.group_id = group_id
        
        db.session.commit()
        return Groups.from_db(grupo_actual)  # Retorna el grupo actualizado

    return 'Invalid request'
