# -*- coding:utf-8 -*-

import os
import unittest

import json
from flask import url_for

from app import create_app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        resp = self.client.get(url_for('api.index'))
        self.assertTrue(resp.status_code == 200)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertTrue(json_resp['body'] == "App is working!")
