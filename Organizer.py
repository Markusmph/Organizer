import datetime as dt
import pickle as pk

from Classes.Ambits import Ambit, School, Subject, Natma, Personal, Category
from Classes.Assignments import Assignment, Homework, Exam, PersAssignment, PersAssignmentPeriodic


# for subj in school.get_subj_list():
#     for assignm in subj.get_assignm_list():
#         assignm.set_mandatory(True)
# for assignm in natma.get_assignm_list():
#     assignm.set_mandatory(True)


#----------------------------------------------------------------------------
# User interaction


#----- files ----
def read_files():
    pickle_in = open("school.pickle", "rb")
    school = pk.load(pickle_in)
    pickle_in.close()
    pickle_in = open("natma.pickle", "rb")
    natma = pk.load(pickle_in)
    pickle_in.close()
    pickle_in = open("personal.pickle", "rb")
    personal = pk.load(pickle_in)
    pickle_in.close()
    return (school, natma, personal)

def save_in_school_file():
    pickle_out = open("school.pickle", "wb")
    pk.dump(school, pickle_out)
    pickle_out.close()

def save_in_natma_file():
    pickle_out = open("natma.pickle", "wb")
    pk.dump(natma, pickle_out)
    pickle_out.close()

def save_in_personal_file():
    pickle_out = open("personal.pickle", "wb")
    pk.dump(personal, pickle_out)
    pickle_out.close()


def save_files():
    save_in_school_file()
    save_in_natma_file()
    save_in_personal_file()


def get_input():
    return input("----------\n: ").split()

def run_instruc(instruction):
    # noun, subj_index, assignm_index, value
    verb = instruction[0]
    del instruction[0]
    if verb in verb_dict:
        verb_dict[verb](instruction)
    else:
        print("{0} is not a programmed instruction.".format(verb))

def decimal_to_time(value):
    hours = int(value)
    decimales = value - int(value)
    minutes = decimales * 60
    return (hours, minutes)

def update_deliveries():
    # School
    for subj in school.get_subj_list():
        for assignm in subj.get_assignm_list():
            mandatory = assignm.get_mandatory()
            #print(str(assignm.get_delivery_date()) + " " + str(assignm.get_delivery_date() < today.date()) + " {0}".format(mandatory))
            if assignm.get_delivery_date() < today.date() and not mandatory:
                assignm.set_delivery_date(today.date())
            elif assignm.get_delivery_date() < today.date() and mandatory:
                assignm.set_late(True)
    # Natma
    for assignm in natma.get_assignm_list():
        mandatory = assignm.get_mandatory()
        if assignm.get_delivery_date() < today.date() and not mandatory:
            assignm.set_delivery_date(today.date())
        elif assignm.get_delivery_date() < today.date() and mandatory:
            assignm.set_late(True)
    
    # Personal
    for categ in personal.get_categ_list():
        for assignm in categ.get_assignm_list():
            mandatory = assignm.get_mandatory()
            if assignm.get_delivery_date() < today.date() and not mandatory:
                if type(assignm) == PersAssignmentPeriodic:
                    assignm.update_delivery_date()
                else:
                    assignm.set_delivery_date(today.date())
            elif assignm.get_delivery_date() < today.date() and mandatory:
                assignm.set_late(True)

    save_files()

def ordered_list():
    assignments = []
    subject_name = []
    # delivery_dates = []
    for subj in school.get_subj_list():
        for assignm in subj.get_assignm_list():
            assignments.append(assignm)
            subject_name.append(subj.get_name())
            # delivery_dates.append(assignm.get_delivery_date())

    for assignm in natma.get_assignm_list():
        assignments.append(assignm)
        subject_name.append("Natma")
        # delivery_dates.append(assignm.get_delivery_date())

    for categ in personal.get_categ_list():
        for assignm in categ.get_assignm_list():
            assignments.append(assignm)
            subject_name.append("Personal")
            # delivery_dates.append(assignm.get_delivery_date())

    for i in range(1, len(assignments)):
        j = i
        while j < len(assignments):
            if assignments[i-1].get_delivery_date() > assignments[j].get_delivery_date():
                (assignments[i-1], assignments[j]) = (assignments[j], assignments[i-1])
                (subject_name[i-1], subject_name[j]) = (subject_name[j], subject_name[i-1])
                j = i
            else:
                j += 1
    return (assignments, subject_name)

