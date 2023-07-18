from django.db import models

class EmailOtpVerification(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()
    
