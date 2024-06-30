# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.groups import Groups  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response404 import InlineResponse404  # noqa: E501
from swagger_server.models.inline_response500 import InlineResponse500  # noqa: E501
from swagger_server.models.job_specification import JobSpecification  # noqa: E501
from swagger_server.models.probe import Probe  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProbesGroupsController(BaseTestCase):
    """ProbesGroupsController integration test stubs"""

    def test_create_job(self):
        """Test case for create_job

        Registra el trabajo al grupo
        """
        body = JobSpecification()
        response = self.client.open(
            '/v1/probes-groups/{groupId}/jobs'.format(group_id=789),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_group(self):
        """Test case for delete_group

        Eliminar un grupo de sondas
        """
        response = self.client.open(
            '/v1/probes-groups/{groupId}'.format(group_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_group_job(self):
        """Test case for get_group_job

        Accede a todos los trabajos realizados por el grupo
        """
        response = self.client.open(
            '/v1/probes-groups/{groupId}/jobs'.format(group_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_job(self):
        """Test case for get_job

        Accede a las especificaciones del trabajo
        """
        response = self.client.open(
            '/v1/probes-groups/{groupId}/jobs/{jobId}'.format(group_id=789, job_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_monitorize(self):
        """Test case for get_monitorize

        Descarga el fichero resultante o el archivo procesado de una operación monitorize
        """
        response = self.client.open(
            '/v1/probes-groups/{groupId}/jobs/{jobId}/monitorize'.format(group_id=789, job_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_probe_group_information(self):
        """Test case for get_probe_group_information

        Accede a la información del grupo de sondas
        """
        response = self.client.open(
            '/v1/probes-groups/{groupId}'.format(group_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_scan(self):
        """Test case for get_scan

        Descarga el archivo procesado resultante de una operación scan
        """
        response = self.client.open(
            '/v1/probes-groups/{groupId}/jobs/{jobId}/scan'.format(group_id=789, job_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_probe_group_list(self):
        """Test case for probe_group_list

        Lista y filtra entre todos los grupos de sondas
        """
        query_string = [('nombre', 'nombre_example'),
                        ('is_active', true)]
        response = self.client.open(
            '/v1/probes-groups',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_probe_group_register(self):
        """Test case for probe_group_register

        Registra un nuevo grupo de sondas
        """
        body = [Probe()]
        query_string = [('nombre', 'nombre_example')]
        response = self.client.open(
            '/v1/probes-groups',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_work_monitorize(self):
        """Test case for send_work_monitorize

        Envía el fichero resultante de una operación monitorize
        """
        data = dict(file='file_example',
                    probe_id=789)
        response = self.client.open(
            '/v1/probes-groups/{groupId}/jobs/{jobId}/monitorize'.format(group_id=789, job_id=789),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_work_scan(self):
        """Test case for send_work_scan

        Envía el fichero resultante de una operación scan
        """
        data = dict(file='file_example',
                    probe_id=789)
        response = self.client.open(
            '/v1/probes-groups/{groupId}/jobs/{jobId}/scan'.format(group_id=789, job_id=789),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_group(self):
        """Test case for update_group

        Actualizar un grupo de sondas existente
        """
        body = Groups()
        response = self.client.open(
            '/v1/probes-groups/{groupId}'.format(group_id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