def order_list(list_to_order, list_with_parameter):
    for i in range(1, len(list_to_order)):
        j = i
        while j < len(list_to_order):
            if list_with_parameter[i-1] > list_with_parameter[j]:
                (list_to_order[i-1], list_to_order[j]) = (list_to_order[j], list_to_order[i-1])
                (list_with_parameter[i-1], list_with_parameter[j]) = (list_with_parameter[j], list_with_parameter[i-1])
                j = i
            else:
                j += 1
    return list_to_order


def periodic_instructions():
    print("Every day = 0")
    print("Monday = 1")
    print("Tuesday = 2")
    print("Wednesday = 3")
    print("Thursday = 4")
    print("Friday = 5")
    print("Saturday = 6")
    print("Sunday = 7")
    print("Every month = 8")
    print("Every 2 days = 9")


#----- display instruction ----
def display(instruction):
    noun_dict = {
        "assignm": display_assignments,
        "subj": display_subj,
        "inor": display_in_order,
        "mand": display_mand,
        #"display one": dislpay_one,
        "n": display_natma,
        "p": display_pers,
        "s": dislpay_one,
        "c": display_completed
    }
    if len(instruction) == 0:
        display_all()
    elif instruction[0] in noun_dict:
        noun = instruction[0]
        del instruction[0]
        noun_dict[noun](instruction)
    else:
        print("Please use a valid noun")

def display_all():
    print("--------------------- SCHOOL -----------------------------")
    i = 1
    for subject in school.get_subj_list():
        print(str(i) + ") " + subject.get_name())
        j = 1
        for assignm in subject.get_assignm_list():
            if assignm.get_mandatory():
                mand = "Mandatory"
            else:
                mand = ""
            print("     " + str(j) + ") " + assignm.get_name() + " | " + str(assignm.get_perc_completed()) + "%" + " " + str(assignm.get_delivery_date()) + " " + mand)
            j += 1
        i += 1

    print("--------------------- NATMA -----------------------------")
    i = 1
    for assignm in natma.get_assignm_list():
        if assignm.get_mandatory():
           mand = "Mandatory"
        else:
            mand = ""
        print(str(i) + ") " + assignm.get_name() + " | " + str(assignm.get_perc_completed()) + "% " + str(assignm.get_delivery_date()) + " " + mand)
        i += 1

    print("--------------------- PERSONAL -----------------------------")
    display_pers([])
    # i = 1
    # for categ in personal.get_categ_list():
    #     print(str(i) + ") " + categ.get_name())
    #     j = 1
    #     for assignm in categ.get_assignm_list():
    #         if assignm.get_mandatory():
    #             mand = "Mandatory"
    #         else:
    #             mand = ""
    #         print("     " + str(j) + ") " + assignm.get_name() + " | " + str(assignm.get_perc_completed()) + "%" + " " + str(assignm.get_delivery_date()) + " " + mand)
    #         j += 1
    #     i += 1

def display_subj(instruction):
    if len(instruction) == 0:
        i = 1
        for subject in range(len(school.subj_list)):
            print(str(i) + ") " + school.subj_list[subject].name)
            i += 1
    elif len(instruction) >= 1:
        subj_index = int(instruction[0]) - 1
        subj = school.get_subj_list()[subj_index]
        print(subj.get_name())
        print("------------------------------")
        i = 1
        for assignm in subj.get_assignm_list():
            print(str(i) + ") " + assignm.get_name() + " Delivery: " + str(assignm.get_delivery_date()))
            i += 1
def display_assignments(instrucion):
    i = 1
    for subj in school.get_subj_list():
        for assignm in subj.get_assignm_list():
            print(str(i) + ") " + assignm.get_name() + " - " + subj.get_name())
            i += 1
