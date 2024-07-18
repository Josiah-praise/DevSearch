from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

email_template = """
Dear {username},

Welcome to {app_name}! We're thrilled to have you join our community.

This is a test email.

If you have any questions or need assistance, don't hesitate to reach out to us at praisechinonso21@gmail.com.

Once again, welcome aboard, and thank you for choosing {app_name}!

Best regards,
Praiseafk
{app_name}
"""

@receiver(post_save, sender=get_user_model())
def send_welcome_email(sender, instance, created, *args, **kwargs):
    '''
    Send email to a newly registered user
    '''
    if created:
        subject = 'Welcome to DevSearch'
        body = email_template.format(
            app_name='DevSearch',
            username=instance.get_full_name()
        )
        sender_email = 'praisechinonso21@gmail.com'
        recipient_email = instance.email

        send_mail(
            subject,
            body,
            sender_email,
            [recipient_email],
            fail_silently=False
        )
