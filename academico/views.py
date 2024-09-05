from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumnos, Casas, Colegios, Familia, Localidad, Lugar_Nacimiento, Nacionalidad, Parentezco, Tutores
from .forms import AlumnosForm, FamiliaForm, ParentezcoForm, TutorForm

def index(request):
    return render(request, "index.html")
def configuracion(request):
    return render(request, "baseconfiguracion.html")

                                ## VIWS DE TUTORES

# Lista de tutores
def tutores_list(request):
    tutores = Tutores.objects.all()
    context = {'tutores': tutores}
    return render(request, 'tutores_list.html', context)

# Crear un tutor
def tutores_create(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tutores_list')  # Redirige a la lista de tutores
    else:
        form = TutorForm()
    context = {'form': form}
    return render(request, 'anadirtutor.html', context)

# Actualizar un tutor
def tutores_update(request, pk):
    tutor = get_object_or_404(Tutores, pk=pk)
    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor)
        if form.is_valid():
            form.save()
            return redirect('tutores_list')
    else:
        form = TutorForm(instance=tutor)
    context = {'form': form, 'tutor': tutor}
    return render(request, 'tutores_form.html', context)

# Eliminar un tutor
def tutores_delete(request, pk):
    tutor = get_object_or_404(Tutores, pk=pk)
    if request.method == 'POST':
        tutor.delete()
        return redirect('tutores_list')
    context = {'tutor': tutor}
    return render(request, 'tutores_confirm_delete.html', context)

# Vista de detalle de un tutor
def tutores_detail(request, pk):
    tutor = get_object_or_404(Tutores, pk=pk)
    context = {'tutor': tutor}
    return render(request, 'tutores_detail.html', context)




                                        #VIWS DE PARENTEZCOS


# Lista de Parentezcos
def parentezcos_list(request):
    parentescos = Parentezco.objects.all()
    context = {'parentescos': parentescos}
    return render(request, 'parentezcos_list.html', context)

# Crear un Parentezco
def parentezcos_create(request):
    if request.method == 'POST':
        form = ParentezcoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parentezcos_list')
    else:
        form = ParentezcoForm()
    context = {'form': form}
    return render(request, 'parentezco_form.html', context)

# Actualizar un Parentezco
def parentezcos_update(request, pk):
    parentesco = get_object_or_404(Parentezco, pk=pk)
    if request.method == 'POST':
        form = ParentezcoForm(request.POST, instance=parentesco)
        if form.is_valid():
            form.save()
            return redirect('parentezcos_list')
    else:
        form = ParentezcoForm(instance=parentesco)
    context = {'form': form, 'parentesco': parentesco}
    return render(request, 'tutores_form.html', context)

# Eliminar un Parentezco
def parentezcos_delete(request, pk):
    parentesco = get_object_or_404(Parentezco, pk=pk)
    if request.method == 'POST':
        parentesco.delete()
        return redirect('parentezcos_list')
    context = {'parentesco': parentesco}
    return render(request, 'tutores_confirm_delete.html', context)



                                            # VIWS DE FAMILIAS 

def familia_list(request):
    familias = Familia.objects.all()
    context = {'familias': familias}
    return render(request, 'familia_list.html', context)

def familia_create(request):
    if request.method == 'POST':
        form = FamiliaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('familia_list')
    else:
        form = FamiliaForm()
    context = {'form': form}
    return render(request, 'familia_form.html', context)

def familia_update(request, pk):
    familia = get_object_or_404(Familia, pk=pk)
    if request.method == 'POST':
        form = FamiliaForm(request.POST, instance=familia)
        if form.is_valid():
            form.save()
            return redirect('familia_list')
    else:
        form = FamiliaForm(instance=familia)
    context = {'form': form}
    return render(request, 'editar_familia.html', context)
    
def familia_detail(request, pk):
    familia = get_object_or_404(Familia, pk=pk)
    context = {'familia': familia}
    return render(request, 'familia_detail.html', context)


def familia_delete(request, pk):
    familia = get_object_or_404(Familia, pk=pk)
    if request.method == 'POST':
        familia.delete()
        return redirect('familia_list')
    context = {'familia': familia}
    return render(request, 'familia_confirm_delete.html', context)



                        # CASAS

def casa_list(request):
    casas = Casas.objects.all()
    context = {'casas': casas}
    return render(request, 'casa_list.html', context)



def casa_create(request):
    if request.method == 'POST':
        # Procesar datos del formulario
        nombre = request.POST['Nombre']
        casa = Casas.objects.create(Nombre=nombre)
        return HttpResponseRedirect('/configuracion/')
    else:
        # Mostrar el formulario vacío
        return render(request, 'casa_form.html')





                            # COLEGIOS


def colegio_list(request):
    colegios = Colegios.objects.all()
    context = {'colegios': colegios}
    return render(request, 'colegio_list.html', context)



