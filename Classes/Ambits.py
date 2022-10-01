from Classes.Assignments import PersAssignment, PersAssignmentPeriodic


class Ambit:
    def __init__(self, list=[]):
        self.list = list

    def add(self, new):
        self.list.append(new)

# ------------------------------------------------------


class School(Ambit):
    def __init__(self, subj_list=[]):
        self.subj_list = subj_list

    def add_subj(self, new_subj):
        self.subj_list.append(new_subj)

    def set_subj_list(self, new_list):
        self.subj_list = new_list

    def get_subj_list(self):
        return self.subj_list


class Natma(Ambit):
    def __init__(self, assignm_list=[]):
        self.assignm_list = assignm_list

    def add_assignm(self, new_assignm):
        self.assignm_list.append(new_assignm)

    def create_completed_list(self):
        self.completed = []

    def set_as_completed(self, index):
        self.completed.append(self.assignm_list[index])
        del self.assignm_list[index]

    def set_assignm_list(self, new_list):
        self.assignm_list = new_list

    def get_assignm_list(self):
        return self.assignm_list

    def get_completed_list(self):
        return self.completed


class Personal(Ambit):
    def __init__(self, categ_list=[]):
        self.categ_list = categ_list

    def add_categ(self, new_categ):
        self.categ_list.append(new_categ)

    def set_categ_list(self, new_list):
        self.categ_list = new_list

    def get_categ_list(self):
        return self.categ_list

# ------------------------------------------------------
#
# ------------------------------------------------------


class Subject:
    def __init__(self, name, assignm_list=[]):
        self.name = name
        self.assignm_list = assignm_list
        self.completed = []

    def add_assignm(self, new_assignm):
        self.assignm_list.append(new_assignm)
        print("Ambits msg: Assignment added to " + self.name)

    def set_assignm_list(self, assignm_list):
        self.assignm_list = assignm_list

    def remove_assignm(self, index):
        pass

    def set_hour(self, new_hour):
        pass

    def create_completed_list(self):
        self.completed = []

    def set_as_completed(self, index):
        self.completed.append(self.assignm_list[index])
        del self.assignm_list[index]

    def get_name(self):
        return self.name

    def get_hour(self):
        return self.hour

    def get_assignm_list(self):
        return self.assignm_list

    def get_completed_list(self):
        return self.completed


class Category:
    def __init__(self, name, assignm_list=[]):
        self.name = name
        self.assignm_list = assignm_list
        self.completed = []

    def set_name(self, name):
        self.name = name

    def add_assignm(self, new_assignm):
        self.assignm_list.append(new_assignm)

    def set_as_completed(self, index):
        self.completed.append(self.assignm_list[index])
        del self.assignm_list[index]

    def set_completed(self, index, value):
        if (value == 100) and (type(self.assignm_list[index]) == PersAssignment):
            self.completed.append(self.assignm_list[index])
            del self.assignm_list[index]
        else:
            self.assignm_list[index].set_completed(value)

    def get_name(self):
        return self.name

    def get_assignm_list(self):
        return self.assignm_list

    def get_completed_list(self):
        return self.completed

# ------------------------------------------------------
