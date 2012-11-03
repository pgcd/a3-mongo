"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def setUp(self):
        super(SimpleTest, self).setUp()

    def test_homepage_topic_list(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code,200)
        self.assertTrue('topic_list' in r.context)

    def test_topic_list(self):
        r = self.client.get('/p/')
        self.assertEqual(r.status_code,200)
        self.assertTrue('topic_list' in r.context)

    def test_post_new_topic(self):
        r = self.client.post('/p/', {'title':'test topic', 'body_markup':'test body markup'}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['topic'].title, 'test topic')
        self.assertEqual(r.context['topic'].body, 'test body markup')
        self.assertEqual(r.context['topic'].obj.body, 'test body markup')
        r = self.client.get('/p/')
        self.assertEqual(r.status_code,200)
        self.assertTrue(r.context['topic_list'])
        self.assertGreaterEqual(len(r.context['topic_list']),1)