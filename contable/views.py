from django.db.models import Exists, OuterRef
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, date # Importamos datetime para combinar fecha y hora
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
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
    matriculas = Matricula.objects.all().order_by('alumno__Apellidos')  # Ordenar por 'alumno__Apellidos'
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
                messages.error(request, "Ya existe una matrícula para este alumno en este año.")
                return render(request, 'matriculas_forms.html', {'form': form})

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
                messages.error(request, "El alumno no tiene un tutor asignado.")
                return render(request, 'matriculas_forms.html', {'form': form})
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
    

def get_familia(request, alumno_id):
    """Vista para obtener la familia del alumno seleccionado."""
    try:
        alumno = Alumnos.objects.get(pk=alumno_id)
        familia = alumno.Familia
        return JsonResponse({'familia_id': familia.id, 'familia_nombre': familia.Nombre_Familia})
    except Alumnos.DoesNotExist:
        return JsonResponse({'error': 'Alumno no encontrado'}, status=404)

    

def sin_tutor(request, alumno_id):
    alumno = Alumnos.objects.get(pk=alumno_id)  # Obtén el objeto Alumno usando alumno_id
    context = {
        'alumno': alumno,
    }
    return render(request, 'sin_tutor.html', context)




def imprimir_datos_padre_madre(request, matricula_id):
    matricula = get_object_or_404(Matricula, pk=matricula_id)
    alumno = matricula.alumno
    tutores = alumno.Familia.Tutores.all()  # Obtiene los tutores de la familia del alumno
    año_matriculacion = matricula.Año
    
    # Obtén el año y la división del curso
    curso_año = alumno.curso.años 
    curso_division = alumno.curso.Division

    # Define un diccionario para mapear los números a las letras del año
    letras_año = {
        '1': 'Primero',
        '2': 'Segundo',
        '3': 'Tercero',
        '4': 'Cuarto',
        '5': 'Quinto',
        '6': 'Sexto',
        '7': 'Septimo',
    }

    # Obtiene la letra del año usando el diccionario
    letra_año = letras_año.get(curso_año, curso_año)  # Si no se encuentra la clave, devuelve el mismo valor

    context = {
        'alumno': alumno,
        'tutores': tutores,
        'año_matriculacion': año_matriculacion,
        'letra_año': letra_año,
        'curso_division': curso_division,
    }
    return render(request, 'imprimir_datos_padre_madre.html', context)




                                            ##CUOTAS

def lista_cuotas(request):
    # Obtén las cuotas de los alumnos que tienen una matrícula
    cuotas = Cuotas.objects.annotate(
        tiene_matricula=Exists(
            Matricula.objects.filter(alumno=OuterRef('Alumnos_id'))
        )
    ).filter(tiene_matricula=True).order_by('Alumnos')

    # Agrupa las cuotas por alumno
    cuotas_por_alumno = {}
    for cuota in cuotas:
        alumno_id = cuota.Alumnos.id
        if alumno_id not in cuotas_por_alumno:
            cuotas_por_alumno[alumno_id] = []
        cuotas_por_alumno[alumno_id].append(cuota)

    context = {
        'cuotas_por_alumno': cuotas_por_alumno,
    }
    return render(request, 'lista_cuotas.html', context)



def detalle_cuota(request, cuota_id):
    cuota = get_object_or_404(Cuotas, pk=cuota_id)
    context = {'cuota': cuota}
    return render(request, 'detalle_cuota.html', context)

# def crear_cuota(request):
#     if request.method == 'POST':
#         form = CuotasForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Cuota creada exitosamente.')
#             return redirect('lista_cuotas')
#     else:
#         form = CuotasForm()
#     context = {'form': form}
#     return render(request, 'crear_cuota.html', context)

