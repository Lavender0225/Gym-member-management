from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Course(models.Model):
    day_choices = (('Mon','Monday'),
                   ('Tue','Tuesday'),
                   ('Wed','Wednesday'),
                   ('Thu','Thursday'),
                   ('Fri','Friday'),
                   ('Sat','Saturday'),
                   ('Sun','Sunday'))
    time_choices = (('10:00 - 12:00','10:00 - 12:00'),
                    ('14:00 - 16:00','14:00 - 16:00'),
                    ('16:00 - 18:00','16:00 - 18:00'))
    name = models.CharField(max_length=30)
    day = models.CharField(max_length= 3,
                           choices = day_choices,)
    time = models.CharField(max_length = 20,
                            choices = time_choices,)
    start_day = models.DateField()
    end_day = models.DateField()
    price = models.IntegerField(default = 200)
    
    def __unicode__(self):
            return u'%s, %s, %s, %s, %s' %(self.name,self.day,self.time,self.start_day,self.end_day)
        

class Member_Course(models.Model):
    member_name = models.ForeignKey(User)
    courses = models.ForeignKey(Course)
    def __unicode__(self):
        return u'%s, %s' %(self.member_name,self.courses)    
    
class Instructor_Course(models.Model):
    instructor_name = models.ForeignKey(User)
    courses = models.ForeignKey(Course)  
    def __unicode__(self):
        return u'%s, %s' %(self.instructor_name.username,self.courses)  

class Cost_Record(models.Model):
    member_name = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    balance = models.IntegerField()
    def __unicode__(self):
        return u'%s, %s, %d' %(self.member_name,self.course,self.balance)
    
class Member_Balance(models.Model):
    member = models.ForeignKey(User)
    balance =  models.IntegerField(default = 1000)
    def __unicode__(self):
        return u'%s, %d' %(self.member, self.balance)    
    
class Member_Instructor(models.Model):
    member = models.ForeignKey(User)
    instructor = models.CharField(max_length=100)
    day_choices = (('Mon','Monday'),
                   ('Tue','Tuesday'),
                   ('Wed','Wednesday'),
                   ('Thu','Thursday'),
                   ('Fri','Friday'),
                   ('Sat','Saturday'),
                   ('Sun','Sunday'))
    time_choices = (('10:00 - 12:00','10:00 - 12:00'),
                    ('14:00 - 16:00','14:00 - 16:00'),
                    ('16:00 - 18:00','16:00 - 18:00'))
    ack_choices = ((0, 'undo'),
                   (1, 'agree'),
                   (2, 'refuse'),)
    
    day = models.CharField(max_length= 3,
                              choices = day_choices,)
    time = models.CharField(max_length = 20,
                            choices = time_choices,)
    start_day = models.DateField()
    end_day = models.DateField()  
    acknowlage = models.IntegerField(default = 0)
    def __unicode__(self):
        return u'%s, %s, %s, %s, %s, %s' %(self.member, self.instructor,self.day, self.time, self.start_day, self.end_day)  
    
class Instructor_Profile(models.Model):
    instructor = models.ForeignKey(User)
    sex_choices = (('Female','Famale'),
                   ('Male','Male'))
    sex = models.CharField(max_length = 6,
                           choices = sex_choices)
    best = models.CharField(max_length = 500)
    def __unicode__(self):
        return u'%s, %s, %s' %(self.instructor, self.sex, self.best)


