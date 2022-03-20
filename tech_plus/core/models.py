from django.db import models
from django.db.models.aggregates import Max
from django.forms.fields import CharField
from django.urls import reverse
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

from guide.classifier_kcp.models import * 
from guide.machines_mechanisms import models as machines
from guide.tk_gesn import models as tk

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Логин'), max_length=50, unique=True)
    first_name = models.CharField(_('Имя'), max_length=50)
    last_name = models.CharField(_('Фамилия'), max_length=50)
    third_name = models.CharField(_('Отчество'), max_length=50)
    is_active = models.BooleanField(_('Активный пользователь'), default=True)
    is_verifier = models.BooleanField(_('Эксперт'), default=False)
    is_staff = models.BooleanField(_('Администратор'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.last_name +' ' +self.first_name+ ' '+self.third_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural ='users'

    def get_absolute_url(self):
        return reverse('user_account_url', kwargs={'pk': self.pk})

    def get_full_name(self):
        if self.last_name and self.third_name:
            return self.last_name +' ' +self.first_name[0].upper()+ '. '+self.third_name[0].upper()+'.'
        else:
            return self.first_name


class Measure(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.code


class Snap(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    meashure = models.ForeignKey(Measure, related_name='snap_measure', on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    
class MainObj(models.Model):
    title = models.CharField(max_length=500)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Form_8(models.Model):
    object = models.ForeignKey(MainObj, related_name='form_8', on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField()
    code = models.CharField(max_length=200)
    process_meter = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    process_measure = models.ForeignKey(Measure, related_name='measure_process', on_delete=models.SET_NULL, null=True)
    main_measure = models.ForeignKey(Measure, related_name='measure_main', on_delete=models.SET_NULL, null=True)
    workman_k = models.DecimalField(decimal_places=2, max_digits=10, default=1)
    creator = models.ForeignKey(
        User, related_name='creator', on_delete=models.PROTECT, null=True, blank=True)
    verifier = models.ForeignKey(
        User, related_name='verifire', on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['object','code','created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('form_8_main_url', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('form_8_delete_url', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('form_8_update_url', kwargs={'pk': self.pk})
    
    def get_form_1_url(self):
        return reverse('detail_form_1_url', kwargs={'pk': self.pk})

    def get_form_2_url(self):
        return reverse('detail_form_2_url', kwargs={'pk': self.pk})

    def get_form_3_url(self):
        return reverse('detail_form_3_url', kwargs={'pk': self.pk})

    def get_form_4_url(self):
        return reverse('detail_form_4_url', kwargs={'pk': self.pk})
    
    def get_form_5_url(self):
        return reverse('detail_form_5_url', kwargs={'pk': self.pk})

    def get_form_6_url(self):
        return reverse('detail_form_6_url', kwargs={'pk': self.pk})
    
    def get_form_8_url(self):
        return reverse('form_8_detail_url', kwargs={'pk': self.pk})

    def get_verifier_url(self):
        return reverse('form_8_verifie_url', kwargs={'pk': self.pk})


class Form_7(models.Model):
    """
    Модель для - Формы №7 из списка форм
    """
    created_at = models.DateField(auto_now_add=True)
    start = models.TimeField()
    end = models.TimeField(null=True, blank=True)
    form_8 = models.ForeignKey(
        Form_8, related_name='form_8', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.form_8.title

    def save(self):
        if not self.id:
            self.start = datetime.now()
        return super().save()

    def get_time_diff(self):
        if self.end:
            minutes = self.end.minute - self.start.minute
            hours = self.end.hour - self.start.hour
            return str(hours)+' ч. '+str(minutes)+' м.'

        else:
            return "-"

    def get_absolute_url(self):
        return reverse('form_7_detail_table_url', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('form_7_update_url', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('form_7_detail_url', kwargs={'pk':self.pk})


class Ratio(models.Model):
    """
    Модель для справочника коэффициентов Нпзр и Но
    """
    name = models.CharField(max_length=500)
    npzr = models.IntegerField()
    no = models.IntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '(Нпзр - ' + str(self.npzr) +')' + ' (Но - ' + str(self.no) +') ' + self.name


class RatioNtp(models.Model):
    """
    Модель для справочника коэффициентов Нтп
    """
    name = models.CharField(max_length=500)
    ntp = models.IntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '(Нтп - ' + str(self.ntp) + ')' + self.name


class Workman(models.Model):
    """
    Модель для справочника рабочих и их разрядов
    """
    name = models.CharField(max_length=100)
    measure = models.CharField(max_length=10 ,default='чел.-ч')
    ratio = models.DecimalField(decimal_places=3, max_digits=10, default=1.0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Operation(models.Model):
    """
    Модель "Операция" для наполнения Формы 7
    """
    code = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200)
    start = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    form = models.ManyToManyField(Form_7, related_name='has_operations')
    products = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    measure = models.ForeignKey(
        Measure, related_name='measure_operations', on_delete=models.CASCADE, null=True)
    ratio = models.ForeignKey(Ratio, related_name='operations', on_delete=models.SET_NULL, null=True)
    ntp = models.ForeignKey(RatioNtp, related_name='operations_ntp', on_delete=models.SET_NULL, null=True)
    workman = models.ManyToManyField(Workman, through='Members')
    material = models.ManyToManyField(Resource, through='Material_Operation')
    machine = models.ManyToManyField(machines.Resource, through='Machines_operation')
    verified = models.BooleanField(default=False)
    number = models.IntegerField(default=1)

    class Meta:
        ordering = ['number', 'start']

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse('operation_update_url', kwargs={'pk': self.pk})

    def get_workman_url(self):
        url = reverse('operation_update_url', kwargs={'pk': self.pk})
        return url+'workman/'

    def get_material_url(self):
        url = reverse('operation_update_url', kwargs={'pk': self.pk})
        return url+'material/'

    def get_machine_url(self):
        url = reverse('operation_update_url', kwargs={'pk': self.pk})
        return url+'machine/'

    def get_copy_url(self):
        return reverse('operation_copy_url', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('operation_delete_url', kwargs={'pk': self.pk})


class MainOperation(models.Model):
    name = models.CharField(max_length=200)
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class OperationBook(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200, unique=True)
    products = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    measure = models.ForeignKey(
        Measure, related_name='measure_operations_book', on_delete=models.CASCADE, null=True)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Material_Operation(models.Model):
    operation = models.ForeignKey(Operation, related_name='material_operation', on_delete=models.CASCADE)
    material = models.ForeignKey(Resource, related_name='material_resourse' ,on_delete=models.CASCADE)
    count = models.DecimalField(decimal_places=4, max_digits=10, default=0.0)

    class Meta:
        ordering = ['material']
    
    def __str__(self):
        return self.material.description

    def get_update_url(self):
        return reverse('material_update_url', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('material_delete_url', kwargs={'pk': self.pk})


class Machines_operation(models.Model):
    operation = models.ForeignKey(Operation, related_name='machine_operation', on_delete=models.CASCADE)
    machine = models.ForeignKey(machines.Resource, related_name='machine_resourse', on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False)

    class Meta:
        ordering = ['machine']

    def __str__(self):
        return self.machine.description

    def get_delete_url(self):
        return reverse('machines_delete_url', kwargs={'pk': self.pk})


class Members(models.Model):
    operation = models.ForeignKey(Operation, related_name='member_operation', on_delete=models.CASCADE)
    workman = models.ForeignKey(Workman, related_name='member_workman' ,on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    class Meta:
        ordering = ['workman']

    def __str__(self):
        return self.workman.name

    def get_update_url(self):
        return reverse('member_update_url', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('member_delete_url', kwargs={'pk': self.pk})


class MainModel(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Instruction(models.Model):
    type = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.type


    
class CheckExcel(models.Model):
    status = models.BooleanField(default=False)

