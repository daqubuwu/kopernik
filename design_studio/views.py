from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from . import models
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models


def home(request):
    company_info = CompanyInfo.objects.first()
    features = Feature.objects.filter(is_active=True).order_by('order')

    # Ограничение количества фич для обычных пользователей
    if not request.user.is_superuser:
        features = features[:4]

    # Список иконок для выбора в модальном окне
    available_icons = [
        'fa-star', 'fa-bolt', 'fa-heart', 'fa-code', 'fa-magic',
        'fa-lightbulb', 'fa-chart-line', 'fa-cogs', 'fa-lock', 'fa-globe'
    ]

    context = {
        'company_info': company_info,
        'reviews': Review.objects.filter(is_published=True)[:3],
        'features': features,
        'icons': available_icons
    }

    return render(request, 'design_studio/home.html', context)



def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'design_studio/about.html', {'company_info': company_info})


@login_required
def workflow(request):
    stages = WorkStage.objects.all()
    return render(request, 'design_studio/workflow.html', {
        'stages': stages,
        'layout': 'cards'  # флаг для нового макета
    })


@login_required
def delete_stage(request, pk):
    WorkStage.objects.filter(id=pk).delete()
    return redirect('workflow')


@login_required
@require_POST
def add_stage(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    insert_after_id = int(request.POST.get('insert_after', 0))

    if insert_after_id == 0:
        new_order = 1
    else:
        after_stage = get_object_or_404(WorkStage, id=insert_after_id)
        new_order = after_stage.order + 1

    WorkStage.objects.filter(order__gte=new_order).update(order=models.F('order') + 1)

    WorkStage.objects.create(title=title, description=description, order=new_order)
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


@login_required
@csrf_exempt
def edit_stage(request, pk):
    stage = get_object_or_404(WorkStage, id=pk)
    if request.method == 'POST':
        stage.title = request.POST.get('title')
        stage.description = request.POST.get('description')
        stage.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def join(request):
    if request.method == 'POST':
        form = DesignerApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_authenticated:
                application.user = request.user
            if not request.user.is_superuser:
                application.status = 'pending'
            application.save()

            # 🔔 Отправка письма админу
            email_message = f"""
📌 Новая заявка от дизайнера

👤 Имя: {application.name}
📧 Email: {application.email}
📞 Телефон: {application.phone}

💼 Специализация: {application.specialization}
🧠 Опыт: {application.experience}
🔗 Портфолио: {application.portfolio_link}
"""
            try:
                send_mail(
                    subject='Новая заявка от дизайнера',
                    message=email_message.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['daqubeen@yandex.ru'],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f'Ошибка при отправке уведомления: {str(e)}')

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
            email_message = f"""
            📌 Новая заявка

            Контактные данные:
            👤 Имя: {request_obj.name}
            📧 Email: {request_obj.email}
            📞 Телефон: {request_obj.phone}

            💪 Тип: {request_obj.project_type}
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
            return redirect('home')
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
    selected_client_status = request.GET.get('client_status', '')
    selected_designer_status = request.GET.get('designer_status', '')
    client_requests = ClientRequest.objects.all() if request.user.is_superuser else ClientRequest.objects.filter(
        user=request.user)
    if selected_client_status:
        client_requests = client_requests.filter(status=selected_client_status)
    designer_applications = DesignerApplication.objects.all() if request.user.is_superuser else DesignerApplication.objects.filter(
        user=request.user)
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
    if not request.user.is_superuser and client_request.user != request.user:
        return redirect('applications')

    if request.method == 'POST' and request.user.is_superuser:
        action = request.POST.get('action')
        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in dict(ClientRequest.STATUS_CHOICES).keys():
                client_request.status = new_status
                client_request.save()

                # Отправка email с уведомлением клиенту
                status_messages = {
                    'new': 'Ваша заявка принята в обработку.',
                    'in_progress': 'Ваша заявка сейчас в работе.',
                    'completed': 'Ваша заявка успешно выполнена.',
                    'rejected': 'К сожалению, ваша заявка была отклонена.'
                }

                message_body = status_messages.get(new_status, 'Статус вашей заявки обновлён.')

                try:
                    send_mail(
                        subject='Обновление статуса вашей заявки',
                        message=message_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client_request.email],
                        fail_silently=False,
                    )
                    messages.success(request, f'Статус заявки обновлен и уведомление отправлено на {client_request.email}')
                except Exception as e:
                    messages.warning(request, f'Статус обновлен, но не удалось отправить email: {str(e)}')

        elif action == 'delete':
            client_request.delete()
            messages.success(request, 'Заявка успешно удалена')
            return redirect('applications')

    return render(request, 'design_studio/request_detail.html', {'request': client_request})



@login_required
def designer_application_detail(request, pk):
    application = get_object_or_404(DesignerApplication, pk=pk)

    if not request.user.is_superuser and application.user != request.user:
        return redirect('applications')

    if request.method == 'POST' and request.user.is_superuser:
        action = request.POST.get('action')

        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in dict(application.STATUS_CHOICES).keys():
                application.status = new_status
                application.save()

                # ✉️ Автоматическое письмо дизайнеру
                status_messages = {
                    'pending': 'Ваша заявка находится на рассмотрении.',
                    'accepted': 'Поздравляем! Ваша заявка принята.',
                    'rejected': 'К сожалению, ваша заявка была отклонена.'
                }
                message = status_messages.get(new_status, 'Статус вашей заявки обновлён.')

                try:
                    send_mail(
                        subject='Обновление статуса вашей заявки',
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[application.email],
                        fail_silently=False
                    )
                except Exception as e:
                    messages.error(request, f'Ошибка при отправке уведомления: {str(e)}')

                messages.success(request, 'Статус заявки обновлён')
        elif action == 'delete':
            application.delete()
            messages.success(request, 'Заявка успешно удалена')
            return redirect('applications')

    return render(request, 'design_studio/designer_application_detail.html', {'application': application})



@login_required
def delete_request(request, pk):
    if request.method == 'POST' and request.user.is_superuser:
        client_request = get_object_or_404(ClientRequest, pk=pk)
        client_request.delete()
        messages.success(request, 'Заявка успешно удалена')
    return redirect('applications')


@login_required
@require_POST
def add_feature(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    icon = request.POST.get('icon')
    order = int(request.POST.get('order', 0))

    if order < 1:
        order = 1

    Feature.objects.filter(order__gte=order).update(order=models.F('order') + 1)
    Feature.objects.create(title=title, description=description, icon=icon, order=order)
    messages.success(request, 'Фича успешно добавлена!')
    return redirect('home')


@login_required
@require_POST
def update_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    feature.title = request.POST.get('title', feature.title)
    feature.description = request.POST.get('description', feature.description)
    icon = request.POST.get('icon')
    if icon:
        feature.icon = icon

    new_order = int(request.POST.get('order', feature.order))
    if new_order != feature.order:
        if new_order < feature.order:
            Feature.objects.filter(order__gte=new_order, order__lt=feature.order).update(order=models.F('order') + 1)
        else:
            Feature.objects.filter(order__gt=feature.order, order__lte=new_order).update(order=models.F('order') - 1)
        feature.order = new_order

    feature.save()
    messages.success(request, 'Фича обновлена успешно!')
    return redirect('home')




@login_required
def delete_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    feature.delete()
    return redirect('home')
