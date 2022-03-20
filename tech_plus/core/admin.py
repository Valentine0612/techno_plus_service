from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)
from .models import *
sys.path.append(".")
from guide.classifier_kcp.models import *
from guide.machines_mechanisms import models as machines
from guide.tk_gesn import models as tk


class OperationAdmin(admin.TabularInline):
    model = Operation
    extra = 1


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('username',)
    list_filter = ('username',)
    list_display = ('username','first_name','last_name')
    fieldsets = (
        (None, {'fields': ('username','first_name','last_name','third_name',)}),
        ('Роли', {'fields': ('is_active','is_staff','is_verifier')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','first_name','last_name','third_name', 'password1','password2' )}
         ),
         ('Роли', {'fields': ('is_staff','is_verifier')}),
    )


admin.site.register(MainModel)
admin.site.register(Instruction)
admin.site.register(User, UserAdminConfig)
admin.site.register(Form_7)
admin.site.register(OperationBook)
admin.site.register(Operation)
admin.site.register(Form_8)
admin.site.register(Measure)
admin.site.register(Ratio)
admin.site.register(RatioNtp)
admin.site.register(Workman)
admin.site.register(Members)
admin.site.register(Resource)
admin.site.register(MainObj)
admin.site.register(Snap)
admin.site.register(MainOperation)
admin.site.register(Machines_operation)
admin.site.register(Material_Operation)
admin.site.register(machines.Resource)
admin.site.register(tk.TkMainTechCard)
admin.site.register(tk.TkMainCollection)
admin.site.register(tk.TkMainSection)
admin.site.register(tk.TkMainDepartment)
admin.site.register(tk.TkInstallationEquipmentCollection)
admin.site.register(tk.TkInstallationEquipmentDepartment)
admin.site.register(tk.TkInstallationEquipmentSection)
admin.site.register(tk.TkPre_commissioningTableSubsection)
admin.site.register(tk.TkPre_commissioningSubsection)
admin.site.register(tk.TkPre_commissioningDepartment)
admin.site.register(tk.TkPre_commissioningSection)