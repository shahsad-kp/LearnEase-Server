from django.db import models
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


class EmailVerification(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def send(self):
        subject = 'Verify your email - LearnEase'
        verification_link = settings.FRONTEND_URL + reverse('verify-email', kwargs={'token': self.token})
        message = render_to_string('email_verification_template.html', {'verification_link': verification_link})
        return send_mail(
            subject=subject,
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email],
            html_message=message,
        )
