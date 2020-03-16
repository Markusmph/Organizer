import datetime as dt
import pickle as pk

from Classes.Ambits import Ambit, School, Subject
from Classes.Assignments import Assignment, Homework


pickle_in = open("school.pickle", "rb")
school = pk.load(pickle_in)




#----------------------------------------------------------------------------
# User interaction



def get_input():
    return input("----------\n: ").split()

def run_instruc(verb, noun, subj_index, assignm_index, value):
    if verb in verb_dict:
        verb_dict[verb](noun, subj_index, assignm_index, value)
    else:
        print("{0} is not a programmed instruction.".format(instruction[0]))



#----- display instruction ----
def display(noun, subj_index, assignm_index, value):
    noun_dict = {
        "assignm": display_assignments,
        "subj": display_subj
    }

    if noun == None:
        display_all()
    elif noun in noun_dict:
        noun_dict[noun]()
    else:
        print("Please use a valid noun")

def display_all():
    i = 1
    for subject in school.get_subj_list():
        print(str(i) + ") " + subject.get_name())
        j = 1
        for assignm in subject.get_assignments():
            print("     " + str(j) + ") " + assignm.get_name() + " | " + str(assignm.get_perc_completed()) + "%")
            j = j + 1
        i = i + 1
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
def edit(noun, subj_index, assignm_indexm, value):
    noun_dict = {
        "name": edit_name,
        "pcomp": edit_perc_completed
    }
    if noun == None:
        display_all()
    elif noun in noun_dict:
        noun_dict[noun](subj_index, assignm_index, value)
    else:
        print("Please use a valid noun")

def edit_name(subj_index, assignm_index, value):
    school.get_subj_list()[subj_index].get_assignments()[assignm_index].set_name(value)

    pickle_out = open("school.pickle", "wb")
    pk.dump(school, pickle_out)
    pickle_out.close()

def edit_perc_completed():
    pass
#----- edit instruction ----

#----- remove instruction ----
def remove(noun):
    pass
#----- remove instruction ----



verb_dict = {
    "disp": display,
    "add": add,
    "edit": edit,
    "rem": remove,
    "q": exit,
    "quit": exit,
    "exit": exit
}



while True:
    instruction = get_input()
    verb = instruction[0]

    if len(instruction) > 1:
        noun = instruction[1]
        if len(instruction) > 2:
            subj_index = int(instruction[2]) - 1
            assignm_index = int(instruction[3]) - 1
            value = instruction[4]
            if len(instruction) > 4:
                for i in range(5, len(instruction)):
                    value = value + " " + instruction[i]
            run_instruc(verb, noun, subj_index, assignm_index, value)
        else:
            run_instruc(verb, noun, None, None, None)
    else:
        run_instruc(verb, None, None, None, None)


# TODO: save everything in files
# TODO: set date of subject
# TODO: set recomended date based on duration and delivery date
# TODO: show to the user what to do