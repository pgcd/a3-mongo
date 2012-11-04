"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User

from django.test import TestCase


class SimpleTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username="test", password="test")
        super(SimpleTest, self).setUp()

    def test_homepage_topic_list(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('topic_list' in r.context)

    def test_topic_list(self):
        r = self.client.get('/p/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('topic_list' in r.context)

    def test_post_new_topic_anon(self):
        r = self.client.post('/p/', {'title': 'test topic', 'body_markup': 'test body markup'}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['topic'].title, 'test topic')
        self.assertEqual(r.context['topic'].body, 'test body markup')
        self.assertEqual(r.context['topic'].obj.body, 'test body markup')
        self.assertEqual(r.context['topic'].obj.user.username, 'anon')
        r = self.client.get('/p/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['topic_list'])
        self.assertGreaterEqual(len(r.context['topic_list']), 1)

    def test_post_new_topic_user(self):
        self.client.login(username="test", password="test")
        r = self.client.post('/p/',
            {'title': 'test topic', 'body_markup': 'test body markup', 'user': self.test_user.pk}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['topic'].title, 'test topic')
        self.assertEqual(r.context['topic'].body, 'test body markup')
        self.assertEqual(r.context['topic'].obj.body, 'test body markup')
        self.assertEqual(r.context['topic'].obj.user.username, 'test')
