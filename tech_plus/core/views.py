from django.views.generic.base import TemplateView
from guide.classifier_kcp.models import *
from django.http.response import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.forms import model_to_dict
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.http import HttpResponseRedirect, JsonResponse
from django.apps import apps
import django.db.utils
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
import base64
import json
from django.core.files.storage import default_storage

from .utils.utils import (
    create_table_form8,
    load_data,
    get_form_1_data,
    get_form_2_data,
    get_form_3_data,
    get_form_4_data,
    get_form_5_data,
    get_form_6_data,
)
from .utils.excel import Excel

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalDeleteView
)

from .models import *
from .forms import *
from .tasks import fill

import sys
sys.path.append(".")

CHOISE_PARAM = {
    "TkMainCollection": "table_subsection",
    "TkRemoteConstructionCollection": "subsection",
    "TkInstallationEquipmentCollection": "table",
    "TkPre_commissioningCollection": "table_subsection"
}


def home(request):
    return render(request, 'core/home.html')


class User_account(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = MyPasswordChangeForm(self.request.user)
        return render(request, 'core/user_page.html',{'form': form})

    def post(self, request, *args, **kwargs):
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Ваш пароль успешно обновлен!')
            return render(request, 'core/form_8/form_8_list.html', {'form': form, 'password_changed': True})
        else:
            messages.warning(request, 'Произошла ошибка. Попробуйте еще раз.')
            return render(request, 'core/user_page.html', {'form': form, 'password_changed': False})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы авторизованы как {user}.")
                return redirect("form_8_list_url")
            else:
                messages.warning(request, "Неверный логин или пароль.")
        else:
            messages.warning(request, "Неверный логин или пароль.")
    form = AuthenticationForm()
    return render(request, "core/login.html", context={"form": form})


def logout_request(request):
    logout(request)
    return redirect("home_url")


class Form_8DetailView(LoginRequiredMixin, DetailView):
    model = Form_8
    template_name = 'core/form_8/form_8_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = create_table_form8(
            other_context=context, pk=self.kwargs['pk'])
        return context


class Form_8MainView(LoginRequiredMixin, DetailView):
    model = Form_8
    template_name = 'core/form_8/form_8_detail_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_form_2_data(other_context=context, pk=self.kwargs['pk'])
        context = get_form_1_data(other_context=context, pk=self.kwargs['pk'])
        return context


class Form_1DetailView(LoginRequiredMixin, DetailView):
    model = Form_8
    template_name = 'core/form_1/form_1_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_form_1_data(other_context=context, pk=self.kwargs['pk'])
        return context


