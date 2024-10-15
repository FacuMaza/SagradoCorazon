from django.contrib import messages
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from .models import *
from .forms import *
from django.views.generic import ListView, UpdateView, FormView,CreateView

# Create your views here.


@login_required
def contable(request):
    return render(request, "indexcontable.html")


                ## MATRICULAS

def listar_matriculas(request):
    matriculas = Matricula.objects.all()
    context = {'matriculas': matriculas}
    return render(request, 'listar_matriculas.html', context)

def crear_matricula(request):
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            # Obtén el objeto Alumno desde el formulario
            alumno = form.cleaned_data['alumno'] 

            # Obtén la familia del alumno
            familia = alumno.Familia

            # Verifica si ya existe una matrícula para este alumno en este año
            existing_matricula = Matricula.objects.filter(alumno=alumno, Año=form.cleaned_data['Año']).exists()
            if existing_matricula:
                # Si existe, muestra un mensaje de error y redirige al formulario
              
                return render(request, 'matricula_existe.html', {'form': form})

            # Verifica si el alumno tiene un tutor
            tutor = familia.Tutores.first()
            if tutor:
                # Guarda la matrícula
                matricula = form.save(commit=False)
                matricula.pagado = False
                matricula.save()

                # Crea las cuotas para el alumno actual
                meses = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                for mes in meses:
                    Cuotas.objects.create(
                        Mes=mes,
                        Año=matricula.Año,
                        Monto_cuota=200000.00,
                        Alumnos=alumno,
                        Extraordinario='',
                        Tutor=tutor
                    )
                return redirect('/matriculas/')
            else:
                # Si no tiene tutor, muestra un mensaje de error y no guarda la matrícula
             
                return render(request, 'sintutor.html', {'form': form})
    else:
        form = MatriculaForm()
        # Obtener la familia seleccionada (si la hay) desde la URL
        familia_id = request.GET.get('familia_id')
        if familia_id:
            # Obtener la familia seleccionada
            familia = Familia.objects.get(pk=familia_id)
            # Obtener los alumnos de la familia seleccionada
            alumnos = Alumnos.objects.filter(Familia=familia)
        else:
            # Si no se ha seleccionado una familia, mostrar una lista vacía
            alumnos = []  

        return render(request, 'matriculas_forms.html', {'form': form,'alumnos': alumnos})

    

def sin_tutor(request, alumno_id):
    alumno = Alumnos.objects.get(pk=alumno_id)  # Obtén el objeto Alumno usando alumno_id
    context = {
        'alumno': alumno,
    }
    return render(request, 'sin_tutor.html', context)
       