import calendar
import datetime

class Homework:

    def __init__(self, name, percentage_in_1hr=0, percentage_completed=0):
        self.name = name
        self.percentage_in_1hr = percentage_in_1hr
        self.percentage_completed = percentage_completed
        self.missing_per = 100
        self.date = "unknown"

    def set_date(self, date):
        self.date = date
    def set_percentage_in_1hr(self, new_per):
        self.percentage_in_1hr = new_per
    def set_completed(self, completed):
        self.percentage_completed = completed
        self.missing_per = 100 - completed
        
    def get_name(self):
        return self.name
    def get_percentage(self):
        return self.percentage_in_1hr
    def get_missing_per(self):
        return self.missing_per
    def get_time_to_finish(self):
        if self.percentage_in_1hr == 0:
            return 0
        else:
            return (self.missing_per/self.percentage_in_1hr)
    def get_completed(self):
        return self.percentage_completed
    def get_date(self):
        return self.date

#class Hw_list:
#
#    def __init__(self, *args):
#        self.list = []
#        for i in args:
#            self.list.append(args[i])
#    def add_hw(self, new_hw):
#        self.list.append(new_hw)
#    def complete_hw(self):
#        pass
#    def print_list(self):
#        items = len(self.list)
#        names = []
#        for i in range(items):
#            names = self.list[i].get_name()
#        return names

class Subject:

    def __init__(self, name):
        self.name = name
        self.hw_list = []
    def add_hw(self, new_hw):
        self.hw_list.append(new_hw)
    def print_hw_list(self):
        items = len(self.hw_list)
        names = []
        for i in range(items):
            print("     " + self.hw_list[i].get_name()
            + " {0}{1}".format(self.hw_list[i].get_completed(), "%")
            + " | % to finish: {0}{1}".format(self.hw_list[i].get_missing_per(), "%")
            + " time to finish: {0}".format(decimal_to_time(self.hw_list[i].get_time_to_finish()))
            + " | delivery: {0}".format(self.hw_list[i].get_date()))
    def get_name(self):
        return self.name


class Work_type:
    
    def __init__(self):
        self.categories = []
    def set_sub_category(self, sub_cat_name):
        self.categories.append(sub_cat_name)
    def get_sub_category(self, index):
        return self.categories[index]


#..........................................................
#..........................................................
#..........................................................
#..........................................................
#..........................................................
#..........................................................
#..........................................................

def decimal_to_time(value):
    hours = int(value)
    decimales = value - int(value)
    minutes = decimales * 60
    return str(hours) + " horas" + " " + str(minutes) + " minutos"

def print_assignments(subjects):
    for i in range(len(subjects)):
        print("")
        print(subjects[i].get_name())
        subjects[i].print_hw_list()
    print("")

escuela = Work_type()
cimb = Work_type()
personal = Work_type()

circuitosII = Subject("Circuitos Eléctricos II")
electronica = Subject("Electrónica")
flc = Subject("Film, literature and culture")
lab_circuitos = Subject("Laboratorio de circuitos eléctricos y mediciones")
etica = Subject("Ética, persona y sociedad")
mate = Subject("Matemáticas avanzadas")

subjects = [circuitosII, electronica, flc, lab_circuitos, etica, mate]

#..........................................................
# Circuitos eléctricos II

tc6 = Homework("TC6")
tc6.set_date("19/03/2020")

tc6.set_percentage_in_1hr((3/10)*100)

circuitosII.add_hw(tc6)

#..........................................................
# Electrónica

tarea3 = Homework("Tarea 3")
tarea3.set_date("13/03/2020")
tarea3.set_percentage_in_1hr((2/7)*100)
tarea3.set_completed((4/7)*100)

electronica.add_hw(tarea3)

#..........................................................
# Film, literature and culture

exam = Homework("Exam")
exam.set_date("13/03/2020")
read_film_txt = Homework("Read film text")
read_film_txt.set_date("13/03/2020")
read_film_txt.set_completed((37/40)*100)
read_film_txt.set_percentage_in_1hr((5/40)*100)

flc.add_hw(exam)
flc.add_hw(read_film_txt)

#..........................................................
# Laboratorio de circuitos eléctricos y mediciones

practs = Homework("Entrega prácticas")
practs.set_date("13/03/2020")

lab_circuitos.add_hw(practs)

#..........................................................
# Ética, persona y sociedad

examen = Homework("Examen en línea")
examen.set_date("14/03/2020")
correcciones_trabajo_equipo = Homework("Corregir trabajo en equipo")
correcciones_trabajo_equipo.set_date("14/03/2020")
lectura = Homework("Comenzar lecutra")

etica.add_hw(examen)
etica.add_hw(correcciones_trabajo_equipo)
etica.add_hw(lectura)

#..........................................................
# Matemáticas avanzadas

ejercicios = Homework("Ejercicios")
quiz = Homework("Quiz 2")
quiz.set_date("15/03/2020 checar fecha real")

mate.add_hw(ejercicios)
mate.add_hw(quiz)


#print_assignments(subjects)

#current_date = datetime.date.today()
#print(current_date)

#c = calendar.TextCalendar(calendar.SUNDAY)
#for i in range(1, 13):
#    s = c.formatmonth(2022, i)
#    print(s)

#----------------------------------------------------------------------------
# User interaction

def get_input():
    return input(": ").split()



#----- display instruction ----
def display(noun):
    noun_dict = {
        "all": display_all,
        "one": dislpay_one
    }

    if noun == None:
        print("Displaying")
    elif noun in noun_dict:
        noun_dict[noun]()
    else:
        print("Please use a valid noun")

def display_all():
    print("displaying all")

def dislpay_one():
    assignment = str(input("Which assignment do you want to display?\n"))
    print("displaying {}".format(assignment))
#----- display instruction ----

#----- add instruction ----
#----- add instruction ----

#----- edit instruction ----
#----- edit instruction ----



verb_dict = {
    "disp": display,
    "exit": exit
}



while True:
    instruction = get_input()
    verb = instruction[0]

    if len(instruction) > 1:
        noun = instruction[1]
    else:
        noun = None

    if verb in verb_dict:
        verb_dict[verb](noun)
    else:
        print("{0} is not a programmed instruction.".format(instruction[0]))
