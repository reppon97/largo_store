from django.conf import settings
from django.contrib.auth.models import User
from importlib import import_module
from django.http import HttpRequest
from django.shortcuts import reverse
from django.test import Client, TestCase

from store.models import Category, Product
from store.views import product_all


class TestViewResponses(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        Product.objects.create(category_id=1, title='product test title', created_by_id=1,
                               slug='product-test-title', price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='domain.com')
        self.assertEqual(response.status_code, 400)

        response = self.c.get('/', HTTP_HOST='mydomain.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test product response status
        :return:
        """
        response = self.c.get(reverse('store:product_detail', args=['product-test-title']))

        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test category response status
        :return:
        """
        response = self.c.get(reverse('store:category_list', args=['django']))

        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf-8')

        self.assertIn('<title>Largo Store</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
