from django.db import models



class Chapter(models.Model):
    title = models.CharField(max_length=500, primary_key=True)
    description = models.TextField()

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
    description = models.TextField()
    measurement = models.CharField(max_length=500)
    group = models.ForeignKey(Group, related_name='group',  on_delete=models.CASCADE)  

    def __str__(self):
        return self.description



    

      