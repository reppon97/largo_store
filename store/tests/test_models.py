from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Category, Product


class TestCategoryModel(TestCase):

    def setUp(self) -> None:
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')


class TestProductModel(TestCase):

    def setUp(self) -> None:
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='product test title', created_by_id=1,
                                            slug='product-test-title', price='20.00', image='django')

    def test_product_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertEqual(str(data), 'product test title')
