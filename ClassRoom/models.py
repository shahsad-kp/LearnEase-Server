from django.db import models


class ClassRoom(models.Model):
    title = models.CharField(max_length=255)
    lecturer = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name='classrooms')
    students = models.ManyToManyField('Users.User', related_name='classrooms_joined', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title + ' - ' + self.lecturer.name + ' - ' + str(self.created_at)

    class Meta:
        ordering = ['-created_at']


class Topic(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.title + ' - ' + str(self.class_room)
