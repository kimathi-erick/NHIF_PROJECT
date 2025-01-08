from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from nhif_app.views import custom_login_view
from django.urls import reverse
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('kimathidedan/', admin.site.urls),
    path('nhif/', include('nhif_app.urls')),
    path('login/', custom_login_view, name='login'),
    path('', lambda request: redirect(reverse('claim_list'))),  # Use reverse for safer URL resolution
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)