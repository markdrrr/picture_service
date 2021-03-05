from django import forms

from images.models import Image


class ImageForm(forms.ModelForm):
    url = forms.URLField(label='Ссылка на картинку', required=False)
    img = forms.ImageField(label='Картинка', required=False)

    class Meta:
        model = Image
        fields = ['url', 'img']

    def clean(self):
        url = self.cleaned_data.get('url')
        img = self.cleaned_data.get('img')
        if not img and not url:
            raise forms.ValidationError('Воспользуйтесь одним из вариантов загрузки')
        if img and url:
            raise forms.ValidationError('Воспользуйтесь ТОЛЬКО одним из вариантов загрузки')
        return self.cleaned_data


class NewSizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)

    def clean(self):
        self.cleaned_data = super().clean()
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')
        if not width and not height:
            raise forms.ValidationError('Укажите один из параметров')
        return self.cleaned_data
