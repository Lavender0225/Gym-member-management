from django.contrib import admin
from gym_manage.models import Course, Member_Course, Instructor_Course, Cost_Record, Member_Balance, Member_Instructor, Instructor_Profile

admin.site.register(Course)
admin.site.register(Member_Course)
admin.site.register(Instructor_Course)
admin.site.register(Cost_Record)
admin.site.register(Member_Balance)
admin.site.register(Member_Instructor)
admin.site.register(Instructor_Profile)