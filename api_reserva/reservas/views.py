from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import Reserva, Cliente, Encargado, Complejo, Cabania, Servicio, ReservaServicio
from .forms import formCabania, formEncargado, formCliente, formComplejo, formServicio, formReserva, formReservaServicio
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from django.contrib.auth import logout
from django.http import HttpResponse
from datetime import datetime
from django.forms import inlineformset_factory

# Create your views here.

def main(request):
    """
    Vista principal que recupera información de la base de datos para mostrar en la plantilla 'main.html'.

    Obtiene todos los objetos de las diferentes tablas de la base de datos para mostrar en la página principal.

    Returns:
        HttpResponse: Renderiza la plantilla 'main.html' con el contexto que contiene los datos recuperados.
    """
    reservas = Reserva.objects.all()
    clientes = Cliente.objects.all()
    encargados = Encargado.objects.all()
    complejos = Complejo.objects.all()
    cabanias = Cabania.objects.all()
    servicios = Servicio.objects.all()
    reservaServicio = ReservaServicio.objects.all()

    context = {'reservas': reservas,
               'clientes': clientes,
               'encargados': encargados,
               'complejos': complejos,
               'cabanias': cabanias,
               'servicios':servicios,
               'reservaServicio':reservaServicio}
    
    return render(request, 'main.html', context)


def detalle_cliente(request, cliente_id):
    """
    Vista que muestra los detalles de un cliente específico identificado por su ID.

    Recupera y muestra los detalles de un cliente, identificado por el parámetro cliente_id, 
    incluyendo todos los atributos disponibles del cliente.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        cliente_id (int): El ID del cliente del cual se mostrarán los detalles.

    Returns:
        HttpResponse: Renderiza la plantilla 'detalle_cliente.html' con el contexto que contiene los detalles del cliente.
    
    Raises:
        Cliente.DoesNotExist: Si el cliente con el ID proporcionado no existe en la base de datos.
    """
    cliente = Cliente.objects.get(id=cliente_id) #solo toma el id del cliente         #toma todos los atributos del cliente

    context = {
        'cliente': cliente
    }
    return render(request, 'detalle_cliente.html', context)


def detalle_encargado(request, encargado_id):
    """
    Vista que muestra los detalles de un encargado específico identificado por su ID.

    Recupera y muestra los detalles de un encargado, identificado por el parámetro encargado_id, 
    incluyendo todos los atributos disponibles del encargado.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        encargado_id (int): El ID del encargado del cual se mostrarán los detalles.

    Returns:
        HttpResponse: Renderiza la plantilla 'detalle_encargado.html' con el contexto que contiene los detalles del encargado.
    
    Raises:
        Encargado.DoesNotExist: Si el encargado con el ID proporcionado no existe en la base de datos.
    """
    encargado = Encargado.objects.get(id=encargado_id)

    context={
        'encargado': encargado
    }
    return render(request,'detalle_encargado.html', context)


def detalle_complejo(request, complejo_id):
    """
    Vista que muestra los detalles de un complejo específico identificado por su ID.

    Recupera y muestra los detalles de un complejo, identificado por el parámetro complejo_id, 
    incluyendo todos los atributos disponibles del complejo.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        complejo_id (int): El ID del complejo del cual se mostrarán los detalles.

    Returns:
        HttpResponse: Renderiza la plantilla 'detalle_complejo.html' con el contexto que contiene los detalles del complejo.
    
    Raises:
        Complejo.DoesNotExist: Si el complejo con el ID proporcionado no existe en la base de datos.
    """
    complejo = Complejo.objects.get(id=complejo_id)

    context = {
        'complejo': complejo
    }
    return render(request, 'detalle_complejo.html', context)


def detalle_cabania(request, cabania_id):
    """
    Vista que muestra los detalles de una cabaña específica identificada por su ID.

    Recupera y muestra los detalles de una cabaña, identificada por el parámetro cabania_id, 
    incluyendo todos los atributos disponibles de la cabaña.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        cabania_id (int): El ID de la cabaña de la cual se mostrarán los detalles.

    Returns:
        HttpResponse: Renderiza la plantilla 'detalle_cabania.html' con el contexto que contiene los detalles de la cabaña.
    
    Raises:
        Cabania.DoesNotExist: Si la cabaña con el ID proporcionado no existe en la base de datos.
    """
    cabania = Cabania.objects.get(id=cabania_id)

    context = {
        'cabania': cabania
    }
    return render(request, 'detalle_cabania.html', context)

