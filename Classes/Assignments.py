class Assignment:
    def __init__(self, name, duration, delivery_date, recomended_date, perc_completed=0):
        self.name = name
        self.duration = duration
        self.delivery_date = delivery_date
        self.recomended_date = recomended_date
        self.perc_completed = perc_completed
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
    def __init__(self):
        pass

class Exam(Assignment):
    def __init__(self):
        pass

class Meeting(Assignment):
    def __init__(self):
        pass

class ProjectPart(Assignment):
    def __init__(self):
        pass

class F1Teenth(Assignment):
    def __init__(self):
        pass

class ROS(Assignment):
    def __init__(self):
        pass

class Exam(Assignment):
    def __init__(self):
        pass