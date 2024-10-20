from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Profile, Legal
from orders.models import OrderItem

from .forms import (
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)


from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password in hash
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )



def dashboard(request):
    return render(
        request,
        "account/admin_dashboard.html"
    )


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        },
    )



# def page_not_found(request, exception):
#     return render(request, 'authenticator/error.html', status=404)



def legal (request):
    context = {
        'terms': Legal.objects.all()
    }
    return render(request, 'account/legal.html', context)

def admin_dashboard(request):
    all_orders = OrderItem.objects.all()

    return render(
        request,
        "administrator/admin_dashboard.html",
        context = {
            "all_orders": all_orders,
            "total_orders": all_orders.count()
        }
    )