from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class ClientRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('rejected', 'Отклонена'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    project_type = models.CharField(max_length=100, verbose_name='Тип проекта')
    description = models.TextField(verbose_name='Описание проекта')
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бюджет')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')

    def __str__(self):
        return f'Заявка от {self.name} - {self.project_type}'

    class Meta:
        verbose_name = 'Заявка клиента'
        verbose_name_plural = 'Заявки клиентов'
        ordering = ['-created_at']


class DesignerApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    portfolio_link = models.URLField(verbose_name='Ссылка на портфолио')
    experience = models.TextField(verbose_name='Опыт работы')
    specialization = models.CharField(max_length=100, verbose_name='Специализация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')

    def __str__(self):
        return f'Заявка дизайнера от {self.name}'

    class Meta:
        verbose_name = 'Заявка дизайнера'
        verbose_name_plural = 'Заявки дизайнеров'
        ordering = ['-created_at']


class Review(models.Model):
    author = models.CharField(max_length=100, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    def __str__(self):
        return f'Отзыв от {self.author}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']


class CompanyInfo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    years_of_experience = models.IntegerField(verbose_name='Лет опыта')
    projects_completed = models.IntegerField(verbose_name='Завершенных проектов')
    happy_clients = models.IntegerField(verbose_name='Довольных клиентов')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'


class WorkStage(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок этапа')
    description = models.TextField(verbose_name='Описание этапа')
    order = models.IntegerField(verbose_name='Порядок')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Этап работы'
        verbose_name_plural = 'Этапы работы'
        ordering = ['order']