from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Room, Booking
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required




def logout_view(request):
    logout(request)
    return redirect('signup')

# Стартовая страница
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return signup(request)

# Регистрация
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# Страница с информацией — защищена логином
@login_required(login_url='/accounts/signup/')
def home(request):
    return render(request, 'home.html')

# Список номеров
@login_required(login_url='/accounts/signup/')
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

# Бронирование
from datetime import date

@login_required(login_url='/accounts/signup/')
def book_room(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            room_id = request.POST['room_id']
            check_in = request.POST['check_in']
            check_out = request.POST['check_out']

            # Преобразуем строки в объекты даты
            check_in_date = date.fromisoformat(check_in)
            check_out_date = date.fromisoformat(check_out)

            # Проверяем, что даты не раньше сегодняшнего дня
            today = date.today()
            if check_in_date < today or check_out_date < today:
                # Ошибка: нельзя бронировать на прошедшие даты
                return redirect('failed')

            # Проверяем, что заезд раньше выезда
            if check_in_date >= check_out_date:
                return redirect('failed')

            room = Room.objects.get(id=room_id)

            if not room.is_available:
                return redirect('book_room')

            booking = Booking(
                name=name,
                email=email,
                phone=phone,
                room=room,
                check_in=check_in_date,
                check_out=check_out_date
            )

            booking.full_clean()
            booking.save()
            return redirect('success')

        except ValidationError:
            return redirect('failed')
        except Exception:
            return redirect('failed')

    rooms = Room.objects.filter(is_available=True)
    return render(request, 'book.html', {'rooms': rooms})


# Успешное бронирование
@login_required(login_url='/accounts/signup/')
def success(request):
    return render(request, 'success.html')

# Ошибка бронирования
@login_required(login_url='/accounts/signup/')
def failed(request):
    return render(request, 'failed.html')

# Контакты
def contacts(request):
    return render(request, 'contacts.html')

# Кастомный logout, который гарантированно чистит сессию
def custom_logout(request):
    logout(request)
    return redirect('signup')
