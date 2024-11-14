from django.db.models import Exists, OuterRef
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, date # Importamos datetime para combinar fecha y hora
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
import locale
from django.views.decorators.csrf import csrf_exempt  # Exenta de la comprobación CSRF
from django.db.models import Sum
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.views.generic import ListView, UpdateView, FormView,CreateView

# Create your views here.


@login_required
def contable(request):
    return render(request, "indexcontable.html")



recibo_contador = 1  # Variable global para el contador de recibos

def generar_numero_recibo():
    global recibo_contador
    numero = recibo_contador
    recibo_contador += 1
    return numero

@login_required

def recibo(request, cuota_id=None, matricula_id=None, recibo_id=None):
    if recibo_id:
        # Mostrar el recibo generado
        recibo = get_object_or_404(Recibo, pk=recibo_id)
        context = {
            'recibo': recibo
        }
        return render(request, 'recibo_detalle.html', context)
    
    if cuota_id:
        # Recibo de cuota
        cuota = get_object_or_404(Cuotas, pk=cuota_id)

        # Obtén los pagos asociados a la cuota
        pagocuotas = cuota.pagocuota_set.all()

        # Obtiene la fecha actual
        fecha_actual = timezone.now().strftime('%d/%m/%Y')

        # Agrupa los pagos por fecha de pago y tutor
        pagos_agrupados = {}
        for pagocuota in pagocuotas:
            fecha_pago = pagocuota.cuota.Fecha_hora_del_pago
            tutor = pagocuota.cuota.Tutor
            if fecha_pago not in pagos_agrupados:
                pagos_agrupados[fecha_pago] = {}
            if tutor not in pagos_agrupados[fecha_pago]:
                pagos_agrupados[fecha_pago][tutor] = []
            pagos_agrupados[fecha_pago][tutor].append({
                "pagocuota": pagocuota,
                "nombre_tutor": tutor.Nombre + " " + tutor.Apellido
            })

        # Calcula el total de pago, descuento total y monto final
        total_pago = 0
        descuento_total = 0
        for pagocuota in pagocuotas:
            total_pago += (pagocuota.efectivo or 0) + (pagocuota.transferencia or 0) + (pagocuota.cheque or 0) + (pagocuota.pagare or 0)
            descuento_total += pagocuota.descuento or 0

        # Redondea el descuento total al múltiplo de 50, 500 o 5000 más cercano
        if descuento_total >= 5000:
            descuento_total = round(descuento_total / 5000) * 5000
        elif descuento_total >= 500:
            descuento_total = round(descuento_total / 500) * 500
        elif descuento_total >= 50:
            descuento_total = round(descuento_total / 50) * 50

        # Define monto_total antes del bloque if
        monto_total = cuota.Monto_cuota
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

        # Obtén los tutores asociados a la cuota
        tutores_asociados = Tutores.objects.filter(cuotas__in=[cuota])

        # Define un diccionario para obtener el nombre del mes por ID
        meses = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre',
        }

        mes_nombre = meses.get(cuota.Mes, cuota.Mes) # Si la clave no está en el diccionario, usa el valor de cuota.Mes

        # Genera el número de recibo consecutivo
        recibo_numero = generar_numero_recibo()

        # Guarda el recibo en la base de datos
        recibo = Recibo.objects.create(
            matricula=cuota.Alumnos.matricula_set.first(),  # Obtén la matrícula desde la cuota
            cuota=cuota,
            tutor=cuota.Tutor,  # Obtén el tutor desde la cuota
            Fecha_hora_del_pago=ultima_fecha_pago  # Si hay un pago, usa la última fecha
        )

        # Crea el contexto para el template
        context = {
            'cuota': cuota,
            'pagos_agrupados': pagos_agrupados,
            'total_pago': total_pago,
            'descuento_total': descuento_total,
            'monto_final': monto_final,
            'monto_total': monto_total,
            'ultima_fecha_pago': ultima_fecha_pago,
            'ultimo_metodo_pago': ultimo_metodo_pago,
            'tutor_seleccionado': tutor_seleccionado,
            'tutores_asociados': tutores_asociados,
            'año': cuota.Año,
            'mes_nombre': mes_nombre,
            'recibo_numero': recibo_numero,
            'recibo': recibo,
            'fecha_actual': fecha_actual
        }

        # Renderiza el template recibo.html
        return render(request, 'recibo.html', context)

    elif matricula_id:
        # Recibo de matrícula
        matricula = get_object_or_404(Matricula, pk=matricula_id)

        # Obtén los pagos de matrícula asociados
        pagos_matricula = pagomatricula.objects.filter(matriculas=matricula)

        # Obtiene la fecha actual
        fecha_actual = timezone.now().strftime('%d/%m/%Y')
        
        # Calcula el total de pago y descuento total
        total_pago = 0
        descuento_total = 0
        for pago in pagos_matricula:
            total_pago += (pago.efectivo or 0) + (pago.transferencia or 0) + (pago.cheque or 0) + (pago.pagare or 0)
            descuento_total += pago.descuento or 0

        # Calcula el monto final
        monto_final = matricula.monto_total - descuento_total

        # Obtén la última fecha de pago (si hay)
        ultima_fecha_pago = None
        ultimo_metodo_pago = None
        for pago in pagos_matricula:
            if pago.fecha_pago_matricula:
                ultima_fecha_pago = pago.fecha_pago_matricula
                ultimo_metodo_pago = "Efectivo" if pago.efectivo else "Transferencia" if pago.transferencia else "Cheque" if pago.cheque else "Pagaré" if pago.pagare else "Desconocido"
                break

        # Obtén el ID del tutor seleccionado de la sesión
        tutor_seleccionado_id = request.session.get('tutor_seleccionado_id')

        # Obtén el tutor seleccionado (si hay)
        tutor_seleccionado = None
        if tutor_seleccionado_id:
            tutor_seleccionado = Tutores.objects.get(pk=tutor_seleccionado_id)

        # Genera el número de recibo consecutivo
        recibo_numero = generar_numero_recibo()

        # Guarda el recibo en la base de datos
        recibo = Recibo.objects.create(
            matricula=matricula,
            cuota=None,  # Si es un recibo de matrícula, cuota es None
            tutor=matricula.alumno.cuotas.first().Tutor,  # Obtén el tutor desde la matrícula
            Fecha_hora_del_pago=ultima_fecha_pago  # Si hay un pago, usa la última fecha
        )

        # Crea el contexto para el template
        context = {
            'matricula': matricula,
            'pagos_matricula': pagos_matricula,  # Lista de pagos de matrícula
            'total_pago': total_pago,
            'descuento_total': descuento_total,
            'monto_final': monto_final,
            'ultima_fecha_pago': ultima_fecha_pago,
            'ultimo_metodo_pago': ultimo_metodo_pago,
            'tutor_seleccionado': tutor_seleccionado,
            'recibo_numero': recibo_numero,
            'recibo': recibo,
            'fecha_actual': fecha_actual  # Agrega el objeto Recibo al contexto
        }

        # Renderiza el template recibo.html
        return redirect('recibo_detalle', recibo_id=recibo.id)  # Redirige al detalle del recibo

    else:
        # Maneja el caso en que no se proporcionó ni cuota_id ni matricula_id
        return render(request, 'error.html', {'error': 'No se especificó un tipo de recibo válido'})
