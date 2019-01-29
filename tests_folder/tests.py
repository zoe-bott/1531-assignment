import pytest
import sys
sys.path.append('../')
from library.eHealthSystem import *
from library.userTypes import *
from routes import healthSystem
import os



    
class TestMakeBooking (object):
    def setup_method(self): #setup method resets the persistence on the server each time a test is called
                                #for more straightforward testing
        healthSystem.patients = []    
        healthSystem.providers = [] 
        healthSystem.centres = []     
        healthSystem.bookings.clear()
        healthSystem.setUp()  

    def test_makevalidbooking(self):

        provider = healthSystem.get_user_byName("Toby Morgan") #Toby Morgan
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am

        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)
        
        assert(booking1.time == "9:00am")
        assert(booking1.provider.name == "Toby Morgan")
        assert(booking1.date == "2018-11-25")

    def test_invalid_booking_in_past(self):

        provider = healthSystem.get_user_byName("Toby Morgan") #Toby Morgan
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-05-05"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am

        try:
            booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)
        except BookingError as be:
            assert(be.error == "Cannot book an appointment in the past. Choose another date.")
        else:
            assert(False)

    def test_availableHours(self):

        provider = healthSystem.get_user_byName("Toby Morgan") #Toby Morgan
        centre = healthSystem.getCentreWithID("1111") #Sydney Childrens Hospital
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am
        AvailableHoursBookedProvider = len(healthSystem.getAvailableHours(provider,centre,date))
        otherProvider = healthSystem.get_user_byName("Anna Azzam") 
        AvailableHoursOtherProvider = len(healthSystem.getAvailableHours(otherProvider,centre,date)) 
        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)
        
        assert(booking1.time == "9:00am")
        assert(booking1.provider.name == "Toby Morgan")
        assert(booking1.date == "2018-11-25")
        assert((len(healthSystem.getAvailableHours(provider,centre,date))) == (AvailableHoursBookedProvider-1)) 
        #asserts that the available hours of this provider has gone down by 1
        assert(len(healthSystem.getAvailableHours(otherProvider, centre, date)) == AvailableHoursOtherProvider)
        #asserts that another providers hours have not gone down aswell


class TestsViewPatientHistory (object):
    def setup_method(self):
        healthSystem.patients = []    
        healthSystem.providers = [] 
        healthSystem.centres = []     
        healthSystem.bookings.clear()
        healthSystem.setUp()   

    def test_patient_authorised_list(self):
        provider = healthSystem.get_user_byName("Toby Morgan")
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am
        notes = "Jack is going to die"
        assert(len(patient.bookings) == 0)

        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)
        booking1.addANote(notes)



        provider = healthSystem.get_user_byName("Anna Azzam")
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0]
        notes = "Jack is looking pretty good"

        booking2 = healthSystem.makeBooking(time, centre, provider, patient, date)
        booking2.addANote(notes)


        assert(patient.authorisedUsers == [healthSystem.get_user_byName("Toby Morgan"), healthSystem.get_user_byName("Anna Azzam")])


    def test_bookingHistoryBeforeAppointment(self):
        provider = healthSystem.get_user_byName("Toby Morgan")
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am
        notes = "Jack is going to die"

        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)
        assert(booking1.completed == False)


    def test_bookingHistoryAfterAppointment(self):
        provider = healthSystem.get_user_byName("Toby Morgan")
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am
        notes = "Jack is going to die"

        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)
        assert(booking1.completed == False)
        booking1.markCompleted()
        assert(booking1.completed == True)
        
        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)

    def test_patient_booking_history(self):
        provider = healthSystem.get_user_byName("Toby Morgan")
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am
        notes = "Jack is going to die"

        assert(len(patient.bookings) == 0)

        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)
        booking1.addANote(notes)



        assert(len(patient.bookings) == 1)
        assert(patient.bookings[0].date == "2018-11-25")
        assert(patient.bookings[0].provider == provider)
        assert(patient.bookings[0].notes == "Jack is going to die")
        
        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)



    def test_viewNotes(self):
        provider = healthSystem.get_user_byName("Toby Morgan")
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am
        notes = "Jack is going to die"
        
        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)

        booking1.addANote(notes)
        assert(booking1.notes == "Jack is going to die")

    def test_view_all_notes(self):
        provider = healthSystem.get_user_byName("Toby Morgan")
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am
        notes = "Jack is going to die..."
        
        booking1 = healthSystem.makeBooking(time, centre, provider, patient, date)
        booking1.addANote(notes)

        provider = healthSystem.get_user_byName("Anna Azzam")
        centre = healthSystem.getCentreWithID("1111")
        patient = healthSystem.get_user("jack@gmail.com")
        date = "2018-11-25"
        time = healthSystem.getAvailableHours(provider, centre, date)[0] #9:00am
        notes = "if he doesn't take a panadol right now"
        booking2 = healthSystem.makeBooking(time, centre, provider, patient, date)
        booking2.addANote(notes)
        
        allpatientnotes = "" 
        for abooking in patient.bookings:
            allpatientnotes = allpatientnotes + abooking.notes
        assert(allpatientnotes == "Jack is going to die...if he doesn't take a panadol right now")


    #Test if the patient has made a booking with that specific person - are they authorised
    #If you book an appointment does it show up in the patient history
    # 
