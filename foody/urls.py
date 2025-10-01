from django.contrib import admin
from django.urls import path,include

from django .conf.urls.static import static 
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('firebaseUser.urls')),
    path('api/', include('foodItems.urls')),
    path('api/', include('cart.urls')),
    path('api/',include('stats.urls')),
    path('api/',include('pament.urls')),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)