from django.db import models
from openpyxl import load_workbook
import os


class Book(models.Model):
    title = models.CharField(max_length=500, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return self.description


class PartBook(models.Model):
    title = models.CharField(max_length=500, primary_key=True)
    description = models.TextField()
    book = models.ForeignKey(Book, related_name='book',  on_delete=models.CASCADE)

    def __str__(self):
        return self.description  


class Chapter(models.Model):
    title = models.CharField(max_length=500, primary_key=True)
    description = models.TextField()
    partbook = models.ForeignKey(PartBook, related_name='partbook',  on_delete=models.CASCADE)

    def __str__(self):
        return self.description



class Group(models.Model):
    title = models.CharField(max_length=500, primary_key=True)
    description = models.TextField()
    chapter = models.ForeignKey(Chapter, related_name='chapter',  on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Resource(models.Model):
    title = models.CharField(max_length=500, primary_key=True)
    description = models.CharField(max_length=800)
    measurement = models.CharField(max_length=500, null=True)
    group = models.ForeignKey(Group, related_name='group',  on_delete=models.CASCADE)

    def __str__(self):
        return self.description + ' (' + self.measurement +')'