def lista_recibos(request):
    # Obtén todos los recibos
    recibos = Recibo.objects.all()

    # Agrega el atributo "tipo" a cada recibo
    for recibo in recibos:
        if recibo.cuota:
            recibo.tipo = 'Cuota'
        elif recibo.matricula:
            recibo.tipo = 'Matrícula'
        else:
            recibo.tipo = 'Desconocido'  # En caso de que no se pueda determinar el tipo

    # Crea el contexto para el template
    context = {
        'recibos': recibos,
    }

    return render(request, 'lista_recibos.html', context)

def recibo_detalle(request, recibo_id):
    recibo = get_object_or_404(Recibo, pk=recibo_id)

    context = {
        'recibo': recibo,
    }

    return render(request, 'recibo_detalle.html', context)
                ## MATRICULAS

@login_required  # Asegúrate de que el usuario esté autenticado
@csrf_exempt  # Exenta de la comprobación CSRF
def eliminar_matricula(request, matricula_id):
    if request.method == 'POST':
        try:
            matricula = Matricula.objects.get(pk=matricula_id)
            matricula.delete()
            return JsonResponse({'success': True})  # Retorna un JSON para indicar éxito
        except Matricula.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Matrícula no encontrada'})
    else:
        # Maneja las solicitudes no POST (por ejemplo, muestra un error)
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

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

                # Obtén el monto_matricula de la instancia recién creada
                monto_cuota = matricula.monto_matricula

                # Crea las cuotas para el alumno actual
                meses = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                for mes in meses:
                    Cuotas.objects.create(
                        Mes=mes,
                        Año=matricula.Año,
                        Monto_cuota=monto_cuota,  # Usa el monto_matricula de la Matricula
                        Alumnos=alumno,
                        Extraordinario='',
                        Tutor=tutor
                    )
            
                # Redirige a la vista de pago con el monto de la matrícula
                return redirect('pagar_matricula', matricula_id=matricula.id)
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
    
    # Convierte el ID del mes a su nombre textual en español
    meses_es = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }
    
    # Convierte el ID del mes a su nombre textual
    for cuota in cuotas_alumno:
        cuota.mes_nombre = meses_es[int(cuota.Mes)]  # Asigna el nombre del mes
    
    context = {
        'alumno': alumno,
        'cuotas_alumno': cuotas_alumno,
    }
    return render(request, 'cuotas_alumno.html', context)

