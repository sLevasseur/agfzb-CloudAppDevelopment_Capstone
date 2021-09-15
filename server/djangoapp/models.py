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
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Dealer address
        self.dealership = dealership
        # Dealer city
        self.name = name
        # Dealer Full Name
        self.purchase = purchase
        # Dealer id
        self.review = review
        # Location lat
        self.purchase_date = purchase_date
        # Location long
        self.car_make = car_make
        # Dealer short name
        self.car_model = car_model
        # Dealer state
        self.car_year = car_year
        # Dealer zip
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review : " + self.review