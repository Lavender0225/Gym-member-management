from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from gym_manage.models import Course, Member_Course, Instructor_Course, Cost_Record, Member_Balance, Member_Instructor, Instructor_Profile
from django.contrib.auth.models import User
import datetime

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
            return  render_to_response('index.html',{"error":True})   
    

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
    member = User.objects.filter(username = username)
    p = Member_Balance.objects.get(member = member)
    balance = p.balance    
    cost_list = Cost_Record.objects.filter(member_name = request.user)
    
    return render_to_response('user_custom.html',{"cost_list":cost_list,"balance":balance},context_instance=RequestContext(request))

def user_order(request):
    print 'this is user/order'
    if(request.user.is_authenticated()):
            username = request.user.username
    else:
            username = ''   
    course_list = Course.objects.all()
    massage = ''
   
    
    if 'course_id' not in request.POST:
        pass
    else:
        course_id = request.POST['course_id']
        
        if course_id is not '' :
            flag = 0
            print course_id
            course_t = Course.objects.get(id = course_id)
            member = User.objects.get(username = username)
            my_courses = Member_Course.objects.filter(member_name = member)
                
            p = Member_Balance.objects.get(member = member)
            if p.balance >= course_t.price :
                flag = 0
                massage = ''
            else:
                massage = u'您的余额不足，请联系管理员充值'
                flag = 1
           
            for c in my_courses:
                print c.courses.name
                c_end_day = c.courses.end_day.strftime('%Y-%m-%d')
                if(course_t.name == c.courses.name or (c.courses.end_day >= course_t.start_day and course_t.day == c.courses.day and course_t.time == c.courses.time)):
                    massage = u'与已有课程时间冲突,请重新选择'
                    flag = 1
                    print 'massage is %s' %massage            

            if flag == 0 :
                p = Member_Course(member_name = member, courses = course_t)
                p.save()
                
                q = Member_Balance.objects.get(member = member)
                q.balance = q.balance - course_t.price
                q.save()                
                p = Cost_Record(member_name = member, course = course_t, balance = q.balance)
                p.save()
                massage = u'预约成功'
                
            else:
                pass
            
        else:
            print 'null course_id'    
    return render_to_response('user_order.html',{"course_list":course_list,"massage":massage,},context_instance=RequestContext(request))   

def user_info(request):
    if(request.user.is_authenticated()):
            username = request.user.username
    else:
        username = ''    
    flag = 0
    massage = ''
    user = User.objects.get(username = username)
    if 'username' not in request.POST and 'lastname' not in request.POST and 'firstname' not in request.POST and 'email' not in request.POST:
        pass
    else:
        user_name = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        if cmp(user_name, '') is not 0 and cmp(user_name, username) is not 0:
            massage = u'用户名不允许修改'
        else:
            
            if cmp(firstname, '') is not 0 and cmp(firstname, user.first_name) is not 0:
                user.first_name = firstname
                flag = 1
            if cmp(lastname, '') is not 0 and cmp(lastname, user.last_name) is not 0:
                user.last_name = lastname
                flag = 1 
            if cmp(email, '') is not 0 and cmp(email, user.email) is not 0:
                user.email = email
                flag = 1
            if flag == 1:
                user.save()
                massage = u'修改成功'
    return render_to_response('user_change_info.html',{"massage":massage,"p":user,},context_instance=RequestContext(request))
    
            
                
            

def user_change_password(request):
    if(request.user.is_authenticated()):
        username = request.user.username
    else:
        username = '' 
    massage = ''
    if 'old_password' not in request.POST:
        pass
    else:
        old_pass = request.POST['old_password']
        new_pass = request.POST['new_password']
        new_pass_again = request.POST['new_password_again']
        if old_pass == '':
            massage = u'请输入旧密码'
        else:
            if cmp(new_pass_again,new_pass) is not 0:
                massage = u'确认密码不正确，请重新输入'
            else:
                user = User.objects.get(username = username)
                user.set_password(new_pass)
                user.save()
                massage = u'修改成功'
    usergroup =request.user.groups.all()
   
    if usergroup.count()==1:
        usertype =usergroup[0].name
    else:
        usertype =u""
    if usertype == u"会员":
        user_type = 1
    elif usertype ==u"教练":
        user_type = 2    
    if user_type == 1:           
        return render_to_response('user_change_password.html',{"massage":massage,},context_instance=RequestContext(request))
    else:
        return render_to_response('instructor_change_password.html',{"massage":massage,},context_instance=RequestContext(request))



def user_instructor(request):
    print 'this is user/instructor'
    if(request.user.is_authenticated()):
        username = request.user.username
    else:
        username = ''    
    instructor_list = Instructor_Profile.objects.all()   
    massage = ''
    if ('instructor_name' and 'order_day' and 'order_time' and 'start_day' and 'end_day') not in request.POST:
        pass
    else:
        instructor_name = request.POST['instructor_name']
        order_day = request.POST['order_day']
        order_time = request.POST['order_time']
        start_day = request.POST['start_day']
        end_day = request.POST['end_day']        
        if instructor_name == '' or order_day == '' or order_time == '' or start_day== ''  or end_day == '':
            massage = u'请填写完整信息'
        else:
            
            instructor = User.objects.get(username = instructor_name)
            member = User.objects.get(username = username)
            p = Member_Instructor(member = member, instructor = instructor_name, time = order_time, day = order_day, start_day = start_day, end_day = end_day, acknowlage = 0)
            p.save()
            massage = u'预约成功，等待教练同意'
            
        
            
    return render_to_response('user_instructor.html',{"instructor_list":instructor_list,"massage":massage},context_instance=RequestContext(request))  

