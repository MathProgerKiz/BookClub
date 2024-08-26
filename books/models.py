from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(verbose_name='Заголовок')
    author = models.CharField(max_length=255,verbose_name='Автор')
    genre = models.CharField(verbose_name='Жанр')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    average_rating = models.PositiveIntegerField(blank=True,null=True)
    description = models.CharField(verbose_name='Описание')

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

