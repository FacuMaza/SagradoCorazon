from django.shortcuts import render, redirect, get_object_or_404
from .models import Familia, Parentezco, Tutores
from .forms import FamiliaForm, ParentezcoForm, TutorForm

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


























































