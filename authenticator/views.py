from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NameForm
from .models import Client, Estate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy

# for email sending
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def page_not_found(request, exception):
    return render(request, 'authenticator/error.html', status=404)
@login_required
def purge (request):
    logout(request)
    return redirect('browser:index')


# also known as inspect
def register(request):

    try:
        if request.method == "POST":
            # print(f"Post Data: {request.POST}")
            # Retrieve estate id from the form submission
            estate_id = request.POST.get('estate_id')
            # estate adding logic
            if estate_id is not None:
                # print(f"EstateID: {estate_id}")
                try:
                    estate_id = int(estate_id)
                except ValueError:
                    # print(f"Invalid estate_id: {estate_id}")
                    context = {
                        "error": "A Technical Issue Occurred while trying to apply!"
                    }
                    return render(request, 'authenticator/error.html', context)

                # Assuming your NameForm includes a field for the estate ID
                form = NameForm(request.POST, initial={'estate_id': estate_id})
                # Use get_or_create to handle new or existing user
                client, created = Client.objects.get_or_create(
                    username=request.POST.get('username'),
                    password=request.POST.get('password')
                )

                estate = Estate.objects.get(pk=estate_id)

                # prevent client from applying if estate count >=3
                if client.applications.count() >= 3 :
                    context = {
                        'error': f"{client.username} your application was declined, only 3 allowed! "
                    }
                    return render(request, 'authenticator/error.html', context)
                else:
                    client.applications.add(estate)
                    client.save()

                    # Send email to notify admin
                    # subject = 'New Client Registration'
                    # message = f'New client registered:\nName: {client.username}\nPhone Number: {client.password}'
                    # from_email = settings.EMAIL_HOST_USER
                    # to_email = 'viktor.akintola@gmail.com'  # Change this to your admin's email address
                    # send_mail(subject, message, from_email, [to_email])

                    context = {
                        "success": f"{client.username} your application has been submitted successfully, our agent will normally contact you within few minutes "
                    }
                    return render(request, 'authenticator/success.html', context)
                # if form.is_valid():
                #     # Use get_or_create to handle new or existing user
                #     client, created = Client.objects.get_or_create(
                #         username=form.cleaned_data['username'],
                #         password=form.cleaned_data['password'],
                #     )
                #
                #     estate = Estate.objects.get(pk=estate_id)
                #     client.applications.add(estate)
                #     client.save()
                #
                #     if created:
                #         # User was created successfully
                #         return render(request, 'authenticator/success.html')
                #     else:
                #         # User already existed
                #         return render(request, 'authenticator/user_already_exists.html')
                # else:
                #     # Handle form validation errors
                #     context = {'error': 'Form validation failed', 'form': form}
                #     return render(request, 'authenticator/
                #     ion.html', context)
            else:
                # for estate ID problems
                return render(request, 'authenticator/error.html')
        else:
            form = NameForm()
            context = {'form': form}
            return render(request, 'authenticator/inspection.html', context)

    except IntegrityError:
        context = {
            "error": "This phone number already exists in our system!"
        }
        return render(request, 'authenticator/error.html', context)


def client_login(request):

    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']

        user = authenticate(request, username=name, password=password, )

        if user is not None:
            login(request, user)

            if request.user.is_staff:
                return redirect('authenticator:realtor')

            # applied_estates = user.applications.all()
            #
            # print(f"Data: {applied_estates}")
            #
            # context = {
            #     "applied_estates" : applied_estates
            # }
            # # return redirect("authenticator:dashboard")
            return redirect("authenticator:dashboard")
        else:
            context = {
                'error': 'Invalid username or password'
            }
            return render(request, 'authenticator/login.html', context)
    else:
        return render(request, 'authenticator/login.html')

@login_required
def dashboard(request):

    if request.user.is_authenticated:
        applied_estates = request.user.applications.all()

        # print(f"Data: {applied_estates}")

        context = {
            "applied_estates": applied_estates,
            "applied_estates_count": applied_estates.count()
        }
        # return redirect("authenticator:dashboard")
        return render(request, 'authenticator/dashboard.html', context)
    else:
        return redirect("login")

    # return render(request, 'authenticator/dashboard.html')

@staff_member_required(login_url=reverse_lazy('browser:index'))
def view_client_application(request, client_id):
    
    client = Client.objects.get(pk=client_id)
    applied_estates = client.applications.all().order_by("-id")

    print(applied_estates)

    context = {
        "client": client,
        "applied_estates": applied_estates,
        "applied_estates_count": applied_estates.count()
    }

    return render(request, 'authenticator/dashboard.html', context)