def detalle_reserva(request, reserva_id):
    """
    Vista que muestra los detalles de una reserva específica identificada por su ID.

    Recupera y muestra los detalles de una reserva, identificada por el parámetro reserva_id, 
    incluyendo el cálculo del precio total de la reserva, considerando el precio de la cabaña y servicios asociados.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        reserva_id (int): El ID de la reserva de la cual se mostrarán los detalles.

    Returns:
        HttpResponse: Renderiza la plantilla 'detalle_reserva.html' con el contexto que contiene los detalles de la reserva.
    
    Raises:
        Reserva.DoesNotExist: Si la reserva con el ID proporcionado no existe en la base de datos.
    """

    #obtener la reservas especifica por su ID
    reserva = Reserva.objects.get(id=reserva_id)

    #calculo de detalles de la reserva
    cabania = reserva.cabania.precio
    entrada = reserva.diaEntrada #dia entrada
    salida = reserva.diaSalida  #dia salida
    cantidad_dias = (salida - entrada).days #calculo de la diferencia entre dia de entrada y salida
    total_cabania = cabania * cantidad_dias #calculo entre el precio de la cabaña y la cantidad de dias
    total_servicios = 0 #calculo sobre el total de servicios
    reserva_servicios = ReservaServicio.objects.filter(reserva=reserva)

    # Iterar sobre cada formulario en el formset
    for reserva_servicio in reserva_servicios:
        servicio = reserva_servicio.servicio
        total_servicios += servicio.precio

    total_servicios = total_servicios * cantidad_dias

    total_reserva = total_cabania + total_servicios #calculo sobre el total de la reserva
    print(total_servicios, total_reserva)

    context = {
            'reserva': reserva,
            'cabania': cabania,
            'cantidad_dias': cantidad_dias,
            'total_cabania': total_cabania,
            'total_servicios': total_servicios,
            'total_reserva': total_reserva,
            'total_servicios': total_servicios
        }

    return render(request, 'detalle_reserva.html', context)

def obtener_cabanias(request, complejo_id):
    cabanias = Cabania.objects.filter(complejo_id=complejo_id).values_list('id','nombre')
    cabanias_dict = dict(cabanias)
    return JsonResponse(cabanias_dict)

def detalle_servicio(request, servicio_id):
    """
    Vista que muestra los detalles de un servicio específico identificado por su ID.

    Recupera y muestra los detalles de un servicio, identificado por el parámetro servicio_id.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        servicio_id (int): El ID del servicio del cual se mostrarán los detalles.

    Returns:
        HttpResponse: Renderiza la plantilla 'detalle_servicio.html' con el contexto que contiene los detalles del servicio.
    
    Raises:
        Servicio.DoesNotExist: Si el servicio con el ID proporcionado no existe en la base de datos.
    """
    servicio = Servicio.objects.get(id=servicio_id)

    context = {
        'servicio': servicio
    } 
    return render(request, 'detalle_servicio.html', context)

#VISTAS ENCARGADO

class lista_encargados(LoginRequiredMixin, ListView):
    """
    Vista basada en clase que muestra una lista paginada de encargados.

    Permite filtrar la lista de encargados por nombre/apellido o número de DNI.

    Attributes:
        login_url (str): URL a la que se redirige si el usuario no ha iniciado sesión.
        model (Encargado): Modelo utilizado para obtener los datos de la lista.
        template_name (str): Nombre de la plantilla utilizada para renderizar la vista.
        context_object_name (str): Nombre del objeto de contexto utilizado en la plantilla.
        paginate_by (int): Número de elementos por página para la paginación.
    """
    login_url = '/login/'
    model = Encargado
    template_name = 'lista_encargados.html'
    context_object_name = 'encargados'
    paginate_by = 10

    def get_queryset(self):
        """
        Obtiene la lista de encargados filtrada según el parámetro de búsqueda.

        Returns:
            QuerySet: Lista filtrada de encargados según la consulta de búsqueda.
        """
        query = self.request.GET.get('q','')
        encargados = Encargado.objects.filter(
            Q(apellido_nombre__icontains=query) |
            Q(dni__icontains=query)
        )
        return encargados

