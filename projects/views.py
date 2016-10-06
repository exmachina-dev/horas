from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from utils.auth_mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Project
from .forms import ProjectForm

class HomeView(ListView):
    template_name = 'projects/home.html'
    model = Project


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Project
    permission_required = 'projects.view_project_list'
    permission_denied_message = 'You don\'t have the permission to project list.'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'is_closed' in self.kwargs and self.kwargs['is_closed'] is not None:
            qs = qs.filter(is_closed=self.kwargs['is_closed'])

        qs = qs.order_by('initials')
        return qs


class ProjectNewView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'projects/project_edit.html'
    form_class = ProjectForm
    success_url = '/projects'
    permission_required = 'projects.add_project'
    permission_denied_message = 'You don\'t have the permission to create projects.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'

        return context


class ProjectEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'projects/project_edit.html'
    form_class = ProjectForm
    success_url = '/projects'
    model = Project
    permission_required = 'projects.change_project'
    permission_denied_message = 'You don\'t have the permission to edit projects.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'

        return context

    def get_initial(self):
        self.initial = super().get_initial()
        self.initial['employee'] = self.request.user.employee
        return self.initial


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/confirm_delete.html'
    success_url = '/projects/'
    permission_required = 'projects.delete_project'
    permission_denied_message = 'You don\'t have the permission to delete projects.'

    def dispatch(self, *args, **kwargs):

        response = super().dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            return response
