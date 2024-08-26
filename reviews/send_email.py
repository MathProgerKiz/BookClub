from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_new_book_notification(user, book_title, book_url):
    """
    Отправляет email уведомление пользователю о новой книге.

    :param user: Объект пользователя с атрибутом `email`
    :param book_title: Заголовок книги
    :param book_url: URL книги
    """
    subject = 'New Book Available!'
    context = {
        'user': user,
        'book_title': book_title,
        'book_url': book_url,
    }
    message = render_to_string('new_book_email.html', context)

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()
