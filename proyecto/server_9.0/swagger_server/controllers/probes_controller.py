import connexion
import six
from swagger_server.database import db
import logging
from swagger_server.models.groups_database import GroupDataBase
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.job_specification import JobSpecification  # noqa: E501
from swagger_server.models.jobs_database import JobDataBase
from swagger_server.models.probe import Probe  # noqa: E501
from swagger_server import util
from swagger_server.models.probe_database import ProbeDataBase

logging.basicConfig(level=logging.DEBUG,  # Puedes cambiar el nivel a INFO, WARNING, etc.
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)  # Obtener el logger para el módulo actual

def elimina_sonda(id_):  # noqa: E501
    """Elimina una sonda

    Elimina una sonda # noqa: E501

    :param id: Id de la sonda a eliminar
    :type id: int

    :rtype: None
    """
    probe = db.session.query(ProbeDataBase).filter_by(id=id_).one_or_none()
    if not probe:
        return {"error": "Probe not found"}, 404

    probe.is_active = False
    probe.group_id = None  # Desasignar del grupo
    db.session.commit()


def get_probe_job(id_):  # noqa: E501
    """Endpoint donde la sonda preguntará por su trabajo a hacer

    Devuelve el trabajo realizado por la sonda # noqa: E501

    :param id: ID de la sonda a consultar
    :type id: int

    :rtype: JobSpecification
    """
    probe = db.session.query(ProbeDataBase).filter_by(id=id_, is_active=True).one_or_none()
    if not probe:
        return {"error": "Probe not found or is inactive"}, 404

    if not probe.group_id:
        return {"error": "Probe is not assigned to any group"}, 400

    group = db.session.query(GroupDataBase).filter_by(id=probe.group_id, is_active=True).one_or_none()
    if not group:
        return {"error": "Group not found or is inactive"}, 404

    job = db.session.query(JobDataBase)\
                    .filter_by(group_id=group.id, is_active=True)\
                    .order_by(JobDataBase.created_at.desc())\
                    .first()
    if not job:
        return {"error": "No active job found for the group"}, 404

    job_spec = JobSpecification.from_db(job)
    return job_spec


def probe_register(nombre, ip):  # noqa: E501
    """Registra una nueva sonda

    Registra una nueva sonda para operar # noqa: E501

    :param nombre: Nombre de la sonda
    :type nombre: str
    :param ip: IP de la sonda
    :type ip: str

    :rtype: InlineResponse200
    """
    probe = ProbeDataBase(name=nombre, last_recorded_ip=ip, in_use=False, is_active=True)
    db.session.add(probe)
    db.session.commit()

    response = InlineResponse200(id=probe.id)
    return response


def probeid(id_):  # noqa: E501
    """Devuelve la sonda seleccionada

    Devuelve la sonda seleccionada # noqa: E501

    :param id: Id de la sonda
    :type id: int

    :rtype: Probe
    """
    probe = ProbeDataBase.query.get(id_)
    if probe:
        return Probe.from_db(probe)
    else:
        return 404


def probelist(nombre=None, is_active=None):  # noqa: E501
    """Lista y filtra entre todas las sondas

    Lista todas las sondas, pudiendo filtrar su nombre para obtener un resultado más óptimo # noqa: E501

    :param nombre: Nombre de la sonda a devolver
    :type nombre: str
    :param is_active: Filtra los grupos por su estado activo o inactivo
    :type is_active: bool

    :rtype: List[Probe]
    """
    query = ProbeDataBase.query  # Inicia la consulta

    # Aplicar filtros basados en los parámetros proporcionados
    if is_active is True:
        query = query.filter(ProbeDataBase.is_active)
    if nombre:
        query = query.filter(ProbeDataBase.name == nombre)

    sondas_db = query.all()  # Ejecuta la consulta con los filtros aplicados
    sondas_swagger = [Probe.from_db(probe_db) for probe_db in sondas_db]  # Convierte las sondas de DB a objetos Swagger

    return sondas_swagger


def update_probe(body, id_):  # noqa: E501
    """Actualizar una sonda existente

    Actualizar una sonda existente dada el Id # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: ID de la sonda a actualizar
    :type id: int

    :rtype: Probe
    """
    if connexion.request.is_json:
        body = connexion.request.get_json()  # Obtiene el JSON del body de la solicitud
        body_obj = Probe.from_dict(body)  # Convierte el diccionario a objeto Probe
        
        probe_db = ProbeDataBase.query.get(id_)  # Obtiene la instancia de la sonda desde la base de datos
        
        if probe_db is None:
            return "Probe no encontrada", 404

        # Actualiza solo los atributos permitidos y que existen en el modelo de la base de datos
        allowed_attrs = {'name', 'last_recorded_ip', 'in_use', 'is_active', 'group_id'}  # Atributos permitidos para actualizar
        for attr in allowed_attrs:
            if hasattr(body_obj, attr):
                setattr(probe_db, attr, getattr(body_obj, attr))

        db.session.commit()  # Confirma los cambios en la base de datos
        return Probe.from_db(probe_db)  # Retorna la sonda actualizada como un objeto de modelo

    return 400
