from django.db import models
from django.utils.timezone import now



# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return f' {self.name} : {self.description}'

class CarModel(models.Model):
    SUV = "SUV"
    SEDAN = "Sedan"
    WAGON = "Wagon"
    PEUGEOT = "Peugeot"
    MODEL_CHOICES = [
        (SUV, 'Suv'),
        (SEDAN, 'Sedan'),
        (WAGON, 'Wagon'),
        (PEUGEOT, 'Peugeot'),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealer_id = models.IntegerField(help_text='refers to a dealer created in Cloudant database')
    type = models.CharField(max_length=8, choices=MODEL_CHOICES, default=SUV)
    year = models.DateField()

    def __str__(self):
        return f'{self.car_make.name} from dealer number {self.dealer_id}\
            is a {self.type} from {self.year}'

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
