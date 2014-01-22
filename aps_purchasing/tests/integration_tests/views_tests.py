"""Tests for the views of the ``aps_purchasing`` app."""
import os

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import now

from django_libs.tests.mixins import ViewTestMixin
from django_libs.tests.factories import UserFactory

from ..factories import (
    CurrencyFactory,
    DistributorFactory,
    ManufacturerFactory,
)
from ...models import Quotation, QuotationItem, Price
from ...views import QuotationUploadView


class QuotationUploadViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``QuotationUploadView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'aps_purchasing_quotation_upload'

    def setUp(self):
        self.user = UserFactory()
        self.distributor = DistributorFactory()
        self.manufacturer = ManufacturerFactory()
        self.usd = CurrencyFactory(iso_code='USD')

        self.quotation_file = open(os.path.join(
            settings.APP_ROOT, 'tests/files/Quotation.csv'))

        self.data = {
            'distributor': self.distributor.pk,
            'manufacturer': self.manufacturer.pk,
            'ref_number': 'REF123',
            'issuance_date': now(),
            'expiry_date': now(),
            'is_completed': True,
            'quotation_file': SimpleUploadedFile('Quotation.csv',
                                                 self.quotation_file.read()),
        }

        self.get_req = RequestFactory().get(self.get_url())
        self.post_req = RequestFactory().post(self.get_url(), data=self.data)
        self.post_req.user = self.user
        self.view = QuotationUploadView.as_view()

    def test_view(self):
        self.get_req.user = AnonymousUser()
        resp = self.view(self.get_req)
        self.assertEqual(resp.status_code, 302, msg=(
            'When called anonymously, the view should redirect.'))
        self.assertEqual(resp['Location'], '{0}?next={1}'.format(
            settings.LOGIN_URL, self.get_url()), msg=(
                'When called anonymously, the view should redirect to login.'))

        self.get_req.user = self.user
        resp = self.view(self.get_req)
        self.assertEqual(resp.status_code, 200, msg=(
            'When called while logged in, the view should be callable.'))

        resp = self.view(self.post_req)
        self.assertEqual(resp.status_code, 302, msg=(
            'When posting with valid data, the view should redirect.'))

        self.assertEqual(Quotation.objects.count(), 1, msg=(
            'After a post with valid data, there should be one Quotation in'
            ' the database.'))
        self.assertEqual(QuotationItem.objects.count(), 2, msg=(
            'After a post with valid data, there should be four QuotationItems'
            ' in the database.'))
        self.assertEqual(Price.objects.count(), 4, msg=(
            'After a post with valid data, there should be three Prices in'
            ' the database.'))

        resp = self.view(self.post_req)
        self.assertEqual(Quotation.objects.count(), 1, msg=(
            'After posting again, there should stil be one Quotation in the'
            ' database.'))
        self.assertEqual(QuotationItem.objects.count(), 2, msg=(
            'After posting again, there should still be four QuotationItems'
            ' in the database.'))
        self.assertEqual(Price.objects.count(), 4, msg=(
            'After posting again, there should still be three Prices in'
            ' the database.'))