class nuevo_encargado(LoginRequiredMixin, CreateView):
    """
    Vista basada en clase para crear un nuevo encargado.

    Permite a los usuarios crear un nuevo encargado proporcionando un formulario predefinido.

    Attributes:
        login_url (str): URL a la que se redirige si el usuario no ha iniciado sesión.
        model (Encargado): Modelo utilizado para crear una nueva instancia de encargado.
        form_class (formEncargado): Formulario utilizado para la creación del encargado.
        template_name (str): Nombre de la plantilla utilizada para renderizar el formulario.
        success_url (str): URL a la que se redirige después de que se crea un nuevo encargado con éxito.
    """
    login_url = '/login/'
    model = Encargado
    form_class = formEncargado
    template_name = 'form_encargado.html'
    success_url = reverse_lazy('lista_encargados')

class modif_encargado(LoginRequiredMixin, UpdateView):
    """
    Vista basada en clase para modificar un encargado existente.

    Permite a los usuarios modificar un encargado existente proporcionando un formulario predefinido.

    Attributes:
        login_url (str): URL a la que se redirige si el usuario no ha iniciado sesión.
        model (Encargado): Modelo utilizado para modificar la instancia de encargado existente.
        form_class (formEncargado): Formulario utilizado para la modificación del encargado.
        template_name (str): Nombre de la plantilla utilizada para renderizar el formulario.
        success_url (str): URL a la que se redirige después de que se modifica el encargado con éxito.
    """
    login_url = '/login/'
    model = Encargado
    form_class = formEncargado
    template_name = 'form_encargado.html'
    success_url = reverse_lazy('lista_encargados')

