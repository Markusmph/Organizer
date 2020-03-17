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

def run_instruc(instruction):
    # noun, subj_index, assignm_index, value
    verb = instruction[0]
    if verb in verb_dict:
        if len(instruction) == 1:
            verb_dict[verb]()
        elif len(instruction) == 2:
            verb_dict[verb](instruction[1])
        elif len(instruction) == 3:
            verb_dict[verb](instruction[1], instruction[2])
        elif len(instruction) == 4:
            verb_dict[verb](instruction[1], instruction[2], instruction[3])
        elif len(instruction) > 4:
            value = instruction[4]
            if len(instruction) > 5:
                for i in range(5, len(instruction)):
                    value = value + " " + instruction[i]
            verb_dict[verb](instruction[1], instruction[2], instruction[3], value)
    else:
        print("{0} is not a programmed instruction.".format(instruction[0]))

def save_in_file():
    pickle_out = open("school.pickle", "wb")
    pk.dump(school, pickle_out)
    pickle_out.close()




#----- display instruction ----
def display(*args):
    noun_dict = {
        "assignm": display_assignments,
        "subj": display_subj,
        "inor": display_in_order,
        "display one": dislpay_one
    }

    if len(args) == 0:
        display_all()
    elif len(args) == 1:
        if args[0] in noun_dict:
            noun_dict[args[0]]()
        else:
            print("Please use a valid noun")
    else:
        noun_dict["display one"](args[0], args[1])

def display_all():
    i = 1
    for subject in school.get_subj_list():
        print(str(i) + ") " + subject.get_name())
        j = 1
        for assignm in subject.get_assignments():
            print("     " + str(j) + ") " + assignm.get_name() + " | " + str(assignm.get_perc_completed()) + "%")
            j += 1
        i += 1
def display_subj():
    i = 1
    for subject in range(len(school.subj_list)):
        print(str(i) + ") " + school.subj_list[subject].name)
        i += 1
def display_assignments():
    i = 1
    for subj in school.get_subj_list():
        for assignm in subj.get_assignments():
            print(str(i) + ") " + assignm.get_name() + " - " + subj.get_name())
            i += 1
def dislpay_one(subj_index, assignm_index):
    i = int(subj_index) - 1
    j = int(assignm_index) - 1
    try:
        assignment = school.get_subj_list()[i].get_assignments()[j]
        print(assignment.get_name())
        print("     " + "Delivery date: " + str(assignment.get_delivery_date()))
        print("     " + "Recomended date: " + str(assignment.get_recomended_date()))
        print("     " + "Percentage completed: " + str(assignment.get_perc_completed()) + "%")
        print("     " + "Percentage missing: " + str(assignment.get_missing_perc()) + "%")
        print("     " + "Time remaining: " + str(assignment.get_time_to_finish()) + " hours")
        print("     " + "Percentage completed in 1 hour: " + str(assignment.get_perc_in1hr()) + "% in 1 hour")
        #print("     " + "Days remaining to delivery: " + str(assignment.get_days_remaining()))
    except IndexError:
        print("That assignment doesn't exist!")
def display_in_order():
    assignments = []
    for subj in school.get_subj_list():
        for assignm in subj.get_assignments():
            assignments.append(assignm)

    for i in range(1, len(list)):
        j = i
        while j < len(list):
            if list[i-1] > list[j]:
                (list[i-1], list[j]) = (list[j], list[i-1])
                j = i
            else:
                j += 1
    
    for assignm in assignments:
        print(str(assignm.get_delivery_date()))
    #assignments = []
    #assignments_dates = []
    #for subj in school.get_subj_list():
    #    for assignm in subj.get_assignments():
    #        assignments.append(assignm)
    #        assignments_dates.append(assignm.get_delivery_date())
#----- display instruction ----

#----- add instruction ----
def add(*args):
    noun_dict = {
        "hw": add_homework
    }
    if args[0] in noun_dict:
        noun_dict[args[0]](args[1])
    else:
        print("Please use a valid noun")
def add_homework(subj_index):
    delivery_date = dt.date(2020, int(input("Month of delivery: ")), int(input("Day of delivery: ")))
    assignment = Homework(input("Name: "), delivery_date)
    school.get_subj_list()[int(subj_index)-1].add_assignm(assignment)
    save_in_file()
#----- add instruction ----

#----- edit instruction ----
def edit(*args):
    # noun, subj_index, assignm_index, value
    noun_dict = {
        "name": edit_name,
        "pcomp": edit_perc_completed,
        "p1hr": edit_perc_1hr
    }
    if args[0] in noun_dict:
        noun_dict[args[0]](args[1], args[2], args[3])
    else:
        print("Please use a valid noun")
def edit_name(subj_index, assignm_index, value):
    school.get_subj_list()[int(subj_index)-1].get_assignments()[int(assignm_index)-1].set_name(value)
    save_in_file()
def edit_perc_completed(subj_index, assignm_index, value):
    school.get_subj_list()[int(subj_index)-1].get_assignments()[int(assignm_index)-1].set_completed(float(value))
    save_in_file()
def edit_perc_1hr(subj_index, assignm_index, value):
    school.get_subj_list()[int(subj_index)-1].get_assignments()[int(assignm_index)-1].set_perc_in1hr(float(value))
    save_in_file()
#----- edit instruction ----

#----- remove instruction ----
def remove(*args):
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
    run_instruc(get_input())




# Sort without sorting method
#-----------------------------------
# def order_list(list):
# for i in range(1, len(list)):
#         j = i
#         while j < len(list):
#             if list[i-1] > list[j]:
#                 (list[i-1], list[j]) = (list[j], list[i-1])
#                 j = i
#             else:
#                 j += 1
#     return list

    


# TODO: set date of subject
# TODO: set recomended date based on duration and delivery date
# TODO: show to the user what to do