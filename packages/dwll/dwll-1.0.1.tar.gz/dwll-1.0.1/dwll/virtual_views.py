from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.http import HttpResponseRedirect

from dwll import messages

from django.views.generic import (
    UpdateView, 
    CreateView, 
    ListView, 
    DeleteView
)

from django.db.models import Q

from abc import (
    ABC, 
    abstractmethod
)

class LoginRequiredSecurityMixin:
    """ Clase para exigir login antes de ingresar """
    
    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CRUDListView(ABC):
    """ Clase abstracta para vistas de tipo Lista """
    
    @property
    @abstractmethod
    def view_filters(self):
        pass
    
    @property
    @abstractmethod
    def view_orderedby(self):
        pass

class VirtualListView(ABC, ListView):
    """ Clase base para vistas de tipo lista """
    
    def get_queryset(self):
        queryset = self.model.objects.get_active()
        view_filters = self.view_filters
        try:
            query = None
            for field in view_filters:
                q = Q(**{"%s__icontains" % field: self.request.GET[field] })
                query = query & q if query else q
  
            queryset = queryset.filter(query)  
        except Exception as e:
            django_messages.error(self.request, str(e))

        if self.view_orderedby:
            return queryset.order_by(self.view_orderedby)
        
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        view_filters = self.view_filters

        for filter in view_filters:
            ctx[filter] = self.request.GET[filter] if filter in self.request.GET else None
        
        return ctx

class CRUDSaveView(ABC):
    """ Clase abstracta para vistas de tipo Create y Update """
    
    @abstractmethod
    def do_after_save(self, obj):
        pass
    
    @abstractmethod
    def get_success_url(self):
        pass

    @abstractmethod
    def get_fail_url(self):
        pass
    
    def get_form_kwargs(self):
        kwargs = super(CRUDSaveView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    
    def form_valid(self, form, **kwargs):
        obj = form.save()
        if obj and obj.id:
            self.do_after_save(obj)
            
            obj_name = obj.__class__.__name__.lower()
            django_messages.success(self.request, 
                    messages.get_full_message(self.request, 
                    '{}.create.success'.format(obj_name)))

        return HttpResponseRedirect(self.get_success_url())

class VirtualCreateView(CRUDSaveView, CreateView):
    
    def get_success_url(self):
        return self.request.path_info
    
    def get_fail_url(self):
        return self.request.path_info
    
    def do_after_save(self, obj):
        pass

class VirtualUpdateView(CRUDSaveView, UpdateView):
    
    def get_success_url(self):
        return self.request.path_info
    
    def get_fail_url(self):
        return self.request.path_info
    
    def do_after_save(self, obj):
        pass