# Generated by Django 5.1.7 on 2025-03-30 07:52

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('years_of_experience', models.IntegerField(verbose_name='Лет опыта')),
                ('projects_completed', models.IntegerField(verbose_name='Завершенных проектов')),
                ('happy_clients', models.IntegerField(verbose_name='Довольных клиентов')),
            ],
            options={
                'verbose_name': 'Информация о компании',
                'verbose_name_plural': 'Информация о компании',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликован')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WorkStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок этапа')),
                ('description', models.TextField(verbose_name='Описание этапа')),
                ('order', models.IntegerField(verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Этап работы',
                'verbose_name_plural': 'Этапы работы',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ClientRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('project_type', models.CharField(max_length=100, verbose_name='Тип проекта')),
                ('description', models.TextField(verbose_name='Описание проекта')),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Бюджет')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('in_progress', 'В работе'), ('completed', 'Завершена')], default='new', max_length=20, verbose_name='Статус')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка клиента',
                'verbose_name_plural': 'Заявки клиентов',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DesignerApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('portfolio_link', models.URLField(verbose_name='Ссылка на портфолио')),
                ('experience', models.TextField(verbose_name='Опыт работы')),
                ('specialization', models.CharField(max_length=100, verbose_name='Специализация')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('status', models.CharField(choices=[('pending', 'На рассмотрении'), ('accepted', 'Принята'), ('rejected', 'Отклонена')], default='pending', max_length=20, verbose_name='Статус')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка дизайнера',
                'verbose_name_plural': 'Заявки дизайнеров',
                'ordering': ['-created_at'],
            },
        ),
    ]
