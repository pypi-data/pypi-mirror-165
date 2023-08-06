"""assets_generator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from les_assets_generator.app import views as app_views

admin.site.site_header = _("Lyon e-Sport assets generator admin")
admin.site.index_title = _("Assets generator")
admin.site.site_title = _("admin")

urlpatterns = [
    path("", app_views.index, name="index"),
    path("assets/", include("les_assets_generator.app.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
