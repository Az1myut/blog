from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail, mail_admins
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.utils.text import slugify
from blog.models import Post
from icecream import ic


my_signal = Signal()


@receiver(pre_save, sender=Post)
def add_slug(sender, instance, **kwargs):
    # if not instance.slug:
    ic("add_slug")
    instance.slug = slugify(instance.title)


@receiver(pre_save, sender=Post, dispatch_uid="send_email_on_save_std")
def send_email_on_save_std(
    sender,
    instance,
    **kwargs,
):
    """
    Send an email when Post is saved.

    В этом примере мы определяем функцию-обработчик send_email_on_save_std,
    которая принимает аргументы sender, instance и kwargs.
    Мы используем декоратор @receiver, чтобы связать эту функцию-обработчик
    с сигналом pre_save, который отправляется после сохранения экземпляра
    модели Post.

    Внутри функции мы формируем тему и текст сообщения, указываем
    отправителя и получателя, и используем функцию send_mail для отправки
    электронной почты. Если fail_silently установлен в False, то ошибка
    будет возбуждена, если отправка электронной почты не удалась.

    """
    ic("send_email_on_save_std")
    subject = "Post was just saved! Form send_email_on_save_std"
    message = "Hi there, {} was just saved. From send_email_on_save_std".format(
        instance
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [settings.ADMIN[2][1]]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    msg1 = (subject + "msg1", message, from_email, recipient_list)
    msg2 = ("Никита хватит страдать фигнёй " + "msg2", 
            "А смотрите на Никиту. УУУУУУУ.", 
            from_email, 
            recipient_list)

    send_mass_mail(
        (
            msg1,
            msg2,
        ),
        fail_silently=False,
    )


@receiver(post_save, sender=Post, dispatch_uid="send_email_on_save")
def send_email_on_save(sender, instance, **kwargs):
    """
    Send an email when Post is saved and trigger my_signal.
    """
    # ic(settings.ADMIN[2][1])
    ic("send_email_on_save")
    my_signal.send(sender=sender, instance=instance, created=kwargs["created"])

    subject = "Post was just saved! Form send_email_on_save"
    message = "Hi there, {} was just saved. From send_email_on_save".format(instance)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [settings.ADMIN[2][1]]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.send(fail_silently=False)

    mail_admins(
        subject="Post was just saved! Form send_email_on_save",
        message="Hi there, {} was just saved. From send_email_on_save".format(instance),
        fail_silently=False,
    )


@receiver(my_signal)
def my_signal_handler(sender, instance, created, **kwargs):
    """
    Handle my_signal by doing something with the saved instance.
    """
    ic("My Signal")
    if created:
        print("A new instance of {} was just created!".format(sender))
    else:
        print("{} was just updated!".format(instance))



my_signal.connect(my_signal_handler)