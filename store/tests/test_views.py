from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import reverse
from django.test import Client, RequestFactory, TestCase

from store.models import Category, Product
from store.views import all_products


class TestViewResponses(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        Product.objects.create(category_id=1, title='product test title', created_by_id=1,
                                            slug='product-test-title', price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/')
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
        response = all_products(request)
        html = response.content.decode('utf-8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get('/item/product-test-title')
        response = all_products(request)
        html = response.content.decode('utf-8')
        self.assertIn('<title>Home</title>', html)
        self.assertEqual(response.status_code, 200)
