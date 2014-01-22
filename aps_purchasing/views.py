"""Views of the ``aps_purchasing`` app."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from .forms import QuotationUploadForm
from .models import Quotation


class QuotationUploadView(CreateView):
    """View to upload a quotation and create Quotation items."""
    model = Quotation
    template_name = 'aps_purchasing/quotation_upload.html'
    form_class = QuotationUploadForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuotationUploadView, self).dispatch(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('aps_purchasing_quotation_upload')
