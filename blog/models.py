import uuid
from django.db import models

from users.models import User
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    user = models.ForeignKey(
        verbose_name=_("Пользователь"), to=User, on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        verbose_name=_("Пост"), to="Post", on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name=_("Текст комментария"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")

        permissions = (("hide_comments", _("Скрыть комментарии")),)
        default_permissions = ("change", "delete")

    def __str__(self) -> str:
        return f"{self.text} от {self.user}"


class Post(models.Model):
    user = models.ForeignKey(
        verbose_name=_("Пользователь"), to=User, on_delete=models.CASCADE
    )
    slug = models.SlugField(default=uuid.uuid1, unique=True)
    title = models.CharField(verbose_name=_("Заголовок"), max_length=255)
    text = models.TextField(verbose_name=_("Текст поста"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")

        permissions = (("hide_posts", _("Скрыть посты")),)
        default_permissions = ("change", "delete")

    def __str__(self) -> str:
        return f"{self.title} от {self.user}"

