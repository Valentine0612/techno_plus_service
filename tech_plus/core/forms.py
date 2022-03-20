from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django.contrib.auth.forms import PasswordChangeForm
from django.forms.widgets import NumberInput
from django.apps import apps


from .models import *

TK_CHOISE_VALUES = (
    ('', '--- Выберите значение ---'),
    ("TkMainCollection", "ТК ГЭСН"),
    ("TkRemoteConstructionCollection", "ТК ГЭСН Рем.-строит работ"),
    ("TkInstallationEquipmentCollection", "ТК ГЭСН Монтаж оборудования"),
    ("TkPre_commissioningCollection", "ТК ГЭСН Пусконаладочные работы"),
)

CHOICE_DEPARTAMENT = {
    "TkMainCollection": tk.TkMainDepartment,
    "TkRemoteConstructionCollection": tk.TkRemoteConstructionDepartment,
    "TkInstallationEquipmentCollection": tk.TkInstallationEquipmentDepartment,
    "TkPre_commissioningCollection": tk.TkPre_commissioningDepartment
}

CHOICE_SECTION = {
    "TkMainCollection": tk.TkMainSection,
    "TkRemoteConstructionCollection": tk.TkRemoteConstructionSection,
    "TkInstallationEquipmentCollection": tk.TkInstallationEquipmentSection,
    "TkPre_commissioningCollection": tk.TkPre_commissioningSection
}

CHOICE_SUBSECTION = {
    "TkMainCollection": tk.TkMainSubsection,
    "TkRemoteConstructionCollection": tk.TkRemoteConstructionSubsection,
    "TkInstallationEquipmentCollection": tk.TkInstallationEquipmentTable,
    "TkPre_commissioningCollection": tk.TkPre_commissioningSubsection
}

CHOICE_SUBTABLE = {
    "TkMainCollection": tk.TkMainTableSubsection,
    "TkPre_commissioningCollection": tk.TkPre_commissioningTableSubsection
}

CHOICE_TECHKART = {
    "TkMainCollection": tk.TkMainTechCard,
    "TkRemoteConstructionCollection": tk.TkRemoteConstructionTechCard,
    "TkInstallationEquipmentCollection": tk.TkInstallationEquipmentTechCard,
    "TkPre_commissioningCollection": tk.TkPre_commissioningTechCard
}


class form_8Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collections'].queryset = tk.TkMainCollection.objects.none()
        self.fields['departament'].queryset = tk.TkMainCollection.objects.none()
        self.fields['section'].queryset = tk.TkMainSection.objects.none()
        self.fields['subsection'].queryset = tk.TkMainSubsection.objects.none()
        self.fields['tablesubsection'].queryset = tk.TkMainTableSubsection.objects.none()
        self.fields['techkart'].queryset = tk.TkMainTechCard.objects.none()

        if 'tk_field' in self.data and self.data['tk_field']:
            model = apps.get_model('tk_gesn', self.data['tk_field'])
            self.fields['collections'].queryset = model.objects.all()

            if 'collections' in self.data:
                departament = CHOICE_DEPARTAMENT[self.data['tk_field']]
                self.fields['departament'].queryset = departament.objects.all()

            if 'departament' in self.data:
                section = CHOICE_SECTION[self.data['tk_field']]
                self.fields['section'].queryset = section.objects.all()

            if 'subsection' in self.data:
                subsection = CHOICE_SUBSECTION[self.data['tk_field']]
                self.fields['subsection'].queryset = subsection.objects.all()

            if 'tablesubsection' in self.data and self.data['tk_field'] in CHOICE_SUBTABLE:
                tablesubsection = CHOICE_SUBTABLE[self.data['tk_field']]
                self.fields['tablesubsection'].queryset = tablesubsection.objects.all()

            if 'techkart' in self.data:
                techkart = CHOICE_TECHKART[self.data['tk_field']]
                self.fields['techkart'].queryset = techkart.objects.all()

    object = forms.ModelChoiceField(
        queryset=MainObj.objects.all(),
        label='Наименование объекта',
        empty_label="--- Выберите значение ---"
    )

    tk_field = forms.ChoiceField(
        choices=TK_CHOISE_VALUES,
        label='Справочник ТК ГЭСН',
        required=False
    )

    collections = forms.ModelChoiceField(
        queryset=None,
        label='Сборник',
        required=False,
        empty_label="--- Выберите значение ---"
    )

    departament = forms.ModelChoiceField(
        queryset=None,
        label='Отдел',
        required=False,
        empty_label="--- Выберите значение ---"
    )

    section = forms.ModelChoiceField(
        queryset=None,
        label='Раздел',
        required=False,
        empty_label="--- Выберите значение ---"
    )

    subsection = forms.ModelChoiceField(
        queryset=None,
        label='Подраздел',
        required=False,
        empty_label="--- Выберите значение ---"
    )

    tablesubsection = forms.ModelChoiceField(
        queryset=None,
        label='Таблица подраздела (Для ТК ГЭСН и ТК ГЭСН Пусконаладочные)',
        required=False,
        empty_label="--- Выберите значение ---"
    )

    techkart = forms.ModelChoiceField(
        queryset=None,
        label='Технологическая карта',
        required=False,
        empty_label="--- Выберите значение ---"
    )

    code = forms.CharField(
        label='Шифр ТК',
    )

    title = forms.CharField(
        label='Название',
    )
    process_meter = forms.FloatField(
        label='Значение измерителя',
    )
    process_measure = forms.ModelChoiceField(
        label='Ед. измерения',
        queryset=Measure.objects.all(),
        empty_label="--- Выберите значение ---"
    )
    main_measure = forms.ModelChoiceField(
        label='Измеритель ЭСН',
        queryset=Measure.objects.all(),
        empty_label="--- Выберите значение ---"
    )
    workman_k = forms.DecimalField(
        label='Коэффициент рабочего звена'
    )

    field_order = ['object', 'tk_field', 'collections', 'departament', 'section', 'subsection', 'tablesubsection', 'techkart', 'code',
                   'title', 'process_meter', 'process_measure', 'main_measure', 'workman_k']

    class Meta:
        model = Form_8
        fields = ['object', 'title', 'code', 'process_meter',
                  'process_measure', 'main_measure', 'workman_k']


