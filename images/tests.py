from io import BytesIO

# in python 3: from io import StringIO
from PIL import Image as Image_PIL
from django.core.files.base import File
from django.test import TestCase
# Create your tests here.
from django.urls import reverse

from images.forms import ImageForm, NewSizeForm
from images.models import Image


class ImageTest(TestCase):

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image_PIL.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        for i in range(10):
            self.img = Image(img=self.get_image_file())
            self.img.save()

    def test_first_name_label(self):
        img1 = Image.objects.get(id=1)
        field_label = img1._meta.get_field('img').verbose_name
        self.assertEquals(field_label, 'Картинка')

    def test_lists_all_images(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['images']) == 10)

    def test_iamgeform_field_label(self):
        form = ImageForm()
        self.assertTrue(form.fields['url'].label == 'Ссылка на картинку')

    def test_empty_form_is_no_valid(self):
        form = NewSizeForm()
        self.assertFalse(form.is_valid())

    def test_new_size_create_new_image(self):
        self.client.post(reverse('view_image', kwargs={'pk': 9, }), {'width': 300})
        imgs = Image.objects.all()
        self.assertTrue(len(imgs) > 10)

    def test_new_size(self):
        self.client.post(reverse('view_image', kwargs={'pk': 10, }), {'width': 300})
        image = Image.objects.order_by('-pk').first()
        self.assertTrue(image.img.width == 300)

    def test_new_image(self):
        self.client.post(reverse('add_image'), {'url': 'https://stackru.com/static/img/logo.png'})
        imgs = Image.objects.all()
        self.assertTrue(len(imgs) > 10)
