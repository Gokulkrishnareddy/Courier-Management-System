from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns =[
    path('dashboard/',views.dashboard,name="dashboard"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('signup/',views.signup,name="signup"),
    path('track/',views.track,name="track"),
    path('shipments/',views.shipments,name="shipments"),
    path('view-reports/',views.report_manager,name="report_manager"),
    path('create-reports/<str:id>',views.create_reports,name="create_reports"),
]