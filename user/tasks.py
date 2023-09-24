import uuid
from user.models import User, Verification_Email
from datetime import timedelta
from django.utils.timezone import now
from celery import shared_task


@shared_task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    record = Verification_Email.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()
