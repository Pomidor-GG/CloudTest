from django.forms import ModelForm
from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import *


# Register your models here.
class PostAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загружайте изображения в формате 16x9'


class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, MyModelAdmin)
