from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('staff:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect),
    path('staff/', include('staff.urls', namespace='staff')),
    path('scheduling/', include('scheduling.urls', namespace='scheduling')),
]
