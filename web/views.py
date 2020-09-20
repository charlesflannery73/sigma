from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from .models import Type, Signature
from .forms import TypeSearchForm, SigSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from django.db.models import Q
from django.urls import reverse
import logging
from django.contrib import messages


logger = logging.getLogger(__name__)


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logger.info("user=" + str(self.request.user) + ", action=view, data=[home_page]")
        types = Type.objects.filter().order_by('-modified')[:5]
        sigs = Signature.objects.filter().order_by('-modified')[:5]
        return render(request, 'home.html', {'types': types, 'sigs': sigs})


class AboutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logger.info("user=" + str(self.request.user) + ", action=view, data=[about_page]")
        return render(request, 'about.html')



class SigFilter(BaseFilter):
    search_fields = {
        'search_text': ['text'],
        'search_type': ['type__name'],
        'search_status': ['status'],
        'search_expiry': ['expiry'],
        'search_reference': ['reference'],
        'search_comment': ['comment'],
    }


class TypeFilter(BaseFilter):
    search_fields = {
        'search_text': ['name'],
        'search_id': ['id'],
        'search_comment': ['comment'],
    }

class SigSearch(LoginRequiredMixin, SearchListView):
    model = Signature
    template_name = "web/search.html"
    form_class = SigSearchForm
    filter_class = SigFilter
    ordering = ['name']

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            text = form.cleaned_data['search_text']
            type = form.cleaned_data['search_type']
            status = form.cleaned_data['search_status']
            expiry = form.cleaned_data['search_expiry']
            comment = form.cleaned_data['search_comment']
            params = "text=" + text + "&status=" + status + "&expiry=" + expiry + "&type=" + type + "&comment=" + comment
            logger.info("user=" + str(self.request.user) + ", action=search_sigs, data=[" + params + "]")
            return HttpResponseRedirect(reverse('sig-list') +'?%s' % params)

        return render(request, self.template_name, {'form': form})


class TypeSearch(LoginRequiredMixin, SearchListView):
    model = Type
    template_name = "web/search.html"
    form_class = TypeSearchForm
    filter_class = TypeFilter
    ordering = ['name']

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['search_name']
            comment = form.cleaned_data['search_comment']
            params = "name=" + name + "&comment=" + comment
            logger.info("user=" + str(self.request.user) + ", action=search_types, data=[" + params + "]")
            return HttpResponseRedirect(reverse('type-list') +'?%s' % params)

        return render(request, self.template_name, {'form': form})


class TypeListView(LoginRequiredMixin, ListView):
    model = Type
    template_name = 'web/type_list.html'
    context_object_name = 'types'
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('name') == None:
            logger.info("user=" + str(self.request.user) + ", action=list, data=[types]")
            return Type.objects.filter().order_by('name')
        name_val = self.request.GET.get('name')
        comment_val = self.request.GET.get('comment')
        new_context = Type.objects.filter(
            Q(name__icontains=name_val) &
            Q(comment__icontains=comment_val)
        ).order_by('name')
        return new_context


class TypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Type
    fields = ['name', 'comment']
    success_url = '/'
    permission_required = ('web.add_type')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        data = "name=" + name + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=create_type, data=[" + data + "]")
        return super().form_valid(form)


class TypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Type
    fields = ['name', 'comment']
    success_url = '/'
    permission_required = ('web.change_type')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        data = "name=" + name + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=update_type, data=[" + data + "]")
        return super().form_valid(form)


class TypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView, View):
    model = Type
    success_url = '/'
    permission_required = ('web.delete_type')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        pk = self.object.id
        sigs = Signature.objects.filter(type=pk)
        if sigs:
            messages.warning(request, 'Cannot delete the type "' + name + '" while it has signatures.')
            return HttpResponseRedirect(reverse('sig-list') +'?type=%s' % name)
        comment = self.object.comment
        data = "name=" + name + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=delete_type, data=[" + data + "]")
        return super(TypeDeleteView, self).delete(request, *args, **kwargs)


class SigListView(LoginRequiredMixin, ListView):
    model = Signature
    template_name = 'web/sig_list.html'
    context_object_name = 'sigs'
    ordering = ['-modified']
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('name') == None:
            logger.info("user=" + str(self.request.user) + ", action=list, data=[sigs]")
            return Signature.objects.filter().order_by('text')
        text_val = self.request.GET.get('text')
        status_val = self.request.GET.get('status')
        reference_val = self.request.GET.get('reference')
        type_val = self.request.GET.get('type')
        comment_val = self.request.GET.get('comment')
        new_context = Signature.objects.filter(
            Q(text__icontains=text_val) &
            Q(status__icontains=status_val) &
            Q(type__name__icontains=type_val) &
            Q(reference__icontains=reference_val) &
            Q(comment__icontains=comment_val)
        ).order_by('text')
        return new_context


class SigCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Signature
    fields = ['text', 'type', 'status', 'reference', 'expiry', 'comment']
    success_url = '/'
    permission_required = ('web.add_signature')

    def form_valid(self, form):
        text = form.cleaned_data['text']
        type = form.cleaned_data['type']
        status = form.cleaned_data['status']
        expiry = form.cleaned_data['expiry']
        reference = form.cleaned_data['reference']
        comment = form.cleaned_data['comment']
        data = "text=" + text + ", type=" + str(type) + ", status=" + status + ", expiry=" + expiry + ", reference=" + reference + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=create_sig, data=[" + data + "]")
        return super().form_valid(form)


class SigUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Signature
    fields = ['text', 'type', 'status', 'reference', 'expiry', 'comment']
    success_url = '/'
    permission_required = ('web.change_signature')

    def form_valid(self, form):
        text = form.cleaned_data['text']
        type = form.cleaned_data['type']
        status = form.cleaned_data['status']
        expiry = form.cleaned_data['expiry']
        reference = form.cleaned_data['reference']
        comment = form.cleaned_data['comment']
        data = "text=" + text + ", type=" + str(type) + ", status=" + status + ", expiry=" + expiry + ", reference=" + reference + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=update_sig, data=[" + data + "]")
        return super().form_valid(form)


class SigDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Signature
    success_url = '/'
    permission_required = ('web.delete_signature')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        text = self.object.text
        type = self.object.type
        status = self.object.status
        expiry = self.object.expiry
        reference = self.object.reference
        comment = self.object.comment
        data = "text=" + text + ", type=" + str(type) + ", status=" + status + ", expiry=" + expiry + ", reference=" + reference + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=delete_sig, data=[" + data + "]")
        return super(SigDeleteView, self).delete(*args, **kwargs)