def editar_cuota(request, cuota_id):
    cuota = get_object_or_404(Cuotas, pk=cuota_id)
    if request.method == 'POST':
        form = CuotasForm(request.POST, instance=cuota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuota actualizada exitosamente.')
            return redirect('lista_cuotas')
    else:
        form = CuotasForm(instance=cuota)
    context = {'form': form}
    return render(request, 'editar_cuota.html', context)

# def eliminar_cuota(request, cuota_id):
#     cuota = get_object_or_404(Cuotas, pk=cuota_id)
#     if request.method == 'POST':
#         cuota.delete()
#         messages.success(request, 'Cuota eliminada exitosamente.')
#         return redirect('lista_cuotas')
#     context = {'cuota': cuota}
#     return render(request, 'eliminar_cuota.html', context)




def cuotas_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumnos, pk=alumno_id)
    
    cuotas_alumno = Cuotas.objects.filter(Alumnos=alumno)

    context = {
        'alumno': alumno,
        'cuotas_alumno': cuotas_alumno,
    }
    return render(request, 'cuotas_alumno.html', context)

def cuotas_alumno_con_pago_guardado(request, alumno_id):
    alumno = get_object_or_404(Alumnos, pk=alumno_id)
    
    cuotas_alumno = Cuotas.objects.filter(Alumnos=alumno)

    context = {
        'alumno': alumno,
        'cuotas_alumno': cuotas_alumno,
        'pago_guardado': True,
    }
    return render(request, 'cuotas_alumno.html', context)




##PAGO DE CUOTAS

