# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.
# All the testcases below seem to be failing and I can't figure out why.
class TasksTest(TestCase):
    def test_index_view(self):
        url = reverse('index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_add_tasks(self):
        url = reverse('add_tasks')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_detail(self):
        url = reverse('detail')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_claim(self):
        url = reverse('index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_claimed_tasks(self):
        url = reverse('claimed_tasks')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
