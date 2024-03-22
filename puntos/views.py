from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Entrada, Seccion
from .forms import EntradaForm

# Create your views here.
def index(request):
    entry_list = Entrada.objects.order_by("-fecha")
    secciones = Seccion.objects.order_by('-puntos_totales')
    template = loader.get_template('puntos/index.html')
    context = {
        "entry_list": entry_list,
        "secciones": secciones,
    }
    return HttpResponse(template.render(context, request))

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to a success page or some other page
            return redirect('entrada_list')  
        
        return render(request, 'puntos/login.html', {'error': 'Credenciales inválidas. Si sale mucho este mensaje preguntale a Cami'})
    
    return render(request, 'puntos/login.html')

def entrada_list(request):
    entradas = Entrada.objects.all()
    secciones = Seccion.objects.order_by('-puntos_totales')  # Order by puntos_totales in descending order
    return render(request, 'puntos/entrada_list.html', {'entradas': entradas, 'secciones': secciones})

def entrada_create(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)  # Don't save to DB yet
            tipo_oracion = entrada.tipo_oracion
            seccion = entrada.seccion
            puntos_oracion = tipo_oracion.puntos
            
            # Add puntos from TipoOracion to puntos_totales of Seccion
            seccion.puntos_totales += puntos_oracion
            seccion.save()  # Save the updated Seccion

            entrada.save()  # Now save the Entrada to DB
            return redirect('entrada_list')
    else:
        form = EntradaForm()
    return render(request, 'puntos/entrada_form.html', {'form': form})

def entrada_update(request, pk):
    entrada = get_object_or_404(Entrada, pk=pk)
    
    if request.method == 'POST':
        form = EntradaForm(request.POST, instance=entrada)
        if form.is_valid():
            updated_entrada = form.save(commit=False)  # Don't save to DB yet
            tipo_oracion = updated_entrada.tipo_oracion
            seccion = updated_entrada.seccion
            
            # Calculate the difference in puntos before and after the update
            original_entrada = Entrada.objects.get(pk=pk)
            original_puntos = original_entrada.tipo_oracion.puntos
            updated_puntos = tipo_oracion.puntos
            puntos_difference = updated_puntos - original_puntos
            
            # Update puntos_totales of Seccion
            seccion.puntos_totales += puntos_difference
            seccion.save()  # Save the updated Seccion
            
            updated_entrada.save()  # Now save the updated Entrada to DB
            return redirect('entrada_list')
    else:
        form = EntradaForm(instance=entrada)
    
    return render(request, 'puntos/entrada_form.html', {'form': form})

def entrada_delete(request, pk):
    entrada = get_object_or_404(Entrada, pk=pk)
    
    if request.method == 'POST':
        tipo_oracion = entrada.tipo_oracion
        seccion = entrada.seccion
        puntos_oracion = tipo_oracion.puntos
        
        # Subtract puntos from TipoOracion to puntos_totales of Seccion
        seccion.puntos_totales -= puntos_oracion
        if seccion.puntos_totales < 0:
            seccion.puntos_totales = 0
        seccion.save()  # Save the updated Seccion
        
        entrada.delete()  # Delete the Entrada
        return redirect('entrada_list')
    
    return render(request, 'puntos/entrada_confirm_delete.html', {'entrada': entrada})