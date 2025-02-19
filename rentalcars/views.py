from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, UserLoginForm, BookingForm
from .models import Car
import razorpay
from django.conf import settings
from django.http import  HttpResponse
from .models import Booking
import logging




# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# Home view (Show all available cars)
def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars})

# Booking view
def book_car(request, car_id):
    car = Car.objects.get(id=car_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.total_price = (booking.return_date - booking.rental_date).days * car.price_per_day
            booking.save()
            return redirect('payment', booking.id)
    else:
        form = BookingForm(initial={'car': car})
    return render(request, 'book_car.html', {'form': form, 'car': car})

# Razorpay payment view
@csrf_exempt


def payment(request, booking_id):
    try:
        # Retrieve the booking object based on booking_id
        booking = Booking.objects.get(id=booking_id)

        # Convert amount to paise (Razorpay expects the amount in paise)
        amount = int(booking.total_price * 100)  # Convert to paise

        # Initialize the Razorpay client with your credentials
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create an order with Razorpay
        order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        })

        # Store the Razorpay order ID in the booking record
        booking.payment_order_id = order['id']  # Save the Razorpay order ID in the booking
        booking.save()  # Save the updated booking with the Razorpay order ID

        # Prepare the context to pass to the template
        context = {
            'booking': booking,
            'order_id': order['id'],
            'amount': amount,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        }

        return render(request, 'payment.html', context)

    except Booking.DoesNotExist:
        return HttpResponse("Booking not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def search(request):
    query = request.GET.get('query', '')
    if query:
        cars = Car.objects.filter(name__icontains=query)  # Filters cars by name
    else:
        cars = Car.objects.all()  # If no query, show all cars

    return render(request, 'search.html', {'cars': cars, 'query': query})



# Razorpay client setup
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt

# Payment Success view
def payment_success(request):
    try:
        # Extract Razorpay order ID from request
        razorpay_order_id = request.POST.get('razorpay_order_id')
        # Try to get the booking related to the order ID
        booking = Booking.objects.get(payment_order_id=razorpay_order_id)
        logger = logging.getLogger(__name__)
        razorpay_order_id = request.POST.get('razorpay_order_id')
        logger.debug(f"Received Razorpay order ID: {razorpay_order_id}")

        # Render the success template and pass the booking object
        return render(request, 'payment_success.html', {'booking': booking})

    except Booking.DoesNotExist:
        return HttpResponse(f"Booking with Razorpay order ID {razorpay_order_id} not found.")
    except Exception as e:
        return HttpResponse(f"Payment verification failed: {str(e)}")