class Form_8UpdateForm(forms.ModelForm):

    object = forms.ModelChoiceField(
        queryset=MainObj.objects.all(),
        label='Наименование предприятия',
        empty_label="--- Выберите значение ---"
    )

    code = forms.CharField(
        label='Шифр ТК',
    )

    title = forms.CharField(
        label='Название',
    )
    process_meter = forms.FloatField(
        label='Значение измерителя',
    )
    process_measure = forms.ModelChoiceField(
        label='Ед. измерения',
        queryset=Measure.objects.all()
    )
    main_measure = forms.ModelChoiceField(
        label='Измеритель ЭСН',
        queryset=Measure.objects.all()
    )
    workman_k = forms.DecimalField(
        label='Коэффициент рабочего звена'
    )

    field_order = ['object', 'code', 'title', 'process_meter',
                   'process_measure', 'main_measure', 'workman_k']

    class Meta:
        model = Form_8
        fields = ['object', 'title', 'code', 'process_meter',
                  'process_measure', 'main_measure', 'workman_k']


class Form_7From(BSModalModelForm):

    class Meta:
        model = Form_7
        fields = ['end', 'start']

    field_order = ['start', 'end']

    start = forms.TimeField(
        label='Время начала измерений',
        widget=forms.TimeInput(
            attrs={'placeholder': 'ЧЧ:ММ', 'type': 'time'},
            format='%H:%M'),
        required=False)

    end = forms.TimeField(
        label='Время окончания измерений',
        widget=forms.TimeInput(attrs={'placeholder': 'ЧЧ:ММ', 'type': 'time'}),
        required=False)


class MembersForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request')
        workmans = self.get_operation(self.request.path)
        if workmans:
            qs = Workman.objects.all()
            for workman in workmans:
                qs = qs.exclude(name=workman.name)
            self.fields['workman'].queryset = qs
        else:
            self.fields['workman'].queryset = Workman.objects.all()

    def get_operation(self, path):
        pk = path.split('/')[2]
        return Operation.objects.get(pk=pk).workman.all()

    workman = forms.ModelChoiceField(
        label='Рабочий',
        queryset=None
    )
    count = forms.IntegerField(
        label='Количество человек'
    )

    class Meta:
        model = Members
        fields = ['workman', 'count']
        exclude = ['operations']


class Material_OperationCreateForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Resource.objects.none()
        self.fields['group'].queryset = Group.objects.none()
        self.fields['chapter'].queryset = Chapter.objects.none()
        self.fields['partbook'].queryset = PartBook.objects.none()

        if 'book' in self.data:
            try:
                self.fields['partbook'].queryset = self.filter_data(
                    PartBook, 'book')
            except (ValueError, TypeError):
                pass

        if 'partbook' in self.data:
            try:
                self.fields['chapter'].queryset = self.filter_data(
                    Chapter, 'partbook')
            except (ValueError, TypeError):
                pass

        if 'chapter' in self.data:
            try:
                self.fields['group'].queryset = self.filter_data(
                    Group, 'chapter')
            except (ValueError, TypeError):
                pass

        if 'group' in self.data:
            try:
                self.fields['material'].queryset = self.filter_data(
                    Resource, 'group')
            except (ValueError, TypeError):
                pass

    def filter_data(self, model, params):
        val = self.data.get(params)
        kwargs = {}
        kwargs[params] = val
        data = model.objects.filter(**kwargs)
        return data

    material = forms.ModelChoiceField(
        label='Материал',
        queryset=None,
    )

    group = forms.ModelChoiceField(
        label='Группа раздела книги',
        queryset=None
    )

    chapter = forms.ModelChoiceField(
        label='Раздел книги',
        queryset=None
    )

    partbook = forms.ModelChoiceField(
        label='Часть книги',
        queryset=None
    )

    book = forms.ModelChoiceField(
        label='Книга',
        queryset=Book.objects.all()
    )

    count = forms.DecimalField(
        label='Количество'
    )

    field_order = ['book', 'partbook', 'chapter', 'group', 'material', 'count']

    class Meta:
        model = Material_Operation
        fields = ['material', 'count']


