from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=False, null=False)
    room = models.ForeignKey('ClassRoom.ClassRoom', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.docfile.name