def cuotas_alumno_con_pago_guardado(request, alumno_id):
    alumno = get_object_or_404(Alumnos, pk=alumno_id)
    
    cuotas_alumno = Cuotas.objects.filter(Alumnos=alumno)

    meses_es = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }
    # Convierte el ID del mes a su nombre textual
    for cuota in cuotas_alumno:
        cuota.mes_nombre = meses_es[int(cuota.Mes)]  # Asigna el nombre del mes

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
    nuevo_ingreso = ingresos()  # Elimina la instancia de ingresos aquí

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

            # Redondea el monto del descuento al múltiplo de 1000 más cercano
            monto_descuento = round(monto_descuento / 1000) * 1000

            # Calcula el monto de la cuota con el descuento redondeado
            monto_cuota = monto_cuota_original - monto_descuento 

            # Redondea el monto de la cuota al múltiplo de 1000 más cercano
            monto_cuota = round(monto_cuota / 1000) * 1000

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

        # Impacta el pago en el modelo ingresos
        nuevo_ingreso = ingresos.objects.create(
            descripcion=f"Pago de cuota {cuota.id} - {alumno}",
            monto=total_pagado,
            tipo_ingreso="Cuota",
            fecha=timezone.now().date()
        )

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

    # Agrupa los pagos por fecha de pago y tutor
    pagos_agrupados = {}
    for pagocuota in pagocuotas:
        fecha_pago = pagocuota.cuota.Fecha_hora_del_pago
        tutor = pagocuota.cuota.Tutor  # Obtén el tutor desde la cuota
        if fecha_pago not in pagos_agrupados:
            pagos_agrupados[fecha_pago] = {}  # Crea un diccionario para cada fecha
        if tutor not in pagos_agrupados[fecha_pago]:
            pagos_agrupados[fecha_pago][tutor] = []  # Crea una lista para cada tutor
        # Agrega el nombre del tutor a los pagos
        pagos_agrupados[fecha_pago][tutor].append({
            "pagocuota": pagocuota,
            "nombre_tutor": tutor.Nombre + " " + tutor.Apellido
        }) 

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

    # Obtén los tutores asociados a la cuota
    tutores_asociados = Tutores.objects.filter(cuotas__in=[cuota]) 

    # Define un diccionario para obtener el nombre del mes por ID
    meses = {
        '01': 'Enero',
        '02': 'Febrero',
        '03': 'Marzo',
        '04': 'Abril',
        '05': 'Mayo',
        '06': 'Junio',
        '07': 'Julio',
        '08': 'Agosto',
        '09': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',
    }

    mes_nombre = meses.get(cuota.Mes, cuota.Mes) # Si la clave no está en el diccionario, usa el valor de cuota.Mes

    context = {
        'cuota': cuota,
        'pagos_agrupados': pagos_agrupados, # Diccionario con pagos agrupados
        'total_pago': total_pago,
        'descuento_total': descuento_total,
        'monto_final': monto_final,
        'monto_total': monto_total,  # Pasar el monto total redondeado
        'ultima_fecha_pago': ultima_fecha_pago,
        'ultimo_metodo_pago': ultimo_metodo_pago,
        'tutor_seleccionado': tutor_seleccionado,
        'tutores_asociados': tutores_asociados, # Pasa la lista de tutores asociados
        'año': cuota.Año,  # Obtén el año desde el objeto cuota
        'mes_nombre': mes_nombre, 
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
    


## PAGO DE MATRICULA

def pagar_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, pk=matricula_id)
    monto_total = matricula.monto_matricula

    if request.method == 'POST':
        # Obtén los datos del formulario de pago
        efectivo = request.POST.get('efectivo', 0)
        transferencia = request.POST.get('transferencia', 0)
        cheque = request.POST.get('cheque', 0)
        pagare = request.POST.get('pagare', 0)
        descuento = request.POST.get('descuento', 0)

        # Valida que al menos un método de pago esté seleccionado
        if not any([efectivo, transferencia, cheque, pagare]):
            messages.error(request, "Debes seleccionar al menos un método de pago.")
            return render(request, 'pagar_matricula.html', {'monto_total': monto_total, 'matricula': matricula})

        # Valida pagos únicos
        if pagomatricula.objects.filter(matriculas=matricula).exists():
            messages.error(request, "Esta matrícula ya ha sido pagada.")
            return render(request, 'pagar_matricula.html', {'monto_total': monto_total, 'matricula': matricula})

        # Convierte los valores a números si no están vacíos
        efectivo = float(efectivo) if efectivo else 0.0 
        transferencia = float(transferencia) if transferencia else 0.0 
        cheque = float(cheque) if cheque else 0.0 
        pagare = float(pagare) if pagare else 0.0
        descuento = float(descuento) if descuento else 0.0

        # Crea un nuevo objeto Pagomatricula
        nuevo_pago = pagomatricula.objects.create(
            matriculas=matricula,  # Usa la relación 'matriculas'
            efectivo=efectivo,
            transferencia=transferencia,
            cheque=cheque,
            pagare=pagare,
            descuento=descuento,  # Guarda el descuento
            Pagado=True  # Marca como pagado
        )

        # Calcula el monto total pagado (con descuento)
        total_pagado = efectivo + transferencia + cheque + pagare - descuento

        # Actualiza el estado "pagado" en la matrícula
        matricula.pagado = True
        matricula.save()

        # Registra el pago en el modelo "ingresos"
        ingresos.objects.create(
            descripcion=f"Pago de matrícula {matricula.alumno.Nombres} {matricula.alumno.Apellidos}",
            monto=total_pagado,
            tipo_ingreso="Matrícula",
            fecha=nuevo_pago.fecha_pago_matricula  # Usa la fecha del pago
        )

        # Redirige a la vista 'listar_matriculas'
        return redirect('listar_matriculas')
    else:
        return render(request, 'pagar_matricula.html', {'monto_total': monto_total, 'matricula': matricula})

