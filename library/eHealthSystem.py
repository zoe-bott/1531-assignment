from library.userTypes import Patient, Provider, HealthCentre, Booking 
from library.errors import BookingError, LoginError, EditError
import csv
import datetime


class eHealthSystem():
    
    def __init__(self):
        self._patients = []
        self._providers = []
        self._centres = []
        self._bookings = {}

    @property
    def patients(self):
        return self._patients
    
    @patients.setter
    def patients(self, patients):
        self._patients = patients

    @property
    def providers(self):
        return self._providers
    
    @providers.setter
    def providers(self, providers):
        self._providers = providers

    @property
    def centres(self):
        return self._centres
    
    @centres.setter
    def centres(self, centres):
        self._centres = centres

    @property
    def bookings(self):
        return self._bookings
    
    @bookings.setter
    def bookings(self, newBooking):
        self._bookings = newBooking

    def populatePatients(self):
        with open("patient.csv", "r") as patient_csv_file:
            for patient in patient_csv_file:
                email, password, name, phone, id, medicare = patient.split(',')
                patient = Patient(email, password, medicare, name.strip(), phone, id.strip())
                self._patients.append(patient)

    def populateProviders(self):
        with open("provider.csv", "r") as provider_csv_file:
            for provider in provider_csv_file:
                email, password, name, profession, phone, id, providerNumber = provider.split(',')
                prov = Provider(email, password, name.strip(), profession.strip(), phone, id.strip(), providerNumber.strip())
                self._providers.append(prov)        
    def populateCentres(self):
        with open("health_centres.csv", "r") as centres_csv_file:
            for centre in centres_csv_file:
                typeOfCentre, ident, name, phone, address, suburb = centre.split(',')
                cen = HealthCentre(typeOfCentre, ident, name, phone, address, suburb.strip())
                self._centres.append(cen)

    def associateCentreAndProvider(self):
        with open("provider_health_centre.csv", "r") as provider_health_csv:
            for line in provider_health_csv:
                line = line.split(',')
                email = line[0]
                name = line[1]
                hours = line[2:]
                for prov in self._providers:    
                    if prov.email.strip() == email.strip():
                        user = prov

                for centre in self._centres:
                    if centre._name.strip() == name.strip():
                        centre._providers[user] = hours
                        user._centres[centre] = hours

    def getCentreWithID(self, ident):
        for centre in self.centres:
            if centre.ident == ident:
                return centre

    def getBookingWithId(self, id):
        for date in self.bookings:
            for booking in self.bookings[date]:
                if str(booking.id) == id:
                    return booking
        

    def makeBooking(self, time, centre, provider, patient, date):
        self._check_date(date)
        print(provider)
        new_booking = Booking(time=time, centre=centre, provider=provider, patient=patient, date=date)
        patient.bookings.append(new_booking)

        provider.bookings.append(new_booking)
        patient.authorisedUsers.append(provider) 
        if (date in self.bookings):
            self.bookings[date].append(new_booking)
        else:
            self.bookings[date]= [new_booking]

        return new_booking

    def _check_date(self, date):
        error = self.check_date_error(date)
        if error:
            raise BookingError(error)
    
    def check_date_error(self, date):
        error = ""
        
        curr_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if (curr_date > date):
            error = "Cannot book an appointment in the past. Choose another date."

        if date == "":
            error = "Please specify a date."

        return error


    def getAvailableHours(self, chosenProvider, centre, date):
        avaiableHours = []
        for provider, hours in (centre.providers).items():
            if provider == chosenProvider:
                for hour in hours:
                    if str(date) not in self.bookings: 
                        avaiableHours.append(hour)
                    elif all((booking.time.strip() != hour.strip() or booking.provider != chosenProvider)for booking in self.bookings[date]):
                        avaiableHours.append(hour)

        return avaiableHours
    
    def searchProviders(self, searchTerm, searchBy):
        results = []
        searchTerm = searchTerm.lower()
        for provider in self.providers:
            name = provider.name.lower()
            
            profession = provider.profession.lower()

            if (searchBy == "name"):
                if (searchTerm in name or searchTerm == ""):
                    results.append(["Provider", provider])
            elif (searchBy == "profession"):
                if (searchTerm in profession or searchTerm == ""):
                    results.append(["Provider", provider])
            else:
                if (searchTerm in profession or searchTerm in name or searchTerm == ""):
                    results.append(["Provider", provider])

        return results
    
    def searchCentres(self, searchTerm, searchBy):
        results = []
        searchTerm = searchTerm.lower()
        for centre in self.centres:
            name = centre.name.lower()
            suburb = centre.suburb.lower()
            if (searchBy == "name"):
                if (searchTerm in name or searchTerm == ""):
                    results.append(["Centre", centre])
            elif (searchBy == "suburb"):
                if (searchTerm in suburb or searchTerm == ""):
                    results.append(["Centre", centre])
            else:
                if (searchTerm in suburb or searchTerm in name or searchTerm == ""):
                    results.append(["Centre", centre])
        return results
    
    def addRating(self, element, new_rating, user):
        element.rating[user.email] = new_rating
        average = 0
        for i in element.rating:
            average += element.rating[i]
        average = average/len(element.rating)
        element.averageRating = average


    def check_password(self, email, password):
        self._check_login(email, password)

        for patient in self.patients:
            if patient.email == email and patient.password == password:
                return patient
        for provider in self.providers:
            if provider.email == email and provider.password == password:
                return provider
        return None

    def _check_login(self, email, password):
        errors = self.check_login_error(email, password)

        if errors:
            raise LoginError(errors)

    def check_login_error(self, email, password):
        errors = {}

        if not email:
            errors['email'] = "Email is empty"
        if not password:
            errors['password'] = "Password is empty"

        return errors

    
    def get_user(self, email):
        for patient in self._patients:
            if patient.email == email:
                return patient
        for prov in self._providers:
            if prov.email == email:
                return prov
        return None

    def get_user_byName(self, name):
        for patient in self._patients:
            if patient.name == name:
                return patient
        for prov in self._providers:
            if prov.name == name:
                return prov
        return None

    def editDetails(self, user, name, email, phone):
        self._check_new_details(user, name, email, phone)

        user.name = name
        user.email = email
        user.phone = phone

    def _check_new_details(self, user, name, email, phone):
        errors = self.check_new_detail_errors(user, name, email, phone)

        if errors:
            raise EditError(errors)

    def check_new_detail_errors(self, user, name, email, phone):
        errors = {}

        if not name:
            errors['name'] = "Please enter a valid name."
        if not email:
            errors['email'] = "Please enter a valid email."
        if not phone:
            errors['phone'] = "Please enter a valid phone."

        return errors

    def setUp(self):
        self.populatePatients()
        self.populateProviders()
        self.populateCentres()
        self.associateCentreAndProvider()