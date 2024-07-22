from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    name = models.CharField('Название', max_length=70)
    content = models.TextField('Контент')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    is_closed = models.BooleanField(
        'Закрытая',
        default=False,
        db_index=True,
    )

    def __str__(self):
        return self.name

