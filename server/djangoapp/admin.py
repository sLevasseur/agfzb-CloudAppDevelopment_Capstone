from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 10
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ('car_make', 'name', 'dealer_id', 'type', 'year')
    search_fields = ['year', 'name', 'type']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    fields = ["name", "date_created"]
    search_fields=["name"]


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)