import os
import datetime as dt
import pickle as pk

from Classes.Ambits import Ambit, School, Subject, Natma, Personal, Category
from Classes.Assignments import Assignment, Homework, Exam, PersAssignment, PersAssignmentPeriodic
from Classes.Budget import Budget

from PyQt5 import QtCore, QtGui, QtWidgets  # works for pyqt5


# ----------------------------------------------------------------------------
# User interaction


# ----- files ----
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


def read_budget():
    pickle_in = open("budget.pickle", "rb")
    load = pk.load(pickle_in)
    pickle_in.close()
    return load


def save_budget():
    pickle_out = open("budget.pickle", "wb")
    budgets = (total_budget, real_budget, expected_budget)
    pk.dump(budgets, pickle_out)
    print("Budgets saved!")
    pickle_out.close()


def get_input():
    return input("----------\n: ").split()


def run_instruc(instruction):
    # noun, subj_index, assignm_index, value
    try:
        verb = instruction[0]
        del instruction[0]
        if verb in verb_dict:
            verb_dict[verb](instruction)
        else:
            print("{0} is not a programmed instruction.".format(verb))
    except IndexError:
        print("Please enter an instruction")


def decimal_to_time(value):
    hours = int(value)
    decimales = value - int(value)
    minutes = decimales * 60
    return (hours, minutes)

# def update_deliveries():
#     # School
#     for subj in school.get_subj_list():
#         for assignm in subj.get_assignm_list():
#             mandatory = assignm.get_mandatory()
#             try:
#                 if assignm.get_delivery_date() < today.date() and not mandatory:
#                     assignm.set_delivery_date(today.date())
#                 elif assignm.get_delivery_date() < today.date() and mandatory:
#                     assignm.set_late(True)
#             except TypeError:
#                 date1 = assignm.get_delivery_date()
#                 date2 = today.date()
#                 if isinstance(date1, date):
#                     date1 = datetime.combine(date1, datetime.min.time())
#                 if isinstance(date2, date):
#                     date2 = datetime.combine(date2, datetime.min.time())
#                 if date1 > date2:
#                     (assignments[i-1], assignments[j]) = (assignments[j], assignments[i-1])
#                     (subject_name[i-1], subject_name[j]) = (subject_name[j], subject_name[i-1])
#                     j = i
#                 else:
#                     j += 1

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
            try:
                if assignments[i-1].get_delivery_date() > assignments[j].get_delivery_date():
                    (assignments[i-1], assignments[j]
                     ) = (assignments[j], assignments[i-1])
                    (subject_name[i-1], subject_name[j]
                     ) = (subject_name[j], subject_name[i-1])
                    j = i
                else:
                    j += 1
            except TypeError:
                date1 = assignments[i-1].get_delivery_date()
                date2 = assignments[j].get_delivery_date()
                if isinstance(date1, dt.date):
                    date1 = dt.datetime.combine(date1, dt.datetime.min.time())
                if isinstance(date2, dt.date):
                    date2 = dt.datetime.combine(date2, dt.datetime.min.time())
                if date1 > date2:
                    (assignments[i-1], assignments[j]
                     ) = (assignments[j], assignments[i-1])
                    (subject_name[i-1], subject_name[j]
                     ) = (subject_name[j], subject_name[i-1])
                    j = i
                else:
                    j += 1
    return (assignments, subject_name)


def order_list(list_to_order, list_with_parameter):
    for i in range(1, len(list_to_order)):
        j = i
        while j < len(list_to_order):
            if list_with_parameter[i-1] > list_with_parameter[j]:
                (list_to_order[i-1], list_to_order[j]
                 ) = (list_to_order[j], list_to_order[i-1])
                (list_with_parameter[i-1], list_with_parameter[j]
                 ) = (list_with_parameter[j], list_with_parameter[i-1])
                j = i
            else:
                j += 1
    return list_to_order


def assignments_ordered():
    # Function that returns 4 lists: assignments, list, category index, assignment index
    assignments = []
    list_name = []
    category_index = []
    assignm_index = []

    # delivery_dates = []
    for subj in school.get_subj_list():
        for assignm in subj.get_assignm_list():
            assignments.append(assignm)
            list_name.append(subj.get_name())
            category_index.append(school.get_subj_list().index(subj))
            assignm_index.append(subj.get_assignm_list().index(assignm))

    for assignm in natma.get_assignm_list():
        assignments.append(assignm)
        list_name.append("Natma")
        category_index.append(0)
        assignm_index.append(natma.get_assignm_list().index(assignm))

    for categ in personal.get_categ_list():
        for assignm in categ.get_assignm_list():
            assignments.append(assignm)
            list_name.append("Personal")
            category_index.append(personal.get_categ_list().index(categ))
            assignm_index.append(categ.get_assignm_list().index(assignm))

    for i in range(1, len(assignments)):
        j = i
        while j < len(assignments):
            if assignments[i-1].get_delivery_date() > assignments[j].get_delivery_date():
                (assignments[i-1], assignments[j]
                 ) = (assignments[j], assignments[i-1])
                (list_name[i-1], list_name[j]) = (list_name[j], list_name[i-1])
                (category_index[i-1], category_index[j]
                 ) = (category_index[j], category_index[i-1])
                (assignm_index[i-1], assignm_index[j]
                 ) = (assignm_index[j], assignm_index[i-1])
                j = i
            else:
                j += 1
    return (assignments, list_name, category_index, assignm_index)


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