def dislpay_one(instrucion):
    i = int(instrucion[0]) - 1
    j = int(instrucion[1]) - 1
    try:
        assignment = school.get_subj_list()[i].get_assignm_list()[j]
        if type(assignment) == Homework:
            print(assignment.get_name())
            print("     " + "Delivery date: " + str(assignment.get_delivery_date()))
            print("     " + "Percentage completed: " + str(assignment.get_perc_completed()) + "%")
            print("     " + "Percentage missing: " + str(assignment.get_missing_perc()) + "%")
            print("     " + "Time remaining: " + str(assignment.get_time_to_finish()) + " hours")
            print("     " + "Percentage completed in 1 hour: " + str(assignment.get_perc_in1hr()) + "% in 1 hour")
            print("     " + "Mandatory: " + str(assignment.get_mandatory()))
            #print("     " + "Days remaining to delivery: " + str(assignment.get_days_remaining()))
        elif type(assignment) == Exam:
            print(assignment.get_name())
            print("     " + "Delivery date: " + str(assignment.get_delivery_date()))
            print("     " + "Percentage completed: " + str(assignment.get_perc_completed()) + "%")
            print("     " + "Percentage missing: " + str(assignment.get_missing_perc()) + "%")
            print("     " + "Time remaining: " + str(assignment.get_time_to_finish()) + " hours")
    except IndexError:
        print("That assignment doesn't exist!")
    
def display_in_order(instruction):
    (assignments, subject_name) = ordered_list()
    i = 0
    assignments.reverse()
    subject_name.reverse()
    for assignm in assignments:
        (hours, minutes) = decimal_to_time(assignm.get_time_to_finish())
        delivery = str(assignm.get_delivery_date())
        if assignm.get_mandatory():
            mand = "      MANDATORY"
        else:
            mand = ""
        if type(assignm) == Homework:
            if assignm.get_late():
                late = " LATE"
                mand = ""
            else:
                late = ""
        else:
            late = ""
            
        text = "Delivery: " + delivery + " " + assignm.get_name() + " | " + "Remaining time: " + str(hours) + " hours " + str(minutes) + " minutes - " + subject_name[i] + late + mand
            
        print(text)
        i += 1
        try:
            if not (assignm.get_delivery_date() == assignments[i].get_delivery_date()):
                print("")
        except IndexError:
            print("")

def display_mand(instruction):
    (assignments, subject_name) = ordered_list()
    assignments.reverse()
    subject_name.reverse()
    for assignm in assignments:
        if assignm.get_mandatory():
            print(assignm.get_name() + " Delivery: " + str(assignm.get_delivery_date()))

def display_natma(instruction):
    i = 1
    for assignm in natma.get_assignm_list():
        print(str(i) + ") " + assignm.get_name())
        i += 1

def display_pers(instruction):
    try:
        if len(instruction) == 0:
            i = 1
            for categ in personal.get_categ_list():
                print(str(i) + ") " + categ.get_name())
                j = 1
                for assignm in categ.get_assignm_list():
                    if assignm.get_mandatory():
                        mand = "Mandatory"
                    else:
                        mand = ""
                    print("     " + str(j) + ") " + assignm.get_name() + " | " + str(assignm.get_perc_completed()) + "%" + " " + str(assignm.get_delivery_date()) + " " + mand)
                    j += 1
                i += 1
        elif len(instruction) >= 1:
            categ_index = int(instruction[0]) - 1
            print(personal.get_categ_list()[categ_index].get_name() + ":")
            print("---------------------------------------------------------")
            i = 1
            for assignm in personal.get_categ_list()[categ_index].get_assignm_list():
                delivery = str(assignm.get_delivery_date())
                print("     " + str(i) + ") " + assignm.get_name())
                if type(assignm) == PersAssignmentPeriodic:
                    assignm_type = "Periodic"
                elif type(assignm) == PersAssignment:
                    assignm_type = "Non periodic"
                print("          " + assignm_type + " || " + delivery)
                i += 1
    except IndexError:
        print("Not enough elements to the instruction")
        print("Please enter \"disp p <category index>\"")

def display_completed(instruction):
    try:
        subj_index = int(instruction[0]) - 1
        i = 1
        for assignm in school.get_subj_list()[subj_index].get_completed_list():
            print(str(i) + ") " + assignm.get_name())
            i += 1
    except IndexError:
        print("Please enter the full instruction")
        print("")

#----- display instruction ----

#----- add instruction ----
def add(instruction):
    noun_dict = {
        "s": add_subject,
        "hw": add_homework,
        "e": add_exam,
        "n": add_natma,
        "pc": add_personal_categ,
        "p": add_personal_assignment
    }
    if instruction[0] in noun_dict:
        noun = instruction[0]
        del instruction[0]
        noun_dict[noun](instruction)
    else:
        print("Please use a valid noun")
