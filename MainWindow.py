# from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QLabel, QScrollArea, QVBoxLayout, QMainWindow, QStackedWidget)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDateTime
from datetime import *

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
    for subject in school.get_subj_list():
        for assignment in subject.get_assignm_list():
            try:
                if assignment.get_delivery_date() < datetime.today():
                    subject_index = school.get_subj_list().index(subject)
                    assignment_index = subject.get_assignm_list().index(assignment)
                    school.get_subj_list()[subject_index].get_assignm_list()[
                        assignment_index].set_delivery_date(datetime.today())
            except TypeError:
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
                personal.get_categ_list()[subject_index].get_assignm_list()[
                    assignment_index].set_delivery_date(datetime.today())
                # Rotate list values in periodic assignments
                if isinstance(assignment, PersAssignmentPeriodic):
                    if assignment.get_periodic_type() == 0:
                        # Start times
                        start_times = personal.get_categ_list()[subject_index].get_assignm_list()[
                            assignment_index].get_start_time()
                        start_times.append(start_times.pop(0))
                        personal.get_categ_list()[subject_index].get_assignm_list()[
                            assignment_index].set_start_time(start_times)
                        # p1hr
                        p1hrList = personal.get_categ_list()[subject_index].get_assignm_list()[
                            assignment_index].get_perc_in1hr()
                        p1hrList.append(p1hrList.pop(0))
                        personal.get_categ_list()[subject_index].get_assignm_list()[
                            assignment_index].set_perc_in1hr(p1hrList)
                        # pcomp
                        pcompList = personal.get_categ_list()[subject_index].get_assignm_list()[
                            assignment_index].get_perc_completed()
                        pcompList.append(pcompList.pop(0))
                        personal.get_categ_list()[subject_index].get_assignm_list()[
                            assignment_index].set_perc_completed(pcompList)
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
                    if assignment.get_periodic_type() == 0:
                        hour_index = (int(assignment.get_start_time()[
                                      i].hour)*2) + round(int(assignment.get_start_time()[i].minute) / 30) + 1
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
                                color = "lightblue"
                                self.used_matrix[hour_index +
                                                 j - 1][i + next_day] = True
                            self.gridbox.addWidget(
                                label_assignment, hour_index+j, i+2 + next_day)
                            label_assignment.setStyleSheet(
                                "background-color: {0}".format(color))
                elif assignment.get_delivery_date().strftime("%d/%m/%y") == day.strftime("%d/%m/%y"):
                    hour_index = assignment.get_start_time_hours_int(
                    ) * 2 + round(assignment.get_start_time_minutes_int() / 30) + 1
                    time_blocks = round(assignment.get_time_to_finish() / 0.5)
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
                            if subject_name[assignments.index(assignment)] == "Personal":
                                color = "lightblue"
                            else:
                                color = "lightgrey"
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
        add_button = QPushButton("Add activity")
        self.gridbox.addWidget(add_button, 0, 0)
        add_button.clicked.connect(self.gotoAddScreen)

        edit_button = QPushButton("Edit activity")
        self.gridbox.addWidget(edit_button, 1, 0)
        edit_button.clicked.connect(self.gotoEditScreen)

        simultaneous_button = QPushButton("Edit simultaneous activities")
        self.gridbox.addWidget(simultaneous_button, 2, 0)
        simultaneous_button.clicked.connect(self.gotoSimultaneousScreen)

        pushActivityButton = QPushButton("Push activity")
        self.gridbox.addWidget(pushActivityButton, 3, 0)
        pushActivityButton.clicked.connect(self.gotoPushActivityScreen)

        pushSubjectButton = QPushButton("Push subject")
        self.gridbox.addWidget(pushSubjectButton, 4, 0)
        pushSubjectButton.clicked.connect(self.gotoPushSubjectScreen)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Organizer')
        self.show()

    def gotoAddScreen(self):
        addScreen = Ui_AddScreen()
        widget.addWidget(addScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoEditScreen(self):
        editScreen = Ui_EditScreen()
        widget.addWidget(editScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoSimultaneousScreen(self):
        simultaneousScreen = Ui_SimultaneousScreen(self.simultaneous_matrix)
        widget.addWidget(simultaneousScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoPushActivityScreen(self):
        pushActivityScreen = Ui_PushActivityScreen()
        widget.addWidget(pushActivityScreen)
        widget.setCurrentIndex(widget.count() - 1)

    def gotoPushSubjectScreen(self):
        pushSubjectScreen = Ui_PushSubjectScreen()
        widget.addWidget(pushSubjectScreen)
        widget.setCurrentIndex(widget.count() - 1)


class Ui_AddScreen(QMainWindow):
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
        self.form.addRow(QLabel("Category"), self.categoryComboBox)

        self.subjectComboBox = QComboBox()  # Subject
        subject_names = []
        for subject in school.get_subj_list():
            subject_names.append(subject.get_name())
        for category in personal.get_categ_list():
            subject_names.append(category.get_name())
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
        if subject_index >= len(school.get_subj_list()):
            subject_index_personal_list = subject_index - \
                len(school.get_subj_list())
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
            periodic_number = 8
        elif periodic == "Yearly":
            periodic_number = 10

        if category == "School":
            new_assignment = Homework(
                0, assignment_name, delivery_date, start_time, perc_in_1hr=p1hr)
            school.get_subj_list()[subject_index].add_assignm(
                new_assignment)
            save_in_school_file()
        elif category == "Personal" and self.new_assignment_periodic:
            start_time_list = []
            p1hrList = []
            for i in range(30):
                start_time_list.append(start_time)
                p1hrList.append(p1hr)
            new_assignment = PersAssignmentPeriodic(
                assignment_name, periodic_number, start_time_list, perc_in_1hr=p1hr)
            personal.get_categ_list()[subject_index_personal_list].add_assignm(
                new_assignment)
            save_in_personal_file()
        else:
            start_time = time(hour=start_time_hours, minute=start_time_minutes)
            new_assignment = PersAssignment(
                assignment_name, delivery_date, start_time, perc_in_1hr=p1hr)
            personal.get_categ_list()[subject_index_personal_list].add_assignm(
                new_assignment)
            save_in_personal_file()

        mainWindow = Ui_MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def periodicCheckBoxClick(self, state):
        self.new_assignment_periodic = state == Qt.Checked


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
        self.gridbox.addWidget(self.editAssignmentPushButton, i, 0)

        self.cancelPushButton = QPushButton("Cancel")
        self.cancelPushButton.clicked.connect(self.gotoMainScreen)
        self.gridbox.addWidget(self.cancelPushButton, i, 1)

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

            for i in range(5):
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
        else:  # Non Periodic assignments

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

    def saveValues(self):

        assignment_name = self.assignmentNameLineEdit.text()
        delivery_date = datetime.strptime(
            self.deliveryDateEdit.date().toString('yyyy/MM/dd'), "%Y/%m/%d")

        if self.list == "School":
            p1hr = float(self.p1hrLineEdit.text())
            start_time_hours = int(self.startTimeHoursSpinBox.text())
            start_time_minutes = int(self.startTimeMinutesSpinBox.text())
            startTime = time(hour=start_time_hours, minute=start_time_minutes)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_name(assignment_name)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_delivery_date(delivery_date)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_start_time(startTime)
            school.get_subj_list()[self.subjectIndex].get_assignm_list()[
                self.assignmentIndex].set_perc_in1hr(p1hr)

            save_in_school_file()
        elif self.list == "Personal":
            if isinstance(self.assignmentToEdit, PersAssignmentPeriodic):
                start_time_hours = []
                start_time_minutes = []
                start_time_new = []
                p1hr_new = []
                for i in range(5):
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
                for i in range(5):
                    start_times[i] = start_time_new[i]
                    p1hrList[i] = p1hr_new[i]
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_start_time(start_times)

                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_perc_in1hr(p1hrList)
            else:
                start_time_hours = int(self.startTimeHoursSpinBox.text())
                start_time_minutes = int(self.startTimeMinutesSpinBox.text())
                startTime = time(hour=start_time_hours,
                                 minute=start_time_minutes)
                p1hr = int(float(self.p1hrLineEdit.text()))
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_name(assignment_name)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_delivery_date(delivery_date)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_start_time(startTime)
                personal.get_categ_list()[self.subjectIndex].get_assignm_list()[
                    self.assignmentIndex].set_perc_in1hr(p1hr)

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
                            simultaneousSchoolAssignments.append(assignment)
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
    def __init__(self):
        super().__init__()

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.gridbox = QGridLayout()

        self.widget.setLayout(self.gridbox)

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
        for assignment in self.assignments:
            if self.assignmentSelected == assignment.get_name():
                assignment.set_delivery_date(
                    assignment.get_delivery_date() + timedelta(days=1))
        save_in_personal_file()
        save_in_school_file()
        self.gotoMainScreen()

    def selectAssignment(self):
        btn = self.sender()
        if btn.isChecked():
            self.assignmentSelected = btn.text()

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


update_assignments()  # Update assignment dates
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