def colegio_create(request):
    if request.method == 'POST':
        # Procesar datos del formulario
        nombre = request.POST['Nombre']
        colegio = Colegios.objects.create(Nombre=nombre)
        return HttpResponseRedirect('/configuracion/')
    else:
        # Mostrar el formulario vacío
        return render(request, 'colegio_form.html')



                            # LUGAR DE NACIMIENTO
def lugar_nacimiento_list(request):
    lugares_nacimiento = Lugar_Nacimiento.objects.all()
    context = {'lugares_nacimiento': lugares_nacimiento}
    return render(request, 'lugar_nacimiento_list.html', context)



def lugar_nacimiento_create(request):
    if request.method == 'POST':
        # Procesar datos del formulario
        lugar = request.POST['Lugar']
        lugar_nacimiento = Lugar_Nacimiento.objects.create(Lugar=lugar)
        return HttpResponseRedirect('/configuracion/')
    else:
        # Mostrar el formulario vacío
        return render(request, 'lugar_nacimiento_form.html')

def lugar_nacimiento_update(request, pk):
    lugar_nacimiento = get_object_or_404(Lugar_Nacimiento, pk=pk)
    if request.method == 'POST':
        # Actualizar datos del formulario
        lugar_nacimiento.Lugar = request.POST['Lugar']
        lugar_nacimiento.save()
        return HttpResponseRedirect('/configuracion/')
    else:
        # Mostrar el formulario con datos existentes
        context = {'lugar_nacimiento': lugar_nacimiento}
        return render(request, 'lugar_nacimiento_form.html', context)



                                # NACIONALIDAD
def nacionalidad_list(request):
    nacionalidades = Nacionalidad.objects.all()
    context = {'nacionalidades': nacionalidades}
    return render(request, 'nacionalidad_list.html', context)



def nacionalidad_create(request):
    if request.method == 'POST':
        # Procesar datos del formulario
        nacionalidad = request.POST['Nacionalidad']
        nacionalidad_obj = Nacionalidad.objects.create(Nacionalidad=nacionalidad)
        return HttpResponseRedirect('/configuracion/')
    else:
        # Mostrar el formulario vacío
        return render(request, 'nacionalidad_form.html')

def nacionalidad_update(request, pk):
    nacionalidad = get_object_or_404(Nacionalidad, pk=pk)
    if request.method == 'POST':
        # Actualizar datos del formulario
        nacionalidad.Nacionalidad = request.POST['Nacionalidad']
        nacionalidad.save()
        return HttpResponseRedirect('/configuracion/')
    else:
        # Mostrar el formulario con datos existentes
        context = {'nacionalidad': nacionalidad}
        return render(request, 'nacionalidad_form.html', context)



                                    # LOCALIDAD
def localidad_list(request):
    localidades = Localidad.objects.all()
    context = {'localidades': localidades}
    return render(request, 'localidad_list.html', context)


def localidad_create(request):
    if request.method == 'POST':
        # Procesar datos del formulario
        localidad = request.POST['Localidad']
        localidad_obj = Localidad.objects.create(Localidad=localidad)
        return HttpResponseRedirect('/configuracion/')
    else:
        # Mostrar el formulario vacío
        return render(request, 'localidad_form.html')

def localidad_update(request, pk):
    localidad = get_object_or_404(Localidad, pk=pk)
    if request.method == 'POST':
        # Actualizar datos del formulario
        localidad.Localidad = request.POST['Localidad']
        localidad.save()
        return HttpResponseRedirect('/configuracion/')
    else:
        # Mostrar el formulario con datos existentes
        context = {'localidad': localidad}
        return render(request, 'localidad_form.html', context)

                                            ##ALUMNOS



def lista_alumnos(request):
    alumnos = Alumnos.objects.all()
    context = {'alumnos': alumnos}
    return render(request, 'lista_alumnos.html', context)

def detalle_alumno(request, pk):
    alumno = Alumnos.objects.get(pk=pk)
    context = {'alumno': alumno}
    return render(request, 'alumnos_detail.html', context)

def nuevo_alumno(request):
    if request.method == 'POST':
        form = AlumnosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnosForm()
    context = {'form': form}
    return render(request, 'alumnos_list.html', context)

def editar_alumno(request, pk):
    alumno = Alumnos.objects.get(pk=pk)
    if request.method == 'POST':
        form = AlumnosForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnosForm(instance=alumno)
    context = {'form': form}
    return render(request, 'editar_alumno.html', context)

def eliminar_alumno(request, pk):
    alumno = Alumnos.objects.get(pk=pk)
    if request.method == 'POST':
        alumno.delete()
        return redirect('lista_alumnos')
    context = {'alumno': alumno}
    return render(request, 'eliminar_alumno.html', context)






















































