import json

from django.http import HttpResponse
from django.template.loader import get_template
from django.views import generic
from weasyprint import HTML

from huscy.consents.forms import SignatureForm


class ConsentView(generic.FormView):
    form_class = SignatureForm
    template_name = 'consents/consent-page.html'

    def form_valid(self, form):
        signature = form.cleaned_data.get('signature_field')
        html_template = get_template('consents/signature-image-template.html')
        rendered_html = html_template.render({
            "signature": json.dumps(signature),
        })
        content = HTML(string=rendered_html).write_pdf()
        return HttpResponse(content, content_type="application/pdf")
