from io import BytesIO
from urllib.request import urlopen

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from PIL import Image, ImageDraw, ImageFont

from les_assets_generator.app.models import Asset, Parameter


def index(request):
    return redirect("https://github.com/lyon-esport/assets-generator")


def generate(request, title: str):
    asset = get_object_or_404(Asset.objects.select_related(), pk=title)
    if asset.authentication and not request.user.is_authenticated:
        raise PermissionDenied()
    else:
        params = Parameter.objects.select_related().filter(asset=asset)

        img = Image.open(asset.picture)
        draw = ImageDraw.Draw(img)

        for param in params:
            param_value = request.GET.get(param.name)
            if param.mandatory and param_value is None:
                return HttpResponse(_("Missing GET parameter %s" % param), status=422)
            elif param_value is not None:
                try:
                    if param.font.font_url:
                        font_file = urlopen(param.font.font_url)
                    else:
                        font_file = param.font.font.path
                    font = ImageFont.truetype(font_file, param.font_size)
                except OSError:
                    return HttpResponse(
                        _("Font %s not supported" % param.font),
                        status=422,
                    )
                draw.text(
                    (param.x, param.y),
                    param_value,
                    font=font,
                    anchor="ms",
                    fill=param.color,
                )

        byte_io = BytesIO()
        img.save(byte_io, "png")
        byte_io.seek(0)

        return HttpResponse(byte_io, content_type="image/png")