def success(request):
    return render(request, 'authenticator/success.html')

@login_required
def delete_estate(request, estate_id):
    # Get the estate object
    estate = get_object_or_404(Estate, pk=estate_id)
    # Remove the estate from the user's applications
    request.user.applications.remove(estate)
    # Redirect back to the dashboard
    return redirect('authenticator:dashboard')

def delete_estate_for_client(request):
    pass

@login_required
@staff_member_required(login_url=reverse_lazy('browser:index'))
def delete_estate_listing(request, estate_id):
    # Get the estate object
    estate = get_object_or_404(Estate, pk=estate_id)
    # Remove the estate from the user's applications
    estate.delete()
    # Redirect back to the dashboard
    return redirect('authenticator:listings')

@login_required
@staff_member_required(login_url=reverse_lazy('browser:index'))
def delete_client(request, client_id):
    #get client
    client = get_object_or_404(Client, pk=client_id)
    client.delete()
    return redirect('authenticator:realtor')


@login_required
@staff_member_required(login_url=reverse_lazy('browser:index'))
def realtor(request):

    applications = Estate.objects.filter(applications__isnull=False)
    clients = Client.objects.all().order_by("-id")
    application_data = []

    for application in applications:

        for client in application.applications.all():
            client_name = client.username
            client_phone = client.password

            # collect all the details for the realtor
            application_details = {
                "estate_title": application.title,
                "client_name": client_name,
                "client_phone": client_phone,
            }

            application_data.append(application_details)

    clients_count = clients.exclude(is_staff=True).count()

    context = {
        "application_data" : application_data,
        "clients" : clients,
        "clients_count": clients_count
    }

    return render(request, 'authenticator/realtor.html', context)

@login_required
@staff_member_required(login_url=reverse_lazy('browser:index'))
def upload_estate(request):
    
    if request.method == "POST":

        print(f"POST DATA: {request.POST}")
        img = request.FILES.get("img")
        img2 = request.FILES.get("img2")
        img3 = request.FILES.get("img3")
        img4 = request.FILES.get("img4")
        title = request.POST["title"]
        desc = request.POST["desc"]
        area = request.POST["area"]
        insp_fee = int(request.POST["insp_fee"])
        agent_fee = int(request.POST["agent_fee"])
        rent_fee = int(request.POST["rent_fee"])
        print(f'Request Data: {type(request.POST["insp_fee"])}')

        Estate.objects.create(
            img=img,
            img2=img2,
            img3=img3,
            img4=img4,
            title=title,
            area=area,
            description = desc,
            inspection_fee=insp_fee,
            agent_fee = agent_fee,
            rental_fee = rent_fee,
        )

        return redirect("authenticator:listings")

    else:
        return render(request, 'authenticator/upload.html')

@login_required
@staff_member_required(login_url=reverse_lazy('browser:index'))
def edit_estate(request, estate_id):

    estate = get_object_or_404 (Estate, pk=estate_id)
    # estates = Estate.objects.all()

    if request.method == "POST":

        # print(f"POST DATA: {request.POST}")
        img = request.FILES.get("img")
        img2 = request.FILES.get("img2")
        img3 = request.FILES.get("img3")
        img4 = request.FILES.get("img4")

        title = request.POST["title"]
        desc = request.POST["description"]
        area = request.POST["area"]
        insp_fee = int(request.POST["insp_fee"])
        agent_fee = int(request.POST["agent_fee"])
        rent_fee = int(request.POST["rent_fee"])

        if img:
            estate.img=img
        if img2:
            estate.img2=img2
        if img3:
            estate.img3=img3
        if img4:
            estate.img4=img4

        estate.title=title
        estate.area = area
        estate.description = desc
        estate.inspection_fee = insp_fee
        estate.agent_fee = agent_fee
        estate.rental_fee = rent_fee

        # save updated records to database
        estate.save()

        return redirect("authenticator:listings")

    else:
        context = {
            "estate": estate
        }
        return render(request, 'authenticator/edit.html', context)

@login_required
@staff_member_required(login_url=reverse_lazy('browser:index'))
def estate_listings(request):
    estates = Estate.objects.all().order_by("-id")

    context = {
        'estates': estates,
        'Welcome': 'You are wired!'
    }
    return render(request, "authenticator/listings.html", context)



