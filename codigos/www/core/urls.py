
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('painel/', admin.site.urls),
    path('', include('figital.urls'))
]


# from django.conf import settings
# from django.conf.urls.static import static

# if settings.DEBUG is False:  # Apenas quando DEBUG = False
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
