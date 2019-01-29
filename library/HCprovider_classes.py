from enum import Enum
#do my enum variables need an underscore? 
class Professions(Enum):
    GENERAL_PRACTITIONER = 1
    PHARMACIST = 2
    PHYSIOTHERAPIST = 3
    PATHOLOGIST = 4

#print(Professions.PHARMACIST)
class HealthCareProvider (object):
    def __init__(self, profession, firstname, surname, email, phoneNum, providerNum, hours='N/A', rating= 'N/A'):
        self._profession = profession
        self._rating = rating
        self._hours = hours
        self._first_name = firstname
        self._surname = surname
        self._email = email
        self._phoneNum = phoneNum
        self._providerNum = int(providerNum)
        self._affiliatedCentres = ["Centre1", "Centre2", "Centre3"]
        


    @property
    def profession(self):
        return self._profession
        
    @profession.setter
    def profession(self, profession):
        self._profession = profession     


    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        self._rating = rating


    @property
    def hours(self):
        return self._hours
    @hours.setter
    def hours(self, hours):
        self._hours = hours

    @property
    def firstname(self):
        return self._firstname
    
    @firstname.setter
    def firstname(self, firstname):
        self._firstname = firstname

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, surname):
        self._surname = surname

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email
    @property
    def phoneNum(self):
        return self._phoneNum

    @phoneNum.setter
    def phoneNum(self, phoneNum):
        self._phoneNum = phoneNum
    @property
    def providerNum(self):
        return self._providerNum
    @providerNum.setter
    def providerNum (self, providerNum):
        self._providerNum = providerNum

    def add_HCCentre (self, centre):
        self._affiliatedCentres.append(centre)
    
    def __str__ (self):
        return (self._profession + ' ' +
        self._first_name + ' ' +
        self._surname + ' ' +
        self._email + ' ' +
        self._phoneNum + ' ' +
        str(self._providerNum) + ' ' +
        self._hours + ' ' +
        self._rating + ' ' +
        ' '.join(map(lambda x: ' ' + str(x), self._affiliatedCentres)))
class HealthCareCentre (object):
    pass

a = HealthCareProvider('Pharmacist', 'Bob', 'Jones', '123@gmail.com', '041212212', '55')
a.add_HCCentre("Blackwattle bay")

print(a)