class Machine_operationForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['machine'].queryset = machines.Resource.objects.none()
        self.fields['group'].queryset = machines.Resource.objects.none()

        if 'chapter' in self.data:
            try:
                self.fields['group'].queryset = self.filter_data(
                    machines.Group, 'chapter')
            except (ValueError, TypeError):
                pass

        if 'group' in self.data:
            try:
                self.fields['machine'].queryset = self.filter_data(
                    machines.Resource, 'group')
            except (ValueError, TypeError):
                pass

    def filter_data(self, model, params):
        val = self.data.get(params)
        kwargs = {}
        kwargs[params] = val
        data = model.objects.filter(**kwargs)
        return data

    chapter = forms.ModelChoiceField(
        label='Раздел',
        queryset=machines.Chapter.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    group = forms.ModelChoiceField(
        label='Группа',
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    machine = forms.ModelChoiceField(
        label='Машины и механизмы',
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    is_driver = forms.BooleanField(
        label='Наличие машиниста',
        required=False
    )

    field_order = ['chapter', 'group', 'machine', 'is_driver']

    class Meta:
        model = Machines_operation
        fields = ['machine', 'is_driver']


class EditMaterialForm(BSModalModelForm):

    count = forms.DecimalField(
        label='Количество'
    )

    class Meta:
        model = Material_Operation
        fields = ['count']
        exclude = ['operations', 'material']


class EditMemberForm(BSModalModelForm):

    count = forms.IntegerField(
        label='Количество человек'
    )

    class Meta:
        model = Members
        fields = ['count']
        exclude = ['operations', 'workman']


class AddOperationForm(BSModalForm):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        choices = [(x.name, x.name) for x in MainOperation.objects.all()]
        choices.insert(0, ('', '--- Выберите значение ---'))
        self.fields['name'].choices = choices

    name = forms.ChoiceField(
        label='Операции',
        choices=[],
    )


class AddOperationFromBookForm(BSModalForm):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

    name = forms.ModelChoiceField(
        label='Список операций в Справочнике',
        queryset=OperationBook.objects.all(),
        empty_label="--- Выберите значение ---",
    )


class OperationFrom(BSModalModelForm):

    name = forms.CharField(
        label='Название операции',
        widget=forms.TextInput())
    duration = forms.IntegerField(
        label='Продолжительность',
        min_value=1,
        max_value=60,
        widget=forms.NumberInput())
    start = forms.IntegerField(
        label='Начало измерений',
        min_value=0,
        max_value=59,
        widget=forms.NumberInput())
    products = forms.DecimalField(
        label='Количество измерителя',
        widget=NumberInput(attrs={'placeholder': '00,00', 'step': '0.01'}),
        min_value=0.01,
        required=True)
    ratio = forms.ModelChoiceField(
        queryset=Ratio.objects.all(),
        label="Коэффициенты Нпзр Но",
        required=True,
        widget=forms.Select(attrs={'class': 'selectpicker selectStyle'})
    )
    ntp = forms.ModelChoiceField(
        label="Коэффициент Нтп",
        required=True,
        queryset=RatioNtp.objects.all()
    )
    measure = forms.ModelChoiceField(
        label='Измеритель',
        queryset=Measure.objects.all(),
    )
    number = forms.IntegerField(
        label='Порядоковый номер',
    )

    field_order = ['name', 'number', 'duration', 'start',
                   'measure', 'products', 'ratio', 'ntp']

    class Meta:
        model = Operation
        fieldset = ['name', 'duration', 'start',
                    'measure', 'products', 'ratio', 'ntp', 'number']
        exclude = ['form', 'info', 'workman',
                   'material', 'machine', 'verified','code']


# password_helper = "<ul><li>Пароль должен содержать не менее 8 символов</li></ul>"

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    new_password1 = forms.CharField(
        label=("Новый пароль"),
        widget=forms.PasswordInput(),
        strip=False,
        help_text="""<li>Пароль должен содержать не менее 8 символов</li>
        <li>Пароль должен содержать буквы и цифры</li>
        <li>Пароль не должен содержать схожую информацию с другими данными</li>
        <li>Пароль не должен быть слишком простым (Недопустимые пароли: QWERTY1, ASDFG и т. д.)</li>
        """
    )

    new_password2 = forms.CharField(
        label=("Новый пароль (подтверждение)"),
        widget=forms.PasswordInput(),
        strip=False,
    )

    old_password = forms.CharField(
        label=("Текущий пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )


    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user