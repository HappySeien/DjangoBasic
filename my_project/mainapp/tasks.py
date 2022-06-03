from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

import logging
from typing import Dict, Union
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_feedback_mail(message_form: Dict[str, Union[int, str]]) -> None:
    logger.info(f'send message: "{message_form}"')
    model_user = get_user_model()
    user_obj = model_user.objects.get(pk=message_form['user_id'])
    send_mail(
        subject='TechSupport Help', # Тема
        message=message_form['message'], # Тело сообщения
        from_email=user_obj.email, # От кого
        recipient_list=['techsupport@my_project.com'], # Кому
        fail_silently=False,
    )