# ----- display instruction ----
def display(instruction):
    noun_dict = {
        "assignm": display_assignments,
        "s": display_subj,
        "inor": display_in_order,
        "mand": display_mand,
        # "display one": dislpay_one,
        "n": display_natma,
        "p": display_pers,
        # "s": dislpay_one,
        "c": display_completed,
        "d": display_day,
        "r": display_rules,
        "bud": display_budget
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
            print("     " + str(j) + ") " + assignm.get_name() + " | " +
                  str(assignm.get_perc_completed()) + "%" + " " + str(assignm.get_delivery_date()) + " " + mand)
            j += 1
        i += 1

    print("--------------------- NATMA -----------------------------")
    i = 1
    for assignm in natma.get_assignm_list():
        if assignm.get_mandatory():
            mand = "Mandatory"
        else:
            mand = ""
        print(str(i) + ") " + assignm.get_name() + " | " + str(assignm.get_perc_completed()
                                                               ) + "% " + str(assignm.get_delivery_date()) + " " + mand)
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
    elif len(instruction) == 1:
        subj_index = int(instruction[0]) - 1
        subj = school.get_subj_list()[subj_index]
        print(str(instruction[0]) + ") " + subj.get_name())
        print("------------------------------")
        i = 1
        for assignm in subj.get_assignm_list():
            print(str(i) + ") " + assignm.get_name() +
                  " Delivery: " + str(assignm.get_delivery_date()))
            i += 1
    elif len(instruction) == 2:
        i = int(instruction[0]) - 1
        j = int(instruction[1]) - 1
        try:
            assignment = school.get_subj_list()[i].get_assignm_list()[j]
            if type(assignment) == Homework:
                print(assignment.get_name())
                print("     " + "Delivery date: " +
                      str(assignment.get_delivery_date()))
                print("     " + "Percentage completed: " +
                      str(assignment.get_perc_completed()) + "%")
                print("     " + "Percentage missing: " +
                      str(assignment.get_missing_perc()) + "%")
                print("     " + "Time remaining: " +
                      str(assignment.get_time_to_finish()) + " hours")
                print("     " + "Percentage completed in 1 hour: " +
                      str(assignment.get_perc_in1hr()) + "% in 1 hour")
                print("     " + "Mandatory: " +
                      str(assignment.get_mandatory()))
                #print("     " + "Days remaining to delivery: " + str(assignment.get_days_remaining()))
            elif type(assignment) == Exam:
                print(assignment.get_name())
                print("     " + "Delivery date: " +
                      str(assignment.get_delivery_date()))
                print("     " + "Percentage completed: " +
                      str(assignment.get_perc_completed()) + "%")
                print("     " + "Percentage missing: " +
                      str(assignment.get_missing_perc()) + "%")
                print("     " + "Time remaining: " +
                      str(assignment.get_time_to_finish()) + " hours")
        except IndexError:
            print("That assignment doesn't exist!")
    else:
        print("Please enter one of the instructions:")
        print("     disp s")
        print("     disp s <subject index>")
        print("     disp s <subject index> <assignment index>")


def display_assignments(instrucion):
    i = 1
    for subj in school.get_subj_list():
        for assignm in subj.get_assignm_list():
            print(str(i) + ") " + assignm.get_name() + " - " + subj.get_name())
            i += 1

# def dislpay_one(instrucion):
#     i = int(instrucion[0]) - 1
#     j = int(instrucion[1]) - 1
#     try:
#         assignment = school.get_subj_list()[i].get_assignm_list()[j]
#         if type(assignment) == Homework:
#             print(assignment.get_name())
#             print("     " + "Delivery date: " + str(assignment.get_delivery_date()))
#             print("     " + "Percentage completed: " + str(assignment.get_perc_completed()) + "%")
#             print("     " + "Percentage missing: " + str(assignment.get_missing_perc()) + "%")
#             print("     " + "Time remaining: " + str(assignment.get_time_to_finish()) + " hours")
#             print("     " + "Percentage completed in 1 hour: " + str(assignment.get_perc_in1hr()) + "% in 1 hour")
#             print("     " + "Mandatory: " + str(assignment.get_mandatory()))
#             #print("     " + "Days remaining to delivery: " + str(assignment.get_days_remaining()))
#         elif type(assignment) == Exam:
#             print(assignment.get_name())
#             print("     " + "Delivery date: " + str(assignment.get_delivery_date()))
#             print("     " + "Percentage completed: " + str(assignment.get_perc_completed()) + "%")
#             print("     " + "Percentage missing: " + str(assignment.get_missing_perc()) + "%")
#             print("     " + "Time remaining: " + str(assignment.get_time_to_finish()) + " hours")
#     except IndexError:
#         print("That assignment doesn't exist!")


def display_in_order(instruction):
    (assignments, subject_name) = ordered_list()
    assignments.reverse()
    subject_name.reverse()
    i = 0
    i_subj = 0
    i_day = 1
    day = assignments[0].get_delivery_date()
    total_time = 0

    for assignm in assignments:
        (hours, minutes) = decimal_to_time(assignm.get_time_to_finish())
        if isinstance(assignm.get_delivery_date(), dt.datetime):
            assignm_delivery = assignm.get_delivery_date().date()
        else:
            assignm_delivery = assignm.get_delivery_date()

        if str(assignm_delivery) == str(day):
            # Sumar horas
            total_time += assignm.get_time_to_finish()
        else:
            (hours_day, minutes_day) = decimal_to_time(total_time)
            weekday = day.weekday()
            if weekday == 0:
                print("Monday")
            elif weekday == 1:
                print("Tuesday")
            elif weekday == 2:
                print("Wednesday")
            elif weekday == 3:
                print("Thursday")
            elif weekday == 4:
                print("Friday")
            elif weekday == 5:
                print("Saturday")
            elif weekday == 6:
                print("Sunday")
            print("Hours: " + str(hours_day))
            print("Minutes: " + str(minutes_day))
            print("")
            i = 0
            i_day = 1
            day = assignm_delivery
            total_time = assignm.get_time_to_finish()

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

        text = str(i_day) + ") Delivery: " + str(assignm_delivery) + " " + assignm.get_name() + " | " + \
            "Remaining time: " + str(hours) + " hours " + str(minutes) + \
            " minutes - " + subject_name[i_subj] + late + " {0}:{1}".format(
                assignm.get_start_time_hours_int(), assignm.get_start_time_minutes_int())

        print(text)

        i += 1
        i_day += 1
        i_subj += 1

    (hours, minutes) = decimal_to_time(total_time)
    weekday = day.weekday()
    if weekday == 0:
        print("Monday")
    elif weekday == 1:
        print("Tuesday")
    elif weekday == 2:
        print("Wednesday")
    elif weekday == 3:
        print("Thursday")
    elif weekday == 4:
        print("Friday")
    elif weekday == 5:
        print("Saturday")
    elif weekday == 6:
        print("Sunday")
    print("Hours: " + str(hours))
    print("Minutes: " + str(minutes))

    # try:
    #     if not (assignm.get_delivery_date() == assignments[i].get_delivery_date()):
    #         print("Hours: ")
    #         print("")
    #         i_day = 1
    # except IndexError:
    #     print("")


def display_mand(instruction):
    (assignments, subject_name) = ordered_list()
    assignments.reverse()
    subject_name.reverse()
    for assignm in assignments:
        if assignm.get_mandatory():
            print(assignm.get_name() + " Delivery: " +
                  str(assignm.get_delivery_date()))


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
                    print("     " + str(j) + ") " + assignm.get_name() + " | " + str(
                        assignm.get_perc_completed()) + "%" + " " + str(assignm.get_delivery_date()) + " " + mand)
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


def display_day(instruction):
    try:
        if(len(instruction) == 2):
            year = today.year
        elif(len(instruction) == 3):
            year = int(instruction[2])

        month = int(instruction[0])
        day = int(instruction[1])

        (assignments, subject_name) = ordered_list()
        assignments.reverse()
        subject_name.reverse()

        for assignm in assignments:
            if assignm.get_delivery_date() != dt.date(year, month, day):
                del assignm
            else:
                delivery = str(assignm.get_delivery_date())
                text = "Delivery: " + delivery + " " + assignm.get_name()
                print(text)

    except IndexError:
        print("Please enter the full instruction")
        print("disp d <month> <day>")
        print("or")
        print("disp d <month> <day> <year>")


def display_budget(instruction):

    print("Total budget: ${0}".format(total_budget.get_amount()))

    print("Real budget: ${0}".format(real_budget.get_amount()))

    print("Expected budget: ${0}".format(expected_budget.get_amount()))


# ----- display instruction ----

# ----- display rules ----
def display_rules(instruction):
    print("1. Hacer cada tarea con pomodoros")
    print("2. Si algo no urge, alternar entre lo que se entrega próximamente (LO QUE SE ENTREGA) y lo que está en la lista, ")
    print("de lo contrario, se perderá mucho tiempo")
    print("3. Son más importantes las tareas individuales que las de equipo")
# ----- display rules ----


# ----- add instruction ----
def add(instruction):
    noun_dict = {
        "s": add_subject,
        "hw": add_homework,
        "e": add_exam,
        "n": add_natma,
        "pc": add_personal_categ,
        "p": add_personal_assignment,
        "bud": add_budget
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
    try:
        if(len(instruction) == 1):
            year = today.year
        elif(len(instruction) == 2):
            year = int(instruction[1])

        subj_index = instruction[0]
        name = input("Name: ")
        delivery_date = dt.date(
            year, int(input("Month of delivery: ")), int(input("Day of delivery: ")))
        p1hr = float(input("Percentage done in 1 hour: "))
        startTime = dt.time(hour=0, minute=0)
        assignment = Homework(name, delivery_date, startTime, p1hr)
        school.get_subj_list()[int(subj_index)-1].add_assignm(assignment)
        save_in_school_file()

    except IndexError:
        print("Not enough elements to the instruction")
        print("Please enter \"add hw <subject index>\"")
        print("or")
        print("\"add hw <subject index> <year>\"")


def add_natma(instruction):
    try:
        if(len(instruction) == 0):
            year = today.year
        elif(len(instruction) == 1):
            year = int(instruction[0])

        name = input("Name: ")
        delivery_date = dt.date(
            year, int(input("Month: ")), int(input("Day: ")))
        perc1hr = float(input("Percentage in 1 hour: "))
        new_assignm = Homework(name, delivery_date, perc1hr)
        natma.add_assignm(new_assignm)
        save_in_natma_file()

    except IndexError:
        print("Not enough elements to the instruction")
        print("Please enter \"add n <subject index>\"")
        print("or")
        print("\"add n <year>\"")


def add_exam(instruction):
    try:
        if(len(instruction) == 1):
            year = today.year
        elif(len(instruction) == 2):
            year = int(instruction[1])

        subj_index = instruction[0]
        name = input("Name: ")
        date = dt.date(year, int(input("Month: ")), int(input("Day: ")))
        exam = Exam(name, date)
        school.get_subj_list()[int(subj_index)-1].add_assignm(exam)
        save_in_school_file()

    except IndexError:
        print("Not enough elements to the instruction")
        print("Please enter \"add e <subject index>\"")
        print("or")
        print("Please enter \"add e <subject index> <year>\"")


def add_personal_categ(instruction):
    try:
        value = instruction[0]
        for i in range(1, len(instruction)):
            value += " " + instruction[i]
        new_categ = Category(value.strip())
        personal.add_categ(new_categ)
        save_in_personal_file()
    except IndexError:
        print("Please enter the complete instruction: ")
        print("     add pc <category name>")


def add_personal_assignment(instruction):
    try:
        if(len(instruction) == 1):
            year = today.year
        elif(len(instruction) == 2):
            year = int(instruction[1])

        value = int(instruction[0]) - 1
        name = input("Name: ")
        p_input = input("Periodic? (y/n) ")
        if p_input == "True" or p_input == "true" or p_input == "t" or p_input == "yes" or p_input == "y" or p_input == "Y":
            periodic_instructions()
            periodic_type = int(
                input("Enter periodic instruction with integer: "))
            perc_in1hr = float(input("Percentage done in 1 hour: "))
            new_assingm = PersAssignmentPeriodic(
                name, periodic_type, perc_in1hr)
            personal.get_categ_list()[value].add_assignm(new_assingm)
            save_in_personal_file()
        elif p_input == "False" or p_input == "false" or p_input == "f" or p_input == "no" or p_input == "n" or p_input == "N":
            delivery_date = dt.date(
                year, int(input("Month: ")), int(input("Day: ")))
            perc_in1hr = float(input("Percentage done in 1 hour: "))
            new_assignm = PersAssignment(name, delivery_date, perc_in1hr)
            personal.get_categ_list()[value].add_assignm(new_assignm)
            save_in_personal_file()
        else:
            print("Creating a non-periodic assignment...")
            delivery_date = dt.date(
                year, int(input("Month: ")), int(input("Day: ")))
            perc_in1hr = float(input("Percentage done in 1 hour: "))
            new_assignm = PersAssignment(name, delivery_date, perc_in1hr)
            personal.get_categ_list()[value].add_assignm(new_assignm)
            save_in_personal_file()
    except (IndexError, ValueError, UnboundLocalError):
        print("Please enter the complete instruction: ")
        print("     add p <category index>")
        print("     or")
        print("     add p <category index> <year>")


def add_budget(instruction):
    amount = int(input("Amount: $"))
    if(instruction[0] == "t"):
        total_budget.set_amount(amount)
    elif(instruction[0] == "r"):
        real_budget.set_amount(amount)
    elif(instruction[0] == "e"):
        expected_budget.set_amount(amount)

    save_budget()
    display_budget(instruction)
# ----- add instruction ----


# ----- edit instruction ----
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
        "nmand": edit_mandatory_natma,
        "st": edit_start_time,
        "pst": edit_start_time_personal,
        "nst": edit_start_time_natma
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
    school.get_subj_list()[subj_index].get_assignm_list()[
        assignm_index].set_name(value)
    save_in_school_file()


def edit_name_personal(instruction):
    try:
        categ_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        value = instruction[2]
        for i in range(3, len(instruction)):
            value += " " + instruction[i]
        personal.get_categ_list()[categ_index].get_assignm_list()[
            assignm_index].set_name(value)
        save_in_personal_file()
    except (IndexError, ValueError):
        print("Please enter the full instruction:")
        print("edit pname <category index> <assignment index> <new name>")


def edit_perc_completed(instruction):
    try:
        subj_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        value = float(instruction[2])
        school.get_subj_list()[subj_index].get_assignm_list()[
            assignm_index].set_completed(value)
        if value >= 100:
            try:
                school.get_subj_list()[subj_index].set_as_completed(
                    assignm_index)
            except AttributeError:
                print("Subject has no attribute completed, creating one...")
                school.get_subj_list()[subj_index].create_completed_list()
                school.get_subj_list()[subj_index].set_as_completed(
                    assignm_index)
                print("Completed list created!")
        display_subj([instruction[0]])
        save_in_school_file()
    except IndexError:
        print("Please enter the full instruction:")
        print("     edit pcomp <subject index> <assignment index> <new value>")


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
        personal.get_categ_list()[categ_index].set_completed(
            assignm_index, value)
        save_in_personal_file()
    except IndexError:
        print("Please enter the full instruction:")
        print("     edit ppcomp <category index> <assignment index> <percentage>")


def edit_perc_1hr(instruction):
    try:
        subj_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        value = float(instruction[2])
        school.get_subj_list()[subj_index].get_assignm_list()[
            assignm_index].set_perc_in1hr(value)
        save_in_school_file()
    except IndexError:
        print("Please enter the full instruction:")
        print("     edit p1hr <subject index> <assignment index> <new value>")


def edit_perc_1hr_personal(instruction):
    categ_index = int(instruction[0]) - 1
    assignm_index = int(instruction[1]) - 1
    value = float(instruction[2])
    personal.get_categ_list()[categ_index].get_assignm_list()[
        assignm_index].set_perc_in1hr(value)
    save_in_personal_file()


def edit_delivery_date(instruction):
    try:
        if(len(instruction) == 2):
            year = dt.datetime.now().year
        elif(len(instruction) == 3):
            year = int(instruction[2])

        subj_index = instruction[0]
        assignm_index = instruction[1]
        delivery_date = dt.date(
            year, int(input("Month: ")), int(input("Day: ")))
        school.get_subj_list()[int(subj_index)-1].get_assignm_list()[
            int(assignm_index)-1].set_delivery_date(delivery_date)
        save_in_school_file()

    except IndexError:
        print("Please enter the full instruction:")
        print("     edit delivery <subject index> <assignment index>")
        print("     or")
        print("     edit delivery <subject index> <assignment index> <year>")


def edit_delivery_date_natma(instruction):
    try:
        if(len(instruction) == 1):
            year = dt.datetime.now().year
        elif(len(instruction) == 2):
            year = int(instruction[1])

        assignm_index = int(instruction[0]) - 1
        delivery_date = dt.date(
            year, int(input("Month: ")), int(input("Day: ")))
        natma.get_assignm_list()[assignm_index].set_delivery_date(
            delivery_date)
        save_in_natma_file()

    except IndexError:
        print("Please enter the full instruction:")
        print("     edit ndelivery <assignment index>")
        print("     or")
        print("     edit ndelivery <assignment index> <year>")


def edit_delivery_date_personal(instruction):
    try:
        if(len(instruction) == 2):
            year = dt.datetime.now().year
        elif(len(instruction) == 3):
            year = int(instruction[2])

        categ_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        delivery_date = dt.date(
            year, int(input("Month: ")), int(input("Day: ")))
        personal.get_categ_list()[categ_index].get_assignm_list()[
            assignm_index].set_delivery_date(delivery_date)
        save_in_personal_file()

    except IndexError:
        print("Please enter the full instruction:")
        print("     edit pdelivery <category index> <assignment index>")
        print("     or")
        print("     edit pdelivery <category index> <assignment index> <year>")


def edit_mandatory(instruction):
    try:
        subj_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        if instruction[2] == "True" or instruction[2] == "true" or instruction[2] == "t":
            new_value = True
        elif instruction[2] == "False" or instruction[2] == "false" or instruction[2] == "f":
            new_value = False
            assignm = school.get_subj_list()[subj_index].get_assignm_list()[
                assignm_index]
            if assignm.get_delivery_date() < today.date():
                assignm.set_delivery_date(today.date())
        else:
            print("Setting value as True")
            new_value = True
        school.get_subj_list()[subj_index].get_assignm_list()[
            assignm_index].set_mandatory(new_value)
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
            natma.get_assignm_list()[int(
                assignm_index) - 1].set_delivery_date(today.date)
    else:
        print("Setting value as True")
        new_value = True
    natma.get_assignm_list()[int(assignm_index)-1].set_mandatory(new_value)
    save_in_natma_file()


def edit_start_time(instruction):
    try:
        subj_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        new_value = dt.time(hour=int(input("Hour: ")),
                            minute=int(input("Minute: ")))
        school.get_subj_list()[subj_index].get_assignm_list()[
            assignm_index].set_start_time(new_value)
        save_in_school_file()
    except IndexError:
        print("Not enough info.")


def edit_start_time_personal(instruction):
    try:
        category_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        new_value = dt.time(hour=int(input("Hour: ")),
                            minute=int(input("Minute: ")))
        personal.get_categ_list()[category_index].get_assignm_list()[
            assignm_index].set_start_time(new_value)
        save_in_personal_file()
    except IndexError:
        print("Not enough info.")


def edit_start_time_natma(instruction):
    try:
        assignm_index = int(instruction[0])
        new_value = dt.time(hour=input("Hour: "), minute=input("Minute: "))
        natma.get_assignm_list()[int(assignm_index) -
                                 1].set_start_time(new_value)
        save_in_natma_file()
    except IndexError:
        print("Not enough info.")
# ----- edit instruction ----


# ----- remove instruction ----
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
            display_subj([instruction[0]])
        elif len(instruction) == 1:
            confirmation = input(
                "Are you sure you want to remove {0}? y/n: ".format(school.get_subj_list()[subj].get_name()))
            while (confirmation != "y") and (confirmation != "n"):
                confirmation = input(
                    "Are you sure you want to remove {0}? y/n: ".format(school.get_subj_list()[subj].get_name()))
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
# ----- remove instruction ----


# ----- push instruction ----
def push(instruction):
    noun = instruction[0]
    del instruction[0]
    noun_dict = {
        "s": push_school,
        "p": push_personal,
        "n": push_natma,
        "d": push_day,
        "a": push_all_day
    }
    if noun in noun_dict:
        noun_dict[noun](instruction)
    else:
        print("Please use a valid noun")


def push_school(instruction):
    try:
        subj_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        new_date = school.get_subj_list()[subj_index].get_assignm_list(
        )[assignm_index].get_delivery_date() + dt.timedelta(days=1)
        school.get_subj_list()[subj_index].get_assignm_list()[
            assignm_index].set_delivery_date(new_date)
        save_in_school_file()
        display_subj(instruction)
    except IndexError:
        print("Please enter the full instrucion:")
        print("     push s <subject index> <assignment index>")


def push_natma(instruction):
    try:
        assignm_index = int(instruction[0]) - 1
        new_date = natma.get_assignm_list(
        )[assignm_index].get_delivery_date() + dt.timedelta(days=1)
        natma.get_assignm_list()[assignm_index].set_delivery_date(new_date)
        save_in_natma_file()
        display_natma(instruction)
    except IndexError:
        print("Please enter the full instrucion:")
        print("    push n <assignm index>")


def push_personal(instruction):
    try:
        categ_index = int(instruction[0]) - 1
        assignm_index = int(instruction[1]) - 1
        new_date = personal.get_categ_list()[categ_index].get_assignm_list()[
            assignm_index].get_delivery_date() + dt.timedelta(days=1)
        personal.get_categ_list()[categ_index].get_assignm_list()[
            assignm_index].set_delivery_date(new_date)
        save_in_personal_file()
        display_pers(instruction)
    except IndexError:
        print("Please enter the full instrucion:")
        print("     push s <subject index> <assignment index>")


def push_day(instruction):
    try:
        if(len(instruction) == 2):
            year = today.year
        elif(len(instruction) == 3):
            year = int(instruction[2])

        month = int(instruction[0])
        day = int(instruction[1])

        # Function that returns 4 lists: assignments, list, category index, assignment index
        (assignments, list_name, category_index,
         assignm_index) = assignments_ordered()

        day_assignments = []
        day_assignments_list_name = []
        day_category_index = []
        day_assignm_index = []

        for assignm in assignments:
            index = assignments.index(assignm)
            if assignm.get_delivery_date() == dt.date(year, month, day):
                day_assignments.append(assignm)
                day_assignments_list_name.append(list_name[index])
                day_category_index.append(category_index[index])
                day_assignm_index.append(assignm_index[index])

        day_assignments.reverse()
        day_assignments_list_name.reverse()
        day_category_index.reverse()
        day_assignm_index.reverse()

        print("--------------------------")
        for assignm in day_assignments:
            index = day_assignments.index(assignm)
            delivery = str(assignm.get_delivery_date())
            text = str(index) + ": Delivery: " + delivery + " " + \
                assignm.get_name() + " | " + day_assignments_list_name[index]
            print(text)

        print("..................")
        print(str(len(day_assignments)) + ": End pushing")

        push_index = int(input("push: "))

        while(push_index != len(day_assignments)):
            if day_assignments_list_name[push_index] == "Natma":
                push_natma([day_assignm_index[push_index] + 1])
            elif day_assignments_list_name[push_index] == "Personal":
                push_personal([day_category_index[push_index] +
                              1, day_assignm_index[push_index] + 1])
            else:
                push_school([day_category_index[push_index] + 1,
                            day_assignm_index[push_index] + 1])

            (assignments, list_name, category_index,
             assignm_index) = assignments_ordered()

            day_assignments = []
            day_assignments_list_name = []
            day_category_index = []
            day_assignm_index = []

            for assignm in assignments:
                index = assignments.index(assignm)
                if assignm.get_delivery_date() == dt.date(year, month, day):
                    day_assignments.append(assignm)
                    day_assignments_list_name.append(list_name[index])
                    day_category_index.append(category_index[index])
                    day_assignm_index.append(assignm_index[index])

            day_assignments.reverse()
            day_assignments_list_name.reverse()
            day_category_index.reverse()
            day_assignm_index.reverse()

            print("--------------------------")
            for assignm in day_assignments:
                index = day_assignments.index(assignm)
                delivery = str(assignm.get_delivery_date())
                text = str(index) + ": Delivery: " + delivery + " " + \
                    assignm.get_name() + " | " + \
                    day_assignments_list_name[index]
                print(text)

            print("..................")
            print(str(len(day_assignments)) + ": End pushing")
            push_index = int(input("push: "))

    except (IndexError, ValueError):
        print("Please enter the full instruction")
        print("     push d <month> <day>")


def push_all_day(instruction):
    try:
        if(len(instruction) == 2):
            year = today.year
        elif(len(instruction) == 3):
            year = int(instruction[2])

        month = int(instruction[0])
        day = int(instruction[1])

        # Function that returns 4 lists: assignments, list, category index, assignment index
        (assignments, list_name, category_index,
         assignm_index) = assignments_ordered()

        day_assignments = []
        day_assignments_list_name = []
        day_category_index = []
        day_assignm_index = []

        for assignm in assignments:
            index = assignments.index(assignm)
            if assignm.get_delivery_date() == dt.date(year, month, day):
                day_assignments.append(assignm)
                day_assignments_list_name.append(list_name[index])
                day_category_index.append(category_index[index])
                day_assignm_index.append(assignm_index[index])

        day_assignments.reverse()
        day_assignments_list_name.reverse()
        day_category_index.reverse()
        day_assignm_index.reverse()

        for assignm in day_assignments:
            push_index = day_assignments.index(assignm)
            if day_assignments_list_name[push_index] == "Natma":
                push_natma([day_assignm_index[push_index] + 1])
            elif day_assignments_list_name[push_index] == "Personal":
                push_personal([day_category_index[push_index] +
                              1, day_assignm_index[push_index] + 1])
            else:
                push_school([day_category_index[push_index] + 1,
                            day_assignm_index[push_index] + 1])

    except (IndexError):
        print("Please enter the full instruction")
        print("     push d <month> <day>")
# ----- push instruction ----


# ----- remaining hours ----
def remaining_hrs(instruction):
    try:
        if(len(instruction) == 2):
            year = today.year
        elif(len(instruction) == 3):
            year = int(instruction[2])

        month = int(instruction[0])
        day = int(instruction[1])
        (assignments, subj_name) = ordered_list()

        time_total = 0
        time_mandatory = 0
        time_non_mandatory = 0
        for assignm in assignments:
            if assignm.get_delivery_date() <= dt.date(year, month, day):
                if assignm.get_mandatory():
                    time_mandatory += assignm.get_time_to_finish()
                elif not assignm.get_mandatory():
                    time_non_mandatory += assignm.get_time_to_finish()
        time_total = time_mandatory + time_non_mandatory
        (hours_mandatory, minutes_mandatory) = decimal_to_time(time_mandatory)
        (hours_non_mandatory, minutes_non_mandatory) = decimal_to_time(
            time_non_mandatory)
        (hours_total, minutes_total) = decimal_to_time(time_total)
        print("Time remaining to complete assignments until " +
              str(day) + " of " + str(month))
        print("............................................................................................")
        print("Mandatory assignments: " + str(hours_mandatory) +
              " hours " + str(minutes_mandatory) + " minutes")
        print("Non-mandatory assignments: " + str(hours_non_mandatory) +
              " hours " + str(minutes_non_mandatory) + " minutes")
        print("Total: " + str(hours_total) + " hours " +
              str(minutes_total) + " minutes")

    except IndexError:
        print("Not enough data")

# ----- remaining hours ----


# ----- What to do ----
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
            param_list.append(assignm.get_delivery_date() -
                              dt.timedelta(days=hours))
            #print(str(i) + ") " + assignm.get_name() + " - Missing time: " + str(hours) + " hours, " + str(minutes) + " minutes " + "Delivery: " + str(assignm.get_delivery_date()))
        elif not assignm.get_mandatory() and ((assignm.get_delivery_date() - dt.timedelta(days=hours)) <= today.date()):
            non_mand_list.append(assignm)
            non_mand_param_list.append(
                assignm.get_delivery_date() - dt.timedelta(days=hours))

    to_do_list = order_list(to_do_list, param_list)
    non_mand_list = order_list(non_mand_list, non_mand_param_list)
    to_do_list = urgent_list + to_do_list + non_mand_list

    for assignm in to_do_list:
        (hours, minutes) = decimal_to_time(assignm.get_time_to_finish())
        print(str(i) + ") " + assignm.get_name() + " - Missing time: " + str(hours) + " hours, " +
              str(minutes) + " minutes " + "Delivery: " + str(assignm.get_delivery_date()))
        i += 1
# ----- What to do ----

# ----- help ----


def get_instructions(instruction):
    f = open("instructions.txt", "r")
    instructions = f.read()
    print(instructions)
    f.close()
# ----- help ----

# update_deliveries()

# ----------------------------------------------------------------------------
# GUI
# from PyQt5 import QtCore, QtGui, QtWidgets
# from MainWindow import Ui_MainWindow, Ui_AddScreen
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QLabel, QScrollArea, QVBoxLayout, QMainWindow, QStackedWidget)
# from PyQt5.QtCore import Qt

# import pandas as pd

# import sys


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Prepare assignments to send
#     (assignments, subject_name) = ordered_list()
#     assignments.reverse()
#     subject_name.reverse()

#     mainWindow = Ui_MainWindow()
#     mainWindow.show()

#     sys.exit(app.exec_())

verb_dict = {
    "disp": display,
    "add": add,
    "edit": edit,
    "rem": remove,
    "push": push,
    "h": remaining_hrs,
    "now": what_to_do,
    "help": get_instructions,
    "q": exit
}

(school, natma, personal) = read_files()

#(total_budget, real_budget, expected_budget) = read_budget()
available_time_per_day = dt.timedelta(0, 0, 0, 0, 0, 4)
today = dt.datetime.today()

# for category in personal.get_categ_list():
#     for assignment in category.get_assignm_list():
#         if isinstance(assignment, PersAssignmentPeriodic) and assignment.get_periodic_type() == 0:
#             weekly_start_times = []
#             for i in range(7):
#                 weekly_start_times.append(assignment.get_start_time()[0])
#             print(weekly_start_times)
#             assignment.set_weekly_start_times(weekly_start_times)
#             print("Added weekly start times")
# for i in range(len(assignment.get_start_time())):
# if isinstance(assignment.get_start_time()[i], int):
#     start_times = assignment.get_start_time()
#     start_times[i] = dt.time(hour=0, minute=0)
#     assignment.set_start_time(start_times)
#     print("Changed")
# for category in school.get_subj_list():
#     for assignment in category.get_assignm_list():
#         if isinstance(assignment, PersAssignmentPeriodic) and assignment.get_periodic_type() == 0:
#             weekly_start_times = []
#             for i in range(7):
#                 weekly_start_times.append(assignment.get_start_time())
#             assignment.set_weekly_start_times(weekly_start_times)


# Correr cada dia
# for category in school.get_subj_list() + personal.get_categ_list():
#     for assignment in category.get_assignm_list():
#         if isinstance(assignment, PersAssignmentPeriodic) and assignment.get_periodic_type() == 0:
#             for i in range(len(assignment.get_start_time())):
#                 if isinstance(assignment.get_start_time()[i], int):
#                     start_times = assignment.get_start_time()
#                     start_times[i] = dt.time(hour=0, minute=0)
#                     assignment.set_start_time(start_times)
#                     print("Changed")
# save_in_personal_file()
# save_in_school_file()

# Borrar subject
# print("Deliting " + school.get_subj_list()[26].get_name())
# del school.get_subj_list()[26]
# save_in_school_file()

# for category in school.get_subj_list() + personal.get_categ_list():
#     for assignment in category.get_assignm_list():
#         if isinstance(assignment, PersAssignmentPeriodic) and assignment.get_periodic_type() == 1:
#             start_times = assignment.get_start_time()
#             print(start_times)
#         if assignment.get_name() == "Ver House of the Dragon":
#             start_times = []
#             for i in range(4):
#                 start_times.append(dt.time(20, 0))
#             print(start_times)
#             print("El bueno")
#             assignment.set_start_time(start_times)
#             print("Ahora el modificado:")
#             print(assignment.get_start_time())
# save_in_personal_file()


# while True:
#     run_instruc(get_input())

# Set color to categories
# for category in school.get_subj_list():
#     for assignment in category.get_assignm_list():
#         assignment.set_color_string("lightgrey")
# save_in_school_file()

# for category in personal.get_categ_list():
#     for assignment in category.get_assignm_list():
#         assignment.set_color_string("lightgrey")
# save_in_personal_file()

# TODO: display one assignment
# TODO: clean up code
# TODO: display difference in instruction now
# TODO: set date of subject
# TODO: set recomended date based on duration and delivery date
# TODO: create gui
