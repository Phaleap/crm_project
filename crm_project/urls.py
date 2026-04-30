from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard/'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),  # add this
    path('dashboard/', include('reports.urls')),              # uncomment this
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
