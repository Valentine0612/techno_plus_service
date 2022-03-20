from django.db import models
from django.db.models.base import Model



class TkMainCollection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class TkMainDepartment(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    collection = models.ForeignKey(TkMainCollection, related_name='TkMainCollection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkMainSection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    department = models.ForeignKey(TkMainDepartment, related_name='TkMainDepartment', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkMainSubsection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    section = models.ForeignKey(TkMainSection, related_name='TkMainSection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkMainTableSubsection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    subsection = models.ForeignKey(TkMainSubsection, related_name='TkMainSubsection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkMainTechCard(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    table_subsection = models.ForeignKey(TkMainTableSubsection, related_name='TkMainTableSubsection', on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.description

    


class TkRemoteConstructionCollection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class TkRemoteConstructionDepartment(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    collection = models.ForeignKey(TkRemoteConstructionCollection, related_name='TkRemoteConstructionCollection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkRemoteConstructionSection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    department = models.ForeignKey(TkRemoteConstructionDepartment, related_name='TkRemoteConstructionDepartment', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description


class TkRemoteConstructionSubsection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    section = models.ForeignKey(TkRemoteConstructionSection, related_name='TkRemoteConstructionSection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description



class TkRemoteConstructionTechCard(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    subsection = models.ForeignKey(TkRemoteConstructionSubsection, related_name='TkRemoteConstructionSubsection', on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.description




class TkInstallationEquipmentCollection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class TkInstallationEquipmentDepartment(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    collection = models.ForeignKey(TkInstallationEquipmentCollection, related_name='TkInstallationEquipmentCollection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkInstallationEquipmentSection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    department = models.ForeignKey(TkInstallationEquipmentDepartment, related_name='TkInstallationEquipmentDepartment', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkInstallationEquipmentTable(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    section = models.ForeignKey(TkInstallationEquipmentSection, related_name='TkInstallationEquipmentSection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkInstallationEquipmentTechCard(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    table = models.ForeignKey(TkInstallationEquipmentTable, related_name='TkInstallationEquipmentTable', on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.description



class TkPre_commissioningCollection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class TkPre_commissioningDepartment(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    collection = models.ForeignKey(TkPre_commissioningCollection, related_name='TkPre_commissioningCollection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkPre_commissioningSection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    department = models.ForeignKey(TkPre_commissioningDepartment, related_name='TkPre_commissioningDepartment', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkPre_commissioningSubsection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    section = models.ForeignKey(TkPre_commissioningSection, related_name='TkPre_commissioningSection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkPre_commissioningTableSubsection(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    subsection = models.ForeignKey(TkPre_commissioningSubsection, related_name='TkPre_commissioningSubsection', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TkPre_commissioningTechCard(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=500)
    table_subsection = models.ForeignKey(TkPre_commissioningTableSubsection, related_name='TkPre_commissioningTableSubsection', on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.description