def pagocuota_form(request, cuota_id):
    cuota = get_object_or_404(Cuotas, pk=cuota_id)
    alumno = cuota.Alumnos
    nuevo_ingreso = ingresos()

    # Obtener el monto de la cuota desde la URL
    monto_cuota = request.GET.get('monto')
    if monto_cuota:
        monto_cuota = float(monto_cuota)

    # Obtener el registro existente de pagocuota o crear uno nuevo
    try:
        pagocuota_obj = pagocuota.objects.get(cuota=cuota)
    except pagocuota.DoesNotExist:
        pagocuota_obj = pagocuota(cuota=cuota)

    # Obtener los tutores del alumno
    tutores = alumno.Familia.Tutores.all()

    # Variable para almacenar el monto del descuento
    monto_descuento = 0
    fecha_descuento = None  # Inicializa fecha_descuento

    if request.method == 'POST':
        # Obtiene los datos del formulario
        efectivo = request.POST.get('efectivo')
        transferencia = request.POST.get('transferencia')
        cheque = request.POST.get('cheque')
        pagare = request.POST.get('pagare')
        # Obtener el tutor seleccionado
        tutor_seleccionado_id = request.POST.get('tutor')
        tutor_seleccionado = Tutores.objects.get(pk=tutor_seleccionado_id)

        # Guardar el ID del tutor seleccionado en la sesión
        request.session['tutor_seleccionado_id'] = tutor_seleccionado_id

        # Obtiene el descuento seleccionado
        descuento_aplicado = request.POST.get('descuento_aplicado')

        # Aplica el descuento si está seleccionado
        if descuento_aplicado:
            monto_cuota_original = cuota.Monto_cuota  # Obtén el monto original de la cuota
            if descuento_aplicado == '5':
                monto_cuota = monto_cuota_original * 0.95  # Descuento del 5%
                monto_descuento = monto_cuota_original * 0.05  # Calcula el monto del descuento
            elif descuento_aplicado == '25':
                monto_cuota = monto_cuota_original * 0.75  # Descuento del 25%
                monto_descuento = monto_cuota_original * 0.25  # Calcula el monto del descuento
            elif descuento_aplicado == '50':
                monto_cuota = monto_cuota_original * 0.50  # Descuento del 50%
                monto_descuento = monto_cuota_original * 0.50  # Calcula el monto del descuento

            # Redondea el monto del descuento al múltiplo de 500 más cercano
            if monto_descuento >= 500:
                monto_descuento = round(monto_descuento / 500) * 500

            # Calcula el monto de la cuota con el descuento redondeado
            monto_cuota = monto_cuota_original - monto_descuento 

            # Aplica la lógica para redondear al múltiplo de 50
            resto = monto_cuota % 50
            if resto <= 50:
                monto_cuota = monto_cuota - resto
            else:
                monto_cuota = monto_cuota + (100 - resto)

            fecha_descuento = timezone.now()  # Guarda la fecha actual

        # Calcula el total pagado
        total_pagado = (float(efectivo) if efectivo else 0) + \
                       (float(transferencia) if transferencia else 0) + \
                       (float(cheque) if cheque else 0) + \
                       (float(pagare) if pagare else 0)

        # Verifica si el pago es mayor al monto restante
        monto_restante = monto_cuota - (
            pagocuota_obj.efectivo or 0) - (pagocuota_obj.transferencia or 0) - (pagocuota_obj.cheque or 0) - (pagocuota_obj.pagare or 0)
        if total_pagado > monto_restante:
            messages.error(request, f'El pago ingresado excede el monto de la cuota.')
            return redirect('cuotas_alumno', alumno_id=cuota.Alumnos.id)

        # Actualizar el registro de pagocuota
        pagocuota_obj.efectivo = (pagocuota_obj.efectivo or 0) + (float(efectivo) if efectivo else 0)
        pagocuota_obj.transferencia = (pagocuota_obj.transferencia or 0) + (float(transferencia) if transferencia else 0)
        pagocuota_obj.cheque = (pagocuota_obj.cheque or 0) + (float(cheque) if cheque else 0)
        pagocuota_obj.pagare = (pagocuota_obj.pagare or 0) + (float(pagare) if pagare else 0)

        # Guardar el descuento en el registro de pagocuota
        pagocuota_obj.descuento = monto_descuento  # Guarda el monto total del descuento
        pagocuota_obj.save()

        # Actualiza la fecha de pago en la cuota
        cuota.Fecha_hora_del_pago = timezone.now()

        # Calcula el monto restante
        monto_restante = monto_cuota - (
            pagocuota_obj.efectivo or 0) - (pagocuota_obj.transferencia or 0) - (pagocuota_obj.cheque or 0) - (pagocuota_obj.pagare or 0)

        # Actualizar el estado de la cuota (solo si el monto restante es 0)
        TOLERANCIA = 0.01
        if abs(monto_restante) <= TOLERANCIA:
            cuota.Pagado = True
            messages.success(request, f'La cuota ha sido pagada completamente.')

        # Guarda los cambios en la cuota
        cuota.save()

        # Redirecciona a 'cuotas_alumno_con_pago_guardado'
        return redirect('cuotas_alumno_con_pago_guardado', alumno_id=cuota.Alumnos.id)

    # Calcula el total pagado para mostrar en la plantilla
    total_pagado = (pagocuota_obj.efectivo or 0) + \
                   (pagocuota_obj.transferencia or 0) + \
                   (pagocuota_obj.cheque or 0) + \
                   (pagocuota_obj.pagare or 0)

    # Calcula el monto restante
    monto_restante = monto_cuota - total_pagado

    # Obtiene todas las fechas de pago parciales
    fechas_pago = [pagocuota.cuota.Fecha_hora_del_pago for pagocuota in cuota.pagocuota_set.all()]

    context = {
        'cuota': cuota,
        'pagocuota_obj': pagocuota_obj,
        'total_pagado': total_pagado,
        'monto_cuota': monto_cuota,  # Pasar el monto de la cuota (con descuento)
        'monto_restante': monto_restante,  # Pasar el monto restante (con descuento)
        'monto_descuento': monto_descuento,  # Pasar el monto del descuento
        'fecha_descuento': fecha_descuento,  # Pasar la fecha del descuento
        'fechas_pago': fechas_pago,
        'mostrar_boton_pagar': not cuota.Pagado,
        'tutores': tutores, # Pasa los tutores al contexto
        'alumno': alumno  # Pasa el alumno al contexto
    }
    return render(request, 'pagocuota_form.html', context)

