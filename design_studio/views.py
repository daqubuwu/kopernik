from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST




def home(request):
    company_info = CompanyInfo.objects.first()

    context = {
        'company_info': company_info,
        'reviews': Review.objects.filter(is_published=True)[:3],
        'features': Feature.objects.filter(is_active=True).order_by('order')
    }

    # Если нужно ограничить количество фич для не-админов
    if not request.user.is_superuser:
        context['features'] = context['features'][:4]

    return render(request, 'design_studio/home.html', context)


def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'design_studio/about.html', {'company_info': company_info})

def workflow(request):
    stages = WorkStage.objects.all().order_by('order')
    return render(request, 'design_studio/workflow.html', {'stages': stages})

@login_required
@require_POST
def delete_stage(request, pk):
    if request.user.is_superuser:
        stage = get_object_or_404(WorkStage, pk=pk)
        stage.delete()
        messages.success(request, 'Этап успешно удален')
    return redirect('workflow')

@login_required
def add_stage(request):
    if request.method == 'POST' and request.user.is_superuser:
        WorkStage.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            order=WorkStage.objects.count() + 1
        )
        messages.success(request, 'Новый этап успешно добавлен')
    return redirect('workflow')

@login_required
@require_POST
def update_stage(request, pk):
    if request.user.is_superuser:
        stage = get_object_or_404(WorkStage, pk=pk)
        stage.title = request.POST.get('title')
        stage.description = request.POST.get('description')
        stage.save()
        messages.success(request, 'Изменения сохранены')
    return redirect('workflow')


def join(request):
    if request.method == 'POST':
        form = DesignerApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_authenticated:
                application.user = request.user

            # Для обычных пользователей устанавливаем статус по умолчанию
            if not request.user.is_superuser:
                application.status = 'new'

            application.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('applications')
    else:
        form = DesignerApplicationForm(user=request.user)

    return render(request, 'design_studio/join.html', {'form': form})



def order(request):
    if request.method == 'POST':
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            if request.user.is_authenticated:
                request_obj.user = request.user
            request_obj.save()

            # Формируем текст письма со всеми данными
            email_message = f"""
            📌 Новая заявка

            Контактные данные:
            👤 Имя: {request_obj.name}
            📧 Email: {request_obj.email}
            📞 Телефон: {request_obj.phone}
            
            🛠 Тип: {request_obj.project_type}
            💰 Бюджет: {request_obj.budget}
            
            Описание проекта:
            {request_obj.description}
            """

            try:
                send_mail(
                    subject='Новая заявка с сайта',
                    message=email_message.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['daqubeen@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Ваша заявка успешно отправлена!')
            except Exception as e:
                messages.error(request, f'Ошибка при отправке заявки: {str(e)}')

            return redirect('applications')
    else:
        form = ClientRequestForm()

    return render(request, 'design_studio/order.html', {'form': form})





def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Или другой страницы после входа
        else:
            return render(request, 'design_studio/login.html', {
                'error': 'Неправильные имя пользователя или пароль'
            })

    return render(request, 'design_studio/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')


@login_required
def applications(request):
    # Обработка фильтров
    selected_client_status = request.GET.get('client_status', '')
    selected_designer_status = request.GET.get('designer_status', '')

    # Для клиентских заявок
    client_requests = ClientRequest.objects.all() if request.user.is_superuser else ClientRequest.objects.filter(user=request.user)
    if selected_client_status:
        client_requests = client_requests.filter(status=selected_client_status)

    # Для заявок дизайнеров
    designer_applications = DesignerApplication.objects.all() if request.user.is_superuser else DesignerApplication.objects.filter(user=request.user)
    if selected_designer_status:
        designer_applications = designer_applications.filter(status=selected_designer_status)

    return render(request, 'design_studio/applications.html', {
        'client_requests': client_requests,
        'designer_applications': designer_applications,
        'client_status_choices': ClientRequest.STATUS_CHOICES,
        'designer_status_choices': DesignerApplication.STATUS_CHOICES,
        'selected_client_status': selected_client_status,
        'selected_designer_status': selected_designer_status
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'design_studio/register.html', {'form': form})


@login_required
def request_detail(request, request_id):
    client_request = get_object_or_404(ClientRequest, id=request_id)

    # Проверка прав доступа
    if not request.user.is_superuser and client_request.user != request.user:
        return redirect('applications')

    if request.method == 'POST' and request.user.is_superuser:
        action = request.POST.get('action')

        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in dict(ClientRequest.STATUS_CHOICES).keys():
                client_request.status = new_status
                client_request.save()
                messages.success(request, 'Статус заявки обновлен')

        elif action == 'delete':
            client_request.delete()
            messages.success(request, 'Заявка успешно удалена')
            return redirect('applications')

    return render(request, 'design_studio/request_detail.html', {
        'request': client_request
    })


@login_required
def designer_application_detail(request, pk):
    application = get_object_or_404(DesignerApplication, pk=pk)

    # Проверка прав доступа
    if not request.user.is_superuser and application.user != request.user:
        return redirect('applications')

    if request.method == 'POST' and request.user.is_superuser:
        action = request.POST.get('action')

        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in dict(application.STATUS_CHOICES).keys():
                application.status = new_status
                application.save()
                messages.success(request, 'Статус заявки обновлен')

        elif action == 'delete':
            application.delete()
            messages.success(request, 'Заявка успешно удалена')
            return redirect('applications')

    return render(request, 'design_studio/designer_application_detail.html', {
        'application': application
    })

@login_required
def delete_request(request, pk):
    if request.method == 'POST' and request.user.is_superuser:
        client_request = get_object_or_404(ClientRequest, pk=pk)
        client_request.delete()
        messages.success(request, 'Заявка успешно удалена')
    return redirect('applications')
