# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.job_specification import JobSpecification  # noqa: E501
from swagger_server.models.probe import Probe  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProbesController(BaseTestCase):
    """ProbesController integration test stubs"""

    def test_elimina_sonda(self):
        """Test case for elimina_sonda

        Elimina una sonda
        """
        response = self.client.open(
            '/v1/probes/{Id}'.format(id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_probe_job(self):
        """Test case for get_probe_job

        Endpoint donde la sonda preguntará por su trabajo a hacer
        """
        response = self.client.open(
            '/v1/probes/{Id}/current-job'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_probe_register(self):
        """Test case for probe_register

        Registra una nueva sonda
        """
        query_string = [('nombre', 'nombre_example'),
                        ('ip', 'ip_example')]
        response = self.client.open(
            '/v1/probes',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_probeid(self):
        """Test case for probeid

        Devuelve la sonda seleccionada
        """
        response = self.client.open(
            '/v1/probes/{Id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_probelist(self):
        """Test case for probelist

        Lista y filtra entre todas las sondas
        """
        query_string = [('nombre', 'nombre_example'),
                        ('is_active', true)]
        response = self.client.open(
            '/v1/probes',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_probe(self):
        """Test case for update_probe

        Actualizar una sonda existente
        """
        body = Probe()
        response = self.client.open(
            '/v1/probes/{Id}'.format(id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
