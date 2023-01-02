from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta,timezone
from django.db.models.signals import post_save
from .models import Users,UserActivateTokens
from django.core.mail import EmailMultiAlternatives
@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    user_activate_token = UserActivateTokens.objects.create(
        user=instance, token=str(uuid4()), expired_at=datetime.now()+timedelta(days=1)
    )
    active_bool = instance.is_active
    email = instance.email

    # メール本文
    mail_title = "ユーザ本登録の案内"
    text_content = f'http:127.0.0.1:8000/mountain/activate_user/{user_activate_token.token}'
    html_content = f"""
		<p><strong>下記のURLにアクセスするとユーザ登録が完了します。</strong></p>
		<p>{f'http:127.0.0.1:8000/mountain/activate_user/{user_activate_token.token}'}</p>
		"""

    msg = EmailMultiAlternatives(
    subject=mail_title,
    body=text_content,
    from_email='nagano.mountainsite@gmail.com',
    to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    if active_bool is False:
        msg.send()
