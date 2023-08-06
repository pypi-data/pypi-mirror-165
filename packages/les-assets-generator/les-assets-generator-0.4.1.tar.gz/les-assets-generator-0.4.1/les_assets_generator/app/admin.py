from django.contrib import admin
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from les_assets_generator.app.models import Asset, Font, Parameter

mark_safe_lazy = lazy(mark_safe, str)


class ParameterTabularInline(admin.TabularInline):
    model = Parameter
    extra = 1


class AssetAdmin(admin.ModelAdmin):
    inlines = [
        ParameterTabularInline,
    ]
    readonly_fields = ("example_url",)
    list_display = (
        "title",
        "example_url",
    )

    @admin.display(description=_("example url"))
    def example_url(self, instance):
        if instance.title:
            url = instance.generate_example_url()
            r = mark_safe_lazy(f"<a href='{url}'>{url}</a>")
        else:
            message = _("Can't determine example URL for now")
            r = mark_safe_lazy(f"<span>{message}</span>")
        return r


admin.site.register(Font)
admin.site.register(Asset, AssetAdmin)
