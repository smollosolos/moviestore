from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, get_user_model
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
        
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST,  error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})

User = get_user_model()
@staff_member_required
def top_purchasers_view(request):
    list_size = request.GET.get('limit', None)
    users = User.objects.annotate(purchase_count=Count('order')).order_by('-purchase_count')
    if list_size:
        try:
            limit = int (list_size)
            if limit > 0:
                users = users[:limit]
        except ValueError:
            pass

    context = {
        'users':users,
        'list_size':list_size or ''
    }
    return render(request, 'accounts/top_purchasers.html', context)
