import json 

"""
    To format the api response
"""

class Student():
    def __init__(self, data):
        self.name = " ".join([i[0].upper()+i[1:] for i in data['name'].split(" ")])
        self.branch = data['branch']
        self.roll = data['rollno'].upper()
    
    def __str__(self):
        
        msg = ""
        msg += f"Name   : {self.name}\n"
        msg += f"Roll   : {self.roll}\n"
        msg += f"Branch : {self.branch}\n"

        return msg

class Result():
    def __init__(self, data):
        self.data = data
        self.name = " ".join([i[0].upper()+i[1:] for i in data['name'].split(" ")])
        self.roll = data['rollno'].upper()
        self.cgpi = data['cgpi']
        self.sems = data['semester']

    def __str__(self):
        msg =  f"Name : {self.name}\n"
        msg += f"Roll : {self.roll}\n"
        msg += f"CGPI : {self.cgpi}"

        for sem in self.sems[1:]:
            msg += "\n\n"
            msg += f"{'Subject Code':>12} | 'Pointer'\n"
            for subject in sem['subject']:
                msg += f"{subject['subject_code']:>12} | {int(subject['pointer']):2d}\n"
        return msg