def add_subject(instructions):
    try:
        name = instructions[0]
        for i in range(1, len(instructions)):
            name += (" " + instructions[i])
        new_subject = Subject(name)
        school.add_subj(new_subject)
        save_in_school_file()
    except IndexError:
        print("Please enter the full instruction")
        print("     add s <subject name>")
def add_homework(instruction):
    subj_index = instruction[0]
    name = input("Name: ")
    delivery_date = dt.date(today.year, int(input("Month of delivery: ")), int(input("Day of delivery: ")))
    p1hr = float(input("Percentage done in 1 hour: "))
    assignment = Homework(name, delivery_date, p1hr)
    school.get_subj_list()[int(subj_index)-1].add_assignm(assignment)
    save_in_school_file()
def add_natma(instruction):
    name = input("Name: ")
    delivery_date = dt.date(today.year, int(input("Month: ")), int(input("Day: ")))
    perc1hr = float(input("Percentage in 1 hour: "))
    new_assignm = Homework(name, delivery_date, perc1hr)
    natma.add_assignm(new_assignm)
    save_in_natma_file()
def add_exam(instruction):
    try:
        subj_index = instruction[0]
        name = instruction[1]
        for i in range(2, len(instruction)):
            name += " " + instruction[i]
        date = dt.date(today.year, int(input("Month: ")), int(input("Day: ")))
        exam = Exam(name, date)
        school.get_subj_list()[int(subj_index)-1].add_assignm(exam)
        save_in_school_file()
    except IndexError:
        print("Not enough elements to the instruction")
        print("Please enter \"add e <subject index> <name of the exam>\"")
def add_personal_categ(instruction):
    try:
        value = instruction[0]
        for i in range(1, len(instruction)):
            value += " " + instruction[i]
        new_categ = Category(value)
        personal.add_categ(new_categ)
        save_in_personal_file()
    except IndexError:
        print("Please enter the complete instruction: ")
        print("     add pc <category name>")
def add_personal_assignment(instruction):
    try:
        value = int(instruction[0]) - 1
        name = instruction[1]
        for i in range(2, len(instruction)):
            name += " {0}".format(instruction[i])
        p_input = input("Periodic? (y/n) ")
        if p_input == "True" or p_input == "true" or p_input == "t" or p_input == "yes" or p_input == "y" or p_input == "Y":
            periodic_instructions()
            periodic_type = int(input("Enter periodic instruction with integer: "))
            perc_in1hr = float(input("Percentage done in 1 hour: "))
            new_assingm = PersAssignmentPeriodic(name, periodic_type, perc_in1hr)
            personal.get_categ_list()[value].add_assignm(new_assingm)
            save_in_personal_file()
        elif p_input == "False" or p_input == "false" or p_input == "f" or p_input == "no" or p_input == "n" or p_input == "N":
            delivery_date = dt.date(today.year, int(input("Month: ")), int(input("Day: ")))
            perc_in1hr = float(input("Percentage done in 1 hour: "))
            new_assignm = PersAssignment(name, delivery_date, perc_in1hr)
            personal.get_categ_list()[value].add_assignm(new_assignm)
            save_in_personal_file()
        else:
            print("Creating a non-periodic assignment...")
            delivery_date = dt.date(today.year, int(input("Month: ")), int(input("Day: ")))
            perc_in1hr = float(input("Percentage done in 1 hour: "))
            new_assignm = PersAssignment(name, delivery_date, perc_in1hr)
            personal.get_categ_list()[value].add_assignm(new_assignm)
            save_in_personal_file()
    except IndexError:
        print("Please enter the complete instruction: ")
        print("     add p <category index> <assignment name>")
#----- add instruction ----

#----- edit instruction ----
def edit(instruction):
    noun = instruction[0]
    del instruction[0]
    noun_dict = {
        "name": edit_name,
        "pname": edit_name_personal,
        "pcomp": edit_perc_completed,
        "npcomp": edit_perc_completed_natma,
        "ppcomp": edit_perc_completed_personal,
        "p1hr": edit_perc_1hr,
        "pp1hr": edit_perc_1hr_personal,
        "delivery": edit_delivery_date,
        "ndelivery": edit_delivery_date_natma,
        "pdelivery": edit_delivery_date_personal,
        "mand": edit_mandatory,
        "nmand": edit_mandatory_natma
    }
    if noun in noun_dict:
        noun_dict[noun](instruction)
    else:
        print("Please use a valid noun")
