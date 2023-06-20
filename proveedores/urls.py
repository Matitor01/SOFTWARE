
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib import admin
#from django.urls import path, include
#from core.urls import core_urlpatterns
from django.urls import path
from proveedores import views

urlpatterns = [
    #Gestion de proveedores
    path('proveedores/eliminar/<int:categoria_id>/', views.proveedores_eliminar, name='proveedores_eliminar'),
    path('proveedores_crear/',views.proveedores_crear,name="proveedores_crear"),
    path('proveedores_save/',views.proveedores_save,name="proveedores_save"),
    path('proveedores_ver/<int:proveedores_id>/',views.proveedores_ver,name="proveedores_ver"),
    path('proveedores_list/',views.proveedores_list,name="proveedores_list"),
    path('proveedores_edit/<int:proveedores_id>/',views.proveedores_edit,name="proveedores_edit"),
    path('proveedores_eliminar/<int:proveedores_id>/', views.proveedores_eliminar, name='proveedores_eliminar'),
    
]

#admin.site.site_header = 'Administrador Bussiness_Solutions'
#admin.site.site_title = 'bussinessSolutions'

#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)