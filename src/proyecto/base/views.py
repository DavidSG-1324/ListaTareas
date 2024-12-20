from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic.list import ListView
from . models import Tarea
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

# Create your views here.
# def lista_pendientes(pedido):
#    return HttpResponse('Lista Pendientes')

class Logueo(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tareas')

class CrearCuenta(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)

        return super(CrearCuenta, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
           return redirect('tareas')

        return super(CrearCuenta, self).get(*args, **kwargs)

class ListaTareas(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(usuario = self.request.user)
        context['count'] = context['tareas'].filter(completo = False).count()

        valor_buscado = self.request.GET.get('area-busqueda')
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains = valor_buscado)
            context['valor_buscado'] = valor_buscado

        return context

class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/detalle.html'

class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo']
    # fields = '__all__'
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        return super(CrearTarea, self).form_valid(form)

class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo']
    success_url = reverse_lazy('tareas')

class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')
