import datetime as dt
import pickle as pk

from Classes.Ambits import Ambit, School, Subject
from Classes.Assignments import Assignment, Homework




eg_delivery = dt.date(2020, 3, 21)
eg_recomended = dt.date(2020, 3, 16)

tareas_etica = [
    Homework("Resolver guía", eg_delivery, (2/10), (4/10), eg_recomended),
    Homework("Examen en línea", dt.date(2020, 3, 14)),
    Homework("Corregir trabajo en equipo", dt.date(2020, 3, 16), 50),
    Homework("Lectura comentadad 2", dt.date(2020, 3, 21), 10, recomended_date=dt.date(2020, 3, 19))
]
tareas_circuitos = [
    Homework("Tarea Connect 6", dt.date(2020, 3, 19), ((3/10)*100))
]
tareas_mate = [
    Homework("Ejercicios", dt.date(2020, 3, 26), 20, recomended_date=dt.date(2020, 3, 19)),
    Homework("Quiz 2", dt.date(2020, 3, 15))
]
tareas_lab_sd = []
tareas_bach = []
tareas_flc = []
tareas_elec = []
tareas_lab_cir = []

subjects = [
        Subject("Ética, persona y sociedad", tareas_etica),
        Subject("Circuitos eléctricos II", tareas_circuitos),
        Subject("Matemáticas avanzadas", tareas_mate),
        Subject("Laboratorio de sistemas digitales", tareas_lab_sd),
        Subject("Bachata", tareas_bach),
        Subject("Film, literature and culture", tareas_flc),
        Subject("Electrónica", tareas_elec),
        Subject("Laboratorio de circuitos eléctricos y mediciones", tareas_lab_cir)
    ]

school = School(subjects)















#----------------------------------------------------------------------------
# User interaction



def get_input():
    return input(": ").split()

#----- display instruction ----
def display(noun):
    noun_dict = {
        "all": display_all,
        "subj": display_subj
    }

    if noun == None:
        display_assignments()
    elif noun in noun_dict:
        noun_dict[noun]()
    else:
        print("Please use a valid noun")

def display_all():
    print("displaying all")
def display_subj():
    for subject in range(len(school.subj_list)):
        print(school.subj_list[subject].name)
def display_assignments():
    for i in school.get_subj_list():
        for assignm in i.get_assignments():
            print(assignm.get_name() + " - " + i.get_name())

def dislpay_one():
    assignment = str(input("Which assignment do you want to display?\n"))
    print("displaying {}".format(assignment))
#----- display instruction ----

#----- add instruction ----
def add(noun):
    noun_dict = {
        
    }
#----- add instruction ----

#----- edit instruction ----
#----- edit instruction ----



verb_dict = {
    "disp": display,
    "add": add,
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


# TODO: save everything in files
# TODO: set date of subject
# TODO: set recomended date based on duration and delivery date
# TODO: show to the user what to do