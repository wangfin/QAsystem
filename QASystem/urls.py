"""QASystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.contrib import admin
from django.urls import path
from QAManagement import views
urlpatterns = [
    path('admin/', admin.site.urls),
    #path(r'management/',include(('QAManagement.urls','QAManagement') ,namespace='management')),
    path(r'index/',views.index),
    path(r'upload/',views.upload),
    path(r'QAManagement/',views.QAManagement),
    path(r'Add/',views.Add),
    path(r'modify/',views.modify),
    path(r'search/',views.search),
    path(r'search_all/',views.search_all),
    path(r'delete/',views.delete),
    path(r'Register/',views.Regsiter),
    path(r'Login/',views.Login),
    path(r'userPage/',views.userPage),
    path(r'userQuestion/',views.userQuestion),
    path(r'usermayask/', views.usermayask),
	path(r'completion_search/',views.completion_search),
    path(r'enter_search/',views.enter_search),
    path(r'accurate_search/',views.accurate_search),
    path(r'further_search/',views.further_search),
    path(r'QAManage/',views.QAManage),
    # path(r'chat/',views.chat),
    path(r'getfilename/',views.getfilename),
    path(r'Doexe/',views.Doexe),
    path(r'choose_file/',views.choose_file),
    path(r'show_result/',views.show_result),
    path(r'create_model/',views.create_model),
    path(r'Task/',views.Task),
    path(r'filerename/',views.filerename),
    path(r'saveQA/',views.saveQA),
    path(r'modifyQAres/',views.modifyQAres),
    path(r'userMining/',views.userMining),
    path(r'userGrah/',views.userGrah),
    path(r'search_users_all/',views.search_users_all),
    path(r'usersub/',views.usersub),
    path(r'userattention/',views.userattention),
    path(r'search_single_user/',views.search_single_user),
    path(r'questionnum/',views.questionnum),
    path(r'searchuser/',views.searchuser),
]
urlpatterns += staticfiles_urlpatterns()
