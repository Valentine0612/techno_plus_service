# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CoreForm0(models.Model):
    main_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'core_form_0'


class CoreForm0Form8(models.Model):
    form_0 = models.ForeignKey(CoreForm0, models.DO_NOTHING)
    form_8 = models.ForeignKey('CoreForm8', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_form_0_form_8'
        unique_together = (('form_0', 'form_8'),)


class CoreForm7(models.Model):
    process_name = models.CharField(max_length=200)
    created_at = models.DateField()
    start = models.TimeField()
    end = models.TimeField(blank=True, null=True)
    creator = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    verifier = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    form_8 = models.ForeignKey('CoreForm8', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_form_7'


class CoreForm8(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'core_form_8'


class CoreOperation(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    form = models.ForeignKey(CoreForm7, models.DO_NOTHING)
    info = models.TextField()
    start = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'core_operation'


class CoreOtdel(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'core_otdel'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Otdel(models.Model):
    code = models.TextField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'otdel'


class Podrazdel(models.Model):
    code = models.TextField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'podrazdel'


class Razdel(models.Model):
    code = models.TextField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'razdel'


class Sbornik(models.Model):
    code = models.TextField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'sbornik'


class SoderjanieRabotPodrazdela(models.Model):
    code = models.TextField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'soderjanie_rabot_podrazdela'


class TkGesn(models.Model):
    code = models.TextField()
    name = models.TextField()
    sbornik = models.ForeignKey(Sbornik, models.DO_NOTHING)
    razdel = models.ForeignKey(Razdel, models.DO_NOTHING)
    podrazdel = models.ForeignKey(Podrazdel, models.DO_NOTHING)
    soderjanie_rabot_podrazdela = models.ForeignKey(SoderjanieRabotPodrazdela, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tk_gesn'


class TkGesnMontagOborud(models.Model):
    code = models.TextField()
    name = models.TextField()
    sbornik = models.ForeignKey(Sbornik, models.DO_NOTHING)
    razdel = models.ForeignKey(Razdel, models.DO_NOTHING)
    podrazdel = models.ForeignKey(Podrazdel, models.DO_NOTHING)
    soderjanie_rabot_podrazdela = models.ForeignKey(SoderjanieRabotPodrazdela, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tk_gesn_montag_oborud'


class TkGesnPuskonaladochnie(models.Model):
    code = models.TextField()
    name = models.TextField()
    sbornik = models.ForeignKey(Sbornik, models.DO_NOTHING)
    otdel = models.ForeignKey(Otdel, models.DO_NOTHING)
    razdel = models.ForeignKey(Razdel, models.DO_NOTHING)
    podrazdel = models.ForeignKey(Podrazdel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tk_gesn_puskonaladochnie'


class TkGesnRemStroitRabot(models.Model):
    code = models.TextField()
    name = models.TextField()
    sbornik = models.ForeignKey(Sbornik, models.DO_NOTHING)
    soderjanie_rabot_podrazdela = models.ForeignKey(SoderjanieRabotPodrazdela, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tk_gesn_rem_stroit_rabot'
