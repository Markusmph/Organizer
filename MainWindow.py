# from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QLabel, QScrollArea, QVBoxLayout, QMainWindow, QStackedWidget)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDateTime
from datetime import *

import math
import pickle as pk
import pandas as pd

from Classes.Ambits import Ambit, School, Subject, Natma, Personal, Category
from Classes.Assignments import Assignment, Homework, Exam, PersAssignment, PersAssignmentPeriodic


# Import assignments
pickle_in = open("school.pickle", "rb")
school = pk.load(pickle_in)
pickle_in.close()
pickle_in = open("natma.pickle", "rb")
natma = pk.load(pickle_in)
pickle_in.close()
pickle_in = open("personal.pickle", "rb")
personal = pk.load(pickle_in)
pickle_in.close()


def save_in_school_file():
    pickle_out = open("school.pickle", "wb")
    pk.dump(school, pickle_out)
    pickle_out.close()


def save_in_personal_file():
    pickle_out = open("personal.pickle", "wb")
    pk.dump(personal, pickle_out)
    pickle_out.close()


def update_assignments():

    # School
    for subject in school.get_subj_list():
        for assignment in subject.get_assignm_list():
            date1 = assignment.get_delivery_date()
            date2 = datetime.today()
            if isinstance(date1, date):
                date1 = datetime.combine(date1, datetime.min.time())
            if isinstance(date2, date):
                date2 = datetime.combine(date2, datetime.min.time())
            if date1 < date2:
                subject_index = school.get_subj_list().index(subject)
                assignment_index = subject.get_assignm_list().index(assignment)
                school.get_subj_list()[subject_index].get_assignm_list()[
                    assignment_index].set_delivery_date(datetime.today())
                save_in_school_file()

            if isinstance(assignment, PersAssignmentPeriodic):
                if assignment.get_periodic_type() == 0:
                    days_difference = date2 - date1
                    for i in range(days_difference.days):
                        # Start times
                        start_times = school.get_subj_list()[subject_index].get_assignm_list()[
                            assignment_index].get_start_time()
                        lastDay = assignment.get_delivery_date() + timedelta(days=len(start_times))
                        start_time_eliminated = start_times.pop(0)
                        new_start_time = assignment.get_weekly_start_times()[
                            lastDay.weekday()]
                        start_times.append(new_start_time)
                        school.get_subj_list()[subject_index].get_assignm_list()[
                            assignment_index].set_start_time(start_times)
                save_in_school_file()

    # Personal
    for subject in personal.get_categ_list():
        for assignment in subject.get_assignm_list():
            date1 = assignment.get_delivery_date()
            date2 = datetime.today()
            if isinstance(date1, date):
                date1 = datetime.combine(date1, datetime.min.time())
            if isinstance(date2, date):
                date2 = datetime.combine(date2, datetime.min.time())
            if date1 < date2:
                subject_index = personal.get_categ_list().index(subject)
                assignment_index = subject.get_assignm_list().index(assignment)
                # personal.get_categ_list()[subject_index].get_assignm_list()[
                #     assignment_index].set_delivery_date(datetime.today())
                # Rotate list values in periodic assignments
                if isinstance(assignment, PersAssignmentPeriodic):
                    if assignment.get_periodic_type() == 0:
                        days_difference = date2 - date1
                        for i in range(days_difference.days):
                            # Delivery date
                            personal.get_categ_list()[subject_index].get_assignm_list()[
                                assignment_index].set_delivery_date(assignment.get_delivery_date() + timedelta(days=1))
                            # Start times
                            start_times = personal.get_categ_list()[subject_index].get_assignm_list()[
                                assignment_index].get_start_time()
                            lastDay = assignment.get_delivery_date() + timedelta(days=len(start_times))
                            start_time_eliminated = start_times.pop(0)
                            new_start_time = assignment.get_weekly_start_times()[
                                lastDay.weekday()]
                            start_times.append(new_start_time)
                            personal.get_categ_list()[subject_index].get_assignm_list()[
                                assignment_index].set_start_time(start_times)
                            # p1hr
                            p1hrList = personal.get_categ_list()[subject_index].get_assignm_list()[
                                assignment_index].get_perc_in1hr()
                            p1hrList.append(p1hrList.pop(0))
                            personal.get_categ_list()[subject_index].get_assignm_list()[
                                assignment_index].set_perc_in1hr(p1hrList)
                            # # pcomp
                            # pcompList = personal.get_categ_list()[subject_index].get_assignm_list()[
                            #     assignment_index].get_perc_completed()
                            # pcompList.append(pcompList.pop(0))
                            # personal.get_categ_list()[subject_index].get_assignm_list()[
                            #     assignment_index].set_perc_completed(pcompList)
                    elif assignment.get_periodic_type() == 1:
                        days_difference = date2 - date1
                        for i in range(days_difference.days):
                            # Delivery date
                            personal.get_categ_list()[subject_index].get_assignm_list()[
                                assignment_index].set_delivery_date(assignment.get_delivery_date() + timedelta(days=1))
                else:
                    subject_index = personal.get_categ_list().index(subject)
                    assignment_index = subject.get_assignm_list().index(assignment)
                    personal.get_categ_list()[subject_index].get_assignm_list()[
                        assignment_index].set_delivery_date(datetime.today())

                save_in_personal_file()


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_Main_screen()

    def create_Main_screen(self):
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.gridbox = QGridLayout()

        self.widget.setLayout(self.gridbox)
        update_assignments()  # Update assignment dates

        # Order assignments in a single list
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
                    if isinstance(date1, date):
                        date1 = datetime.combine(date1, datetime.min.time())
                    if isinstance(date2, date):
                        date2 = datetime.combine(date2, datetime.min.time())
                    if date1 > date2:
                        (assignments[i-1], assignments[j]
                         ) = (assignments[j], assignments[i-1])
                        (subject_name[i-1], subject_name[j]
                         ) = (subject_name[j], subject_name[i-1])
                        j = i
                    else:
                        j += 1

        self.daysToShow = daysToShow

        w, h = self.daysToShow, 48
        self.used_matrix = [[False for i in range(w)] for j in range(h)]
        self.simultaneous_matrix = [
            [False for i in range(w)] for j in range(h)]

        # Add days and assignments to grid
        for i in range(self.daysToShow):
            # Add day label
            day = date.today() + timedelta(days=i)
            weekday = day.weekday()
            if weekday == 0:
                weekday_str = "Monday"
            elif weekday == 1:
                weekday_str = "Tuesday"
            elif weekday == 2:
                weekday_str = "Wednesday"
            elif weekday == 3:
                weekday_str = "Thursday"
            elif weekday == 4:
                weekday_str = "Friday"
            elif weekday == 5:
                weekday_str = "Saturday"
            elif weekday == 6:
                weekday_str = "Sunday"
            label_day = QLabel(str(day) + " " + weekday_str)
            label_day.setStyleSheet("background-color: lightgreen")
            self.gridbox.addWidget(label_day, 0, i+2)

            # Add assignments
            for assignment in assignments:
                if isinstance(assignment, PersAssignmentPeriodic):
                    if assignment.get_periodic_type() == 0:  # Daily
                        # try:
                        hour_index = getTimeIndex(
                            assignment.get_start_time()[i]) + 1
                        # hour_index = (int(assignment.get_start_time()[
                        #     i].hour)*2) + round(int(assignment.get_start_time()[i].minute) / 30) + 1
                        # except AttributeError:
                        #     print(assignment.get_start_time()[i])
                        time_blocks = round(
                            assignment.get_time_to_finish(i) / 0.5)
                        next_day = 0
                        for j in range(time_blocks):
                            label_assignment = QLabel(assignment.get_name())
                            if hour_index + j > 48:
                                hour_index = 1 - j
                                if i < self.daysToShow - 1:
                                    next_day = 1
                                else:
                                    break
                            if self.used_matrix[hour_index + j - 1][i + next_day]:
                                color = "red"
                                self.simultaneous_matrix[hour_index +
                                                         j - 1][i + next_day] = True
                            else:
                                color = assignment.get_color_string()
                                self.used_matrix[hour_index +
                                                 j - 1][i + next_day] = True
                            self.gridbox.addWidget(
                                label_assignment, hour_index+j, i+2 + next_day)
                            label_assignment.setStyleSheet(
                                "background-color: {0}".format(color))
                    elif assignment.get_periodic_type() == 1:  # Weekly
                        date1 = assignment.get_delivery_date()
                        date2 = day
                        if isinstance(date1, date):
                            date1 = datetime.combine(
                                date1, datetime.min.time())
                        if isinstance(date2, date):
                            date2 = datetime.combine(
                                date2, datetime.min.time())
                        if assignment.get_weekly_periodic_day_int() == weekday and date1 <= date2:
                            dayDifference = date2 - date1
                            periodicIndex = math.floor(
                                dayDifference.days / 7)
                            if periodicIndex < 4:
                                hour_index = (assignment.get_start_time_hours_int()[
                                    periodicIndex]*2) + round(assignment.get_start_time_minutes_int()[periodicIndex] / 30) + 1
                                # hour_index = (int(assignment.get_start_time()[
                                #     periodicIndex].hour)*2) + round(int(assignment.get_start_time()[periodicIndex].minute) / 30) + 1
                                time_blocks = round(
                                    assignment.get_time_to_finish(periodicIndex) / 0.5)
                                next_day = 0
                                for j in range(time_blocks):
                                    label_assignment = QLabel(
                                        assignment.get_name())
                                    if hour_index + j > 48:
                                        hour_index = 1 - j
                                        if i < self.daysToShow - 1:
                                            next_day = 1
                                        else:
                                            break
                                    if self.used_matrix[hour_index + j - 1][i + next_day]:
                                        color = "red"
                                        self.simultaneous_matrix[hour_index +
                                                                 j - 1][i + next_day] = True
                                    else:
                                        color = assignment.get_color_string()
                                        self.used_matrix[hour_index +
                                                         j - 1][i + next_day] = True
                                    self.gridbox.addWidget(
                                        label_assignment, hour_index+j, i+2 + next_day)
                                    label_assignment.setStyleSheet(
                                        "background-color: {0}".format(color))

                else:
                    if assignment.get_delivery_date().strftime("%d/%m/%y") == day.strftime("%d/%m/%y"):
                        hour_index = assignment.get_start_time_hours_int(
                        ) * 2 + round(assignment.get_start_time_minutes_int() / 30) + 1
                        time_blocks = round(
                            assignment.get_time_to_finish() / 0.5)
                        next_day = 0
                        for j in range(time_blocks):
                            label_assignment = QLabel(assignment.get_name())
                            if hour_index + j > 48:
                                hour_index = 1 - j
                                if i < self.daysToShow - 1:
                                    next_day = 1
                                else:
                                    break
                            if self.used_matrix[hour_index + j - 1][i + next_day]:
                                color = "red"
                                self.simultaneous_matrix[hour_index +
                                                         j - 1][i + next_day] = True
                            else:
                                self.used_matrix[hour_index +
                                                 j - 1][i + next_day] = True
                                color = assignment.get_color_string()
                                # if subject_name[assignments.index(assignment)] == "Personal":
                                #     color = "lightblue"
                                # else:
                                #     color = "lightgrey"
                            self.gridbox.addWidget(
                                label_assignment, hour_index+j, i+2 + next_day)
                            label_assignment.setStyleSheet(
                                "background-color: {0}".format(color))

        # Add hours to grid
        for i in range(48):
            time = datetime.strptime("00:00", "%H:%M") + timedelta(hours=0.5*i)
            label = QLabel("{0}".format(str(time.time()))[:-3])
            # label = QLabel("{0}".format(str(i+1)))
            label.setStyleSheet("background-color: lightgreen")
            self.gridbox.addWidget(label, i+1, 1)

        # Add Buttons
        grid_position = 0
        addActivityButton = QPushButton("Add activity")
        self.gridbox.addWidget(addActivityButton, grid_position, 0)
        addActivityButton.clicked.connect(self.gotoAddActivityScreen)

        grid_position = grid_position + 1
        addSubjectButton = QPushButton("Add subject")
        self.gridbox.addWidget(addSubjectButton, grid_position, 0)
        addSubjectButton.clicked.connect(self.gotoAddSubjectScreen)

        grid_position = grid_position + 1
        edit_button = QPushButton("Edit activity")
        self.gridbox.addWidget(edit_button, grid_position, 0)
        edit_button.clicked.connect(self.gotoEditScreen)

        grid_position = grid_position + 1
        edit_subject_button = QPushButton("Edit subject")
        self.gridbox.addWidget(edit_subject_button, grid_position, 0)
        edit_subject_button.clicked.connect(self.gotoEditSubjectScreen)

        grid_position = grid_position + 1
        simultaneous_button = QPushButton("Edit simultaneous activities")
        self.gridbox.addWidget(simultaneous_button, grid_position, 0)
        simultaneous_button.clicked.connect(self.gotoSimultaneousScreen)

        grid_position = grid_position + 1
        pushActivityButton = QPushButton("Push activity")
        self.gridbox.addWidget(pushActivityButton, grid_position, 0)
        pushActivityButton.clicked.connect(self.gotoPushActivityScreen)

        grid_position = grid_position + 1
        pushSubjectButton = QPushButton("Push subject")
        self.gridbox.addWidget(pushSubjectButton, grid_position, 0)
        pushSubjectButton.clicked.connect(self.gotoPushSubjectScreen)

        grid_position = grid_position + 1
        pushSubjectButton = QPushButton("Push day")
        self.gridbox.addWidget(pushSubjectButton, grid_position, 0)
        pushSubjectButton.clicked.connect(self.gotoPushDayScreen)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Organizer')
        self.show()

    def gotoAddActivityScreen(self):
        addActivityScreen = Ui_AddActivityScreen()
        widget.addWidget(addActivityScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoAddSubjectScreen(self):
        addSubjectScreen = Ui_AddSubjectScreen()
        widget.addWidget(addSubjectScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoEditScreen(self):
        editScreen = Ui_EditScreen()
        widget.addWidget(editScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoEditSubjectScreen(self):
        editSubjectScreen = Ui_EditSubjectScreen()
        widget.addWidget(editSubjectScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoSimultaneousScreen(self):
        simultaneousScreen = Ui_SimultaneousScreen(self.simultaneous_matrix)
        widget.addWidget(simultaneousScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoPushActivityScreen(self):
        pushActivityScreen = Ui_PushActivityScreen(self.used_matrix)
        widget.addWidget(pushActivityScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoPushSubjectScreen(self):
        pushSubjectScreen = Ui_PushSubjectScreen()
        widget.addWidget(pushSubjectScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoPushDayScreen(self):
        pushDayScreen = Ui_PushDayScreen()
        widget.addWidget(pushDayScreen)
        widget.setCurrentIndex(widget.count() - 1)


class Ui_AddActivityScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()

        # Form
        self.form = QFormLayout()

        # creating the form
        self.assignmentNameLineEdit = QLineEdit()  # Assignment name
        self.form.addRow(QLabel("Activity name"), self.assignmentNameLineEdit)

        self.categoryComboBox = QComboBox()  # Category list
        self.categoryComboBox.addItems(["School", "Personal"])
        self.categoryComboBox.currentTextChanged.connect(
            self.onCategoryComboboxChanged)
        self.form.addRow(QLabel("Category"), self.categoryComboBox)

        self.subjectComboBox = QComboBox()  # Subject
        subject_names = []
        for subject in school.get_subj_list():
            subject_names.append(subject.get_name())
        # for category in personal.get_categ_list():
        #     subject_names.append(category.get_name())
        self.subjectComboBox.addItems(subject_names)
        self.form.addRow(QLabel("Subject"), self.subjectComboBox)

        self.deliveryDateEdit = QDateEdit(calendarPopup=True)  # Delivery date
        self.deliveryDateEdit.setDateTime(QDateTime.currentDateTime())
        self.form.addRow(QLabel("Delivery date"), self.deliveryDateEdit)

        self.startTimeHoursSpinBox = QSpinBox()  # Start time hour
        self.form.addRow(QLabel("Start time hours"),
                         self.startTimeHoursSpinBox)
        self.startTimeMinutesSpinBox = QSpinBox()  # Start time minutes
        self.form.addRow(QLabel("Start time minutes"),
                         self.startTimeMinutesSpinBox)

        self.p1hrLineEdit = QLineEdit()  # Percentage in 1 hour
        self.form.addRow(QLabel("Percentage in 1 hour"), self.p1hrLineEdit)

        self.periodicCheckBox = QCheckBox()  # Periodic
        self.periodicCheckBox.stateChanged.connect(self.periodicCheckBoxClick)
        self.form.addRow(QLabel("Periodic"), self.periodicCheckBox)
        self.new_assignment_periodic = False

        self.periodicComboBox = QComboBox()  # Category list
        self.periodicComboBox.addItems(
            ["Daily", "Weekly", "Monthly", "Yearly"])
        self.periodicComboBox.currentTextChanged.connect(
            self.onPeriodicComboboxChanged)
        self.form.addRow(QLabel("Periodic"), self.periodicComboBox)

        self.formGroupBox = QGroupBox("Adding activity")
        self.formGroupBox.setLayout(self.form)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.gotoMainScreen)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)

        self.widget.setLayout(mainLayout)

        self.setCentralWidget(self.widget)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Organizer')

    def gotoMainScreen(self):
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def getInfo(self):
        assignment_name = self.assignmentNameLineEdit.text()
        category = self.categoryComboBox.currentText()
        subject_index = self.subjectComboBox.currentIndex()
        # if category == "School":
        #     subject_index =
        # elif category == "Personal":
        #     pass
        # else:
        #     raise Exception("The category selected does not exist")

        # if subject_index >= len(school.get_subj_list()):
        #     subject_index_personal_list = subject_index - \
        #         len(school.get_subj_list())
        delivery_date = datetime.strptime(
            self.deliveryDateEdit.date().toString("yyyy/MM/dd"), '%Y/%m/%d')
        start_time_hours = int(self.startTimeHoursSpinBox.text())
        start_time_minutes = int(self.startTimeMinutesSpinBox.text())
        start_time = time(hour=start_time_hours, minute=start_time_minutes)
        p1hr = float(self.p1hrLineEdit.text())
        periodic = self.periodicComboBox.currentText()
        if periodic == "Daily":
            periodic_number = 0
        elif periodic == "Weekly":
            periodic_number = 1
        elif periodic == "Monthly":
            periodic_number = 2
        elif periodic == "Yearly":
            periodic_number = 3

        if category == "School":
            if self.new_assignment_periodic:
                if periodic_number == 0:  # Daily
                    start_time_list = []
                    p1hrList = []
                    pcompList = []
                    for i in range(30):
                        start_time_list.append(start_time)
                        p1hrList.append(p1hr)
                        pcompList.append(0)
                    new_assignment = PersAssignmentPeriodic(
                        assignment_name, delivery_date, periodic_number, start_time_list, perc_in_1hr=p1hrList, perc_completed=pcompList)
                    school.get_subj_list()[subject_index].add_assignm(
                        new_assignment)
                if periodic_number == 1:  # Weekly
                    start_time_list = []
                    p1hrList = []
                    pcompList = []
                    for i in range(4):
                        start_time_list.append(start_time)
                        p1hrList.append(p1hr)
                        pcompList.append(0)
                    if self.weeklyComboBox.currentText() == "Monday":
                        weeklyPeriodicDayInt = 0
                    elif self.weeklyComboBox.currentText() == "Tuesday":
                        weeklyPeriodicDayInt = 1
                    elif self.weeklyComboBox.currentText() == "Wednesday":
                        weeklyPeriodicDayInt = 2
                    elif self.weeklyComboBox.currentText() == "Thursday":
                        weeklyPeriodicDayInt = 3
                    elif self.weeklyComboBox.currentText() == "Friday":
                        weeklyPeriodicDayInt = 4
                    elif self.weeklyComboBox.currentText() == "Saturday":
                        weeklyPeriodicDayInt = 5
                    elif self.weeklyComboBox.currentText() == "Sunday":
                        weeklyPeriodicDayInt = 6
                    new_assignment = PersAssignmentPeriodic(
                        assignment_name, delivery_date, periodic_number, start_time_list, perc_in_1hr=p1hrList, perc_completed=pcompList, weekly_periodic_day_int=weeklyPeriodicDayInt)
                    school.get_subj_list()[subject_index].add_assignm(
                        new_assignment)
            else:
                new_assignment = Homework(
                    0, assignment_name, delivery_date, start_time, perc_in_1hr=p1hr)
                school.get_subj_list()[subject_index].add_assignm(
                    new_assignment)
            save_in_school_file()
        elif category == "Personal" and self.new_assignment_periodic:
            if periodic_number == 0:  # Daily
                start_time_list = []
                p1hrList = []
                for i in range(30):
                    start_time_list.append(start_time)
                    p1hrList.append(p1hr)
                new_assignment = PersAssignmentPeriodic(
                    assignment_name, delivery_date, periodic_number, start_time_list, perc_in_1hr=p1hrList)
                personal.get_categ_list()[subject_index].add_assignm(
                    new_assignment)
            elif periodic_number == 1:  # Weekly
                start_time_list = []
                p1hrList = []
                pcompList = []
                for i in range(4):
                    start_time_list.append(start_time)
                    p1hrList.append(p1hr)
                    pcompList.append(0)
                if self.weeklyComboBox.currentText() == "Monday":
                    weeklyPeriodicDayInt = 0
                elif self.weeklyComboBox.currentText() == "Tuesday":
                    weeklyPeriodicDayInt = 1
                elif self.weeklyComboBox.currentText() == "Wednesday":
                    weeklyPeriodicDayInt = 2
                elif self.weeklyComboBox.currentText() == "Thursday":
                    weeklyPeriodicDayInt = 3
                elif self.weeklyComboBox.currentText() == "Friday":
                    weeklyPeriodicDayInt = 4
                elif self.weeklyComboBox.currentText() == "Saturday":
                    weeklyPeriodicDayInt = 5
                elif self.weeklyComboBox.currentText() == "Sunday":
                    weeklyPeriodicDayInt = 6
                new_assignment = PersAssignmentPeriodic(
                    assignment_name, delivery_date, periodic_number, start_time_list, perc_in_1hr=p1hrList, perc_completed=pcompList, weekly_periodic_day_int=weeklyPeriodicDayInt)
                personal.get_categ_list()[subject_index].add_assignm(
                    new_assignment)
            save_in_personal_file()
        else:
            start_time = time(hour=start_time_hours, minute=start_time_minutes)
            new_assignment = PersAssignment(
                assignment_name, delivery_date, start_time, perc_in_1hr=p1hr)
            personal.get_categ_list()[subject_index].add_assignm(
                new_assignment)
            save_in_personal_file()

        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def periodicCheckBoxClick(self, state):
        self.new_assignment_periodic = state == Qt.Checked

    def onCategoryComboboxChanged(self, value):
        subject_names = []
        if value == "School":
            for subject in school.get_subj_list():
                subject_names.append(subject.get_name())
        elif value == "Personal":
            for subject in personal.get_categ_list():
                subject_names.append(subject.get_name())
        else:
            raise Exception("The category selected does not exist")

        self.subjectComboBox.clear()
        self.subjectComboBox.addItems(subject_names)

    def onPeriodicComboboxChanged(self, value):
        # self.periodicComboBox = QComboBox()  # Category list
        # self.periodicComboBox.addItems(
        #     ["Daily", "Weekly", "Monthly", "Yearly"])
        # self.periodicComboBox.currentTextChanged.connect(
        #     self.onPeriodicComboboxChanged)
        # self.form.addRow(QLabel("Periodic"), self.periodicComboBox)

        if value == "Weekly":
            self.weeklyComboBox = QComboBox()
            self.weeklyComboBox.addItems(
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            self.form.addRow(QLabel("Day to repeat"), self.weeklyComboBox)
        else:
            # try:
            self.form.removeRow(self.weeklyComboBox)


class Ui_AddSubjectScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()

        # Form
        self.form = QFormLayout()

        # creating the form
        self.subjectNameLineEdit = QLineEdit()  # Subject name
        self.form.addRow(QLabel("Subject name"), self.subjectNameLineEdit)

        self.categoryComboBox = QComboBox()  # Category list
        self.categoryComboBox.addItems(["School", "Personal"])
        self.form.addRow(QLabel("Category"), self.categoryComboBox)

        self.formGroupBox = QGroupBox("Adding subject")
        self.formGroupBox.setLayout(self.form)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.gotoMainScreen)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)

        self.widget.setLayout(mainLayout)

        self.setCentralWidget(self.widget)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Organizer')

    def gotoMainScreen(self):
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def getInfo(self):
        subjectName = self.subjectNameLineEdit.text()
        category = self.categoryComboBox.currentText()

        if category == "School":
            newSubject = Subject(subjectName)
            school.add_subj(newSubject)
            save_in_school_file()
        elif category == "Personal":
            newSubject = Category(subjectName)
            personal.add_categ(newSubject)
            save_in_personal_file()

        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Ui_EditScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.gridbox = QGridLayout()
        self.widget.setLayout(self.gridbox)

        # Categories
        self.category_label = QLabel("School")
        self.category_label.setFont(QFont('Arial', 16))
        self.gridbox.addWidget(self.category_label, 0, 0)

        self.category_label = QLabel("Personal")
        self.category_label.setFont(QFont('Arial', 16))
        self.gridbox.addWidget(self.category_label, 0, 1)

        myFont = QFont()
        myFont.setBold(True)

        # Subjects and assignments
        i = 1
        for subject in school.get_subj_list():
            self.subject_label = QLabel(subject.get_name())
            self.subject_label.setFont(myFont)
            self.gridbox.addWidget(self.subject_label, i, 0)
            i += 1
            for assignment in subject.get_assignm_list():
                self.assignment_radio_button = QRadioButton(
                    assignment.get_name())
                self.assignment_radio_button.toggled.connect(
                    self.selectAssignment)
                self.gridbox.addWidget(self.assignment_radio_button, i, 0)
                i += 1

        i = 1
        for subject in personal.get_categ_list():
            self.subject_label = QLabel(subject.get_name())
            self.subject_label.setFont(myFont)
            self.gridbox.addWidget(self.subject_label, i, 1)
            i += 1
            for assignment in subject.get_assignm_list():
                self.assignment_radio_button = QRadioButton(
                    assignment.get_name())
                self.assignment_radio_button.toggled.connect(
                    self.selectAssignment)
                self.gridbox.addWidget(self.assignment_radio_button, i, 1)
                i += 1

        # Buttons
        self.editAssignmentPushButton = QPushButton("Edit")
        self.editAssignmentPushButton.clicked.connect(
            self.gotoEditAssignmentScreen)
        self.gridbox.addWidget(self.editAssignmentPushButton, 0, 2)

        self.cancelPushButton = QPushButton("Cancel")
        self.cancelPushButton.clicked.connect(self.gotoMainScreen)
        self.gridbox.addWidget(self.cancelPushButton, 1, 2)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Organizer')

    def gotoMainScreen(self):
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def selectAssignment(self):
        btn = self.sender()
        if btn.isChecked():
            self.assignmentSelected = btn.text()

    def gotoEditAssignmentScreen(self):
        editAssignmentScreen = Ui_EditAssignmentScreen(
            self.assignmentSelected, widget.currentIndex())
        widget.addWidget(editAssignmentScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def periodicCheckBoxClick(self, state):
        self.new_assignment_periodic = state == Qt.Checked


class Ui_EditSubjectScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.gridbox = QGridLayout()
        self.widget.setLayout(self.gridbox)

        # Categories
        self.category_label = QLabel("School")
        self.category_label.setFont(QFont('Arial', 16))
        self.gridbox.addWidget(self.category_label, 0, 0)

        self.category_label = QLabel("Personal")
        self.category_label.setFont(QFont('Arial', 16))
        self.gridbox.addWidget(self.category_label, 0, 1)

        myFont = QFont()
        myFont.setBold(True)

        # Subjects
        i = 1
        for subject in school.get_subj_list():
            self.subject_radio_button = QRadioButton(
                subject.get_name())
            self.subject_radio_button.toggled.connect(
                self.selectSubject)
            self.gridbox.addWidget(self.subject_radio_button, i, 0)
            i += 1

        i = 1
        for subject in personal.get_categ_list():
            self.subject_radio_button = QRadioButton(
                subject.get_name())
            self.subject_radio_button.toggled.connect(
                self.selectSubject)
            self.gridbox.addWidget(self.subject_radio_button, i, 1)
            i += 1

        # Buttons
        self.editSubjectPushButton = QPushButton("Edit")
        self.editSubjectPushButton.clicked.connect(
            self.gotoEditParticularSubjectScreen)
        self.gridbox.addWidget(self.editSubjectPushButton, 0, 2)

        self.cancelPushButton = QPushButton("Cancel")
        self.cancelPushButton.clicked.connect(self.gotoMainScreen)
        self.gridbox.addWidget(self.cancelPushButton, 1, 2)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Organizer')

    def gotoMainScreen(self):
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def selectSubject(self):
        btn = self.sender()
        if btn.isChecked():
            self.subjectSelected = btn.text()

    def gotoEditParticularSubjectScreen(self):
        editParticularSubjectScreen = Ui_EditParticularSubjectScreen(
            self.subjectSelected, widget.currentIndex())
        widget.addWidget(editParticularSubjectScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def periodicCheckBoxClick(self, state):
        self.new_assignment_periodic = state == Qt.Checked


class Ui_EditAssignmentScreen(QMainWindow):

    def __init__(self, assignmentName, perviousScreenIndex):
        super().__init__()

        self.perviousScreenIndex = perviousScreenIndex

        for subject in school.get_subj_list():
            for assignment in subject.get_assignm_list():
                if assignment.get_name() == assignmentName:
                    self.assignmentToEdit = assignment
                    self.subjectIndex = school.get_subj_list().index(subject)
                    self.assignmentIndex = subject.get_assignm_list().index(assignment)
                    self.list = "School"
        for subject in personal.get_categ_list():
            for assignment in subject.get_assignm_list():
                if assignment.get_name() == assignmentName:
                    self.assignmentToEdit = assignment
                    self.subjectIndex = personal.get_categ_list().index(subject)
                    self.assignmentIndex = subject.get_assignm_list().index(assignment)
                    self.list = "Personal"

        self.widget = QWidget()

        # Form
        self.form = QFormLayout()

        # Daily periodic assignments
        if isinstance(self.assignmentToEdit, PersAssignmentPeriodic) and self.assignmentToEdit.get_periodic_type() == 0:
            delivery_date_string = self.assignmentToEdit.get_delivery_date().strftime("%Y/%m/%d")
            # creating the form
            self.assignmentNameLineEdit = QLineEdit()  # Assignment name
            self.assignmentNameLineEdit.setText(
                self.assignmentToEdit.get_name())
            self.form.addRow(QLabel("Activity name"),
                             self.assignmentNameLineEdit)

            self.deliveryDateEdit = QDateEdit(
                calendarPopup=True)  # Delivery date
            assignmentDate = QDateTime.fromString(
                delivery_date_string, 'yyyy/MM/dd')
            self.deliveryDateEdit.setDateTime(assignmentDate)
            self.form.addRow(QLabel("Start date"), self.deliveryDateEdit)

            # Start times
            self.startTimeHoursSpinBoxes = []
            self.startTimeMinutesSpinBoxes = []
            # P1hr list
            self.p1hrLineEdits = []

            self.periodicDaysToShow = 10

            for i in range(self.periodicDaysToShow):
                delivery_date_string = (self.assignmentToEdit.get_delivery_date(
                ) + timedelta(days=i)).strftime("%Y/%m/%d")
                self.periodicListsHBoxLayout = QHBoxLayout()
                self.startTimeLabel = QLabel(
                    "Date: {0}".format(delivery_date_string))
                self.startTimeHoursSpinBox = QSpinBox()  # Start time hour
                self.startTimeHoursSpinBox.setValue(
                    self.assignmentToEdit.get_start_time_hours_int()[i])
                self.startTimeHoursSpinBoxes.append(self.startTimeHoursSpinBox)
                self.startTimeMinutesSpinBox = QSpinBox()  # Start time minutes
                self.startTimeMinutesSpinBox.setValue(
                    self.assignmentToEdit.get_start_time_minutes_int()[i])
                self.startTimeMinutesSpinBoxes.append(
                    self.startTimeMinutesSpinBox)
                self.p1hrLineEdit = QLineEdit()  # p1hr
                self.p1hrLineEdit.setText(
                    str(self.assignmentToEdit.get_perc_in1hr()[i]))
                self.p1hrLineEdits.append(
                    self.p1hrLineEdit)

                self.periodicListsHBoxLayout.addWidget(self.startTimeLabel)
                self.periodicListsHBoxLayout.addWidget(
                    self.startTimeHoursSpinBox)
                self.periodicListsHBoxLayout.addWidget(QLabel(":"))
                self.periodicListsHBoxLayout.addWidget(
                    self.startTimeMinutesSpinBox)
                self.periodicListsHBoxLayout.addWidget(
                    self.p1hrLineEdit)
                self.form.addRow(self.periodicListsHBoxLayout)

            self.startTimeWeeklyHBoxLayout = QHBoxLayout()
            self.startTimeWeeklyLabel = QLabel("Set weekly start times")
            self.dayComboBox = QComboBox()  # Day
            self.dayComboBox.addItems(
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            self.daySelected = 0
            # self.dayComboBox.currentTextChanged.connect(
            #     self.onDayComboboxChanged)
            self.startTimeWeeklyHoursSpinBox = QSpinBox()  # Start time hour
            self.startTimeWeeklyHoursSpinBox.setValue(
                self.assignmentToEdit.get_weekly_start_time_hours_int()[0])
            self.startTimeWeeklyMinutesSpinBox = QSpinBox()  # Start time minutes
            self.startTimeWeeklyMinutesSpinBox.setValue(
                self.assignmentToEdit.get_weekly_start_time_minutes_int()[0])
            self.startTimeWeeklyPushButton = QPushButton("Set")
            self.startTimeWeeklyPushButton.clicked.connect(
                self.setStartTimeWeekly)

            self.startTimeWeeklyHBoxLayout.addWidget(self.startTimeWeeklyLabel)
            self.startTimeWeeklyHBoxLayout.addWidget(self.dayComboBox)
            self.startTimeWeeklyHBoxLayout.addWidget(
                self.startTimeWeeklyHoursSpinBox)
            self.startTimeWeeklyHBoxLayout.addWidget(QLabel(":"))
            self.startTimeWeeklyHBoxLayout.addWidget(
                self.startTimeWeeklyMinutesSpinBox)
            self.startTimeWeeklyHBoxLayout.addWidget(
                self.startTimeWeeklyPushButton)
            self.form.addRow(self.startTimeWeeklyHBoxLayout)

            # # Start times
            # self.weeklyStartTimeHoursSpinBoxes = []
            # self.weeklyStartTimeMinutesSpinBoxes = []

            # for i in range(7):
            #     self.periodicListsHBoxLayout2 = QHBoxLayout()
            #     if i == 0:
            #         weekday = "Monday"
            #     elif i == 1:
            #         weekday = "Tuesday"
            #     elif i == 2:
            #         weekday = "Wednesday"
            #     elif i == 3:
            #         weekday = "Thursday"
            #     elif i == 4:
            #         weekday = "Friday"
            #     elif i == 5:
            #         weekday = "Saturday"
            #     elif i == 6:
            #         weekday = "Sunday"
            #     self.weeklyStartTimeLabel = QLabel(
            #         "{0}".format(weekday))
            #     self.weeklyStartTimeHoursSpinBox = QSpinBox()  # Start time hour
            #     self.weeklyStartTimeHoursSpinBox.setValue(
            #         self.assignmentToEdit.get_weekly_start_time_hours_int()[i])
            #     self.weeklyStartTimeHoursSpinBoxes.append(
            #         self.startTimeHoursSpinBox)
            #     self.weeklyStartTimeMinutesSpinBox = QSpinBox()  # Start time minutes
            #     self.weeklyStartTimeMinutesSpinBox.setValue(
            #         self.assignmentToEdit.get_start_time_minutes_int()[i])
            #     self.weeklyStartTimeMinutesSpinBoxes.append(
            #         self.weeklyStartTimeMinutesSpinBox)

            #     self.periodicListsHBoxLayout2.addWidget(
            #         self.weeklyStartTimeLabel)
            #     self.periodicListsHBoxLayout2.addWidget(
            #         self.weeklyStartTimeHoursSpinBox)
            #     self.periodicListsHBoxLayout2.addWidget(QLabel(":"))
            #     self.periodicListsHBoxLayout2.addWidget(
            #         self.weeklyStartTimeMinutesSpinBox)
            #     self.form.addRow(self.periodicListsHBoxLayout2)

            #     self.startTimeAllPushButton = QPushButton("Set")
            #     self.startTimeAllPushButton.clicked.connect(self.setStartTimeAll)

            self.startTimeAllHBoxLayout = QHBoxLayout()
            self.startTimeAllLabel = QLabel("Set start time for all days")
            self.startTimeAllHoursSpinBox = QSpinBox()  # Start time hour
            self.startTimeAllHoursSpinBox.setValue(
                self.assignmentToEdit.get_start_time_hours_int()[0])
            self.startTimeAllMinutesSpinBox = QSpinBox()  # Start time minutes
            self.startTimeAllMinutesSpinBox.setValue(
                self.assignmentToEdit.get_start_time_minutes_int()[0])
            self.startTimeAllPushButton = QPushButton("Set")
            self.startTimeAllPushButton.clicked.connect(self.setStartTimeAll)

            self.startTimeAllHBoxLayout.addWidget(self.startTimeAllLabel)
            self.startTimeAllHBoxLayout.addWidget(
                self.startTimeAllHoursSpinBox)
            self.startTimeAllHBoxLayout.addWidget(QLabel(":"))
            self.startTimeAllHBoxLayout.addWidget(
                self.startTimeAllMinutesSpinBox)
            self.startTimeAllHBoxLayout.addWidget(self.startTimeAllPushButton)
            self.form.addRow(self.startTimeAllHBoxLayout)

            # self.p1hrLineEdit = QLineEdit()  # Percentage in 1 hour
            # self.p1hrLineEdit.setText(
            #     str(self.assignmentToEdit.get_perc_in1hr()))
            # self.form.addRow(QLabel("Percentage in 1 hour"), self.p1hrLineEdit)
        # Weekly periodic assignments
        elif isinstance(self.assignmentToEdit, PersAssignmentPeriodic) and self.assignmentToEdit.get_periodic_type() == 1:
            delivery_date_string = self.assignmentToEdit.get_delivery_date().strftime("%Y/%m/%d")
            # creating the form
            self.assignmentNameLineEdit = QLineEdit()  # Assignment name
            self.assignmentNameLineEdit.setText(
                self.assignmentToEdit.get_name())
            self.form.addRow(QLabel("Activity name"),
                             self.assignmentNameLineEdit)

            self.deliveryDateEdit = QDateEdit(
                calendarPopup=True)  # Delivery date
            assignmentDate = QDateTime.fromString(
                delivery_date_string, 'yyyy/MM/dd')
            self.deliveryDateEdit.setDateTime(assignmentDate)
            self.form.addRow(QLabel("Start date"), self.deliveryDateEdit)

            # Start time
            self.StartTimeHourSpinBox = QSpinBox()  # Start time hour
            self.StartTimeHourSpinBox.setValue(
                self.assignmentToEdit.get_start_time_hours_int()[0])

            self.StartTimeMinuteSpinBox = QSpinBox()  # Start time minutes
            self.StartTimeMinuteSpinBox.setValue(
                self.assignmentToEdit.get_start_time_minutes_int()[0])

            self.form.addRow(QLabel("Start time hours"),
                             self.StartTimeHourSpinBox)
            self.form.addRow(QLabel("Start time minutes"),
                             self.StartTimeMinuteSpinBox)

            # self.startTimeAllHBoxLayout.addWidget(self.startTimeAllLabel)
            # self.startTimeAllHBoxLayout.addWidget(
            #     self.startTimeAllHoursSpinBox)
            # self.startTimeAllHBoxLayout.addWidget(QLabel(":"))
            # self.startTimeAllHBoxLayout.addWidget(
            #     self.startTimeAllMinutesSpinBox)
            # self.startTimeAllHBoxLayout.addWidget(self.startTimeAllPushButton)
            # self.form.addRow(self.startTimeAllHBoxLayout)

        # Non Periodic assignments
        else:

            # creating the form
            self.assignmentNameLineEdit = QLineEdit()  # Assignment name
            self.assignmentNameLineEdit.setText(
                self.assignmentToEdit.get_name())
            self.form.addRow(QLabel("Activity name"),
                             self.assignmentNameLineEdit)

            self.deliveryDateEdit = QDateEdit(
                calendarPopup=True)  # Delivery date
            assignmentDate = QDateTime.fromString(
                self.assignmentToEdit.get_delivery_date().strftime("%Y/%m/%d"), 'yyyy/MM/dd')
            self.deliveryDateEdit.setDateTime(assignmentDate)
            self.form.addRow(QLabel("Delivery date"), self.deliveryDateEdit)

            self.startTimeHoursSpinBox = QSpinBox()  # Start time hour
            self.startTimeHoursSpinBox.setValue(
                self.assignmentToEdit.get_start_time_hours_int())
            self.form.addRow(QLabel("Start time hours"),
                             self.startTimeHoursSpinBox)
            self.startTimeMinutesSpinBox = QSpinBox()  # Start time minutes
            self.startTimeMinutesSpinBox.setValue(
                self.assignmentToEdit.get_start_time_minutes_int())
            self.form.addRow(QLabel("Start time minutes"),
                             self.startTimeMinutesSpinBox)

            self.p1hrLineEdit = QLineEdit()  # Percentage in 1 hour
            self.p1hrLineEdit.setText(
                str(self.assignmentToEdit.get_perc_in1hr()))
            self.form.addRow(QLabel("Percentage in 1 hour"), self.p1hrLineEdit)

            self.pcompLineEdit = QLineEdit()  # Percentage completed
            self.pcompLineEdit.setText(
                str(self.assignmentToEdit.get_perc_completed()))
            self.form.addRow(QLabel("Percentage completed"),
                             self.pcompLineEdit)

        colors = ["lightblue", "lightgrey", "azure",
                  "beige", "lightgoldenrodyellow", "bisque",
                  "gold", "honeydew", "khaki", "lavender",
                  "lavenderblush", "lemonchiffon", "lightcoral",
                  "lightcyan", "lightgoldenrodyellow", "lightpink",
                  "lightsalmon", "lightseagreen", "lightskyblue",
                  "lightsteelblue", "lightyellow", "lime", "linen",
                  "magenta", "mediumorchid", "mediumseagreen",
                  "mediumspringgreen", "mediumslateblue",
                  "mintcream", "orange", "palegreen", "plum"]
        self.colorStringComboBox = QComboBox()  # color
        self.colorStringComboBox.addItems(colors)
        self.colorStringComboBoxLabel = QLabel("Category color")
        self.colorStringComboBox.currentTextChanged.connect(
            self.onColorStringComboboxChanged)
        self.form.addRow(self.colorStringComboBoxLabel,
                         self.colorStringComboBox)

        index = self.colorStringComboBox.findText(
            self.assignmentToEdit.get_color_string(), Qt.MatchFixedString)
        # print(self.assignmentToEdit.get_color_string())
        # print(index)
        if index >= 0:
            self.colorStringComboBox.setCurrentIndex(index)
        self.colorStringComboBoxLabel.setStyleSheet(
            "background-color: " + self.colorStringComboBox.currentText())

        self.removePushButton = QPushButton("Remove")
        self.removePushButton.clicked.connect(self.removeAssignment)
        self.removePushButton.setStyleSheet(
            'QPushButton {color: red;}')

        self.form.addRow(self.removePushButton)

        self.formGroupBox = QGroupBox("Edit activity")
        self.formGroupBox.setLayout(self.form)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.saveValues)
        self.buttonBox.rejected.connect(self.goBack)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)

        self.widget.setLayout(mainLayout)

        self.setCentralWidget(self.widget)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Organizer')

    def onColorStringComboboxChanged(self, value):
        # newColor = self.colorStringComboBox.currentText()
        self.colorStringComboBoxLabel.setStyleSheet(
            "background-color: " + value)

    def saveValues(self):

        assignment_name = self.assignmentNameLineEdit.text()
        delivery_date = datetime.strptime(
            self.deliveryDateEdit.date().toString('yyyy/MM/dd'), "%Y/%m/%d")

        if self.list == "School" and not isinstance(self.assignmentToEdit, PersAssignmentPeriodic):
            p1hr = float(self.p1hrLineEdit.text())
            pcomp = float(self.pcompLineEdit.text())
            start_time_hours = int(self.startTimeHoursSpinBox.text())
            start_time_minutes = int(self.startTimeMinutesSpinBox.text())
            startTime = time(hour=start_time_hours,
                             minute=start_time_minutes)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_name(assignment_name)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_delivery_date(delivery_date)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_start_time(startTime)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_perc_in1hr(p1hr)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_perc_completed(pcomp)
            if pcomp >= 100:
                school.get_subj_list()[self.subjectIndex].set_as_completed(
                    self.assignmentIndex)
            save_in_school_file()
        elif self.list == "School" and isinstance(self.assignmentToEdit, PersAssignmentPeriodic):
            if self.assignmentToEdit.get_periodic_type() == 0:
                start_time_hours = []
                start_time_minutes = []
                start_time_new = []
                p1hr_new = []
                for i in range(self.periodicDaysToShow):
                    start_time_hours.append(
                        int(self.startTimeHoursSpinBoxes[i].text()))
                    start_time_minutes.append(
                        int(self.startTimeMinutesSpinBoxes[i].text()))
                    start_time_new.append(
                        time(hour=start_time_hours[i], minute=start_time_minutes[i]))
                    p1hr_new.append(int(float(self.p1hrLineEdits[i].text())))

                school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_name(assignment_name)
                school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_delivery_date(delivery_date)

                start_times = school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].get_start_time()
                p1hrList = school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].get_perc_in1hr()
                for i in range(self.periodicDaysToShow):
                    start_times[i] = start_time_new[i]
                    p1hrList[i] = p1hr_new[i]
                school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_start_time(start_times)

                school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_perc_in1hr(p1hrList)
            elif self.assignmentToEdit.get_periodic_type() == 1:
                # p1hr = float(self.p1hrLineEdit.text())
                # pcomp = float(self.pcompLineEdit.text())
                start_time_hours = int(self.StartTimeHourSpinBox.text())
                start_time_minutes = int(self.StartTimeMinuteSpinBox.text())
                startTime = time(hour=start_time_hours,
                                 minute=start_time_minutes)
                school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_name(assignment_name)
                school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_delivery_date(delivery_date)
                school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_start_time(startTime)
                # school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                #     self.assignmentIndex].set_perc_in1hr(p1hr)
                # school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                #     self.assignmentIndex].set_perc_completed(pcomp)
                # if pcomp >= 100:
                #     school.get_subj_list()[self.subjectIndex].set_as_completed(
                #         self.assignmentIndex)
            save_in_school_file()

        elif self.list == "Personal":
            if isinstance(self.assignmentToEdit, PersAssignmentPeriodic) and self.assignmentToEdit.get_periodic_type() == 0:
                start_time_hours = []
                start_time_minutes = []
                start_time_new = []
                p1hr_new = []
                for i in range(self.periodicDaysToShow):
                    start_time_hours.append(
                        int(self.startTimeHoursSpinBoxes[i].text()))
                    start_time_minutes.append(
                        int(self.startTimeMinutesSpinBoxes[i].text()))
                    start_time_new.append(
                        time(hour=start_time_hours[i], minute=start_time_minutes[i]))
                    p1hr_new.append(int(float(self.p1hrLineEdits[i].text())))

                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_name(assignment_name)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_delivery_date(delivery_date)

                start_times = personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].get_start_time()
                p1hrList = personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].get_perc_in1hr()
                for i in range(self.periodicDaysToShow):
                    start_times[i] = start_time_new[i]
                    p1hrList[i] = p1hr_new[i]
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_start_time(start_times)

                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_perc_in1hr(p1hrList)
            elif isinstance(self.assignmentToEdit, PersAssignmentPeriodic) and self.assignmentToEdit.get_periodic_type() == 1:
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_name(assignment_name)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_delivery_date(delivery_date)
                start_time_hours = int(self.StartTimeHourSpinBox.text())
                start_time_minutes = int(self.StartTimeMinuteSpinBox.text())
                startTime = time(hour=start_time_hours,
                                 minute=start_time_minutes)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_start_time(startTime)
            else:
                start_time_hours = int(self.startTimeHoursSpinBox.text())
                start_time_minutes = int(self.startTimeMinutesSpinBox.text())
                startTime = time(hour=start_time_hours,
                                 minute=start_time_minutes)
                p1hr = float(self.p1hrLineEdit.text())
                pcomp = float(self.pcompLineEdit.text())
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_name(assignment_name)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_delivery_date(delivery_date)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_start_time(startTime)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_perc_in1hr(p1hr)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_perc_completed(pcomp)

                if pcomp >= 100:
                    personal.get_categ_list()[self.subjectIndex].set_as_completed(
                        self.assignmentIndex)

            save_in_personal_file()

        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def goBack(self):
        widget.setCurrentIndex(self.perviousScreenIndex)

    def setStartTimeAll(self):
        startTimes = self.assignmentToEdit.get_start_time()
        for i in range(len(startTimes)):
            startTimes[i] = time(hour=int(self.startTimeAllHoursSpinBox.text()), minute=int(
                self.startTimeAllMinutesSpinBox.text()))
        personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
            self.assignmentIndex].set_start_time(startTimes)
        save_in_personal_file()

        # Set Main Window
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def setStartTimeWeekly(self):
        startTimes = self.assignmentToEdit.get_start_time()
        daySelectedInt = self.dayComboBox.currentIndex()
        newStartTime = time(hour=int(self.startTimeWeeklyHoursSpinBox.text()), minute=int(
            self.startTimeWeeklyMinutesSpinBox.text()))
        delivery_date = self.assignmentToEdit.get_delivery_date()
        for i in range(len(startTimes)):
            # Preguntar si la start time cae en el dia a editar
            new_day = delivery_date + timedelta(days=i)
            if new_day.weekday() == daySelectedInt:
                startTimes[i] = newStartTime
        personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
            self.assignmentIndex].set_start_time(startTimes)
        save_in_personal_file()

        # Set Main Window
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def removeAssignment(self):
        if self.list == "School":
            del school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex]
            save_in_school_file()
        elif self.list == "Personal":
            del personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex]
            save_in_personal_file()

        # Set Main Window
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)


