from django.db import migrations


def load_data(apps, schema_editor):
    # Получаем модели
    CompanyInfo = apps.get_model('design_studio', 'CompanyInfo')
    WorkStage = apps.get_model('design_studio', 'WorkStage')
    Review = apps.get_model('design_studio', 'Review')
    User = apps.get_model('auth', 'User')
    ClientRequest = apps.get_model('design_studio', 'ClientRequest')
    DesignerApplication = apps.get_model('design_studio', 'DesignerApplication')

    # 1. Создаем тестового пользователя
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

    # 2. Информация о компании
    CompanyInfo.objects.create(
        title="KOPERNIK Design Studio",
        description="Профессиональная студия дизайна с 10-летним опытом",
        years_of_experience=10,
        projects_completed=235,
        happy_clients=198
    )

    # 3. 10 этапов работы
    stages = [
        (1, "Консультация", "Обсуждение проекта с клиентом"),
        (2, "Анализ", "Исследование требований и рынка"),
        (3, "Концепция", "Разработка концепции дизайна"),
        (4, "Дизайн", "Создание макетов"),
        (5, "Презентация", "Демонстрация клиенту"),
        (6, "Правки", "Корректировка по замечаниям"),
        (7, "Тестирование", "Проверка решений"),
        (8, "Финальная версия", "Утверждение дизайна"),
        (9, "Подготовка", "Создание итоговых файлов"),
        (10, "Передача", "Отправка материалов клиенту")
    ]
    for order, title, desc in stages:
        WorkStage.objects.create(title=title, description=desc, order=order)

    # 4. Отзывы клиентов
    reviews = [
        ("Анна К.", "Отличный дизайн!", 5),
        ("Иван П.", "Профессиональная работа", 5),
        ("Мария С.", "Быстро и качественно", 4)
    ]
    for author, text, rating in reviews:
        Review.objects.create(author=author, text=text, rating=rating, is_published=True)

    # 5. Тестовая заявка клиента
    ClientRequest.objects.create(
        name="Тестовый Клиент",
        email="client@example.com",
        phone="+79991234567",
        project_type="Логотип",
        description="Разработка логотипа для нового бренда",
        budget=50000,
        status="new",
        user=user
    )

    # 6. Тестовая заявка дизайнера
    DesignerApplication.objects.create(
        name="Тестовый Дизайнер",
        email="designer@example.com",
        phone="+79998887766",
        portfolio_link="https://example.com/portfolio",
        experience="5 лет опыта в графическом дизайне",
        specialization="Графический дизайн",
        status="pending",
        user=user
    )


class Migration(migrations.Migration):
    dependencies = [
        ('design_studio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]