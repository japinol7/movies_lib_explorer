import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename


def get_person_full_name(first_name, last_name):
    name = str(first_name).strip() + ' ' + str(last_name).strip()
    return name.strip()


def get_safe_file_name_from_resource(resource, file_name, file_extension):
    picture_name = (
        f"up_im_{resource.__class__.__name__.lower()}"
        f"_{resource.pk}_{file_name}{file_extension}"
        )
    picture_name = get_valid_filename(picture_name)
    return Path(settings.MEDIA_ROOT) / picture_name


def save_uploaded_picture_to_resource(resource, uploaded_file, name):
    file_extension = os.path.splitext(uploaded_file.name)[1] or ".jpg"
    path = get_safe_file_name_from_resource(resource, name, file_extension)

    # Remove the previous file
    if resource.picture:
        resource.picture.delete(save=False)

    with open(path, 'wb+') as output:
        for chunk in uploaded_file.chunks():
            output.write(chunk)

    resource.picture = path.name
    resource.save()


def save_picture_to_resource(resource, image_url, name):
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        raise ValueError("URL does not point to an image")

    path = urlparse(image_url).path
    extension = os.path.splitext(path)[1] or ".jpg"

    safe_name = get_valid_filename(str(name))
    picture_name = (
        f"ex_im_{resource.__class__.__name__.lower()}"
        f"_{resource.pk}_{safe_name}{extension}"
        )
    picture_name = get_valid_filename(picture_name)

    # Remove the previous file
    if resource.ext_picture:
        resource.ext_picture.delete(save=False)

    resource.ext_picture.save(
        picture_name,
        ContentFile(response.content),
        save=True,
        )
