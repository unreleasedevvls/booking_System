from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Room(models.Model):
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"№{self.number} ({self.type})"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Unknown Guest')
    email = models.EmailField(default='unknown@example.com')
    phone = models.CharField(max_length=20, default='000-000-0000')
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.pk:  # Новая бронь
            self.room.is_available = False
            self.room.save()
        else:
            # При изменении существующей брони
            old_booking = Booking.objects.get(pk=self.pk)
            if old_booking.room != self.room:
                old_booking.room.is_available = True
                old_booking.room.save()
                self.room.is_available = False
                self.room.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Бронь №{self.id} - {self.room.number} ({self.name})"

# Сигнал который срабатывает после удаления брони
@receiver(post_delete, sender=Booking)
def update_room_availability(sender, instance, **kwargs):
    """Обновляет статус комнаты после удаления брони"""
    room = instance.room
    
    # Проверяем, есть ли другие активные брони на эту комнату
    active_bookings = Booking.objects.filter(
        room=room, 
        check_out__gte=timezone.now().date()
    )
    
    if not active_bookings.exists():
        room.is_available = True
        room.save()
    else:
        room.is_available = False
        room.save()