class Ui_EditParticularSubjectScreen(QMainWindow):

    def __init__(self, subjectName, perviousScreenIndex):
        super().__init__()

        self.perviousScreenIndex = perviousScreenIndex

        for subject in school.get_subj_list():
            if subject.get_name() == subjectName:
                self.subjectToEdit = subject
                self.subjectIndex = school.get_subj_list().index(subject)
                self.list = "School"
        for subject in personal.get_categ_list():
            if subject.get_name() == subjectName:
                self.subjectToEdit = subject
                self.subjectIndex = personal.get_categ_list().index(subject)
                self.list = "Personal"

        self.widget = QWidget()

        # Form
        self.form = QFormLayout()

        # creating the form
        self.subjectNameLineEdit = QLineEdit()  # Subject name
        self.subjectNameLineEdit.setText(
            self.subjectToEdit.get_name())
        self.form.addRow(QLabel("Subject name"),
                         self.subjectNameLineEdit)

        colors = ["lightblue", "lightgrey", "azure",
                  "beige", "lightgoldenrodyellow", "bisque",
                  "gold", "honeydew", "khaki", "lavender",
                  "lavenderblush", "lemonchiffon", "lightcoral",
                  "lightcyan", "lightgoldenrodyellow", "lightpink",
                  "lightsalmon", "lightseagreen", "lightskyblue",
                  "lightsteelblue", "lightyellow", "lime", "linen",
                  "magenta", "mediumorchid", "mediumseagreen",
                  "mediumspringgreen", "mediumslateblue",
                  "mintcream", "orange", "palegreen", "plum"]
        self.colorStringComboBox = QComboBox()  # color
        self.colorStringComboBox.addItems(colors)
        self.colorStringComboBoxLabel = QLabel("Category color")
        self.colorStringComboBox.currentTextChanged.connect(
            self.onColorStringComboboxChanged)
        self.form.addRow(self.colorStringComboBoxLabel,
                         self.colorStringComboBox)

        index = self.colorStringComboBox.findText(
            self.subjectToEdit.get_color_string(), Qt.MatchFixedString)

        if index >= 0:
            self.colorStringComboBox.setCurrentIndex(index)
        self.colorStringComboBoxLabel.setStyleSheet(
            "background-color: " + self.colorStringComboBox.currentText())

        self.removePushButton = QPushButton("Remove")
        self.removePushButton.clicked.connect(self.removeSubject)
        self.removePushButton.setStyleSheet(
            'QPushButton {color: red;}')

        self.form.addRow(self.removePushButton)

        self.formGroupBox = QGroupBox("Edit subject")
        self.formGroupBox.setLayout(self.form)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.saveValues)
        self.buttonBox.rejected.connect(self.goBack)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)

        self.widget.setLayout(mainLayout)

        self.setCentralWidget(self.widget)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Organizer')

    def onColorStringComboboxChanged(self, value):
        # newColor = self.colorStringComboBox.currentText()
        self.colorStringComboBoxLabel.setStyleSheet(
            "background-color: " + value)

    def saveValues(self):

        subject_name = self.subjectNameLineEdit.text()

        if self.list == "School":
            school.get_subj_list()[self.subjectIndex].set_name(subject_name)
            save_in_school_file()
        elif self.list == "Personal":
            personal.get_categ_list()[self.subjectIndex].set_name(subject_name)
            save_in_personal_file()

        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def goBack(self):
        widget.setCurrentIndex(self.perviousScreenIndex)

    def removeSubject(self):
        if self.list == "School":
            del school.get_subj_list()[self.subjectIndex]
            save_in_school_file()
        elif self.list == "Personal":
            del personal.get_categ_list()[self.subjectIndex]
            save_in_personal_file()

        # Set Main Window
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)


