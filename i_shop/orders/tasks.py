from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order


@shared_task
def order_created(order_id):
    """
    Задача отправки email-уведомлений при успешном оформлении заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ номер {order.id}'
    message = f'Уважаемый {order.first_name},\n\nВы успешно разместили заказ. \
                Номер вашего заказа {order.id}'
    mail_sent = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [order.email],
    )
    return mail_sent

# celery --app config.celery.app worker -l info -P solo -> clery launch
