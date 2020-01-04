
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static
import khovanhanh.settings as settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('khofront.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)