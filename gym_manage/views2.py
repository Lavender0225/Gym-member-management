
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from gym_manage.models import Course, Member_Course, Instructor_Course, Cost_Record, Member_Balance, Member_Instructor, Instructor_Profile
from django.contrib.auth.models import User

def index(request):
   # html = get_template('index.html')
    return render_to_response('index.html')


def login_view(request):
    if 'username' not in request.POST:
        return HttpResponse('username is not in form')
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print user
        if user is not None:
            login(request, user)
            usergroup =request.user.groups.all()
            print usergroup
            if usergroup.count()==1:
                usertype =usergroup[0].name
            else:
                usertype =u""
            if usertype == u"会员":
                user_type = 1
            elif usertype ==u"教练":
                user_type = 2
            return  render_to_response('login.html',{"type":user_type},)
        else:
            return  render_to_response('inedx.html',{"error":true})   
    

def user_course(request):
    print request.user
    print request.user.is_authenticated()
    if(request.user.is_authenticated()):
        username = request.user.username
    else:
        username = ''
    
    course_list = Member_Course.objects.filter(member_name = request.user)
    instructor_list = Member_Instructor.objects.filter(member = request.user)
    print 'OK'
    return render_to_response('user_course.html',{"course_list":course_list,"instructor_list":instructor_list},context_instance=RequestContext(request) )

def user_custom(request):
    if(request.user.is_authenticated()):
            username = request.user.username
    else:
            username = ''   
    cost_list = Cost_Record.objects.filter(member_name = request.user)
    
    return render_to_response('user_custom.html',{"cost_list":cost_list,},context_instance=RequestContext(request))

def user_order(request):
    if(request.user.is_authenticated()):
            username = request.user.username
    else:
            username = ''   
    course_list = Course.objects.all()
    return render_to_response('user_order.html',{"course_list":course_list,},context_instance=RequestContext(request))    

      
def instructor_view(request):
    return render_to_response('instructor.html')

def user_instructor(request):
    if(request.user.is_authenticated()):
        username = request.user.username
    else:
        username = ''    
    temp_list = User.objects.filter(groups__name = u'教练')
    for temp_ins in temp_list:
        instructor.append(instructor_profile.objects.filter(instuctor = temp.instructor))
                        
    return render_to_response('user_instructor.html',{"instructor_list":instructor_list,},context_instance=RequestContext(request))    
    