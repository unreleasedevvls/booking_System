from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Room, Booking


def info(request):
    """Стартовая страница с информацией об отеле"""
    return render(request, 'info.html')


def home(request):
    """Страница со списком всех номеров"""
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


def book_room(request):
    """Страница бронирования номера"""
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            room_id = request.POST['room_id']
            check_in = request.POST['check_in']
            check_out = request.POST['check_out']

            room = Room.objects.get(id=room_id)

            # Проверка доступности номера
            if not room.is_available:
                return redirect('book_room')

            # Создаём бронь с данными гостя
            booking = Booking(
                name=name,
                email=email,
                phone=phone,
                room=room,
                check_in=check_in,
                check_out=check_out
            )

            booking.full_clean()  # проверка валидности
            booking.save()        # save обновляет is_available через save() модели

            return redirect('success')

        except ValidationError:
            return redirect('failed')
        except Exception:
            return redirect('failed')

    # GET-запрос — отображаем только доступные номера
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'book.html', {'rooms': rooms})


def success(request):
    """Страница успешного бронирования"""
    return render(request, 'success.html')


def failed(request):
    """Страница ошибки бронирования"""
    return render(request, 'failed.html')


def contacts(request):
    """Страница контактов"""
    return render(request, 'contacts.html')
