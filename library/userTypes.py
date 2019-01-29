from flask_login import UserMixin
from abc import ABC, abstractmethod
import copy
import pickle

class User(UserMixin, ABC):
    def __init__(self, email, password, id, name, phone):
        self._id = id
        self._email = email
        self._password = password
        self._name = name
        self._phone = phone
        self._bookings = []
        

    @property
    def bookings(self):
        return self._bookings

    @bookings.setter
    def bookings(self, bookings):
        self._bookings = bookings
    
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email 
    
    @property
    def password(self):
        return self._password 

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name 

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone

    def get_id(self):
        return self._email

    def validate_password(self, password):
        return self._password == password

    @property
    def authorisedUsers(self):
        return self._authorisedUsers

    @authorisedUsers.setter
    def authorisedUsers(self, users):
        self._authorisedUsers = users

    @abstractmethod
    def is_patient(self):
        pass


class Patient(User):

    def __init__(self, email, password, medicare, name, phone, id):     
        User.__init__(self, email, password, id, name, phone)
        self._medicare = medicare
        #users that are allowed to view the history
        #of the patient
        self._authorisedUsers = []
    @property
    def medicare(self):
        return self._medicare
        
    @medicare.setter
    def medicare(self, medicare):
        self._medicare = medicare

    @property
    def bookings(self):
        return self._bookings

    @bookings.setter
    def bookings(self, bookings):
        self._bookings = bookings 

    @property
    def is_patient(self):
        return True

    def __str__(self):
        return "Patient email" + self.email + "patient Password" + self.password \
                + "Patient Name " + self.name
    
    
class Provider(User):
    def __init__(self, email, password, name, profession, phone, id, providerNumber):
        User.__init__(self, email, password, id, name, phone)
        self._profession = profession
        self._rating = {}  
        self._averageRating = 'Unrated'
        self._centres = {}
        self._providerNumber = providerNumber

    @property
    def profession(self):
        return self._profession
        
    @profession.setter
    def profession(self, profession):
        self._profession = profession

    @property
    def providerNumber(self):
        return self._providerNumber
        
    @providerNumber.setter
    def providerNumber(self, NewproviderNumber):
        self._providerNumber = NewproviderNumber

    @property
    def centres(self):
        return self._centres

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        self._rating = rating
        
    @property
    def is_patient(self):
        return False

    @property
    def averageRating(self):
        return self._averageRating
    
    @averageRating.setter
    def averageRating(self, NewRating):
        self._averageRating = NewRating

    def __str__(self):
        return "Provider email " + self._email + " Password " + \
        self._password + " Profession " + self._profession \
        + "Provider Name: " + self._name
  

class HealthCentre():
    def __init__(self, typeOfCentre, ident, name, phone, address, suburb):
        self._typeOfCentre = typeOfCentre
        self._ident = ident
        self._name = name
        self._phone = phone
        self._address = address
        self._suburb = suburb
        self._providers = {}
        self._rating = {} 
        self._averageRating = 'Unrated'

    @property
    def typeOfCentre(self):
        return self._typeOfCentre

    @typeOfCentre.setter
    def typeOfCentre(self, typeOfCentre):
        self._typeOfCentre = typeOfCentre

    @property
    def ident(self):
        return self._ident
    
    @ident.setter
    def ident(self, ident):
        self._ident = ident

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name 

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone 

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def suburb(self):
        return self._suburb

    @suburb.setter
    def suburb(self, suburb):
        self._suburb = suburb 

    @property
    def providers(self):
        return self._providers

    @providers.setter
    def providers(self, providers):
        self._providers = providers 

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        self._rating = rating
        
    @property
    def averageRating(self):
        return self._averageRating
    
    @averageRating.setter
    def averageRating(self, NewRating):
        self._averageRating = NewRating

    def __str__(self):
        return self._name + " " + self._typeOfCentre + " "

class Booking():
    try:
        __id = pickle.load(open("idCounter.p", "rb"))
    
    except:
        __id = 1110

    def __init__(self, time, provider, patient, centre, date):
        self._time = time
        self._date = date
        self._notes = ""
        self._provider = provider
        self._patient = patient 
        self._centre = centre
        self._id = self.getNewID()
        self._completed = False
        self._rated = False

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, provider):
        self._provider = provider

    @property
    def patient(self):
        return self._patient

    @patient.setter
    def patient(self, patient):
        self._patient = patient

    @property
    def centre(self):
        return self._centre

    @centre.setter
    def centre(self, centre):
        self._centre = centre   

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, centre):
        self._id = id

    @property
    def completed(self):
        return self._completed

    def markCompleted(self):
        self._completed = True

    @property
    def rated(self):
        return self._rated

    def isRated(self):
        self._rated = True

    def addANote(self, note):
        self._notes = note

    def getNewID(self):
        Booking.__id+=1
        pickle.dump( Booking.__id, open( "idCounter.p", "wb" ) )  
        return Booking.__id
    