def detalle_pago_matricula(request, matricula_id):
    # Busca la matrícula por ID
    matricula = get_object_or_404(Matricula, pk=matricula_id)
    
    # Busca los detalles del pago para esta matrícula
    pagos = pagomatricula.objects.filter(matriculas=matricula)

    # Crea un diccionario para agrupar los pagos por fecha
    pagos_agrupados = {}
    for pago in pagos:
        fecha_pago = pago.fecha_pago_matricula.strftime("%Y-%m-%d")
        if fecha_pago not in pagos_agrupados:
            pagos_agrupados[fecha_pago] = []
        pagos_agrupados[fecha_pago].append(pago)

    # Calcula el total pagado
    total_pagado = sum([
        (pago.efectivo or 0) + (pago.transferencia or 0) + (pago.cheque or 0) + (pago.pagare or 0)
        for pago in pagos
    ])
     # Obtén el año de la matrícula
    año_matricula = matricula.Año
    # Obtén el mes y el año actual
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    mes_actual = datetime.now().strftime("%B")  # Nombre completo del mes en inglés
    año_actual = datetime.now().year
    return render(request, 'detalle_pago_matricula.html', {
        'matricula': matricula,
        'pagos_agrupados': pagos_agrupados,
        'total_pagado': total_pagado,
        'año_matricula': matricula.Año  # Pasa el año como contexto
    })

def generar_recibo(request, matricula_id):
    matricula = get_object_or_404(Matricula, pk=matricula_id)
    pagos = pagomatricula.objects.filter(matriculas=matricula)

    # Obtener el año de la matrícula
    año_matricula = matricula.Año
    # Obtén el mes y el año actual
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    mes_actual = datetime.now().strftime("%B")  # Nombre completo del mes en inglés
    año_actual = datetime.now().year

    # Calcular el total pagado
    total_pagado = 0
    for pago in pagos:
        total_pagado += (pago.efectivo or 0) + (pago.transferencia or 0) + (pago.cheque or 0) + (pago.pagare or 0)

    # Calcular descuentos (si aplica)
    descuento_total = 0  # Reemplaza con la lógica para calcular descuentos
    recibo_numero = generar_numero_recibo()
    # Calcular monto final
    monto_final = total_pagado - descuento_total

    # Crear un nuevo objeto Recibo
    recibo = Recibo.objects.create(
        matricula=matricula,
        cuota=None,  # Ya establecido anteriormente
        tutor=None,  # Establecer tutor como None si no hay tutor asociado
        Fecha_hora_del_pago=datetime.now(),  # Fecha y hora actual
        pagado=True  # Se asume que el recibo se genera cuando el pago se realiza
    )

    # Guardar el recibo en la base de datos
    recibo.save()

    return render(request, 'recibo_matricula.html', {
        'matricula': matricula,
        'pagos': pagos,
        'año_matricula' : año_matricula,
        'recibo_numero' : recibo_numero,
        'mes_actual': mes_actual,
        'año_actual': año_actual,
        'total_pagado': total_pagado,
        'descuento_total': descuento_total,
        'monto_final': monto_final,
        'fecha_actual' : fecha_actual,
        'recibo': recibo  # Pasar el objeto Recibo a la plantilla
    })




