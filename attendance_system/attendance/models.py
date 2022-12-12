from django.db import models

# Create your models here.

class TimeTable(models.Model):
    days=[
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
    ]
    Faculty_id = models.CharField(max_length=10,null=True,default=" ")
    Day = models.CharField(max_length=100,null=True,default=" ")
    Start = models.CharField(max_length=100,null=True,default=" ")
    End = models.CharField(max_length=100,null=True,default=" ")
    Subject = models.CharField(max_length=100,null=True,default=" ")
    RoomNo = models.CharField(max_length=100,null=True,default=" ")
    Code=models.CharField(max_length=100,null=True,default=" ")
    Batch = models.CharField(max_length=100,null=True,default=" ")
    def __str__(self):
        return self.Faculty_id

class Attendance(models.Model):
    Subject = models.CharField(max_length=100,null=True,default=" ")
    Code=models.CharField(max_length=100,null=True,default=" ")
    Batch = models.CharField(max_length=100,null=True,default=" ")
    RoomNo = models.CharField(max_length=100,null=True,default=" ")
    RollNo = models.CharField(max_length=100,null=True,default=" ")
    ips = models.CharField(max_length=100,null=True,default=" ")
    def __str__(self):
        return self.RollNo