def instructor_info(request):
    if(request.user.is_authenticated()):
        username = request.user.username
    else:
        username = ''   
    
    massage = ''
    
    if request.method == 'POST':
        #instructor_id = request.POST['instructor_id']
        instructor_username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        sex = request.POST['sex']
        best = request.POST['best']  

        if (cmp(instructor_username,'') is not 0) and (cmp(instructor_username, username) is not 0) :
            massage = u'用户名不允许修改'
            print 'Post_username: %susername: %s ' %(instructor_username,username, )
            print 'best %s' % best
        else:
            flag = 0
            instructor = User.objects.get(username = username)
            #instructor.username = instructor_username
            if cmp(first_name,'') is not 0 and cmp(instructor.first_name,first_name) is not 0 :
                instructor.first_name = first_name
                flag = 1
            if cmp(last_name,'') is not 0 and cmp(instructor.last_name, last_name) is not 0:
                instructor.last_name = last_name
                flag = 1
            if cmp(email,'') is not 0 and cmp(instructor.email, email) is not 0:
                instructor.email = email
                flag = 1
            instructor_profile = Instructor_Profile.objects.get(instructor = instructor)
            if cmp(sex,'') is not 0 and cmp(instructor_profile.sex ,sex) is not 0:
                instructor_profile.sex = sex
                flag = 1
            if cmp(best,'') is not 0 and cmp(instructor_profile.best, best) is not 0:
                instructor_profile.best = best
                flag = 1
            if flag == 1:
                instructor.save()
                instructor_profile.save()
                massage = u'个人信息修改成功'
            else:
                massage = ''
            
    instructor = User.objects.get(username = username)
    p = Instructor_Profile.objects.get(instructor = instructor)
    
    return render_to_response('instructor_info.html',{"p":p,"massage":massage},context_instance=RequestContext(request))

def instructor_course(request):
    if(request.user.is_authenticated()):
        username = request.user.username
    else:
        username = ''    
    instructor = User.objects.get(username = username)
    my_courses  = Instructor_Course.objects.filter(instructor_name = instructor)
    return render_to_response('instructor_course.html',{"course_list":my_courses,},context_instance=RequestContext(request))

def instructor_order(request):
    if(request.user.is_authenticated()):
        username = request.user.username
    else:
        username = ''    
    my_orders = Member_Instructor.objects.filter(instructor = username)
    massage = ''
    print request.POST
    if 'agree'not in request.POST  and 'refuse' not in request.POST:
        pass
    else:
        if u'agree'  in request.POST:
            order_id = request.POST['agree']
            p = Member_Instructor.objects.get(id = order_id)
            if p.acknowlage is not 0:
                massage = u'已做出决定，请不要如此善变！'
            else:
                p.acknowlage = 1
                p.save()
                massage = u'已同意'
        else:
            order_id = request.POST['refuse']
            p = Member_Instructor.objects.get(id = order_id)
            if p.acknowlage is not 0:
                massage = u'已做出决定，请不要如此善变！'   
            else:
                p.acknowlage = 2
                p.save()
                massage = u'已拒绝'            
    
    return render_to_response('instructor_order.html',{"my_orders":my_orders,"massage":massage,},context_instance=RequestContext(request))

def instructor_add_course(request):
    if(request.user.is_authenticated()):
        username = request.user.username
    else:
        username = ''
    massage = ''
    if 'course_name' and 'course_day' and 'course_time' and 'start_day' and 'end_day' and 'price' not in request.POST:
        pass
    else:
        name = request.POST['course_name']
        day = request.POST['course_day']
        time = request.POST['course_time']
        start_day = request.POST['start_day']
        end_day = request.POST['end_day']
        price = request.POST['price']
        print 'start day: %s' % start_day
        massage = ''
        flag = 0
        if name == '' or day == '' or time == '' or start_day == '' or end_day == '':
            massage = u'请输入完整信息'
        else:
            ins = User.objects.get(username = username)
            my_courses = Instructor_Course.objects.filter(instructor_name = ins)
            for c in my_courses:
                c_end_day = c.courses.end_day.strftime('%Y-%m-%d')
                print 'c_end_day: %s' % c_end_day
                print 'start_day: %s' % start_day
                if (c_end_day >= start_day and c.courses.time == time and c.courses.day == day) or name == c.courses.name :
                    massage = u'与已有课程时间冲突'
                    flag = 1
            
            if flag == 0:
                p = Course(name = name, day = day, time = time, start_day = start_day, end_day = end_day, price = price)
                p.save()
                q = Instructor_Course(instructor_name = ins, courses = p)
                q.save()
                massage = u'课程添加成功'
                    
    return render_to_response('instructor_add_course.html',{"massage":massage,},context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return index(request)