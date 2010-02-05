from django import template
from django.conf import settings
from django.test import TestCase
from django.core import urlresolvers
from shorturls.tests.models import Animal, Vegetable, Mineral
from shorturls.urlresolvers import get_shorturl

class UrlResolversTestCase(TestCase):
    urls = 'shorturls.urls'
    fixtures = ['shorturls-test-data.json']

    def setUp(self):
        self.old_shorten = getattr(settings, 'SHORTEN_MODELS', None)
        self.old_base = getattr(settings, 'SHORT_BASE_URL', None)
        settings.SHORT_BASE_URL = None
        settings.SHORTEN_MODELS = {
            'A': 'shorturls.animal',
            'V': 'shorturls.vegetable',
        }
        
    def tearDown(self):
        if self.old_shorten is not None:
            settings.SHORTEN_MODELS = self.old_shorten
        if self.old_base is not None:
            settings.SHORT_BASE_URL = self.old_base

    def test_shorturl(self):
        r = get_shorturl(Animal.objects.get(id=12345))
        self.assertEqual(r, '/ADNH')
        
    def test_no_prefix(self):
        try:
            r = get_shorturl(Mineral.objects.all()[0])
        except urlresolvers.NoReverseMatch:
            pass
        else:
            self.assertFalse()
        
    def test_short_base_url(self):
        settings.SHORT_BASE_URL = 'http://example.com/'
        r = get_shorturl(Animal.objects.get(id=12345))
        self.assertEqual(r, 'http://example.com/ADNH')
        
