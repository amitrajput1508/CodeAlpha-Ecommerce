from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def checkout(request):
    return render(request, 'checkout.html', {
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY
    })

@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            amount = 5000  # amount in cents
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )
            return JsonResponse({'clientSecret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def payment_success(request):
    return render(request, 'payment_success.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('index')  # Redirect to a success page or home page
        else:
            messages.error(request, 'There was an error with your signup. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'shop/signup.html', {'form': form})

def index(request):
    return render(request, 'shop/index.html')

def shop(request):
    return render(request, 'shop/shop.html')

def sproduct(request):
    return render(request, 'shop/sproduct.html')

def blog(request):
    return render(request, 'shop/blog.html')

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def cart(request):
    return render(request, 'shop/cart.html')

def spro1(request):
    return render(request, 'shop/spro1.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('index')  # Redirect to the home page or dashboard
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'shop/login.html', {'form': form})
