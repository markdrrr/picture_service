from io import BytesIO

import requests
from PIL import Image as Image_PIL
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from images.forms import ImageForm, NewSizeForm
from images.models import Image


class ListImage(ListView):
    model = Image
    template_name = 'images/home.html'
    context_object_name = 'images'


def resize(data: dict, img_path: str):
    """ Изменение размера изображения """
    create_new_img = Image_PIL.open(img_path)
    width, height = create_new_img.size
    if data.get('width') and data.get('height'):
        new_width, new_height = data.get('width'), data.get('height')
    elif new_width := data.get('width'):
        new_height = int(new_width * height / width)
    elif new_height := data.get('height'):
        new_width = int(new_height * height / width)
    create_new_img = create_new_img.resize((new_width, new_height), Image_PIL.ANTIALIAS)
    buffer = BytesIO()
    if create_new_img.mode != 'RGB':
        create_new_img = create_new_img.convert('RGB')
    create_new_img.save(fp=buffer, format='JPEG')
    content = ContentFile(buffer.getvalue())
    return content


def view_image(request, pk):
    """ Представление картинки и формы для изменения """
    picture = get_object_or_404(Image, pk=pk)
    context = {'image': picture}
    form = NewSizeForm()
    if request.method == 'POST':
        form = NewSizeForm(request.POST)
        if form.is_valid():
            content = resize(form.cleaned_data, picture.img.path)
            new_picture = Image()
            new_picture.save()
            new_picture.img.save("image_%s.jpg" % new_picture.pk,
                                 InMemoryUploadedFile(
                                     content,  # file
                                     None,  # field_name
                                     "image_%s.jpg" % new_picture.pk,  # file name
                                     'image/jpeg',  # content_type
                                     content.tell,  # size
                                     None),  # content_type_extra
                                 save=True)
            return redirect(new_picture)
    context['form'] = form
    return render(request, 'images/image_detail.html', context)


def add_image(request):
    """ Представление страницы с формой добавления нового изображения """
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data.get('url')
            if url:
                # name_img = (url.split('/')[-1]).split('.jpg')[0]
                picture = Image()
                picture.save()
                response = requests.get(url)
                if response.status_code == 200:
                    picture.img.save("image_%s.jpg" % picture.pk, ContentFile(response.content), save=True)
                    return redirect(picture)
            picture = form.save()
            return redirect(picture)
    else:
        form = ImageForm()
    return render(request, 'images/add_image.html', {'form': form})