def edit_name(instruction):
    subj_index = int(instruction[0]) - 1
    assignm_index = int(instruction[1]) - 1
    value = instruction[2]
    for i in range(3, len(instruction)):
        value += " " + instruction[i]
    school.get_subj_list()[subj_index].get_assignm_list()[assignm_index].set_name(value)
    save_in_school_file()
def edit_name_personal(instruction):
    try:
        categ_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        value = instruction[2]
        for i in range(3, len(instruction)):
            value += " " + instruction[i]
        personal.get_categ_list()[categ_index].get_assignm_list()[assignm_index].set_name(value)
        save_in_personal_file()
    except IndexError:
        print("Please enter the full instruction:")
        print("edit pname <category index> <assignment index> <new name>")
def edit_perc_completed(instruction):
    subj_index = int(instruction[0]) - 1
    assignm_index = int(instruction[1]) - 1
    value = float(instruction[2])
    school.get_subj_list()[subj_index].get_assignm_list()[assignm_index].set_completed(value)
    if value >= 100:
        try:
            school.get_subj_list()[subj_index].set_as_completed(assignm_index)
        except AttributeError:
            print("Subject has no attribute completed, creating one...")
            school.get_subj_list()[subj_index].create_completed_list()
            school.get_subj_list()[subj_index].set_as_completed(assignm_index)
            print("Completed list created!")
    display_subj(instruction[0])
    save_in_school_file()
def edit_perc_completed_natma(instruction):
    try:
        assignm_index = int(instruction[0]) - 1
        value = float(instruction[1])
        natma.get_assignm_list()[assignm_index].set_completed(value)
        if value == 100:
            try:
                natma.set_as_completed(assignm_index)
                display_natma(instruction)
            except AttributeError:
                print("Natma has no attribute completed, creating one...")
                natma.create_completed_list()
                natma.set_as_completed(assignm_index)
                print("Completed list created!")
        save_in_natma_file()
    except IndexError:
        print("Please enter the full instruction:")
        print("     edit npcomp <assignment index> <new value>")
def edit_perc_completed_personal(instruction):
    try:
        categ_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        value = float(instruction[2])
        personal.get_categ_list()[categ_index].set_completed(assignm_index, value)
        save_in_personal_file()
    except IndexError:
        print("Please enter the full instruction:")
        print("     edit ppcomp <category index> <assignment index> <percentage>")
def edit_perc_1hr(instruction):
    try:
        subj_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        value = float(instruction[2])
        school.get_subj_list()[subj_index].get_assignm_list()[assignm_index].set_perc_in1hr(value)
        save_in_school_file()
    except IndexError:
        print("Please enter the full instruction:")
        print("     edit p1hr <subject index> <assignment index> <new value>")
def edit_perc_1hr_personal(instruction):
    categ_index = int(instruction[0]) - 1
    assignm_index = int(instruction[1]) - 1
    value = float(instruction[2])
    personal.get_categ_list()[categ_index].get_assignm_list()[assignm_index].set_perc_in1hr(value)
    save_in_personal_file()
def edit_delivery_date(instruction):
    subj_index = instruction[0]
    assignm_index = instruction[1]
    delivery_date = dt.date(dt.datetime.now().year, int(input("Month: ")), int(input("Day: ")))
    school.get_subj_list()[int(subj_index)-1].get_assignm_list()[int(assignm_index)-1].set_delivery_date(delivery_date)
    save_in_school_file()
def edit_delivery_date_natma(instruction):
    assignm_index = int(instruction[0]) - 1
    delivery_date = dt.date(dt.datetime.now().year, int(input("Month: ")), int(input("Day: ")))
    natma.get_assignm_list()[assignm_index].set_delivery_date(delivery_date)
    save_in_natma_file()
def edit_delivery_date_personal(instruction):
    categ_index = int(instruction[0]) - 1
    assignm_index = int(instruction[1]) - 1
    delivery_date = dt.date(dt.datetime.now().year, int(input("Month: ")), int(input("Day: ")))
    personal.get_categ_list()[categ_index].get_assignm_list()[assignm_index].set_delivery_date(delivery_date)
    save_in_personal_file()
