import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Project, ProjectImage

@receiver(pre_save, sender=Project)
def delete_old_project_main_image(sender, instance, **kwargs):
    if not instance.pk:
        return  

    try:
        old_image = Project.objects.get(pk=instance.pk).main_image
    except Project.DoesNotExist:
        return

    new_image = instance.main_image

    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(pre_save, sender=ProjectImage)
def delete_old_gallery_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_image = ProjectImage.objects.get(pk=instance.pk).image
    except ProjectImage.DoesNotExist:
        return

    new_image = instance.image

    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)



@receiver(post_delete, sender=Project)
def delete_project_image_on_delete(sender, instance, **kwargs):
    if instance.main_image and os.path.isfile(instance.main_image.path):
        os.remove(instance.main_image.path)


@receiver(post_delete, sender=ProjectImage)
def delete_gallery_image_on_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


