import os
from urllib import parse

from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Length
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

models.FileField.register_lookup(Length)


class Font(models.Model):
    name = models.CharField(_("name"), primary_key=True, max_length=200)
    font = models.FileField(_("font"), upload_to="fonts", blank=True, null=True)
    font_url = models.URLField(_("font url"), blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        if (self.font and self.font_url) or (not self.font and self.font_url is None):
            raise ValidationError(_("You must fill font url or font upload"))
        return super().clean(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(font__length=0, font_url__isnull=False)
                | models.Q(font__length__gt=0, font_url__isnull=True),
                name=_("You must fill font url or font upload"),
            ),
        ]


class Asset(models.Model):
    title = models.CharField(_("title"), primary_key=True, max_length=200)
    picture = models.ImageField(_("picture"), upload_to="assets", blank=True, null=True)
    picture_url = models.URLField(_("picture url"), blank=True, null=True)
    authentication = models.BooleanField(_("authentication required"), default=True)

    def __str__(self):
        return self.title

    def clean(self, *args, **kwargs):
        if (self.picture and self.picture_url) or (
            not self.picture and self.picture_url is None
        ):
            raise ValidationError(_("You must fill picture url or picture upload"))
        return super().clean(*args, **kwargs)

    def generate_example_url(self):
        url = ""
        args = {}
        params = self.assets.all()
        for param in params:
            args[param.name] = param.name
        if len(params) > 0:
            url = f"{os.environ['DEFAULT_DOMAIN']}{reverse('generate', kwargs={'title': self.title})}?{parse.urlencode(args)}"
        return url

    class Meta:
        verbose_name = _("asset")
        verbose_name_plural = _("assets")

        constraints = [
            models.CheckConstraint(
                check=models.Q(picture__length=0, picture_url__isnull=False)
                | models.Q(picture__length__gt=0, picture_url__isnull=True),
                name=_("You must fill picture url or picture upload"),
            ),
        ]


class Parameter(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="assets", verbose_name=_("assets")
    )
    font = models.ForeignKey(
        Font, on_delete=models.CASCADE, related_name="assets", verbose_name=_("font")
    )
    name = models.CharField(_("name"), max_length=200)
    color = ColorField(verbose_name=_("color"))
    font_size = models.IntegerField(_("font size"), default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    mandatory = models.BooleanField(_("mandatory"), default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            "asset",
            "name",
        )
        verbose_name = _("parameter")
        verbose_name_plural = _("parameters")
