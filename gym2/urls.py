from django.conf.urls import patterns, include, url
from gym_manage.views import index, login_view, user_course
from gym_manage.views import user_custom, user_order, user_instructor,instructor_info, instructor_course,instructor_order,instructor_add_course,logout_view,user_change_password,user_info
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^index/$', index),
                       url(r'^login/$', login_view),
                       url(r'^user/course',user_course),
                       url(r'^user/custom',user_custom),
                       url(r'^user/order',user_order),
                       url(r'^user/instructor',user_instructor),
                       url(r'^instructor/info',instructor_info),
                       url(r'^instructor/order',instructor_order),
                       url(r'^instructor/course',instructor_course),
                       url(r'^instructor/add_course',instructor_add_course),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^logout/$',logout_view),
                       url(r'^user/change_password', user_change_password),
                       url(r'^instructor/change_password', user_change_password),\
                       url(r'^user/info', user_info),
                       
    # Examples:
    # url(r'^$', 'gym2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    
)
