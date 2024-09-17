from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Alumnos, Asistencias, Casas, Colegios, Cuotas, Cursos, Division, Docentes, Familia, Localidad, Lugar_Nacimiento, Materias, Nacionalidad, Nivel, Nivel_Docente, Parentezco, Titulos_Profesionales, Tutores, Valor, notas
from .forms import AlumnosForm, AsistenciaForm, CuotaForm, CursosForm, DivisionForm, DocenteForm, FamiliaForm, MateriaForm, NivelDocenteForm, NivelForm, ParentezcoForm, TitulosProfesionalesForm, TutorForm, ValorForm

def index(request):
    return render(request, "index.html")
def configuracion(request):
    return render(request, "baseconfiguracion.html")

                                ## VIWS DE TUTORES

# Lista de tutores
def tutores_list(request):
    tutores = Tutores.objects.all()
    parentezcos = Parentezco.objects.all()
    form = TutorForm()  # Crea una instancia vacía del formulario
    context = {'tutores': tutores, 
               'form': form,
               'parentezcos':parentezcos} 
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
    tutores = Tutores.objects.all()
    form = FamiliaForm()
    context = {'familias': familias,
               'tutores': tutores,
               'form': form}
    return render(request, 'familia_list.html', context)

def familia_create(request):
    if request.method == 'POST':
        form = FamiliaForm(request.POST)
        if form.is_valid():
            familia = form.save()
            # Obtener los tutores seleccionados
            tutores_seleccionados = request.POST.getlist('Tutores')
            # Asignar los tutores a la familia
            familia.Tutores.set(tutores_seleccionados)
            return redirect('familia_list')
    else:
        form = FamiliaForm()
        # Obtener la lista de todos los tutores
        tutores = Tutores.objects.all()
        context = {'form': form, 'tutores': tutores}  # Pasar la lista al contexto
    return render(request, 'familia_form.html', context)

def familia_update(request, pk):
    familia = get_object_or_404(Familia, pk=pk)
    if request.method == 'POST':
        form = FamiliaForm(request.POST, instance=familia)
        if form.is_valid():
            # Si el nombre de la familia está vacío, reemplázalo con el nombre actual
            if not form.cleaned_data['Nombre_Familia']:
                form.cleaned_data['Nombre_Familia'] = familia.Nombre_Familia 
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
    Familias = Familia.objects.all()
    curso = Cursos.objects.all()
    colegio = Colegios.objects.all()
    Casa = Casas.objects.all()
    Lugar_Nacimientos = Lugar_Nacimiento.objects.all()
    Nacionalidades = Nacionalidad.objects.all()
   
    Localidades = Localidad.objects.all()
    context = {'alumnos': alumnos,
               'Familias':Familias,
               'curso': curso,
               'Casa': Casa,
               'Lugar_Nacimientos': Lugar_Nacimientos,
               'Nacionalidades': Nacionalidades,
               'Localidades': Localidades,
               'colegio':colegio}
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
    Familias = Familia.objects.all()
    curso = Cursos.objects.all()
    colegio = Colegios.objects.all()
    Casa = Casas.objects.all()
    Lugar_Nacimientos = Lugar_Nacimiento.objects.all()
    Nacionalidades = Nacionalidad.objects.all()
    Localidades = Localidad.objects.all()
    

    if request.method == 'POST':
        form = AlumnosForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnosForm(instance=alumno)
    context = {'form': form,
               'Familias':Familias,
               'curso': curso,
               'Casa': Casa,
               'Lugar_Nacimientos': Lugar_Nacimientos,
               'Nacionalidades': Nacionalidades,
               'Localidades': Localidades,
               'colegio':colegio}
    return render(request, 'editar_alumno.html', context)

def eliminar_alumno(request, pk):
    alumno = Alumnos.objects.get(pk=pk)
    if request.method == 'POST':
        alumno.delete()
        return redirect('lista_alumnos')
    context = {'alumno': alumno}
    return render(request, 'eliminar_alumno.html', context)


                                            ##VALOR ASISTENCIAS

