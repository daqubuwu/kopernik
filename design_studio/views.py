from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import ClientRequest, DesignerApplication, Review, CompanyInfo, WorkStage
from .forms import ClientRequestForm, DesignerApplicationForm, LoginForm


def home(request):
    reviews = Review.objects.filter(is_published=True)[:3]
    company_info = CompanyInfo.objects.first()
    return render(request, 'design_studio/home.html', {
        'reviews': reviews,
        'company_info': company_info
    })


def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'design_studio/about.html', {'company_info': company_info})


def workflow(request):
    stages = WorkStage.objects.all().order_by('order')
    return render(request, 'design_studio/workflow.html', {'stages': stages})


def join(request):
    if request.method == 'POST':
        form = DesignerApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_authenticated:
                application.user = request.user
            application.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('applications')
    else:
        form = DesignerApplicationForm()

    return render(request, 'design_studio/join.html', {'form': form})


def order(request):
    if request.method == 'POST':
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            if request.user.is_authenticated:
                request_obj.user = request.user
            request_obj.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
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
    client_requests = ClientRequest.objects.filter(user=request.user)
    designer_applications = DesignerApplication.objects.filter(user=request.user)

    # Если пользователь администратор, показываем все заявки
    if request.user.is_superuser:
        client_requests = ClientRequest.objects.all()
        designer_applications = DesignerApplication.objects.all()

    return render(request, 'design_studio/applications.html', {
        'client_requests': client_requests,
        'designer_applications': designer_applications
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


    if request.method == 'POST' and request.user.is_superuser:
        new_status = request.POST.get('status')
        if new_status in dict(ClientRequest.STATUS_CHOICES).keys():
            client_request.status = new_status
            client_request.save()
            messages.success(request, 'Статус заявки обновлен')
            return redirect('request_detail', request_id=request_id)

    return render(request, 'design_studio/request_detail.html', {
        'request': client_request
    })