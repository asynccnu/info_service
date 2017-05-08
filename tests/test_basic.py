# -*- coding: utf-8 -*-
import json
import unittest
from base64 import b64encode
from service import create_app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get(
                '/wrong/url',
                headers=self.get_api_headers('email', 'password'))
        self.assertTrue(response.status_code == 404)

    def test_webview_info(self):
        response = self.client.get(
                '/api/webview_info/'
                )
        self.assertTrue(response.status_code == 200)
