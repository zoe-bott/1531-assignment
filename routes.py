from library.userTypes import Patient, Provider, HealthCentre, Booking
from flask import Flask, render_template, request, abort, redirect, Response ,url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from server import app 
from library.eHealthSystem import eHealthSystem 
from library.errors import BookingError, LoginError, EditError
import copy
import pickle
from functools import wraps


#check for persistence pickle data
#otherwise load data from the CSV files

try:
    healthSystem = pickle.load(open("saved_data.p", "rb"))
except:
    healthSystem = eHealthSystem()
    healthSystem.setUp()
 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(email):
    return healthSystem.get_user(email)


def carer_required(function):
    @wraps(function)
    def wrapper_function(*args, **kwargs):
        user = healthSystem.get_user_byName(current_user.name)
        if user.is_patient != True: #we are a provider
            return function(*args, **kwargs)
        return redirect(url_for("home"))
    return wrapper_function     #in a state ready to execute

def patient_required(function):     
    @wraps(function)
    def wrapper_function(*args, **kwargs):
        user = healthSystem.get_user_byName(current_user.name)
        if user.is_patient: #we are a patient
            return function(*args, **kwargs)
        return redirect(url_for("home"))
    return wrapper_function

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = healthSystem.check_password(email, password) 
        except LoginError as le:
            return render_template("login.html", errors=le.errors)

        if user != None:
            if user.is_patient:
                login_user(user)#patient  
                return redirect(url_for("home", email=email))
            else:
                login_user(user)#provider
                return redirect(url_for("home", email=email))
        
        return render_template("login.html", errors={'email':'Not a valid email/password'})   

    return render_template("login.html") 
    
@app.route("/home")
@login_required
def home():
    pickle.dump( healthSystem, open( "saved_data.p", "wb" ) )
    return render_template("home.html", user=current_user)   
        
@app.route("/patient/profile/<email>")
@login_required
def patient_profile(email):
    patient = healthSystem.get_user(email)
    if patient.is_patient:
        if current_user == patient or current_user in patient.authorisedUsers:
            return render_template("patientProfile.html", patient=patient, user=current_user)
    return redirect(url_for('index'))

@app.route("/provider/profile/<email>")
@login_required
def provider_profile(email):
    provider = healthSystem.get_user(email)
    if not provider.is_patient:
        return render_template("providerProfile.html", provider=provider, user=current_user)
    return redirect(url_for('index'))

@app.route('/editProfile/<email>', methods=["GET", "POST"])
@login_required
def edit_profile(email):
    user = healthSystem.get_user(email)

    if user == current_user:
        if request.method == "POST":
            name = request.form["name"] 
            email = request.form["email"]
            phone = request.form["phone"]

            try:
                healthSystem.editDetails(user, name, email, phone)
            except EditError as ee:
                return render_template("editProfile.html", user=current_user, errors=ee.errors)

            if user.is_patient:
                login_user(user)
                return redirect(url_for('patient_profile', email=user.email))
            else:
                login_user(user)
                return redirect(url_for('provider_profile', email=user.email))
        return render_template("editProfile.html", user=current_user)
    return redirect(url_for('index'))

@app.route("/centre/<id>")
@login_required
def centre_profile(id):
    centre = healthSystem.getCentreWithID(id)       
    return render_template("centreProfile.html", centre=centre, user = current_user)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search', methods = ['GET','POST'])
@login_required
@patient_required
def search():
    results = []
    if request.method == 'POST':
        searchTerm = request.form['search']
        searchFor = request.form['searchFor']
        searchBy = request.form['searchBy']
        
        if (searchFor == 'provider'):
            results = healthSystem.searchProviders(searchTerm, searchBy)
        elif(searchFor == 'centre'):
            results = healthSystem.searchCentres(searchTerm, searchBy)
        else:
            results = healthSystem.searchProviders(searchTerm, searchBy)
            results += (healthSystem.searchCentres(searchTerm, searchBy))
        if searchTerm == "":
            searchTerm = "All"
        return render_template("search.html", searchTerm=searchTerm, showResults=True, results=results,user=current_user)
    return render_template("search.html",user=current_user)


@app.route('/makeBooking/<centreID>', methods = ['GET','POST'])
@login_required
@patient_required
def makeBooking(centreID):
    
    centre = healthSystem.getCentreWithID(centreID)
    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'form1':
            providerString = request.form['provider']
            provider = healthSystem.get_user_byName(providerString)
            return render_template('makeABooking.html', centre=centre, healthSystem=healthSystem, providerSelected=True, chosenProvider=provider, user=current_user)
        elif form_name == 'form2':
            providerString = request.form['provider']
            provider = healthSystem.get_user_byName(providerString)
            date = request.form['date']
            hours = healthSystem.getAvailableHours(provider, centre, date)
            
            return render_template('makeABooking.html', centre=centre,  healthSystem=healthSystem, providerSelected=True, chosenProvider=provider, dateSelected=True, hours=hours, user=current_user, date=date)
        else:              
            providerString = request.form['provider']

            provider = healthSystem.get_user_byName(providerString)
  
            time = request.form['time']
            date = request.form['date']
            patient = copy.copy(current_user)
            try:
                booking = healthSystem.makeBooking(time, centre, provider, patient, date)
            except BookingError as be:
                return render_template('makeABooking.html', centre=centre, healthSystem=healthSystem, providerSelected=True, chosenProvider=provider, user=current_user, error=be.error)

            #update saved_data file
            pickle.dump( healthSystem, open( "saved_data.p", "wb" ) )
            
            return render_template('bookingSuccess.html', booking=booking, user=current_user)
    return render_template('makeABooking.html', centre=centre, healthSystem=healthSystem, providerSelected=False, user=current_user) 

def getkey(booking):
    return booking.date

@app.route('/viewBookings')
@login_required
def viewBookings():
    print(current_user.bookings)
    current_user.bookings = sorted(current_user.bookings, key=getkey)
    return render_template('viewBookings.html', user=current_user)



@app.route('/viewABooking/<bookingID>', methods=['POST', 'GET'])
@login_required
def viewABooking(bookingID):
    
    booking = healthSystem.getBookingWithId(bookingID)
    print(booking.patient.authorisedUsers)
    if current_user in booking.patient.authorisedUsers or current_user == booking.patient:
        if request.method == "POST":
            form = request.form['form-name']
            if form == "notesForm":
                booking.markCompleted()
                notes = request.form['notes']
                booking.addANote(notes)
            else:
                centreRating = int(request.form['centreRating'])
                providerRating = int(request.form['providerRating'])
                
                healthSystem.addRating(booking.provider, providerRating, current_user)
                healthSystem.addRating(booking.centre, centreRating, current_user)
                
                booking.isRated()
                pickle.dump( healthSystem, open( "saved_data.p", "wb" ) )
        return render_template('viewABooking.html', user=current_user, booking=booking)
    return redirect(url_for('index'))




