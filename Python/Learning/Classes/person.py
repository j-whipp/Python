#Create a class named Person, with firstname and lastname properties, and a printname method:
#remember self is a reference to the current instance of the class and is used to access variables that belong to the class

class Person:
    #now define the __init__() function which instantiates an instance of the class Person with attributes firstname,lastname
    def __init__(self, firstname,lastname):
        self.firstname = firstname
        self.lastname = lastname

    def printname(self):
        print("The creature's name is {} {}".format(self.firstname,self.lastname))

#to create a child class that inherits the funcitonality from another class, send the parent class a paremeter when creating the child class
class Species(Person):
    def __init__(self,firstname,lastname,species):
        #to preserve the inheritance of the parent class we need to add a call to the parents __init__() function
        Person.__init__(self, firstname,lastname)
        self.species = species
    def printinfo(self):
        print("The creature's name is {} {} and is of the species:{}".format(self.firstname,self.lastname,self.species))