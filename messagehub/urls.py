from django.contrib import admin
from django.urls import path, include

SITE_NAME = 'web-service-5agj'
BASE_URL = f'https://{SITE_NAME}.onrender.com'

urlpatterns = [
    path(f'{BASE_URL}/admin/', admin.site.urls),
    path(f'web-service = {BASE_URL}/api/', include('base.api.urls'))
]