def confirmacion_pago(request):
    if request.method == 'POST':
        # Obtén la matrícula de la sesión
        matricula_id = request.session.get('matricula_id')
        matricula = Matricula.objects.get(pk=matricula_id)

        # Actualiza el estado de pagado de la matrícula
        matricula.pagado = True
        matricula.save()

        # Elimina la información de la matrícula de la sesión
        del request.session['matricula_id']

        # Redirige a la lista de matriculas
        messages.success(request, "Pago realizado correctamente!")
        return redirect('listar_matriculas')
    else:
        # Si no se realiza una solicitud POST, redirige a la lista de matriculas
        return redirect('listar_matriculas')

def actualizar_matricula(request, matricula_id):
    if request.method == 'POST':
        matricula = get_object_or_404(Matricula, pk=matricula_id)

        # Verifica si hay pagos asociados a la matrícula
        if pagomatricula.objects.filter(matriculas=matricula).exists():
            matricula.pagado = True 
        else:
            matricula.pagado = False 

        matricula.save()

        return JsonResponse({'pagado': matricula.pagado}) 
    else:
        return JsonResponse({'error': 'Método no permitido'})
    


## EXTRAS

def extras_list(request):
    all_extras = extras.objects.all()  # Obtiene todos los extras
    context = {'extras': all_extras}
    return render(request, 'extras_list.html', context)

def extras_create(request):
    if request.method == 'POST':
        form = ExtrasForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            fecha_actual = date.today()  # Obtiene la fecha actual
            if tipo == 'INGRESO':
                # Crea un objeto Ingreso
                ingreso = ingresos(
                    descripcion=form.cleaned_data['descripcion'],
                    monto=form.cleaned_data['monto'],
                    tipo_ingreso=form.cleaned_data['tipo'], 
                    fecha=fecha_actual
                )
                ingreso.save()

                # Crea un objeto extras relacionado al ingreso
                extras_obj = extras(
                    ingreso=ingreso,  # Relaciona con el ingreso
                    descripcion=form.cleaned_data['descripcion'],
                    monto=form.cleaned_data['monto'],
                    fecha=fecha_actual
                )
                extras_obj.save()

            elif tipo == 'EGRESO':
                # Crea un objeto Egreso
                egresos = egreso(
                    descripcion=form.cleaned_data['descripcion'],
                    monto=form.cleaned_data['monto'],
                    tipo_ingreso=form.cleaned_data['tipo'], 
                    fecha=fecha_actual
                )
                egresos.save()

                # Crea un objeto extras relacionado al egreso
                extras_obj = extras(
                    egreso=egresos,  # Relaciona con el egreso
                    descripcion=form.cleaned_data['descripcion'],
                    monto=form.cleaned_data['monto'],
                    fecha=fecha_actual
                )
                extras_obj.save()

            return redirect('extras_list')  # Reemplaza con la URL de tu lista
    else:
        form = ExtrasForm()
    context = {'form': form}
    return render(request, 'extras_form.html', context)

def extras_detail(request, pk):
    extras_item = get_object_or_404(extras, pk=pk)
    context = {'extras': extras_item}
    return render(request, 'extras_detail.html', context)

def extras_update(request, pk):
    extras_item = get_object_or_404(extras, pk=pk)
    if request.method == 'POST':
        form = ExtrasForm(request.POST, instance=extras_item)
        if form.is_valid():
            form.save()
            return redirect('extras_list')
    else:
        form = ExtrasForm(instance=extras_item)
    context = {'form': form}
    return render(request, 'extras_form.html', context)

def extras_delete(request, pk):
    extras_item = get_object_or_404(extras, pk=pk)
    if request.method == 'POST':
        extras_item.delete()
        return redirect('extras_list')
    context = {'extras': extras_item}
    return render(request, 'extras_confirm_delete.html', context)

