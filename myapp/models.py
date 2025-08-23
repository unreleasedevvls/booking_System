from django.db import models

class Room(models.Model):
    number = models.CharField('Номер комнаты', max_length=10)
    type = models.CharField('Тип номера', max_length=50)
    price = models.IntegerField("Цена за ночь")
    capacity = models.IntegerField('Вместимость')
    is_available = models.BooleanField("Доступен", default = True)

    def __str__(self):
        return f"номер {self.number} ({self.type})"
    
class Guest(models.Model):
    name = models.CharField('Имя Гостя' , max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Phone number", max_length= 20 )
    
    def __str__(self):
        return self.name
    
class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name='Гость')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Номер")
    check_in = models.DateField("Дата заезда")
    check_out = models.DateField("Дата выезда")
    created = models.DateTimeField("Дата брони", auto_now_add=True)

    def __str__(self):
        return f"Бронь {self.id} - {self.guest.name}"