def edit_mandatory(instruction):
    try:
        subj_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        if instruction[2] == "True" or instruction[2] == "true" or instruction[2] == "t":
            new_value = True
        elif instruction[2] == "False" or instruction[2] == "false" or instruction[2] == "f":
            new_value = False
            assignm = school.get_subj_list()[subj_index].get_assignm_list()[assignm_index]
            if assignm.get_delivery_date() < today.date():
                assignm.set_delivery_date(today.date())
        else:
            print("Setting value as True")
            new_value = True
        school.get_subj_list()[subj_index].get_assignm_list()[assignm_index].set_mandatory(new_value)
        save_in_school_file()
    except IndexError:
        print("Not enough info. Instruction: \"edit mand <subject index> <assignment index> <text>\"")
def edit_mandatory_natma(instruction):
    assignm_index = instruction[0]
    if instruction[1] == "True" or instruction[1] == "true" or instruction[1] == "t":
        new_value = True
    elif instruction[1] == "False" or instruction[1] == "false" or instruction[1] == "f":
        new_value = False
        if natma.get_assignm_list()[int(assignm_index) - 1].get_late():
            natma.get_assignm_list()[int(assignm_index) - 1].set_delivery_date(today.date)
    else:
        print("Setting value as True")
        new_value = True
    natma.get_assignm_list()[int(assignm_index)-1].set_mandatory(new_value)
    save_in_natma_file()
#----- edit instruction ----

#----- remove instruction ----
def remove(instruction):
    noun_dict = {
        "s": remove_from_school,
        "n": remove_from_natma,
        "p": remove_from_personal,
        "pc": remove_categ_from_personal
    }
    if instruction[0] in noun_dict:
        noun = instruction[0]
        del instruction[0]
        noun_dict[noun](instruction)
    else:
        print("Please use a valid noun")
def remove_from_school(instruction):
    try:
        subj = int(instruction[0]) - 1
        if len(instruction) == 2:
            assignm = int(instruction[1]) - 1
            del school.get_subj_list()[subj].get_assignm_list()[assignm]
            save_in_school_file()
            display_subj(instruction)
        elif len(instruction) == 1:
            confirmation = input("Are you sure you want to remove {0}? y/n: ".format(school.get_subj_list()[subj].get_name()))
            while (confirmation != "y") and (confirmation != "n"):
                confirmation = input("Are you sure you want to remove {0}? y/n: ".format(school.get_subj_list()[subj].get_name()))
            if confirmation == "y":
                del school.get_subj_list()[subj]
                save_in_school_file()
                print("Subject removed")
            elif confirmation == "n":
                print("Action cancelled")
            display_subj([])
        else:
            print("Please enter the instruction as follows:")
            print("     rem s <subject index>")
    except IndexError:
        print("Please enter the instruction as follows:")
        print("     rem s <subject index>")
def remove_from_natma(instruction):
    i = int(instruction[0]) - 1
    del natma.get_assignm_list()[i]
    save_in_natma_file()
def remove_from_personal(instruction):
    try:
        categ = int(instruction[0]) - 1
        assignm = int(instruction[1]) - 1
        del personal.get_categ_list()[categ].get_assignm_list()[assignm]
        save_in_personal_file()
    except IndexError:
        print("Please enter the full instruction:")
        print("     rem p <category index> <assignm index>")
def remove_categ_from_personal(instruction):
    try:
        categ_index = int(instruction[0]) - 1
        del personal.get_categ_list()[categ_index]
        save_in_personal_file()
    except IndexError:
        print("Please enter the full instrucion:")
        print("     rem pc <category index>")
#----- remove instruction ----

#----- remaining hours ----
def remaining_hrs(instruction):
    try:
        month = int(instruction[0])
        day = int(instruction[1])
        (assignments, subj_name) = ordered_list()

        time_total = 0
        time_mandatory = 0
        time_non_mandatory = 0
        for assignm in assignments:
            if assignm.get_delivery_date() <= dt.date(today.year, month, day):
                if assignm.get_mandatory():
                    time_mandatory += assignm.get_time_to_finish()
                elif not assignm.get_mandatory():
                    time_non_mandatory += assignm.get_time_to_finish()
        time_total = time_mandatory + time_non_mandatory
        (hours_mandatory, minutes_mandatory) = decimal_to_time(time_mandatory)
        (hours_non_mandatory, minutes_non_mandatory) = decimal_to_time(time_non_mandatory)
        (hours_total, minutes_total) = decimal_to_time(time_total)
        print("Time remaining to complete assignments until " + str(day) + " of " + str(month))
        print("............................................................................................")
        print("Mandatory assignments: " + str(hours_mandatory) + " hours " + str(minutes_mandatory) + " minutes")
        print("Non-mandatory assignments: " + str(hours_non_mandatory) + " hours " + str(minutes_non_mandatory) + " minutes")
        print("Total: " + str(hours_total) + " hours " + str(minutes_total) + " minutes")
        
    except IndexError:
        print("Not enough data")

