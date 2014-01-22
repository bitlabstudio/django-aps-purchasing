"""URLs for the aps_purchasing app."""
from django.conf.urls import patterns, url

from .views import QuotationUploadView


urlpatterns = patterns(
    '',
    url(r'^quotation-upload/$', QuotationUploadView.as_view(),
        name='aps_purchasing_quotation_upload'),
)
