import datetime as dt

class Assignment:
    def __init__(self, name, delivery_date, duration, perc_completed=0, recomended_date=True):
        self.name = name
        self.duration = duration
        self.delivery_date = delivery_date
        self.perc_completed = perc_completed
        if recomended_date:
            self.recomended_date = self.delivery_date-dt.timedelta(1)
        else:
            self.recomended_date = recomended_date
    def set_name(self, new_name):
        self.name = new_name
    def set_duration(self, new_duration):
        self.duration = new_duration
    def set_delivery_date(self, new_delivery_date):
        self.delivery_date = new_delivery_date
    def set_recomended_date(self, new_recomended_date):
        self.recomended_date = new_recomended_date
    def set_perc_completed(self, new_perc_completed):
        self.perc_completed = new_perc_completed
    def get_name(self):
        return self.name
    def get_duration(self):
        return self.duration
    def get_delivery_date(self):
        return self.delivery_date
    def get_recomended_date(self):
        return self.recomended_date
    def get_perc_completed(self):
        return self.perc_completed

class Homework(Assignment):
    def __init__(self, name, delivery_date, perc_in_1hr=100, perc_completed=0, recomended_date=True):
        self.name = name
        self.delivery_date = delivery_date
        self.perc_in_1hr = perc_in_1hr
        self.perc_completed = perc_completed
        if recomended_date:
            self.recomended_date = self.delivery_date-dt.timedelta(1)
        else:
            self.recomended_date = recomended_date
    def set_perc_in1hr(self, perc):
        self.perc_in_1hr = perc
    def set_completed(self, perc_completed):
        self.perc_completed = perc_completed
    def get_perc_in1hr(self):
        return self.perc_in_1hr
    def get_missing_perc(self):
        return 100 - self.perc_completed
    def get_time_to_finish(self):
        return ((100 - self.perc_completed)/self.perc_in_1hr)
    #def get_days_remaining(self):
    #    return (self.delivery_date - dt.datetime.today())

#class Exam(Assignment):
#    def set_optional(self, optional):
#        self.optional = optional
#    def get_optional(self):
#        return self.optional
#    
#class Meeting(Assignment):
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
#class ProjectPart(Assignment):
#    def __init__(self):
#        pass
#
#class F1Teenth(Assignment):
#    def __init__(self):
#        pass
#
#class ROS(Assignment):
#    def __init__(self):
#        pass
#
#class Exam(Assignment):
#    def __init__(self):
#        pass