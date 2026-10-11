from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path('login/', views.login_view, name='login_view'),
    path("profile",views.profile_view,name='profile'),
    path('user_profile/', views.view_employee, name='info'),
    path('todo/', views.todo, name='todo'),
    path('add_achievements/', views.add_achievements, name='achieve'),
    path('add_workhistory/', views.add_workhistory, name='history'),
    path('add_skills/', views.add_skills, name='skills'),
    path('project_login/', views.project_login, name='project_login'),
    path('collab/', views.collab, name='collab'),
    path('kanban/', views.kanban_board, name='kanban'),
    path('empdir/', views.employee_directory, name='dir'),
    path('zoom-meeting/',views.create_zoom_meeting,name='create_zoom_meeting'),
    path('task/',views.home,name='tasks'),
    path('notifications/',views.notifications,name='notify'),
    path('logout/',views.logout_view,name='logout'),
    path('logoutp/',views.logout,name='logoutp'),
    path('view_emp/',views.view_empadmin,name='view_emp'),
    path('view_pro/',views.view_proadmin,name='view_pro'),

]
