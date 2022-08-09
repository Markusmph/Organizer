import datetime as dt
from calendar import monthrange


class Assignment:
    def __init__(self, id, name, delivery_date, duration, start_time, perc_completed=0):
        self.id = id
        self.name = name
        self.duration = duration
        self.delivery_date = delivery_date
        self.start_time = start_time
        self.perc_completed = perc_completed

    def set_id(self, assignment_id):
        self.id = assignment_id

    def set_name(self, new_name):
        self.name = new_name

    def set_duration(self, new_duration):
        self.duration = new_duration

    def set_delivery_date(self, new_delivery_date):
        self.delivery_date = new_delivery_date

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_perc_completed(self, new_perc_completed):
        self.perc_completed = new_perc_completed

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_duration(self):
        return self.duration

    def get_delivery_date(self):
        return self.delivery_date

    def get_start_time(self):
        return self.start_time

    def get_start_time_hours_int(self):
        return int(self.start_time.strftime("%H"))

    def get_start_time_minutes_int(self):
        return int(self.start_time.strftime("%M"))

    def get_perc_completed(self):
        return self.perc_completed

    def get_time_to_finish(self):
        return ((100 - self.perc_completed)/self.perc_in_1hr)


class Homework(Assignment):
    def __init__(self, hw_id, name, delivery_date, start_time=dt.time(hour=0, minute=0), perc_in_1hr=100, perc_completed=0, recomended_date=True, mandatory=True):
        self.id = hw_id
        self.name = name
        self.delivery_date = delivery_date
        self.start_time = start_time
        self.perc_in_1hr = perc_in_1hr
        self.perc_completed = perc_completed
        if recomended_date:
            self.recomended_date = self.delivery_date-dt.timedelta(1)
        else:
            self.recomended_date = recomended_date
        self.mandatory = mandatory
        self.late = False

    def set_perc_in1hr(self, perc):
        self.perc_in_1hr = perc

    def set_completed(self, perc_completed):
        self.perc_completed = perc_completed

    def set_mandatory(self, mandatory):
        self.mandatory = mandatory

    def set_late(self, late):
        self.late = late

    def get_perc_in1hr(self):
        return self.perc_in_1hr

    def get_missing_perc(self):
        return 100 - self.perc_completed

    def get_time_to_finish(self):
        return ((100 - self.perc_completed)/self.perc_in_1hr)

    def get_mandatory(self):
        return self.mandatory

    def get_late(self):
        return self.late

    def get_days_remaining(self):
        return (self.delivery_date - dt.date.today())


class Exam(Assignment):
    def __init__(self, name, delivery_date, time_to_study=4, perc_completed=0):
        self.name = name
        self.delivery_date = delivery_date
        self.time_to_study = time_to_study
        self.perc_completed = perc_completed
        self.study_date = self.delivery_date-dt.timedelta(1)

    def set_time_to_study(self, time_to_study):
        self.time_to_study = time_to_study

    def set_completed(self, perc_completed):
        self.perc_completed = perc_completed

    def get_time_to_study(self):
        return self.get_time_to_study

    def get_mandatory(self):
        return True

    def get_time_to_finish(self):
        return self.time_to_study - self.perc_completed*self.time_to_study/100

    def get_missing_perc(self):
        return 100 - self.perc_completed


class PersAssignment(Assignment):
    def __init__(self, name, delivery_date, start_time=dt.time(hour=0, minute=0), perc_in_1hr=100, perc_completed=0, mandatory=False):
        self.name = name
        self.delivery_date = delivery_date
        self.start_time = start_time
        self.perc_in_1hr = perc_in_1hr
        self.perc_completed = perc_completed
        self.mandatory = mandatory

    def set_delivery_date(self, new_delivery_date):
        self.delivery_date = new_delivery_date

    def set_perc_in1hr(self, perc):
        self.perc_in_1hr = perc

    def set_completed(self, perc_completed):
        self.perc_completed = perc_completed

    def set_mandatory(self, mandatory):
        self.mandatory = mandatory

    def set_perc_in1hr(self, perc):
        self.perc_in_1hr = perc

    def get_perc_in1hr(self):
        return self.perc_in_1hr

    def get_missing_perc(self):
        return 100 - self.perc_completed

    def get_time_to_finish(self):
        return ((100 - self.perc_completed)/self.perc_in_1hr)

    def get_mandatory(self):
        return self.mandatory

    def get_perc_in1hr(self):
        return self.perc_in_1hr


