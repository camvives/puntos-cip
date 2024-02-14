from django.template import loader
from django.http import HttpResponse
from .models import Entrada

# Create your views here.
def index(request):
    entry_list = Entrada.objects.order_by("-fecha")
    template = loader.get_template('puntos/index.html')
    context = {
        "entry_list": entry_list,
    }
    return HttpResponse(template.render(context, request))