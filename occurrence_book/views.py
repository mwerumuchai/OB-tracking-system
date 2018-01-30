from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf
from ob_system.models import CashBail


def generate_cashbail_view(request):

    single_record = CashBail.single_cashbail_record()

    pdf = render_to_pdf('pdf/cashbail.html', {'single_record': single_record})

    if pdf:

        response = HttpResponse(pdf, content_type='application/pdf')

        filename = "CashBail_%s.pdf" % single_record.id

        content = "inline; filename='%s'" % filename

        download = request.GET.get("download")

        if download:

            content = "attachment; filename='%s'" % filename

        response['Content-Disposition'] = content

        return response

    return HttpResponse('File Not Found!')