class PersAssignmentPeriodic(Assignment):
    def __init__(self, name, delivery_date, periodic_type, start_time, perc_in_1hr=100, perc_completed=0, mandatory=False, weekly_periodic_day_int=0):
        self.name = name
        self.delivery_date = delivery_date
        self.periodic_type = periodic_type
        self.perc_in_1hr = perc_in_1hr
        self.perc_completed = perc_completed
        self.mandatory = mandatory
        self.delivery_date = delivery_date
        self.start_time = start_time  # Array
        self.weekly_periodic_day_int = weekly_periodic_day_int

    def set_delivery_dates(self):
        if self.periodic_type == 0:  # Every day
            if self.perc_completed >= 100:
                self.perc_completed = 0
                new_date = self.delivery_date + dt.timedelta(days=1)
                self.set_delivery_date(new_date)
            else:
                self.set_delivery_date(dt.date.today())
        elif self.periodic_type < 8 and self.periodic_type > 0:  # Weekly
            if self.perc_completed >= 100:
                self.perc_completed = 0
                for i in range(7):
                    date_to_compare = dt.date.today() + dt.timedelta(days=(i+7))
                    if date_to_compare.weekday() == (self.periodic_type - 1):
                        self.set_delivery_date(date_to_compare)
            else:
                for i in range(7):
                    date_to_compare = dt.date.today() + dt.timedelta(days=i)
                    if date_to_compare.weekday() == (self.periodic_type - 1):
                        self.set_delivery_date(date_to_compare)
        elif self.periodic_type == 8:  # Monthly
            try:
                monthly_option = self.monthly_option
            except AttributeError:
                print("Please enter your answer with the index")
                print("1) First saturday of each month")
                print("2) Second saturday of each month")
                print("3) Third saturday of each month")
                print("4) Fourth saturday of each month")
                self.monthly_option = int(input(": "))
                monthly_option = self.monthly_option
            if self.perc_completed >= 100:
                self.perc_completed = 0
                counter = 0
                date_to_compare = self.delivery_date + dt.timedelta(days=1)
                while (date_to_compare + dt.timedelta(days=1)).month == self.delivery_date.month:
                    date_to_compare += dt.timedelta(days=1)
                while counter != monthly_option:
                    date_to_compare += dt.timedelta(days=1)
                    if date_to_compare.weekday() == 5:
                        counter += 1
                self.set_delivery_date(date_to_compare)
            else:
                counter = 0
                date_to_compare = dt.date(
                    self.delivery_date.year, self.delivery_date.month, 1) - dt.timedelta(days=1)
                while counter != monthly_option:
                    date_to_compare += dt.timedelta(days=1)
                    if date_to_compare.weekday() == 5:
                        counter += 1
                if date_to_compare >= dt.date.today():
                    self.set_delivery_date(date_to_compare)
                else:
                    counter = 0
                    date_to_compare = self.delivery_date
                    while (date_to_compare + dt.timedelta(days=1)).month == self.delivery_date.month:
                        date_to_compare += dt.timedelta(days=1)
                    while counter != monthly_option:
                        date_to_compare += dt.timedelta(days=1)
                        if date_to_compare.weekday() == 5:
                            counter += 1
                    self.set_delivery_date(date_to_compare)
        elif self.periodic_type == 9:  # Every 2 days
            if self.perc_completed >= 100:
                self.perc_completed = 0
            self.set_delivery_date(self.delivery_date + dt.timedelta(days=2))
        else:
            raise ValueError

    def set_delivery_date(self, new_delivery_date):
        self.delivery_date = new_delivery_date

    def set_completed(self, perc_completed):
        self.perc_completed = perc_completed
        self.set_delivery_dates()

    def set_perc_in1hr(self, perc):
        self.perc_in_1hr = perc

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_weekly_periodic_day_int(self, weekly_periodic_day_int):
        self.weekly_periodic_day_int = weekly_periodic_day_int

    def set_weekly_start_times(self, weekly_start_times):
        self.weekly_start_times = weekly_start_times

    def update_delivery_date(self):
        self.set_delivery_dates()

    def get_mandatory(self):
        return self.mandatory

    def get_perc_in1hr(self):
        return self.perc_in_1hr

    def get_periodic_type(self):
        return self.periodic_type

    def get_start_time(self):
        return self.start_time

    def get_start_time_hours_int(self):
        self.start_time_hours_int = []
        for i in range(30):
            self.start_time_hours_int.append(
                int(self.start_time[i].strftime("%H")))
        return self.start_time_hours_int

    def get_start_time_minutes_int(self):
        self.start_time_minutes_int = []
        for i in range(30):
            self.start_time_minutes_int.append(
                int(self.start_time[i].strftime("%M")))
        return self.start_time_minutes_int

    def get_time_to_finish(self, i):
        # print("Pcomp: " + str(self.perc_completed[i]))
        # print("p1hr: " + str(self.perc_in_1hr[i]))
        # print(self.name)
        try:
            return ((100 - self.perc_completed[i])/self.perc_in_1hr[i])
        except ZeroDivisionError:
            return 0

    def get_weekly_periodic_day_int(self):
        return self.weekly_periodic_day_int

    def get_weekly_start_times(self):
        return self.weekly_start_times

    def get_weekly_start_time_hours_int(self):
        self.weekly_start_times_hours_int = []
        for i in range(7):
            self.weekly_start_times_hours_int.append(
                int(self.weekly_start_times[i].strftime("%H")))
        return self.weekly_start_times_hours_int

    def get_weekly_start_time_minutes_int(self):
        self.weekly_start_times_minutes_int = []
        for i in range(7):
            self.weekly_start_times_minutes_int.append(
                int(self.weekly_start_times[i].strftime("%M")))
        return self.weekly_start_times_minutes_int


# periodic type = 0: Every day
# periodic type = 1: Every week
# periodic type = 2: Every month
# periodic type = 3: Every year
# #


#
# class Meeting(Assignment):
#    def __init__(self):
#        self.start_time = self.delivery_date
#        self.end_time = start_time + self.duration
#    def set_start_time(self, new_start_time):
#        self.delivery_date = new_start_time
#        self.start_time = new_start_time
#        self.end_time = self.start_time + self.duration
#    def set_duration(self, new_duration):
#        self.duration = new_duration
#        self.end_time = self.start_time + self.duration
#    def get_start_time(self):
#        return self.start_time
#    def get_end_time(self):
#        return self.end_time
#
# class ProjectPart(Assignment):
#    def __init__(self):
#        pass
#
# class F1Teenth(Assignment):
#    def __init__(self):
#        pass
#
# class ROS(Assignment):
#    def __init__(self):
#        pass
#