#----- remaining hours ----

#----- What to do ----
def what_to_do(instruction):
    (assignments, subject_name) = ordered_list()
    to_do_list = []
    param_list = []
    urgent_list = []
    non_mand_list = []
    non_mand_param_list = []
    i = 1
    j = 1

    for assignm in assignments:
        if assignm.get_mandatory() and (assignm.get_delivery_date() <= (today.date() + dt.timedelta(days=1))):
            urgent_list += [assignm]

    for assignm in urgent_list:
        assignments.remove(assignm)

    for assignm in assignments:
        (hours, minutes) = decimal_to_time(round(assignm.get_time_to_finish()))
        if assignm.get_mandatory() and ((assignm.get_delivery_date() - dt.timedelta(days=hours)) <= today.date()):
            to_do_list.append(assignm)
            param_list.append(assignm.get_delivery_date() - dt.timedelta(days=hours))
            #print(str(i) + ") " + assignm.get_name() + " - Missing time: " + str(hours) + " hours, " + str(minutes) + " minutes " + "Delivery: " + str(assignm.get_delivery_date()))
        elif not assignm.get_mandatory() and ((assignm.get_delivery_date() - dt.timedelta(days=hours)) <= today.date()):
            non_mand_list.append(assignm)
            non_mand_param_list.append(assignm.get_delivery_date() - dt.timedelta(days=hours))
            
    to_do_list = order_list(to_do_list, param_list)
    non_mand_list = order_list(non_mand_list, non_mand_param_list)
    to_do_list = urgent_list + to_do_list + non_mand_list

    for assignm in to_do_list:
        (hours, minutes) = decimal_to_time(assignm.get_time_to_finish())
        print(str(i) + ") " + assignm.get_name() + " - Missing time: " + str(hours) + " hours, " + str(minutes) + " minutes " + "Delivery: " + str(assignm.get_delivery_date()))
        i += 1
#----- What to do ----

#----- help ----
def get_instructions(instruction):
    f = open("instructions.txt", "r")
    instructions = f.read()
    print(instructions)
    f.close()
#----- help ----



verb_dict = {
    "disp": display,
    "add": add,
    "edit": edit,
    "rem": remove,
    "h": remaining_hrs,
    "now": what_to_do,
    "help": get_instructions,
    "q": exit
}

(school, natma, personal) = read_files()
available_time_per_day = dt.timedelta(0, 0, 0, 0, 0, 4)
today = dt.datetime.today()
update_deliveries()
while True:
    run_instruc(get_input())

# delivery = dt.date(2020, 4, 11)
# personal.get_categ_list()[2].get_assignm_list()[3].set_delivery_date(delivery)
# save_in_personal_file()


# del personal.get_categ_list()[2].get_assignm_list()[0]
# save_in_personal_file()
# for categ in personal.get_categ_list():
#     for assignm in categ.get_assignm_list():
#         print(categ.get_name() + " Assignm: " + assignm.get_name() + " DeliveryDate: " + str(assignm.get_delivery_date()))


# for subj in school.get_subj_list():
#     for assignm in subj.get_assignm_list():
#         if type(assignm) == Homework:
#             assignm.set_late(False)

# for assignm in natma.get_assignm_list():
#     if type(assignm) == Homework:
#             assignm.set_late(False)

# for categ in personal.get_categ_list():
#     for assignm in categ.get_assignm_list():
#         if type(assignm) == Homework:
#             assignm.set_late(False)

# save_files()

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

# TODO: display one assignment
# TODO: clean up code
# TODO: display difference in instruction now
# TODO: set date of subject
# TODO: set recomended date based on duration and delivery date
# TODO: create gui