from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home_url'),
    path("login/", login_request, name="login"),
    path("logout/", logout_request, name= "logout"),
    path('excel/upload/', ExcelUploadView, name='excel_upload_url'),
    path('excel/check/', CheckExcelDb, name='excel_check'),
    path('user/<int:pk>/', User_account.as_view(), name='user_account_url'),

    path('form_8/create/', Form_8CreateView.as_view(), name='form_8_create_url'),
    path('form_8/', Form_8ListView.as_view(), name='form_8_list_url'),
    path('form_8/<int:pk>/', Form_8DetailView.as_view(), name='form_8_detail_url'),
    path('form_8/<int:pk>/main/', Form_8MainView.as_view(), name='form_8_main_url'),
    path('form_8/<int:pk>/delete/', Form_8DeleteView.as_view(), name='form_8_delete_url'),
    path('form_8/<int:pk>/update/', Form_8UpdateView.as_view(), name='form_8_update_url'),
    path('form_8/<int:pk>/verifie/', form_8Verifie, name='form_8_verifie_url'),
    path('form_8_excel/<int:pk>/', form_8excel, name='form_8_excel'),

    path('form_8/<int:pk>/form_1/', Form_1DetailView.as_view(), name='detail_form_1_url'),
    path('form_8/<int:pk>/form_1/excel', form_1excel, name='form_1_excel'),
    path('form_8/<int:pk>/form_2/', Form_2DetailView.as_view(), name='detail_form_2_url'),
    path('form_8/<int:pk>/form_2/excel', form_2excel, name='form_2_excel'),
    path('form_8/<int:pk>/form_3/', Form_3DetailView.as_view(), name='detail_form_3_url'),
    path('form_8/<int:pk>/form_3/excel', form_3excel, name='form_3_excel'),
    path('form_8/<int:pk>/form_4/', Form_4DetailView.as_view(), name='detail_form_4_url'),
    path('form_8/<int:pk>/form_4/excel', form_4excel, name='form_4_excel'),
    path('form_8/<int:pk>/form_5/', Form_5DetailView.as_view(), name='detail_form_5_url'),
    path('form_8/<int:pk>/form_5/excel', form_5excel, name='form_5_excel'),
    path('form_8/<int:pk>/form_6/', Form_6DetailView.as_view(), name='detail_form_6_url'),
    path('form_8/<int:pk>/form_6/excel', form_6excel, name='form_6_excel'),

    path('form_7/<int:pk>/', Form_7DetailView.as_view(), name='form_7_detail_url'),
    path('form_7/<int:pk>/table/', Form_7DetailTableView.as_view(), name='form_7_detail_table_url'),
    path('form_7/<int:pk>/table/excel', form_7excel, name='form_7_excel'),
    path('form_7/<int:pk>/update/', Form_7UpdateView.as_view(), name='form_7_update_url'),

    path('operation/create/', OperationCreateView.as_view(), name='operation_create_url'),
    path('operation/<int:pk>/update/', OperationUpdateView.as_view(), name='operation_update_url'),
    path('operation/<int:pk>/update/workman/', MemberCreateView.as_view(), name='operation_update_workman_url'),
    path('operation/<int:pk>/update/material/', MaterialCreateView.as_view(), name='operation_update_material_url'),
    path('operation/<int:pk>/update/machine/', MachineCreateView.as_view(), name='operation_update_machine_url'),
    path('operation/<int:pk>/delete/', OperationDeleteView.as_view(), name='operation_delete_url'),
    path('operation/<int:pk>/copy/', OperationCopyView, name='operation_copy_url'),
    path('operation/add/', OperationAdd.as_view(), name='add_operation_url'),
    path('operation/book/add/', AddOperationFromBookView.as_view(), name='add_operation_from_book_url'),

    path('member/<int:pk>/update/', MembersUpdateView.as_view(), name='member_update_url'),
    path('member/<int:pk>/delete/', MembersDeleteView.as_view(), name='member_delete_url'),
    
    path('material/<int:pk>/update/', MaterialUpdateView.as_view(), name='material_update_url'),
    path('material/<int:pk>/delete/', MaterialDeleteView.as_view(), name='material_delete_url'),

    path('machine/<int:pk>/delete/', MachineDeleteView.as_view(), name='machines_delete_url'),

    path('ajax/load-group/', load_group),
    path('ajax/load-chapter/', load_chapter),
    path('ajax/load-part_book/', load_part_book),
    path('ajax/load-book/', load_book),

    path('ajax/load-group-machine/', load_group_machine),
    path('ajax/load-chapter-machine/', load_chapter_machine),

    path('ajax/load-tk-book/', load_tk_book),
    path('ajax/load-tk-departament/', load_tk_departament),
    path('ajax/load-tk-sections/', load_tk_section),
    path('ajax/load-tk-subsections/', load_tk_subsection),
    path('ajax/load-tk-table-subsections/', load_tk_tablesubsection),
    path('ajax/load_tk_techkart/', load_tk_techkart),

]
