from django.db import models
from django.utils import timezone

from django.utils.text import slugify
from time import time
import transliterate
from django.contrib.auth.models import User
from image_cropping import ImageRatioField
import os

import glob


# Create your models here.


def gen_slug(s):
    for i in s:
        if i.lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            temp_slug = transliterate.translit(slugify(s, allow_unicode=True), reversed=True)
            new_slug=''
            for x in temp_slug:
                if x != "'":
                    new_slug+=x

            if Post.objects.filter(slug__iexact=new_slug).count():
                return new_slug + '-' + str(int(time()))
            return new_slug
    new_slug = slugify(s)
    if Post.objects.filter(slug__iexact=new_slug).count():
        return new_slug + '-' + str(int(time()))
    return new_slug


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, blank=True)
    body = models.TextField(blank=True, db_index=True)

    image = models.ImageField(blank=True, verbose_name='Изображение', upload_to='images/')

    cropping = ImageRatioField('image', '1280x720', size_warning=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)
        #
        # print(os.getcwd())
        # print(os.listdir(os.path.join('media/images')))
        #
        # print(glob.glob(os.path.join('media\images', self.image.name.split("/")[-1] + '*')))
        #
        # clean_data_to_del = []
        # for i in glob.glob(os.path.join('media\images', self.image.name.split("/")[-1] + '*')):
        #     temp_data = i.split('\\')
        #
        #     clean_data_to_del.append(temp_data[-1])
        # print(clean_data_to_del)
        #
        # storage, path = self.image.storage, self.image.path
        # print()
        # print(storage)
        # print()


from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


@receiver(pre_delete, sender=Post)
def myfield_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)
    for i in glob.glob(os.path.join('media\images', str(instance.image.name).split("/")[-1] + '*')):
        os.remove(i)

    # def delete(self, *args, **kwargs):
    #     name = self.image.name
    #     # os.remove('media/'+self.image.name)
    #     self.image.delete()
    #     for i in glob.glob(os.path.join('media\images', name.split("/")[-1] + '*')):
    #         os.remove(i)
    #     super().delete(*args, **kwargs)
