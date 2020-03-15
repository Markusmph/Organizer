class Ambit:
    def __init__(self, list=[]):
        pass
    def add(self, new):
        pass
    def edit(self, index):
        pass
    def remove(self, index):
        pass

#------------------------------------------------------
class School(Ambit):
    def __init__(self, subj_list=[]):
        self.list = subj_list

class NATMA(Ambit):
    def __init__(self, assigm_list=[]):
        self.list = assigm_list
        pass

class Personal(Ambit):
    def __init__(self, categ_list=[]):
        self.list = categ_list
        pass
#------------------------------------------------------

#------------------------------------------------------
class Subject:
    def __init__(self, name, hour, assignm_list=[]):
        self.hour = hour
        self.name = name
        self. assignm_list = assignm_list
    def add_assignm(self, new_assignm):
        pass
    def edit_assignm(self, index):
        pass
    def remove_assignm(self, index):
        pass
    def set_hour(self, new_hour):
        pass
    def get_hour(self):
        return self.hour

class Category:
    def __init__(self):
        pass
#------------------------------------------------------