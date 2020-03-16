class Ambit:
    def __init__(self, list=[]):
        self.list = list
    def add(self, new):
        self.list.append(new)
    def edit(self, index):
        pass
    def remove(self, index):
        pass

#------------------------------------------------------
class School(Ambit):
    def __init__(self, subj_list=[]):
        self.subj_list = subj_list
    def set_subj_list(self, new_list):
        self.subj_list = new_list
    def get_subj_list(self):
        return self.subj_list

#class NATMA(Ambit):
#    def __init__(self, assigm_list=[]):
#        self.list = assigm_list
#        pass
#
#class Personal(Ambit):
#    def __init__(self, categ_list=[]):
#        self.list = categ_list
#        pass
##------------------------------------------------------
#
##------------------------------------------------------
class Subject:
    def __init__(self, name, assignm_list=[]):
        self.name = name
        self.assignm_list = assignm_list
    def add_assignm(self, new_assignm):
        self.assignm_list.append(new_assignm)
    def remove_assignm(self, index):
        pass
    def set_hour(self, new_hour):
        pass
    def get_name(self):
        return self.name
    def get_hour(self):
        return self.hour
    def get_assignments(self):
        return self.assignm_list
#
#class Category:
#    def __init__(self):
#        pass
##------------------------------------------------------