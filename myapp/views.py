from django.shortcuts import render, redirect
from .models import Room, Guest, Booking

def home(request):
    return render(request, 'home.html')

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

def book_room(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        room_id = request.POST['room_id']
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        
        guest = Guest.objects.create(
            name=name,
            email=email,
            phone=phone
        )
        
        Booking.objects.create(
            guest=guest,
            room_id=room_id,
            check_in=check_in,
            check_out=check_out
        )
        
        return redirect('success')
    
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'book.html', {'rooms': rooms})

def success(request):
    return render(request, 'success.html')