def form_1excel(request, pk):
    form_8 = Form_8.objects.filter(id=pk)
    context = {'object': form_8, 'metadata': 'form_1'}
    context = get_form_1_data(other_context=context, pk=pk)

    excel = Excel.create_excel(context)

    response = HttpResponse(content=save_virtual_workbook(
        excel), content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=form1.xlsx'
    return response


class Form_2DetailView(LoginRequiredMixin, DetailView):
    model = Form_8
    template_name = 'core/form_2/form_2_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_form_2_data(other_context=context, pk=self.kwargs['pk'])
        return context


def form_2excel(request, pk):
    form_8 = Form_8.objects.filter(id=pk)
    context = {'object': form_8, 'metadata': 'form_2'}
    context = get_form_2_data(other_context=context, pk=pk)

    excel = Excel.create_excel(context)

    response = HttpResponse(content=save_virtual_workbook(
        excel), content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=form2.xlsx'
    return response


class Form_3DetailView(LoginRequiredMixin, DetailView):
    model = Form_8
    template_name = 'core/form_3/form_3_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_form_3_data(other_context=context, pk=self.kwargs['pk'])
        return context


def form_3excel(request, pk):
    form_8 = Form_8.objects.filter(id=pk)[0]
    context = {'object': form_8, 'metadata': 'form_3'}
    context = get_form_3_data(other_context=context, pk=pk)

    excel = Excel.create_excel(context)

    response = HttpResponse(content=save_virtual_workbook(
        excel), content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=form3.xlsx'
    return response


class Form_4DetailView(LoginRequiredMixin, DetailView):
    model = Form_8
    template_name = 'core/form_4/form_4_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_form_4_data(other_context=context, pk=self.kwargs['pk'])
        return context


def form_4excel(request, pk):
    form_8 = Form_8.objects.filter(id=pk)[0] 
    context = {'object': form_8, 'metadata': 'form_4'}
    context = get_form_4_data(other_context=context, pk=pk)

    excel = Excel.create_excel(context)

    response = HttpResponse(content=save_virtual_workbook(
        excel), content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=form4.xlsx'
    return response


class Form_5DetailView(LoginRequiredMixin, DetailView):
    model = Form_8
    template_name = 'core/form_5/form_5_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_form_5_data(other_context=context, pk=self.kwargs['pk'])
        return context


def form_5excel(request, pk):
    form_8 = Form_8.objects.filter(id=pk)[0] 
    context = {'object': form_8, 'metadata': 'form_5'}
    context = get_form_5_data(other_context=context, pk=pk)

    excel = Excel.create_excel(context)

    response = HttpResponse(content=save_virtual_workbook(
        excel), content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=form5.xlsx'
    return response


class Form_6DetailView(LoginRequiredMixin, DetailView):
    model = Form_8
    template_name = 'core/form_6/form_6_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_form_6_data(other_context=context, pk=self.kwargs['pk'])
        return context


def form_6excel(request, pk):
    form_8 = Form_8.objects.filter(id=pk)[0]
    context = {'object': form_8, 'metadata': 'form_6'}
    context = get_form_6_data(other_context=context, pk=pk)

    excel = Excel.create_excel(context)

    response = HttpResponse(content=save_virtual_workbook(
        excel), content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=form6.xlsx'
    return response


def form_8excel(request, pk):
    form_8 = Form_8.objects.filter(id=pk)
    context = {'object': form_8}
    context = create_table_form8(other_context=context, pk=pk)

    excel = Excel.create_excel(context)

    response = HttpResponse(content=save_virtual_workbook(
        excel), content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=form8.xlsx'
    return response


class Form_8CreateView(LoginRequiredMixin, CreateView):
    model = Form_8
    form_class = form_8Form
    template_name = 'core/form_8/form_8_create.html'
    success_url = None

    def form_valid(self, form):
        form_8 = form.save(commit=False)
        form_8.creator = self.request.user
        form_8.save()
        for i in range(5):
            instance = Form_7()
            instance.form_8 = form_8
            instance.save()
        return redirect(reverse('form_8_main_url', kwargs={'pk': form_8.id}))


class Form_8ListView(LoginRequiredMixin, ListView):
    model = Form_8
    context_object_name = 'form_8_list'
    template_name = 'core/form_8/form_8_list.html'
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        from_date = self.request.GET.get('from', None)
        to_date = self.request.GET.get('to', None)
        object_list = self.model.objects.all()
        if name:
            object_list = object_list.filter(
                Q(title__icontains=name) |
                Q(code__icontains=name))

        if from_date:
            object_list = object_list.filter(
                Q(created_at__gte=from_date)
            )
        if to_date:
            object_list = object_list.filter(
                Q(created_at__lte=to_date)
            )
        return object_list


class Form_8UpdateView(LoginRequiredMixin, UpdateView):
    model = Form_8
    template_name = 'core/form_8/form_8_update.html'
    success_url = None
    form_class = Form_8UpdateForm

    def get_success_url(self):
        return reverse_lazy('form_8_main_url', kwargs={'pk': self.object.pk})


class Form_8DeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Form_8
    template_name = 'core/form_8/form_8_delete.html'
    success_message = 'ТК успешно удалена'
    success_url = None

    def get_success_url(self):
        return reverse('form_8_list_url')


class Form_7DetailView(LoginRequiredMixin, DetailView):
    model = Form_7
    template_name = 'core/form_7/form_7_detail.html'

    def get_context_data(self, **kwargs):
        context = super(Form_7DetailView, self).get_context_data(**kwargs)
        return context


class Form_7DetailTableView(LoginRequiredMixin, DetailView):
    model = Form_7
    template_name = 'core/form_7/from_7_detail_table.html'

    def get_context_data(self, **kwargs):
        context = super(Form_7DetailTableView, self).get_context_data(**kwargs)
        form_7 = context['form_7']
        forms = Form_7.objects.filter(form_8=form_7.form_8)
        context['forms'] = forms
        return context


def form_7excel(request, pk):
    form_7 = Form_7.objects.filter(id=pk)
    context = {'object': form_7, 'metadata': 'form_7'}
    excel = Excel.create_excel(context)

    response = HttpResponse(content=save_virtual_workbook(
        excel), content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=form7.xlsx'
    return response


class Form_7UpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Form_7
    template_name = 'core/form_7/form_7_create.html'
    success_url = None
    form_class = Form_7From

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.object.pk})


class OperationAdd(LoginRequiredMixin, BSModalCreateView):
    form_class = AddOperationForm
    template_name = 'core/from_7_operations/operations_add.html'
    success_url = None


    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


class AddOperationFromBookView(LoginRequiredMixin, BSModalCreateView):
    form_class = AddOperationFromBookForm
    template_name = 'core/from_7_operations/operations_add_from_book.html'
    success_url = None


    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


def CheckExcelDb(request):
    try:
        CheckExcel.objects.create(pk=1)
    except django.db.utils.IntegrityError:
        pass
    check = CheckExcel.objects.get(pk=1)
    if check.status:
        result = check.status
        check.status = False
        check.save()
    else:
        result = False
    return JsonResponse({"result": result})


def ExcelUploadView(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = default_storage.save("1.xlsx", file)
        file_url = default_storage.url(file_name)
        message = {"file_name":file_url}
        message_string = json.dumps(message)
        byte_message = base64.b64encode(message_string.encode('utf-8'))
        base64_json_string = byte_message.decode()
        # Celery task        
        fill.delay(base64_json_string)

        return HttpResponseRedirect(reverse("home_url"))
    return render(request, 'core/include/modal_upload_excel.html')


def load_group(request):
    materials = load_data(request.GET.get('group_id'), 'group', Resource)
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_chapter(request):
    materials = load_data(request.GET.get('chapter_id'), 'chapter', Group)
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_part_book(request):
    materials = load_data(request.GET.get('part_book_id'), 'partbook', Chapter)
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_book(request):
    materials = load_data(request.GET.get('book_id'), 'book', PartBook)
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_group_machine(request):
    materials = load_data(request.GET.get('group_id'),
                          'group', machines.Resource)
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_chapter_machine(request):
    materials = load_data(request.GET.get('chapter_id'),
                          'chapter', machines.Group)
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_tk_book(request):
    book = request.GET.get('book')
    model = apps.get_model('tk_gesn', book)
    materials = model.objects.all()
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_tk_departament(request):
    book = request.GET.get('book')
    collection = request.GET.get('collections')
    model = CHOICE_DEPARTAMENT[book]
    if collection:
        materials = model.objects.filter(
            collection=collection).exclude(title='None')
    else:
        materials = model.objects.exclude(title='None')
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_tk_section(request):
    book = request.GET.get('book')
    department = request.GET.get('departament')
    model = CHOICE_SECTION[book]
    if department:
        materials = model.objects.filter(
            department=department).exclude(title='None')
    else:
        materials = model.objects.all().exclude(title='None')
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_tk_subsection(request):
    book = request.GET.get('book')
    section = request.GET.get('section')
    model = CHOICE_SUBSECTION[book]
    if section:
        materials = model.objects.filter(section=section).exclude(title='None')
    else:
        materials = model.objects.all().exclude(title='None')
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_tk_tablesubsection(request):
    book = request.GET.get('book')
    subsection = request.GET.get('subsection')
    model = CHOICE_SUBTABLE[book]
    if subsection:
        materials = model.objects.filter(
            subsection=subsection).exclude(title='None')
    else:
        materials = model.objects.all().exclude(title='None')
    return render(request, 'core/drop_down_list.html', {'materials': materials})


def load_tk_techkart(request):
    book = request.GET.get('book')
    param = request.GET.get('param')
    model = CHOICE_TECHKART[book]
    kwargs = {}
    kwargs[CHOISE_PARAM[book]] = param
    if param:
        materials = model.objects.filter(**kwargs)
    else:
        materials = model.objects.all()
    return render(request, 'core/drop_down_list.html', {'materials': materials})


class MemberCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Members
    form_class = MembersForm
    success_url = None
    template_name = 'core/members/members_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_path(self):
        path = self.request.path.split('/')[2]
        return path

    def form_valid(self, form):
        if not self.request.is_ajax():
            pk = self.get_path()
            form_7 = Form_7.objects.get(pk=self.get_pk())
            queryset = Form_7.objects.filter(form_8=form_7.form_8.pk)
            operation = Operation.objects.get(pk=pk)
            workman = form.save(commit=False)
            workman.operation = operation
            workman.save()
            people = Workman.objects.get(pk=workman.workman.pk)
            kwargs = model_to_dict(
                workman, exclude=['id', 'operation', 'workman'])
            for item in queryset:
                for oper in item.has_operations.all():
                    if oper.name == operation.name:
                        if not oper.workman.filter(member_workman=workman):
                            instance = Members()
                            instance.count = kwargs['count']
                            instance.workman = people
                            instance.operation = oper
                            instance.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


class MembersUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Members
    form_class = EditMemberForm
    success_url = None
    template_name = 'core/members/members_create.html'

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


class MaterialCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Material_Operation
    form_class = Material_OperationCreateForm
    success_url = None
    template_name = 'core/material/material_create.html'

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})

    def get_path(self):
        path = self.request.path.split('/')[2]
        return path

    def form_valid(self, form):
        if not self.request.is_ajax():
            pk = self.get_path()
            form_7 = Form_7.objects.get(pk=self.get_pk())
            queryset = Form_7.objects.filter(form_8=form_7.form_8.pk)
            operation = Operation.objects.get(pk=pk)
            material = form.save(commit=False)
            material.operation = operation
            material.save()
            mater = Resource.objects.get(pk=material.material.pk)
            for item in queryset:
                for oper in item.has_operations.all():
                    if oper.name == operation.name:
                        if not oper.material.filter(material_resourse=material):
                            instance = Material_Operation()
                            instance.material = mater
                            instance.operation = oper
                            instance.count = material.count
                            instance.save()
        return redirect(self.get_success_url())


class MaterialUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Material_Operation
    form_class = EditMaterialForm
    success_url = None
    template_name = 'core/material/material_create.html'

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


class MaterialDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Material_Operation
    template_name = 'core/material/material_delete.html'
    success_url = None
    success_message = 'Материал удален успешно'

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


class MachineCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Machines_operation
    form_class = Machine_operationForm
    success_url = None
    template_name = 'core/machine/machine_create.html'

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})

    def get_path(self):
        path = self.request.path.split('/')[2]
        return path

    def form_valid(self, form):
        if not self.request.is_ajax():
            pk = self.get_path()
            form_7 = Form_7.objects.get(pk=self.get_pk())
            queryset = Form_7.objects.filter(form_8=form_7.form_8.pk)
            operation = Operation.objects.get(pk=pk)
            machine = form.save(commit=False)
            machine.operation = operation
            machine.save()
            mater = machines.Resource.objects.get(pk=machine.machine.pk)
            for item in queryset:
                for oper in item.has_operations.all():
                    if oper.name == operation.name:
                        if not oper.machine.filter(machine_resourse=machine):
                            instance = Machines_operation()
                            instance.machine = mater
                            instance.operation = oper
                            instance.is_driver = machine.is_driver
                            instance.save()
        return redirect(self.get_success_url())


class MachineDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Machines_operation
    template_name = 'core/machine/machine_delete.html'
    success_url = None
    success_message = 'Удалено успешно'

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


class OperationUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Operation
    template_name = 'core/from_7_operations/operation_update.html'
    form_class = OperationFrom
    success_url = None

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def form_valid(self, form):
        pk = self.get_pk()
        form.instance.form.add(Form_7.objects.get(pk=pk))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


class MembersDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Members
    template_name = 'core/members/members_delete.html'
    success_url = None
    success_message = 'Рабочий удален успешно'

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})


class OperationDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Operation
    template_name = 'core/from_7_operations/operation_delete.html'
    success_url = None

    def delete(self, request, *args, **kwargs):
        operation = Operation.objects.get(pk=kwargs['pk'])
        form_7 = Form_7.objects.get(pk=self.get_pk())
        form_8 = form_7.form_8
        for form in form_8.form_8.all():
            for oper in form.has_operations.all():
                if oper.name == operation.name:
                    oper.delete()
        return redirect(self.get_success_url())

    def get_pk(self):
        pk = self.request.META.get('HTTP_REFERER').split('/')[-2]
        return pk

    def get_success_url(self):
        return reverse_lazy('form_7_detail_url', kwargs={'pk': self.get_pk()})