test = TestsViewPatientHistory()
#test.test_patient_authorised_list()
test.setup_method()

class TestManageProviderHistory(object):
    def setup_method(self):
        healthSystem.patients = []    
        healthSystem.providers = [] 
        healthSystem.centres = []     
        healthSystem.bookings.clear()
        healthSystem.setUp()   


    def test_change_details_provider(self):
        provider = healthSystem.get_user_byName("Anna Azzam")
        assert(provider.name == "Anna Azzam")
        assert(provider.email == "anna@gmail.com")
        assert(provider.phone == "0412 009 200")

        healthSystem.editDetails(provider, "Dom Latouche", "Mechanicsgod@gmail.com", "0419 243 333")
        assert(provider.name == "Dom Latouche")
        assert(provider.email == "Mechanicsgod@gmail.com")
        assert(provider.phone == "0419 243 333")


    def test_change_details_provider_email_empty(self):
        provider = healthSystem.get_user_byName("Anna Azzam")
        assert(provider.name == "Anna Azzam")
        assert(provider.email == "anna@gmail.com")
        assert(provider.phone == "0412 009 200")



        try:
            healthSystem.editDetails(provider, "", "owen@gmail.com", "1231 231 123")
        except EditError as ee:
            assert (ee.errors["name"] == "Please enter a valid name.")
            assert(provider.name == "Anna Azzam")
            assert(provider.email == "anna@gmail.com")
            assert(provider.phone == "0412 009 200")

        else:
            assert(false)


    def test_change_details_provider_email_empty(self):
        provider = healthSystem.get_user_byName("Anna Azzam")
        assert(provider.name == "Anna Azzam")
        assert(provider.email == "anna@gmail.com")
        assert(provider.phone == "0412 009 200")



        try:
            healthSystem.editDetails(provider, "Owen Silver", "", "1231 231 123")
        except EditError as ee:
            assert (ee.errors["email"] == "Please enter a valid email.")
            assert(provider.name == "Anna Azzam")
            assert(provider.email == "anna@gmail.com")
            assert(provider.phone == "0412 009 200")

        else:
            assert(false)

    def test_change_details_provider_phone_empty(self):
        provider = healthSystem.get_user_byName("Anna Azzam")
        assert(provider.name == "Anna Azzam")
        assert(provider.email == "anna@gmail.com")
        assert(provider.phone == "0412 009 200")



        try:
            healthSystem.editDetails(provider, "Owen Silver", "dozam8noh8@gmail.com", "")
        except EditError as ee:
            assert (ee.errors["phone"] == "Please enter a valid phone.")
            assert(provider.name == "Anna Azzam")
            assert(provider.email == "anna@gmail.com")
            assert(provider.phone == "0412 009 200")

        else:
            assert(false)

    def test_change_details_patients(self):
        patient = healthSystem.get_user("jack@gmail.com")
        assert(patient.name == "Jack Bilby")
        assert(patient.email == "jack@gmail.com")
        assert(patient.phone == "0420 008 080")



        healthSystem.editDetails(patient, "Owen Silver", "dozam8noh8@gmail.com", "0427 169 346")

        assert(patient.name == "Owen Silver")
        assert(patient.email == "dozam8noh8@gmail.com")
        assert(patient.phone == "0427 169 346")

    def test_change_details_patients_name_empty(self):
        patient = healthSystem.get_user("jack@gmail.com")
        assert(patient.name == "Jack Bilby")
        assert(patient.email == "jack@gmail.com")
        assert(patient.phone == "0420 008 080")


        try:
            healthSystem.editDetails(patient, "", "dozam8noh8@gmail.com", "0427 169 346")
        except EditError as ee:
            assert (ee.errors["name"] == "Please enter a valid name.")
            assert(patient.name == "Jack Bilby")
            assert(patient.email == "jack@gmail.com")
            assert(patient.phone == "0420 008 080")
        else:
            assert(false)

    def test_change_details_patients_email_empty(self):
        patient = healthSystem.get_user("jack@gmail.com")
        assert(patient.name == "Jack Bilby")
        assert(patient.email == "jack@gmail.com")
        assert(patient.phone == "0420 008 080")


        try:
            healthSystem.editDetails(patient, "Owen Silver", "", "0427 169 346")
        except EditError as ee:
            assert (ee.errors["email"] == "Please enter a valid email.")
            assert(patient.name == "Jack Bilby")
            assert(patient.email == "jack@gmail.com")
            assert(patient.phone == "0420 008 080")
        else:
            assert(false)

    def test_change_details_patients_phone_empty(self):
        patient = healthSystem.get_user("jack@gmail.com")
        assert(patient.name == "Jack Bilby")
        assert(patient.email == "jack@gmail.com")
        assert(patient.phone == "0420 008 080")


        try:
            healthSystem.editDetails(patient, "Owen Silver", "dozam8noh8@gmail.com", "")
        except EditError as ee:
            assert (ee.errors["phone"] == "Please enter a valid phone.")
            assert(patient.name == "Jack Bilby")
            assert(patient.email == "jack@gmail.com")
            assert(patient.phone == "0420 008 080")
        else:
            assert(false)