class Ui_SimultaneousScreen(QMainWindow):
    def __init__(self, simultaneousMatrix):
        super().__init__()

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.gridbox = QGridLayout()

        self.widget.setLayout(self.gridbox)

        # Get the simultaneous assignments
        (simultaneousSchoolAssignments, simultaneousSchoolCategory, simultaneousPersonalAssignments,
         simultaneousPersonalCategory) = self.getSimultaneousAssignments(simultaneousMatrix)

        days = [(datetime.today() + timedelta(days=x))
                for x in range(len(simultaneousMatrix[0]))]

        myFont = QFont()
        myFont.setBold(True)

        self.startTimeLabel = QLabel("Start time")
        self.startTimeLabel.setFont(myFont)
        self.gridbox.addWidget(self.startTimeLabel, 0, 1)

        self.durationLabel = QLabel("Duration (hours)")
        self.durationLabel.setFont(myFont)
        self.gridbox.addWidget(self.durationLabel, 0, 2)

        i = 0
        for day in days:

            # Date label
            self.dayLabel = QLabel(day.strftime("%d/%m/%y"))
            self.dayLabel.setFont(myFont)
            self.gridbox.addWidget(self.dayLabel, i, 0)
            i += 1

            # School assignments
            for assignment in simultaneousSchoolAssignments:
                if assignment.get_delivery_date().strftime("%d/%m/%y") == day.strftime("%d/%m/%y"):
                    # Name
                    self.schoolAssignmentRadioButton = QRadioButton(
                        assignment.get_name())
                    self.schoolAssignmentRadioButton.toggled.connect(
                        self.selectAssignment)
                    self.gridbox.addWidget(
                        self.schoolAssignmentRadioButton, i, 0)
                    # Start time
                    self.schoolAssignmentStartTimeLabel = QLabel(
                        assignment.get_start_time().strftime("%H:%M"))
                    self.gridbox.addWidget(
                        self.schoolAssignmentStartTimeLabel, i, 1)
                    # Duration
                    self.schoolAssignmentDurationLabel = QLabel(
                        str(assignment.get_time_to_finish()))
                    self.gridbox.addWidget(
                        self.schoolAssignmentDurationLabel, i, 2)
                    i += 1

            # Personal assignments
            for assignment in simultaneousPersonalAssignments:
                if assignment.get_delivery_date().strftime("%d/%m/%y") == day.strftime("%d/%m/%y") or (isinstance(assignment, PersAssignmentPeriodic) and assignment.get_periodic_type() == 0):
                    # Name
                    self.personalAssignmentRadioButton = QRadioButton(
                        assignment.get_name())
                    self.personalAssignmentRadioButton.toggled.connect(
                        self.selectAssignment)
                    self.gridbox.addWidget(
                        self.personalAssignmentRadioButton, i, 0)
                    # Start time
                    if isinstance(assignment, PersAssignmentPeriodic):
                        index = int(day.strftime("%d")) - \
                            int(datetime.today().strftime("%d"))
                        self.personalAssignmentStartTimeLabel = QLabel(
                            assignment.get_start_time()[index].strftime("%H:%M"))
                        self.personalAssignmentDurationLabel = QLabel(
                            str(assignment.get_time_to_finish(index)))
                    else:
                        self.personalAssignmentStartTimeLabel = QLabel(
                            assignment.get_start_time().strftime("%H:%M"))
                        self.personalAssignmentDurationLabel = QLabel(
                            str(assignment.get_time_to_finish()))
                    self.gridbox.addWidget(
                        self.personalAssignmentStartTimeLabel, i, 1)
                    # Duration
                    self.gridbox.addWidget(
                        self.personalAssignmentDurationLabel, i, 2)
                    i += 1

        # Buttons
        self.editAssignmentPushButton = QPushButton("Edit")
        self.editAssignmentPushButton.clicked.connect(
            self.gotoEditAssignmentScreen)
        self.gridbox.addWidget(self.editAssignmentPushButton, 0, 3)

        self.cancelPushButton = QPushButton("Cancel")
        self.cancelPushButton.clicked.connect(self.gotoMainScreen)
        self.gridbox.addWidget(self.cancelPushButton, 1, 3)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

    def gotoMainScreen(self):
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoEditAssignmentScreen(self):
        editAssignmentScreen = Ui_EditAssignmentScreen(
            self.assignmentSelected, widget.currentIndex())
        widget.addWidget(editAssignmentScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def selectAssignment(self):
        btn = self.sender()
        if btn.isChecked():
            self.assignmentSelected = btn.text()

    def getSimultaneousAssignments(self, simultaneousMatrix):
        simultaneousSchoolAssignments = []
        simultaneousSchoolCategory = []
        simultaneousPersonalAssignments = []
        simultaneousPersonalCategory = []

        # School assignments
        for category in school.get_subj_list():
            for assignment in category.get_assignm_list():
                added = False
                if isinstance(assignment, PersAssignmentPeriodic):
                    if assignment.get_periodic_type() == 0:  # Daily periodic assignments
                        for i in range(len(simultaneousMatrix[0])):
                            if not added:
                                hourIndex = assignment.get_start_time_hours_int(
                                )[i] * 2 + round(assignment.get_start_time_minutes_int()[i] / 30)
                                dayIndex = i
                                time_blocks = round(
                                    assignment.get_time_to_finish(i) / 0.5)
                                for timeBlock in range(time_blocks):
                                    if hourIndex + timeBlock >= len(simultaneousMatrix):
                                        hourIndex = -timeBlock
                                        if dayIndex < len(simultaneousMatrix[0]):
                                            dayIndex += 1
                                        else:
                                            break
                                    if simultaneousMatrix[hourIndex + timeBlock][dayIndex]:
                                        simultaneousPersonalAssignments.append(
                                            assignment)
                                        simultaneousPersonalCategory.append(
                                            category)
                                        added = True
                                        break
                            else:
                                break
                    elif assignment.get_periodic_type() == 1:  # Weekly periodic assignments
                        pass
                else:

                    date1 = assignment.get_delivery_date()
                    date2 = date.today() + \
                        timedelta(days=len(simultaneousMatrix[0]))
                    if isinstance(date1, date):
                        date1 = datetime.combine(date1, datetime.min.time())
                    if isinstance(date2, date):
                        date2 = datetime.combine(date2, datetime.min.time())
                    if date1 <= date2:  # Limit to 5 days
                        hourIndex = assignment.get_start_time_hours_int(
                        ) * 2 + round(assignment.get_start_time_minutes_int() / 30)
                        dayIndex = assignment.get_delivery_date().day - datetime.today().day
                        time_blocks = round(
                            assignment.get_time_to_finish() / 0.5)
                        for i in range(time_blocks):
                            if simultaneousMatrix[hourIndex + i][dayIndex]:
                                simultaneousSchoolAssignments.append(
                                    assignment)
                                simultaneousSchoolCategory.append(category)
                                break

        # Personal assignments
        for category in personal.get_categ_list():
            for assignment in category.get_assignm_list():
                added = False
                if isinstance(assignment, PersAssignmentPeriodic):
                    if assignment.get_periodic_type() == 0:  # Daily periodic assignments
                        for i in range(len(simultaneousMatrix[0])):
                            if not added:
                                hourIndex = assignment.get_start_time_hours_int(
                                )[i] * 2 + round(assignment.get_start_time_minutes_int()[i] / 30)
                                dayIndex = i
                                time_blocks = round(
                                    assignment.get_time_to_finish(i) / 0.5)
                                for timeBlock in range(time_blocks):
                                    if hourIndex + timeBlock >= len(simultaneousMatrix):
                                        hourIndex = -timeBlock
                                        if dayIndex < len(simultaneousMatrix[0]):
                                            dayIndex += 1
                                        else:
                                            break
                                    if simultaneousMatrix[hourIndex + timeBlock][dayIndex]:
                                        simultaneousPersonalAssignments.append(
                                            assignment)
                                        simultaneousPersonalCategory.append(
                                            category)
                                        added = True
                                        break
                            else:
                                break
                else:
                    date1 = assignment.get_delivery_date()
                    date2 = date.today() + \
                        timedelta(days=len(simultaneousMatrix[0]))
                    if isinstance(date1, date):
                        date1 = datetime.combine(date1, datetime.min.time())
                    if isinstance(date2, date):
                        date2 = datetime.combine(date2, datetime.min.time())
                    if date1 <= date2:
                        hourIndex = assignment.get_start_time_hours_int(
                        ) * 2 + round(assignment.get_start_time_minutes_int() / 30)
                        dayIndex = assignment.get_delivery_date().day - datetime.today().day
                        time_blocks = round(
                            assignment.get_time_to_finish() / 0.5)
                        for i in range(time_blocks):
                            if hourIndex + i >= len(simultaneousMatrix):
                                if dayIndex < len(simultaneousMatrix[0]) - 1:
                                    dayIndex = dayIndex + 1
                                    hourIndex = -i
                                else:
                                    break
                            if simultaneousMatrix[hourIndex + i][dayIndex]:
                                simultaneousPersonalAssignments.append(
                                    assignment)
                                simultaneousPersonalCategory.append(category)
                                break
        return (simultaneousSchoolAssignments, simultaneousSchoolCategory, simultaneousPersonalAssignments, simultaneousPersonalCategory)


class Ui_PushActivityScreen(QMainWindow):
    def __init__(self, used_matrix):
        super().__init__()

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.gridbox = QGridLayout()

        self.widget.setLayout(self.gridbox)

        self.usedMatrix = used_matrix

        # Get the ordered assignments
        (self.assignments, self.subject_name) = self.getDeliveryOrderedAssignments()

        days = [(datetime.today() + timedelta(days=x))
                for x in range(daysToShow)]

        myFont = QFont()
        myFont.setBold(True)

        self.startTimeLabel = QLabel("Start time")
        self.startTimeLabel.setFont(myFont)
        self.gridbox.addWidget(self.startTimeLabel, 0, 1)

        self.durationLabel = QLabel("Duration (hours)")
        self.durationLabel.setFont(myFont)
        self.gridbox.addWidget(self.durationLabel, 0, 2)

        i = 0
        for day in days:

            # Date label
            self.dayLabel = QLabel(day.strftime("%d/%m/%y"))
            self.dayLabel.setFont(myFont)
            self.gridbox.addWidget(self.dayLabel, i, 0)
            i += 1

            # Assignments
            for assignment in self.assignments:
                if assignment.get_delivery_date().strftime("%d/%m/%y") == day.strftime("%d/%m/%y"):
                    # Name
                    self.assignmentRadioButton = QRadioButton(
                        assignment.get_name())
                    self.assignmentRadioButton.toggled.connect(
                        self.selectAssignment)
                    self.gridbox.addWidget(
                        self.assignmentRadioButton, i, 0)
                    # Start time
                    if isinstance(assignment, PersAssignmentPeriodic):
                        index = int(day.strftime("%d")) - \
                            int(datetime.today().strftime("%d"))
                        self.assignmentStartTimeLabel = QLabel(
                            assignment.get_start_time()[index].strftime("%H:%M"))
                        self.assignmentDurationLabel = QLabel(
                            str(assignment.get_time_to_finish(index)))
                    else:
                        self.assignmentStartTimeLabel = QLabel(
                            assignment.get_start_time().strftime("%H:%M"))
                        self.assignmentDurationLabel = QLabel(
                            str(assignment.get_time_to_finish()))
                    self.gridbox.addWidget(
                        self.assignmentStartTimeLabel, i, 1)
                    # Duration
                    self.gridbox.addWidget(
                        self.assignmentDurationLabel, i, 2)
                    i += 1

        # Buttons
        self.pushAssignmentPushButton = QPushButton("Push assignment")
        self.pushAssignmentPushButton.clicked.connect(
            self.pushAssignment)
        self.gridbox.addWidget(self.pushAssignmentPushButton, 0, 3)

        self.cancelPushButton = QPushButton("Cancel")
        self.cancelPushButton.clicked.connect(self.gotoMainScreen)
        self.gridbox.addWidget(self.cancelPushButton, 1, 3)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

    def gotoMainScreen(self):
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def pushAssignment(self):
        # 0 Get selected assignment
        for assignment in self.assignments:
            if self.assignmentSelectedText == assignment.get_name():
                self.assignmentSelected = assignment

        # 1 Get index in the used matrix of the delivery of the assignment and the time blocks of the assignment
        startHourIndex = getTimeIndex(self.assignmentSelected.get_start_time())
        timeBlocks = round(self.assignmentSelected.get_time_to_finish() / 0.5)

        date1 = self.assignmentSelected.get_delivery_date()
        date2 = date.today()
        if isinstance(date1, date):
            date1 = datetime.combine(date1, datetime.min.time())
        if isinstance(date2, date):
            date2 = datetime.combine(date2, datetime.min.time())
        dayDifference = date1 - date2

        dayIndex = dayDifference.days

        # 2 Loop through each cell counting the number of continuous free spots
        freeSpotAvailable = False
        currentBlockCount = 0
        hourIndex = startHourIndex
        while not freeSpotAvailable:
            if hourIndex + timeBlocks < len(self.usedMatrix):
                if not self.usedMatrix[hourIndex + timeBlocks][dayIndex]:
                    currentBlockCount += 1
                    # 3 If the number of free spots matches the amount of 30 minutes blocks of the time remaining for the assingment, set the delivery date to that
                    if currentBlockCount == timeBlocks:  # Check if it is possible to put the assignment here
                        newStartTime = getTimeFromTimeIndex(hourIndex + 1)
                        newDeliveryDate = date.today() + timedelta(days=dayIndex)
                        for assignment in self.assignments:
                            if self.assignmentSelectedText == assignment.get_name():
                                assignment.set_delivery_date(newDeliveryDate)
                                assignment.set_start_time(newStartTime)
                                freeSpotAvailable = True
                                save_in_personal_file()
                                save_in_school_file()
                                break

                    else:  # Assignment does not fit yet
                        if hourIndex + timeBlocks + 1 < len(self.usedMatrix):
                            hourIndex += 1
                        else:
                            if dayIndex + 1 < len(self.usedMatrix[0]):
                                hourIndex = -timeBlocks
                                dayIndex += 1
                            else:
                                print(
                                    "There is no space available inside the used matrix space")
                                freeSpotAvailable = True

                else:
                    currentBlockCount = 0
                    if hourIndex + timeBlocks + 1 < len(self.usedMatrix):
                        hourIndex += 1
                    else:
                        if dayIndex + 1 < len(self.usedMatrix[0]):
                            hourIndex = -timeBlocks
                            dayIndex += 1
                        else:
                            print(
                                "There is no space available inside the used matrix space")
                            freeSpotAvailable = True

            else:
                if dayIndex + 1 < len(self.usedMatrix[0]):
                    hourIndex = -timeBlocks
                    dayIndex += 1
                else:
                    print("There is no space available inside the used matrix space")
                    freeSpotAvailable = True

            self.gotoMainScreen()

            # 4 Save everything
            # 5 Goto main screen

            ####### OLD PUSH INSTRUCTION ########
            # for assignment in self.assignments:
            #     if self.assignmentSelected == assignment.get_name():
            #         assignment.set_delivery_date(
            #             assignment.get_delivery_date() + timedelta(days=1))
            # save_in_personal_file()
            # save_in_school_file()
            # self.gotoMainScreen()

    def selectAssignment(self):
        btn = self.sender()
        if btn.isChecked():
            self.assignmentSelectedText = btn.text()

    def getDeliveryOrderedAssignments(self):
        assignments = []
        subject_name = []
        # delivery_dates = []
        for subj in school.get_subj_list():
            for assignm in subj.get_assignm_list():
                assignments.append(assignm)
                subject_name.append(subj.get_name())
                # delivery_dates.append(assignm.get_delivery_date())

        for categ in personal.get_categ_list():
            for assignm in categ.get_assignm_list():
                assignments.append(assignm)
                subject_name.append(categ.get_name())
                # delivery_dates.append(assignm.get_delivery_date())

        for i in range(1, len(assignments)):
            j = i
            while j < len(assignments):
                date1 = assignments[i-1].get_delivery_date()
                date2 = assignments[j].get_delivery_date()
                if isinstance(date1, date):
                    date1 = datetime.combine(
                        date1, datetime.min.time())
                if isinstance(date2, date):
                    date2 = datetime.combine(
                        date2, datetime.min.time())
                if date1 > date2:
                    (assignments[i-1], assignments[j]
                     ) = (assignments[j], assignments[i-1])
                    (subject_name[i-1], subject_name[j]
                     ) = (subject_name[j], subject_name[i-1])
                    j = i
                else:
                    j += 1
        return (assignments, subject_name)


class Ui_PushSubjectScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.gridbox = QGridLayout()

        self.widget.setLayout(self.gridbox)

        myFont = QFont()
        myFont.setBold(True)

        self.deliveryDateLabel = QLabel("Delivery date")
        self.deliveryDateLabel.setFont(myFont)
        self.gridbox.addWidget(self.deliveryDateLabel, 0, 1)

        self.subjects = school.get_subj_list() + personal.get_categ_list()
        i = 0
        for subject in self.subjects:
            # Name
            self.subjectRadioButton = QRadioButton(
                subject.get_name())
            self.subjectRadioButton.setFont(myFont)
            self.subjectRadioButton.toggled.connect(
                self.selectSubject)
            self.gridbox.addWidget(
                self.subjectRadioButton, i, 0)
            i += 1

            for assignment in subject.get_assignm_list():
                self.assignmentLabel = QLabel(
                    assignment.get_name())
                self.gridbox.addWidget(
                    self.assignmentLabel, i, 0)
                deliveryDateStr = assignment.get_delivery_date().strftime("%d/%m/%Y")
                self.assignmentDeliveryLabel = QLabel(deliveryDateStr)
                self.gridbox.addWidget(
                    self.assignmentDeliveryLabel, i, 1)
                i += 1

        # Buttons
        self.pushSubjectPushButton = QPushButton("Push subject")
        self.pushSubjectPushButton.clicked.connect(
            self.pushSubject)
        self.gridbox.addWidget(self.pushSubjectPushButton, 0, 3)

        self.cancelPushButton = QPushButton("Cancel")
        self.cancelPushButton.clicked.connect(self.gotoMainScreen)
        self.gridbox.addWidget(self.cancelPushButton, 1, 3)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

    def gotoMainScreen(self):
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def pushSubject(self):
        for subject in self.subjects:
            if self.subjectSelected == subject.get_name():
                for assignment in subject.get_assignm_list():
                    assignment.set_delivery_date(
                        assignment.get_delivery_date() + timedelta(days=1))
        save_in_personal_file()
        save_in_school_file()
        self.gotoMainScreen()

    def selectSubject(self):
        btn = self.sender()
        if btn.isChecked():
            self.subjectSelected = btn.text()


class Ui_PushDayScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.gridbox = QGridLayout()

        self.widget.setLayout(self.gridbox)

        myFont = QFont()
        myFont.setBold(True)

        days = [(datetime.today() + timedelta(days=x))
                for x in range(daysToShow)]

        (self.assignments, self.subject_name) = self.getDeliveryOrderedAssignments()

        i = 0
        j = 0
        for day in days:
            self.dayRadioButton = QRadioButton(
                day.strftime("%d/%m/%Y"))
            self.dayRadioButton.setFont(myFont)
            self.dayRadioButton.toggled.connect(
                self.selectDay)
            self.gridbox.addWidget(
                self.dayRadioButton, i, 0)
            i += 1
            print("Assignment: " +
                  self.assignments[j].get_delivery_date().strftime("%d/%m/%Y"))
            print("Day: " + day.strftime("%d/%m/%Y"))
            while self.assignments[j].get_delivery_date().strftime("%d/%m/%Y") == day.strftime("%d/%m/%Y"):
                self.assignmentLabel = QLabel(self.assignments[j].get_name())
                self.gridbox.addWidget(self.assignmentLabel, i, 0)
                j += 1
                i += 1

        # Buttons
        self.pushDayPushButton = QPushButton("Push day")
        self.pushDayPushButton.clicked.connect(
            self.pushDay)
        self.gridbox.addWidget(self.pushDayPushButton, 0, 1)

        self.cancelPushButton = QPushButton("Cancel")
        self.cancelPushButton.clicked.connect(self.gotoMainScreen)
        self.gridbox.addWidget(self.cancelPushButton, 1, 1)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

    def getDeliveryOrderedAssignments(self):
        assignments = []
        subject_name = []
        # delivery_dates = []
        for subj in school.get_subj_list():
            for assignm in subj.get_assignm_list():
                assignments.append(assignm)
                subject_name.append(subj.get_name())
                # delivery_dates.append(assignm.get_delivery_date())

        for categ in personal.get_categ_list():
            for assignm in categ.get_assignm_list():
                assignments.append(assignm)
                subject_name.append(categ.get_name())
                # delivery_dates.append(assignm.get_delivery_date())

        for i in range(1, len(assignments)):
            j = i
            while j < len(assignments):
                date1 = assignments[i-1].get_delivery_date()
                date2 = assignments[j].get_delivery_date()
                if isinstance(date1, date):
                    date1 = datetime.combine(
                        date1, datetime.min.time())
                if isinstance(date2, date):
                    date2 = datetime.combine(
                        date2, datetime.min.time())
                if date1 > date2:
                    (assignments[i-1], assignments[j]
                     ) = (assignments[j], assignments[i-1])
                    (subject_name[i-1], subject_name[j]
                     ) = (subject_name[j], subject_name[i-1])
                    j = i
                else:
                    j += 1
        return (assignments, subject_name)

    def gotoMainScreen(self):
        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.count() - 1)

    def pushDay(self):
        subjects = school.get_subj_list() + personal.get_categ_list()
        for subject in subjects:
            for assignment in subject.get_assignm_list():
                if not isinstance(assignment, PersAssignmentPeriodic):
                    if assignment.get_delivery_date().strftime("%d/%m/%Y") == self.daySelected:
                        assignment.set_delivery_date(
                            assignment.get_delivery_date() + timedelta(days=1))
        save_in_personal_file()
        save_in_school_file()
        self.gotoMainScreen()

    def selectDay(self):
        btn = self.sender()
        if btn.isChecked():
            self.daySelected = btn.text()


def getTimeIndex(deliveryTime):
    # try:
    return int(deliveryTime.hour) * 2 + round(int(deliveryTime.minute) / 30)
    # except AttributeError:
    #     print(deliveryTime)


def getTimeFromTimeIndex(timeIndex):
    hour = math.floor(timeIndex / 2)
    minute = (timeIndex % 2) * 30
    return time(hour=hour, minute=minute)


app = QApplication(sys.argv)
widget = QStackedWidget()

daysToShow = 30

mainWindow = Ui_MainWindow()

widget.addWidget(mainWindow)
# widget.addWidget(addScreen)
# widget.addWidget(editScreen)

widget.show()
sys.exit(app.exec_())


# TODO: Agregar colores a cada subject
# TODO: Hacer que haya un valor por defecto de p1hr y start time de los assignments periódicos para que no se repitan las excepciones
# TODO: Agregar instrucciones push
# TODO: Hacer que las fechas de entrega se puedan ordenar para cada día para un mismo subject