class borrar_encargado(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = Encargado
    template_name = 'conf_borrar_encargado.html'
    success_url = reverse_lazy('lista_encargados')

#VISTAS DE CABAÑAS

class lista_cabanias(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Cabania
    template_name = 'lista_cabanias.html'
    context_object_name = 'cabanias'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        cabanias = Cabania.objects.filter(
            Q(nombre__contains = query) |
            Q(tipo__icontains = query)
        )

        return cabanias

class nuevo_cabania(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Cabania
    form_class = formCabania
    template_name = 'form_cabania.html'
    success_url = reverse_lazy('lista_cabanias')

class modif_cabania(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Cabania
    form_class = formCabania
    template_name = 'form_cabania.html'
    success_url = reverse_lazy('lista_cabanias')

class borrar_cabania(LoginRequiredMixin, DeleteView):
    """
    Vista basada en clase para eliminar un encargado existente.

    Permite a los usuarios eliminar un encargado existente utilizando una confirmación.

    Attributes:
        login_url (str): URL a la que se redirige si el usuario no ha iniciado sesión.
        model (Encargado): Modelo utilizado para eliminar la instancia de encargado existente.
        template_name (str): Nombre de la plantilla utilizada para confirmar la eliminación del encargado.
        success_url (str): URL a la que se redirige después de eliminar con éxito el encargado.
    """
    login_url = '/login/'
    model = Cabania
    template_name = 'conf_borrar_cabania.html'
    success_url = reverse_lazy('lista_cabanias')
  
#VISTAS DE CLIENTES

class lista_clientes(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Cliente
    template_name = 'lista_clientes.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        clientes = Cliente.objects.filter(
            Q(apellido_nombre__icontains=query)| # Búsqueda por nombre del cliente
            Q(dni__icontains=query) |
            Q(telefono__icontains=query)            # Búsqueda por DNI del cliente
        )

        return  clientes

class nuevo_cliente(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Cliente
    form_class = formCliente
    template_name = 'form_cliente.html'
    #success_url = reverse_lazy('lista_clientes')

    def form_valid(self, form):
        self.object = form.save()
        next_url = self.request.GET.get('next')
        if self.request.GET.get('from_reserva'):
            # Redirigir de vuelta al formulario de reserva después de guardar el cliente
            return HttpResponseRedirect(next_url or reverse('nuevo_reserva'))
        elif self.request.GET.get('from_lista'):
            # Redirigir de vuelta a la lista de clientes después de guardar el cliente
            return HttpResponseRedirect(reverse('lista_clientes'))
        else:
            # Si no se especifica ninguna fuente, redirigir al formulario de reserva por defecto
            return HttpResponseRedirect(next_url or reverse('nuevo_reserva'))
        
class modif_cliente(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Cliente
    form_class = formCliente
    template_name = 'form_cliente.html'
    success_url = reverse_lazy('lista_clientes')

class borrar_cliente(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Cliente
    template_name = 'conf_borrar_cliente.html'
    success_url = reverse_lazy('lista_clientes')
  
#VISTAS DE COMPLEJO
class lista_complejos(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Complejo
    template_name = 'lista_complejos.html'
    context_object_name = 'complejos'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        complejos = Complejo.objects.filter(
            Q(nombre__icontains=query) 
        )

        return complejos

class nuevo_complejo(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Complejo
    form_class = formComplejo
    template_name = 'form_complejo.html'
    success_url = reverse_lazy('lista_complejos')

class modif_complejo(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Complejo
    form_class = formComplejo
    template_name = 'form_complejo.html'
    success_url = reverse_lazy('lista_complejos')

class borrar_complejo(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Complejo
    template_name = 'conf_borrar_complejo.html'
    success_url = reverse_lazy('lista_complejos')
    
#VISTAS DE SERVICIOS
class lista_servicios(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Servicio
    template_name = 'lista_servicios.html'
    context_object_name = 'servicios'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        servicios = Servicio.objects.filter(
            Q(nombre__icontains=query) 
        )
        return servicios


class nuevo_servicio(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Servicio
    form_class = formServicio
    template_name = 'form_servicio.html'
    success_url = reverse_lazy('lista_servicios')

class modif_servicio(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Servicio
    form_class = formServicio
    template_name = 'form_servicio.html'
    success_url = reverse_lazy('lista_servicios')

class borrar_servicio(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Servicio
    template_name = 'conf_borrar_servicio.html'
    success_url = reverse_lazy('lista_servicios')
    
#VISTAS DE RESERVAS
class lista_reservas(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Reserva
    template_name = 'lista_reservas.html'
    context_object_name = 'reservas'
    paginate_by = 10


    def get_queryset(self):
        query = self.request.GET.get('q', '')

        reservas = Reserva.objects.filter(
            Q(cliente__apellido_nombre__icontains=query) |
            Q(cliente__dni__icontains=query)
        )

        return reservas
    
def obtener_id_cliente(apellido_nombre):
    """
    Obtiene el ID de un cliente dado su apellido y nombre.

    Args:
        apellido_nombre (str): Apellido y nombre del cliente a buscar.

    Returns:
        int or None: El ID del cliente si se encuentra, de lo contrario, retorna None.
    """
    try:
        cliente = Cliente.objects.get(apellido_nombre=apellido_nombre)
        return cliente.id
    except Cliente.DoesNotExist:
        return None
class nuevo_reserva(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva reserva.

    Permite crear una nueva reserva y asociar servicios a esta reserva.

    Attributes:
        login_url (str): URL para redirigir a la página de inicio de sesión.
        model (class): Clase del modelo asociado a la vista.
        form_class (class): Clase del formulario para la vista.
        template_name (str): Nombre de la plantilla HTML utilizada para renderizar la vista.
        success_url (str): URL a la que redirigir después de completar con éxito la acción.

    Methods:
        get_context_data(self, **kwargs): Obtiene el contexto para la vista.
        form_valid(self, form): Valida el formulario enviado por el usuario.
        total(self, reserva_id): Calcula el total de la reserva dada su ID.
    """
    login_url = '/login/'
    model = Reserva
    form_class = formReserva
    template_name = 'form_reserva.html'
    success_url = reverse_lazy('lista_reservas')

    def get_context_data(self, **kwargs):
        """
        Obtiene el contexto para la vista.

        Returns:
            dict: Diccionario con el contexto de la vista.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = formReserva.ReservaServicioFormset(self.request.POST)
        else:
            context['formset'] = formReserva.ReservaServicioFormset()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cabania_id = self.request.GET.get('cabania_id')
        if cabania_id:
            cabania = Cabania.objects.get(pk=cabania_id)
            kwargs['initial'] = {'cabania': cabania_id, 'complejo': cabania.complejo_id}
        return kwargs
    
    
    def form_valid(self, form):
        """
        Valida el formulario enviado por el usuario.

        Args:
            form (object): Formulario enviado por el usuario.

        Returns:
            HttpResponseRedirect: Redirige a la URL de éxito si el formulario es válido, 
            de lo contrario, muestra el formulario con errores.
        """
        cliente_apellido_nombre = form.cleaned_data.get('cliente_apellido_nombre')
        cliente = Cliente.objects.filter(apellido_nombre=cliente_apellido_nombre).first()


        if cliente:
            reserva = form.save(commit=False)
            reserva.cliente = cliente
            reserva.save()

            # Crear el formset de servicios asociados a la reserva
            ReservaServicioFormSet = inlineformset_factory(Reserva, ReservaServicio, form=formReservaServicio, extra=1)
            formset = ReservaServicioFormSet(self.request.POST, instance=reserva)

            # Verificar si el formset y el formulario de la reserva son válidos
            if formset.is_valid() and form.is_valid():
                form.save()
                formset.save(commit=False)  # Guarda los objetos del formset, pero no los aplica a la base de datos

                # Guardar el precio original de cada servicio asociado a la reserva
                for servicio_form in formset.forms:
                    if servicio_form.cleaned_data.get('servicio'):
                        servicio_reserva = servicio_form.save(commit=False)
                        servicio_reserva.precio_original_servicio = servicio_reserva.servicio.precio
                        servicio_reserva.save()
            
                return super().form_valid(form)
        else:
            dato_formulario = form.cleaned_data
            return render(self.request, "validar_reserva_clienteNoExistente.html", {'dato_formulario': dato_formulario})
            #form.add_error('cliente_apellido_nombre', 'Cliente no encontrado')
            #return self.form_invalid(form)
                
    def total(self):
        """
        Calcula los totales relacionados con la reserva.
        """
        reserva = self.object
        precio_original_cabania = reserva.precio_original_cabania  # Usar el precio original de la cabaña

        entrada = reserva.diaEntrada
        salida = reserva.diaSalida
        cantidad_dias = (salida - entrada).days

        total_cabania = precio_original_cabania * cantidad_dias

        total_servicios = 0
        for reserva_servicio in reserva.reservaservicio_set.all():
            servicio = reserva_servicio.servicio
            total_servicios += servicio.precio


        total_servicios_reserva = total_servicios * cantidad_dias 
        total_reserva = total_cabania + total_servicios_reserva


        context = {
            'reserva': reserva,
            'cabania': precio_original_cabania,
            'cantidad_dias': cantidad_dias,
            'total_cabania': total_cabania,
            'total_servicios': total_servicios,
            'total_reserva': total_reserva,
            'total_servicios_reserva': total_servicios_reserva
        }

        return context
class modif_reserva(LoginRequiredMixin, UpdateView):
    """
    Vista para modificar una reserva existente.

    Permite actualizar una reserva y los servicios asociados a esta reserva.

    Attributes:
        login_url (str): URL para redirigir a la página de inicio de sesión.
        model (class): Clase del modelo asociado a la vista.
        form_class (class): Clase del formulario para la vista.
        template_name (str): Nombre de la plantilla HTML utilizada para renderizar la vista.
        success_url (str): URL a la que redirigir después de completar con éxito la acción.

    Methods:
        get_initial(self): Obtiene los datos iniciales para el formulario de la vista.
        get_context_data(self, **kwargs): Obtiene el contexto para la vista.
        form_valid(self, form): Valida el formulario enviado por el usuario.
        total(self): Calcula los totales relacionados con la reserva.
    """
    login_url = '/login/'
    model = Reserva
    form_class = formReserva
    template_name = 'form_reserva.html'
    success_url = reverse_lazy('lista_reservas')

    def get_initial(self):
        """
        Obtiene los datos iniciales para el formulario de la vista.

        Returns:
            dict: Diccionario con los datos iniciales para el formulario.
        """
        initial = super().get_initial()
        reserva = self.get_object()
        if reserva.cliente:
            initial['cliente_apellido_nombre'] = reserva.cliente.apellido_nombre
        return initial

    def get_context_data(self, **kwargs):
        """
        Obtiene el contexto para la vista.

        Returns:
            dict: Diccionario con el contexto de la vista.
        """
        context = super().get_context_data(**kwargs)
        total_context = self.total()
        context.update(total_context)

        if self.request.POST:
            context['formset'] = formReserva.ReservaServicioFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = formReserva.ReservaServicioFormset(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Valida el formulario enviado por el usuario.

        Args:
            form (object): Formulario enviado por el usuario.

        Returns:
            HttpResponseRedirect: Redirige a la URL de éxito si el formulario es válido, 
            de lo contrario, muestra el formulario con errores.
        """
        context = self.get_context_data()
        formset = context['formset']

        cliente_apellido_nombre = form.cleaned_data.get('cliente_apellido_nombre')
        cliente = Cliente.objects.filter(apellido_nombre=cliente_apellido_nombre).first()

        if formset.is_valid() and form.is_valid():
            formset.save()

            reserva = form.save(commit=False)
            reserva.cliente = cliente
            reserva.save()

            # Crear el formset de servicios asociados a la reserva
            ReservaServicioFormSet = inlineformset_factory(Reserva, ReservaServicio, form=formReservaServicio, extra=1)
            formset = ReservaServicioFormSet(self.request.POST, instance=reserva)

            # Guardar el precio original de cada servicio asociado a la reserva
            for servicio_form in formset:
                if servicio_form.is_valid() and servicio_form.cleaned_data.get('servicio'):
                    servicio_reserva = servicio_form.save(commit=False)
                    servicio_reserva.precio_original_servicio = servicio_reserva.servicio.precio
                    servicio_reserva.save()

            # Actualizar el precio de la reserva
            total_context = self.total()
            total_reserva = total_context['total_reserva']
            reserva.total_reserva = total_reserva
            reserva.save()

            return super().form_valid(form)
        else:
            form.add_error('cliente_apellido_nombre', 'Cliente no encontrado')
            return self.form_invalid(form)


        
    def total(self):
        """
        Calcula los totales relacionados con la reserva.
        """
        reserva = self.object
        precio_original_cabania = reserva.precio_original_cabania  # Usar el precio original de la cabaña

        entrada = reserva.diaEntrada
        salida = reserva.diaSalida
        cantidad_dias = (salida - entrada).days

        total_cabania = precio_original_cabania * cantidad_dias

        total_servicios = 0
        for reserva_servicio in reserva.reservaservicio_set.all():
            precio_original_servicio = reserva_servicio.precio_original_servicio
            total_servicios += precio_original_servicio

        total_servicios_reserva = total_servicios * cantidad_dias 
        total_reserva = total_cabania + total_servicios_reserva

        context = {
            'reserva': reserva,
            'cabania': precio_original_cabania,
            'cantidad_dias': cantidad_dias,
            'total_cabania': total_cabania,
            'total_servicios': total_servicios,
            'total_reserva': total_reserva,
            'total_servicios_reserva': total_servicios_reserva
        }

        return context


class borrar_reserva(LoginRequiredMixin, DeleteView):
    model = Reserva
    template_name = 'conf_borrar_reserva.html'
    success_url = reverse_lazy('lista_reservas')


def disponibilidad_cabania(request, cabania_id):
    reservas = Reserva.objects.filter(cabania_id=cabania_id)

    return render(request, 'disponibilidad_cabania.html',{'reservas': reservas})

def disponibilidad_complejo(request, complejo_id):
    reservas = Reserva.objects.filter(complejo_id=complejo_id)

    return render(request, 'disponibilidad_complejo.html',{'reservas': reservas})

def cabanias_disponibles(request):
    if request.method == 'POST':
        fecha_entrada_str = request.POST.get('fecha_entrada')
        fecha_salida_str = request.POST.get('fecha_salida')

        # Validar que las fechas no estén vacías
        if fecha_entrada_str and fecha_salida_str:
            fecha_entrada = datetime.strptime(fecha_entrada_str, '%Y-%m-%d').date()
            fecha_salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d').date()

            # Lógica para encontrar cabañas disponibles
            cabañas_disponibles = Cabania.objects.filter(
                ~Q(id__in=Reserva.objects.filter(
                    diaEntrada__lte=fecha_salida,
                    diaSalida__gte=fecha_entrada
                ).values('cabania_id'))
            )

            return render(request, 'lista_disponibilidad.html', {'cabañas_disponibles': cabañas_disponibles,
                                                                  'fecha_entrada': fecha_entrada,
                                                                  'fecha_salida': fecha_salida})

    # Si las fechas están vacías o si el método de solicitud no es POST,
    # simplemente renderiza el formulario nuevamente
    return render(request, 'lista_disponibilidad.html')
'''
class DetalleReservaServicio(LoginRequiredMixin, ListView):
    model = ReservaServicio
    template_name = 'servicios-reserva.html'
    context_object_name = 'reservaservicio'

    def get_queryset(self):
        reserva_id = self.kwargs['reserva_id']  # Asumiendo que utilizas 'reserva_id' en la URL
        # Filtrar los objetos ReservaServicio relacionados con la reserva específica
        queryset = ReservaServicio.objects.filter(reserva_id=reserva_id)
        return queryset 
'''
    
def Logout(request):
    """
    Función para cerrar la sesión de un usuario.

    Realiza el proceso de cierre de sesión en Django y redirige al usuario a la página de inicio.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponseRedirect: Redirige al usuario a la página de inicio.
    """
    logout(request)
    return redirect('/')
from django.http import JsonResponse

from django.http import JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.shortcuts import get_object_or_404
import io
from django.http import FileResponse
from django.utils import timezone


def factura(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    #encargado = get_object_or_404(Encargado,id=encargado_id)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    # Registro de las fuentes
    pdfmetrics.registerFont(TTFont('Poppins', 'reservas/static/fonts/Poppins-Regular.ttf')),
    pdfmetrics.registerFont(TTFont('Lexend-VariableFont_wght', 'reservas/static/fonts/Lexend-VariableFont_wght.ttf')),
    pdfmetrics.registerFont(TTFont('Poppins-Bold', 'reservas/static/fonts/Poppins-Bold.ttf'))

    # Configuración de la fuente y márgenes
    c.setFont("Lexend-VariableFont_wght", 35)
    line_height = 14
    left_margin = inch
    top_margin = inch * 10

    # Encabezado
    palabra = "ReserVas"
    mitad1 = palabra[:len(palabra)-3]
    mitad2 = palabra[len(palabra)-3:]

    c.setFillColorRGB(0,0,0)  # Color negro para la primera mitad
    c.drawString(left_margin -60, 750, mitad1)
    c.setFillColorRGB(0.57, 0.5, 1)  #Color púrpura para la segunda mitad
    c.drawString(left_margin +35, 750, mitad2)

    # Ubicación
    c.setFillColorRGB(0, 0, 0)
    c.setFont( "Poppins", 20)
    ubicacion = f"Domicilio: {reserva.complejo.direccion}"
    top_margin -= line_height  # Ajusta la posición vertical
    c.drawString(left_margin -60, top_margin - 20, ubicacion)

    # Datos del complejo
    c.setFillColorRGB(0, 0 , 0)
    complejo_cabania = f"Complejo: {reserva.complejo}"
    top_margin -= line_height
    left_margin  -= 50
    c.setFont("Poppins", 20)
    c.drawString(left_margin -10  , top_margin -35 , complejo_cabania)

    #Telefono y correo electrónico
    telefono_encargado = f"Tel: +54 {str(reserva.complejo.encargado.telefono)}"
    email_encargado = f"{reserva.complejo.encargado.email}"
    top_margin -= line_height
    c.setFont( "Poppins", 18)
    c.drawRightString(left_margin +580, top_margin - 25, telefono_encargado)
    top_margin -= line_height
    c.setFillColorRGB(0.07, 0.33, 0.74)   #Color azul para el mail
    c.drawRightString(left_margin +580, top_margin - 30, email_encargado)

    #Línea divisoria superior "FACTURA"
    c.setFillColorRGB(0.57, 0.5, 1)  # Púrpura
    c.rect(left_margin, top_margin - 60, 570, 20, fill=True)

    # Dibujar el título "FACTURA" encima de la barra horizontal
    c.setFillColorRGB(0, 0, 0)  # Color blanco para el texto
    c.setFont("Poppins-Bold", 18)  # Fuente en negrita y tamaño 18
    c.drawString(left_margin + 240, top_margin - 57, "FACTURA")

    c.setLineWidth(1)  # Ajusta el ancho de la línea según sea necesario
    c.line(left_margin + 280, top_margin - 405, left_margin + 280, top_margin - 65)  

    # Detalles de la reserva
    detalles_cabania = [
        f"Cabaña: {reserva.cabania}",
        f"Capacidad: {reserva.cabania.capacidad} personas",
        f"Día de Entrada: {reserva.diaEntrada}",
        f"Día de Salida: {reserva.diaSalida}",
        f"Seña: ${reserva.seña}",
]

    detalles_cliente = [
        f"Cliente: {reserva.cliente}",
        f"Teléfono: {reserva.cliente.telefono}",
        f"Provincia: {reserva.cliente.provincia}",
        f"Localidad : {reserva.cliente.localidad}",
]
    
    # Posición inicial para los detalles de la reserva
    top_margin -= 100
    
# Espaciado uniforme para los detalles de cabaña
    line_height_detalles = 20
# Espaciado para el encabezado    
    line_height_encabezado = 30

# Dibujar detalles de cabaña
    c.setFont("Poppins", 20)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(left_margin + 20, top_margin, "Detalle de Reserva")
    top_margin -= line_height_encabezado

    for detalle in detalles_cabania:
        c.setFont("Poppins", 14)
        c.drawString(left_margin + 10, top_margin, detalle)
        top_margin -= line_height_detalles +5

    line_height_encabezadoCL = 35

# Dibujar detalles del cliente
    c.setFont("Poppins", 20)
    c.drawString(left_margin + 20, top_margin - 25, "Datos del Cliente")
    top_margin -= line_height_encabezadoCL

    for detalle in detalles_cliente:
        c.setFont("Poppins", 14)
        c.drawString(left_margin + 10, top_margin - 20, detalle)
        top_margin -= line_height_detalles +5

    detalle_width = 570

    # Línea divisoria entre 'Datos del Cliente' y 'Cliente'
    c.line(left_margin, top_margin +140, left_margin + detalle_width -300, top_margin +140)
    
    #Línea divisoria final
    c.line(left_margin, top_margin -20, left_margin + detalle_width, top_margin -20)


    # Cálculos de precios y total de reserva
    cabania = reserva.cabania.precio
    entrada = reserva.diaEntrada
    salida = reserva.diaSalida
    cantidad_dias = (salida - entrada).days
    total_cabania = cabania * cantidad_dias

    total_servicios = 0
    reserva_servicios = ReservaServicio.objects.filter(reserva=reserva)

    for reserva_servicio in reserva_servicios:
        servicio = reserva_servicio.servicio
        total_servicios += servicio.precio

    total_servicios_reserva = total_servicios * cantidad_dias
    total_reserva = total_cabania + total_servicios_reserva

    # Mostrar totales
    line_height_totales = -300
    totales = "Total Reserva"
    top_margin -= line_height_totales # Ajusta la posición vertical
    numero_reserva = reserva_id #Numero de factura igual al id de la reserva
    c.setFont("Poppins", 20)
    c.drawString(left_margin +360, top_margin - 90, totales) 
    c.setFont("Poppins", 14)
    c.drawString(left_margin +320, top_margin -130, f"Total Servicios/Día: ${total_servicios}")
    c.drawString(left_margin +320, top_margin -160, f"Total Servicios/Reserva: ${total_servicios_reserva}")
    c.drawString(left_margin +320, top_margin -190, f"Total Cabaña: ${total_cabania}")
    c.setFont("Poppins-Bold",14)
    c.drawString(left_margin +360, top_margin -220, f"Total: ${total_reserva}")
    c.setFont("Poppins-Bold",16)
    fecha_actual = timezone.now().strftime("%Y-%m-%d")
    c.drawString(left_margin, top_margin - 375, f"N° Factura : {numero_reserva}")
    c.drawString(left_margin, top_margin - 395, f"Fecha: {fecha_actual}")
    c.drawString(left_margin, top_margin - 425, "Gracias por su visita!")
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f'reserva{reserva_id}_factura.pdf')


def search_clients(request):
    """
    Vista para buscar clientes mediante una solicitud AJAX.

    Se espera una solicitud XMLHttpRequest con un término de búsqueda 'term' en los parámetros GET.
    Retorna una lista JSON de nombres de clientes que coinciden con el término de búsqueda.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        JsonResponse: Lista JSON de nombres de clientes que coinciden con el término de búsqueda.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Obtiene el término de búsqueda del parámetro GET 'term'
        q = request.GET.get('term', '')
        # Filtra los clientes cuyos nombres o apellidos coincidan con el término de búsqueda
        clients = Cliente.objects.filter(apellido_nombre__icontains=q)
        # Crea una lista de nombres de clientes que coinciden con el término de búsqueda
        results = [client.apellido_nombre for client in clients]
        # Retorna una respuesta JSON con la lista de nombres de clientes
        return JsonResponse(results, safe=False)