def detalle_pago(request, cuota_id):
    cuota = get_object_or_404(Cuotas, pk=cuota_id)

    # Obtén todos los pagos asociados a la cuota
    pagocuotas = cuota.pagocuota_set.all()

    # Agrupa los pagos por fecha de pago
    pagos_agrupados = {}
    for pagocuota in pagocuotas:
        fecha_pago = pagocuota.cuota.Fecha_hora_del_pago
        if fecha_pago not in pagos_agrupados:
            pagos_agrupados[fecha_pago] = []
        pagos_agrupados[fecha_pago].append(pagocuota)

    # Calcula el total de pago, descuento total y monto final
    total_pago = 0
    descuento_total = 0
    for pagocuota in pagocuotas:
        total_pago += (pagocuota.efectivo or 0) + (pagocuota.transferencia or 0) + (pagocuota.cheque or 0) + (pagocuota.pagare or 0)
        descuento_total += pagocuota.descuento or 0

    # Define monto_total antes del bloque if
    monto_total = cuota.Monto_cuota  # Obtén el valor del atributo Monto_cuota

    # Redondea el descuento total al múltiplo de 50, 500 o 5000 más cercano
    if descuento_total >= 5000:
        descuento_total = round(descuento_total / 5000) * 5000
    elif descuento_total >= 500:
        descuento_total = round(descuento_total / 500) * 500
    elif descuento_total >= 50:
        descuento_total = round(descuento_total / 50) * 50

    monto_final = cuota.Monto_cuota - descuento_total

    # Obtén la última fecha de pago (si hay)
    ultima_fecha_pago = None
    ultimo_metodo_pago = None
    for pagocuota in pagocuotas:
        if pagocuota.cuota.Fecha_hora_del_pago:
            ultima_fecha_pago = pagocuota.cuota.Fecha_hora_del_pago
            ultimo_metodo_pago = "Efectivo" if pagocuota.efectivo else "Transferencia" if pagocuota.transferencia else "Cheque" if pagocuota.cheque else "Pagaré" if pagocuota.pagare else "Desconocido"
            break

    # Obtén el ID del tutor seleccionado de la sesión
    tutor_seleccionado_id = request.session.get('tutor_seleccionado_id')

    # Obtén el tutor seleccionado (si hay)
    tutor_seleccionado = None
    if tutor_seleccionado_id:
        tutor_seleccionado = Tutores.objects.get(pk=tutor_seleccionado_id)

    # Convertir ultima_fecha_pago a un objeto datetime si es solo una fecha
    if isinstance(ultima_fecha_pago, date):
        ultima_fecha_pago = datetime.combine(ultima_fecha_pago, datetime.min.time())

    context = {
        'cuota': cuota,
        'pagos_agrupados': pagos_agrupados, # Diccionario con pagos agrupados
        'total_pago': total_pago,
        'descuento_total': descuento_total,
        'monto_final': monto_final,
        'monto_total': monto_total,  # Pasar el monto total redondeado
        'ultima_fecha_pago': ultima_fecha_pago,
        'ultimo_metodo_pago': ultimo_metodo_pago,
        'tutor_seleccionado': tutor_seleccionado 
    }

    return render(request, 'detalle_pago.html', context)




### ACUTALIZACION DE CUOTAS

def actualizar_cuotas(request):
    if request.method == 'POST':
        # Obtener el monto ingresado desde el formulario
        nuevo_monto = request.POST.get('nuevo_monto')

        # Validar que el monto ingresado sea un número válido
        try:
            nuevo_monto = float(nuevo_monto)
        except ValueError:
            # Manejar error de validación (por ejemplo, mostrar un mensaje de error)
            return render(request, 'actualizar_cuotas.html', {'error': 'Ingresa un monto válido.'})

        # Actualiza el Monto_cuota para todas las cuotas no canceladas
        Cuotas.objects.filter(Pagado=False).update(Monto_cuota=nuevo_monto)
        # Redirige a la vista de la lista de alumnos
        return HttpResponseRedirect(reverse('lista_cuotas'))

    else:
        # Muestra el formulario de actualización
        return render(request, 'actualizar_cuotas.html')