def listar_valores(request):
    valores = Valor.objects.all()
    return render(request, 'listar_valores.html', {'valores': valores})

def crear_valor(request):
    if request.method == 'POST':
        form = ValorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_valores')
    else:
        form = ValorForm()
    return render(request, 'crear_valor.html', {'form': form})

def editar_valor(request, valor_id):
    valor = Valor.objects.get(pk=valor_id)
    if request.method == 'POST':
        form = ValorForm(request.POST, instance=valor)
        if form.is_valid():
            form.save()
            return redirect('listar_valores')
    else:
        form = ValorForm(instance=valor)
    return render(request, 'editar_valor.html', {'form': form})



##ASISTENCIAS

def asistencias_list(request):
    asistencias = Asistencias.objects.all()
    return render(request, 'asistencias_list.html', {'asistencias': asistencias})

def asistencia_add(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asistencias_list')
    else:
        form = AsistenciaForm()
    return render(request, 'asistencia_add.html', {'form': form})

def asistencia_edit(request, pk):
    asistencia = get_object_or_404(Asistencias, pk=pk)
    if request.method == 'POST':
        form = AsistenciaForm(request.POST, instance=asistencia)
        if form.is_valid():
            form.save()
            return redirect('asistencias_list')
    else:
        form = AsistenciaForm(instance=asistencia)
    return render(request, 'asistencia_edit.html', {'form': form})


                                ##CUOTAS


def cuotas_list(request):
    cuotas = Cuotas.objects.all()
    context = {'cuotas': cuotas}
    return render(request, 'cuotas_list.html', context)

def cuota_detail(request, pk):
    cuota = get_object_or_404(Cuotas, pk=pk)
    context = {'cuota': cuota}
    return render(request, 'cuota_detail.html', context)

def cuota_create(request):
    if request.method == 'POST':
        form = CuotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuota creada correctamente')
            return redirect('cuotas:cuotas_list')
    else:
        form = CuotaForm()
    context = {'form': form}
    return render(request, 'cuota_form.html', context)

def cuota_update(request, pk):
    cuota = get_object_or_404(Cuotas, pk=pk)
    if request.method == 'POST':
        form = CuotaForm(request.POST, instance=cuota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuota actualizada correctamente')
            return redirect('cuotas:cuota_detail', pk=cuota.pk)
    else:
        form = CuotaForm(instance=cuota)
    context = {'form': form, 'cuota': cuota}
    return render(request, 'cuota_form.html', context)

def cuota_delete(request, pk):
    cuota = get_object_or_404(Cuotas, pk=pk)
    if request.method == 'POST':
        cuota.delete()
        messages.success(request, 'Cuota eliminada correctamente')
        return redirect('cuotas:cuotas_list')
    context = {'cuota': cuota}
    return render(request, 'cuota_confirm_delete.html', context)





##DIVISIONES

def list_division(request):
    divisiones = Division.objects.all()
    return render(request, 'list_division.html', {'divisiones': divisiones})

def crear_division(request):
    if request.method == 'POST':
        form = DivisionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_division')
    else:
        form = DivisionForm()
    return render(request, 'division_form.html', {'form': form})


##NIVELES

def list_nivel(request):
    niveles = Nivel.objects.all()
    return render(request, 'list_nivel.html', {'niveles': niveles})

def crear_nivel(request):
    if request.method == 'POST':
        form = NivelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_nivel')
    else:
        form = NivelForm()
    return render(request, 'nivel_form.html', {'form': form})


##NIVEL DOCENTES


def list_nivel_docente(request):
    niveles_docentes = Nivel_Docente.objects.all()
    return render(request, 'list_nivel_docente.html', {'niveles_docentes': niveles_docentes})

def crear_nivel_docente(request):
    if request.method == 'POST':
        form = NivelDocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_nivel_docente')
    else:
        form = NivelDocenteForm()
    return render(request, 'nivel_docente_form.html', {'form': form})



##TITULOS DOCENTES


def list_titulos_profesionales(request):
    titulos_profesionales = Titulos_Profesionales.objects.all()
    return render(request, 'list_titulos_profesionales.html', {'titulos_profesionales': titulos_profesionales})

def crear_titulo_profesional(request):
    if request.method == 'POST':
        form = TitulosProfesionalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_titulos_profesionales')
    else:
        form = TitulosProfesionalesForm()
    return render(request, 'titulos_profesionales_form.html', {'form': form})




#DONDENTES

def docentes_list(request):
    docentes = Docentes.objects.all()
    nivel_docente = Nivel_Docente.objects.all()
    titulo = Titulos_Profesionales.objects.all()
    context = {'docentes': docentes,
               'nivel_docente': nivel_docente,
               'titulo': titulo,}
    return render(request, 'docentes_list.html', context)

def docente_detail(request, pk):
    docente = get_object_or_404(Docentes, pk=pk)
    context = {'docente': docente}
    return render(request, 'docente_detail.html', context)

def docente_create(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            # Si el campo F_Nacimiento está presente, incluimos la información al guardar
            if 'F_Nacimiento' in request.POST:
                form.instance.F_Nacimiento = form.cleaned_data['F_Nacimiento']
            form.save()
            return redirect('docentes_list')
    else:
        form = DocenteForm()
    context = {'form': form}
    return render(request, 'docente_create.html', context)

def docente_update(request, pk):
    docente = get_object_or_404(Docentes, pk=pk)
    if request.method == 'POST':
        form = DocenteForm(request.POST, instance=docente)
        if form.is_valid():
            # Si el campo F_Nacimiento está presente, incluimos la información al guardar
            if 'F_Nacimiento' in request.POST:
                form.instance.F_Nacimiento = form.cleaned_data['F_Nacimiento']
            form.save()
            return redirect('docentes_list')
    else:
        form = DocenteForm(instance=docente)
    context = {'form': form}
    return render(request, 'docente_update.html', context)

def docente_delete(request, pk):
    docente = get_object_or_404(Docentes, pk=pk)
    if request.method == 'POST':
        docente.delete()
        return redirect('docentes_list')
    context = {'docente': docente}
    return render(request, 'docente_delete.html', context)


#MATERIAS


def materia_list(request):
    materias = Materias.objects.all()
    docentes = Docentes.objects.all() # Agrega esto
    context = {'materias': materias, 'docentes': docentes,}
    return render(request, 'materia_list.html', context)

def materia_detail(request, pk):  # Recibe el argumento 'pk'
    materia = get_object_or_404(Materias, pk=pk)  # Utiliza 'pk' para obtener la materia
    context = {'materia': materia}
    return render(request, 'materia_detail.html', context)

def materia_create(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('materia_list')
    else:
        form = MateriaForm()
    context = {'form': form}
    return render(request, 'materia_form.html', context)

def materia_update(request, pk):
    materia = get_object_or_404(Materias, pk=pk)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('materia_list')
    else:
        form = MateriaForm(instance=materia)
    context = {'form': form}
    return render(request, 'materia_form.html', context)

def materia_delete(request, pk):
    materia = get_object_or_404(Materias, pk=pk)
    if request.method == 'POST':
        materia.delete()
        return redirect('materia_list')
    context = {'materia': materia}
    return render(request, 'materia_confirm_delete.html', context)

##CURSOS

def cursos_list(request):
    cursos = Cursos.objects.all()
    materias = Materias.objects.all()  # Agrega las materias al contexto
    tutores = Docentes.objects.all()  # Agrega los tutores al contexto
    context = {
        'cursos': cursos,
        'materias': materias,
        'tutores': tutores
    }
    return render(request, 'curso_list.html', context)

def curso_detail(request, curso_id):
    curso = Cursos.objects.get(pk=curso_id)
    alumnos = curso.alumnos.all()  # Alumnos del curso
    context = {'curso': curso, 'alumnos': alumnos}
    return render(request, 'curso_detail.html', context)

def curso_create(request):
    if request.method == 'POST':
        form = CursosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cursos_list')
    else:
        form = CursosForm()
    context = {'form': form}
    return render(request, 'curso_form.html', context)

def curso_update(request, curso_id):
    curso = get_object_or_404(Cursos, pk=curso_id)
    if request.method == 'POST':
        form = CursosForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('cursos_list')
    else:
        form = CursosForm(instance=curso)
    context = {'form': form}
    return render(request, 'curso_form.html', context)

def curso_delete(request, curso_id):
    curso = get_object_or_404(Cursos, pk=curso_id)
    if request.method == 'POST':
        curso.delete()
        return redirect('cursos_list')
    context = {'curso': curso}
    return render(request, 'curso_delete.html', context)

#AGREGO MATERIAS A LOS CURSOS
def materias_curso(request, curso_id):
    curso = get_object_or_404(Cursos, pk=curso_id)
    materias_del_curso = curso.Materias.all()
    context = {
        'curso': curso,
        'materias_del_curso': materias_del_curso,
    }
    return render(request, 'materia_por_curso.html', context)




# AGREGAR ALUMNO CURSO
def agregar_alumno_curso(request, curso_id):
    curso = get_object_or_404(Cursos, pk=curso_id) 

    if request.method == 'POST':
        # Obtener los ID de los alumnos seleccionados
        selected_alumnos_ids = request.POST.getlist('alumnos')

        # Obtener el año y la división del formulario
        año = request.POST.get('año')
        division_id = request.POST.get('division') 

        # En este punto, no necesitas buscar el curso de nuevo porque ya tienes "curso"
        # No necesitas buscar por año y división, ya tienes el ID del curso
        # curso_correcto = Cursos.objects.get(años=año, Division=division) 

        # Agregar los alumnos seleccionados al curso
        for alumno_id in selected_alumnos_ids:
            alumno = get_object_or_404(Alumnos, pk=alumno_id)
            curso.alumnos.add(alumno)  # Agrega el alumno al curso actual
            messages.success(request, f"Alumno {alumno} agregado al curso {curso}.")

        return redirect('curso_detail', curso_id=curso.id)  # Redirige al detalle del curso actual

    # Obtener la lista de todos los alumnos
    todos_alumnos = Alumnos.objects.all()

    # Obtener los alumnos que ya están asignados al curso
    alumnos_asignados = curso.alumnos.all()

    # Filtrar la lista de alumnos para mostrar solo los que no están asignados
    alumnos_disponibles = todos_alumnos.exclude(pk__in=alumnos_asignados.values_list('pk', flat=True))

    context = {
        'curso': curso,  # El curso que se está viendo actualmente
        'alumnos_disponibles': alumnos_disponibles,
        'alumnos_asignados': alumnos_asignados,
        'año': curso.años,  # Pasa el año del curso actual
        'division': curso.Division,  # Pasa la división del curso actual
        'divisions': Division.objects.all()  # Pasa una lista de Divisiones
    }
    return render(request, 'agregar_alumno_curso.html', context)


def alumnos_por_materia(request, materia_id):
    materia = get_object_or_404(Materias, pk=materia_id)

    # Obtener los cursos asociados a la materia
    cursos_de_la_materia = Cursos.objects.filter(Materias=materia)

    # Obtener los alumnos de esos cursos
    alumnos = []
    for curso in cursos_de_la_materia:
        alumnos_del_curso = curso.alumnos.all()  # Obtiene los alumnos del curso actual
        alumnos.extend(alumnos_del_curso)  # Agrega los alumnos a la lista

    context = {
        'materia': materia,
        'alumnos': alumnos
    }

    return render(request, 'alumnos_por_materia.html', context)




































