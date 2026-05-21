from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard/'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),  # add this
    path('accounts/', include('accounts.urls')),  # add this
    path('dashboard/', include('reports.urls')),              # uncomment this
    path('customers/', include('customers.urls')),
    path('leads/', include('leads.urls')),
    path('opportunities/', include('opportunities.urls')), 

    
    path('api/', include('api.urls')),
    path('interactions/', include('interactions.urls')),
    path('tasks/', include('tasks.urls')),
    path('support/', include('support.urls')),
    path('reports/', include('reports.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
