from django.contrib import admin
from .models import Room, Booking

# ---------------- Room ----------------
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'type', 'price', 'capacity', 'is_available']
    list_filter = ['type', 'is_available']
    search_fields = ['number', 'type']

# ---------------- Booking ----------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'room', 'check_in', 'check_out', 'created_at']
    list_filter = ['room', 'check_in', 'check_out']
    search_fields = ['name', 'email', 'phone']
    
    def delete_queryset(self, request, queryset):
        """Массовое удаление"""
        for obj in queryset:
            self.delete_model(request, obj)

    def delete_model(self, request, obj):
        """Удаление одного объекта"""
        room = obj.room
        obj.delete()
        
        # Проверяем оставшиеся брони
        from django.utils import timezone
        active_bookings = Booking.objects.filter(
            room=room, 
            check_out__gte=timezone.now().date()
        )
        
        if not active_bookings.exists():
            room.is_available = True
            room.save()