from django.views.generic       import View
from .forms                     import WaWiGForm
from django.shortcuts           import render
from .                          import template
from .libs                      import send_request as sr_lib


class WaWiGView(View):

    template_name = template.path('WaWiGView')

    def get(self, request, **kwargs):

        form = WaWiGForm

        context  = {
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)


    def post(self, request, **kwargs):

        form = WaWiGForm
        city = request.POST.get('city')
        days = request.POST.get('days')

        results = sr_lib.owm_request(city, days)

        context  = {
            'form': form,
            'city': city,
            'days': days,
            'results': results,
            'error':  results['error']
        }

        return render(request, template_name=self.template_name, context=context)
