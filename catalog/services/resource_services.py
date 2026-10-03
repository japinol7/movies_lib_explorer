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


def _download_image(image_url):
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()

    content_type = response.headers.get('Content-Type', '')
    if not content_type.startswith('image/'):
        raise ValueError("URL does not point to an image")

    extension = os.path.splitext(urlparse(image_url).path)[1] or '.jpg'

    return response.content, extension


def _build_picture_name(resource, name, prefix, extension):
    safe_name = get_valid_filename(str(name))

    picture_name = (
        f"{prefix}_im_{resource.__class__.__name__.lower()}"
        f"_{resource.pk}_{safe_name}{extension}")

    return get_valid_filename(picture_name)


def save_picture_to_resource_ext_even_if_already_set(
    resource, image_url, name
    ):
    """Saves a picture to ext_picture, replacing the existing one."""
    content, extension = _download_image(image_url)

    picture_name = _build_picture_name(
        resource, name, prefix='ex', extension=extension)

    if resource.ext_picture:
        resource.ext_picture.delete(save=False)

    resource.ext_picture.save(
        picture_name,
        ContentFile(content),
        save=True,
        )


def save_picture_to_resource(
        resource, image_url, name
    ):
    """Saves a picture to the resource picture if one isn't already set."""
    if resource.picture:
        return

    content, extension = _download_image(image_url)

    picture_name = _build_picture_name(
        resource, name, prefix='up', extension=extension)

    resource.picture.save(
        picture_name,
        ContentFile(content),
        save=True,
        )
