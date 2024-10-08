
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('academico.urls')),
    path('',include('contable.urls')),
    path('accounts/',include('django.contrib.auth.urls')),

]
