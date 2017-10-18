from django.db import models

from ckeditor.fields import RichTextField


class EmailTemplate(models.Model):
    name = models.CharField(
        max_length=30,
        help_text='If editing the name of existing template, you must also update any code that uses it!'
    )
    subject = models.CharField(max_length=30, help_text='Please refer to the code to determine the context available')
    body = RichTextField( help_text='Please refer to the code to determine the context available')
