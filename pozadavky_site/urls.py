"""pozadavky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views as staticfiles_views
from django.urls import path, include, re_path
from django.conf.urls import url, include


from pozadavky_site.pozadavky import views as task_views
from django.views.generic.base import TemplateView
 

urlpatterns = [
    path("", task_views.home_page, name="home_ page"),
    path("home/", task_views.home_page, name="home_page"),
    path("tasks/all/", task_views.tasks_all,name="tasks_all" ),
    path("tasks/all/by/<int:owner_id>/", task_views.tasks_by_owner,name="tasks_owner" ),
    path("tasks/done/", task_views.tasks_done,name="tasks_done" ),
    path("tasks/done/by/<int:user_id>/", task_views.tasks_done_by,name="tasks_done_by" ),
    path("tasks/not_done/", task_views.tasks_not_done,name="tasks_not_done" ),
    path("tasks/not_done/by/<int:user_id>/", task_views.tasks_not_done_by, name="tasks_not_done_by"),
    # path("tasks/splnene/", task_views.tasks_done,name="tasks_done" ),
    path("tasks/not_done_after/", task_views.tasks_not_done_after,name="tasks_not_done_after" ),
    path("tasks/not_done_after/by/<int:user_id>/", task_views.tasks_not_done_after_by, name="tasks_not_done_after_by"),
    path("tasks/done_after/", task_views.tasks_done_after,name="tasks_done_after" ),
    path("tasks/done_after/by/<int:user_id>/", task_views.tasks_done_after_by, name="tasks_done_after_by"),
    path("groups/", task_views.groups,name="groups" ),
    path("authors/", task_views.authors,name="authors" ),
    
    path("tasks/detail/<int:requirement_id>/", task_views.task_detail,name="task_detail" ),
    path("tasks/group/<int:group_owner_id>/", task_views.tasks_group,name="tasks_group" ),
    path("tasks/None/by/<int:owner_id>/", task_views.tasks_by_owner,name="tasks_owner_by" ),
    path("tasks/author/<int:author_id>/", task_views.tasks_author,name="tasks_author" ),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/logout/", TemplateView.as_view(template_name="registration/logout.html"), name="logout"),
    path("logout/", task_views.logout_view, name="logout"),
    path("login_view_authorization/", task_views.login_view_authorization),
    
    # path('chaining/', include('smart_selects.urls')),
    path('ajax/users_by_group/<int:group_id>/', task_views.users_by_group, name='users_by_group'),
]
    
# urlpatterns = [
#     path("tasks/<str:task_type>/", task_views.tasks_by_type, name="tasks-by-type"),
#     path("tasks/<str:task_type>/by/<int:owner_id>/", task_views.tasks_by_owner, name="tasks-by-owner"),
# ]

 # Example usage in a Django template: tasks.html
 #<td> <a href="{% url 'tasks_by_owner' task_type task.owner_id %}">   {{ task.owner.last_name }} {{ task.owner.first_name }} </td></a>
 # Alternative without using 'url' template tag: 
 # <td><a href="/task/owner/{{ task.owner_id }}/">{{ task.owner.last_name }}</a></td> 

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", staticfiles_views.serve),
    ]


# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]