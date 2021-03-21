import json 
from prettytable import PrettyTable

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

class Faculty():
    def __init__(self, data):
        self.name = data['name'].title()
        self.branch = data['branch'].title()
        self.email = data['email']
        self.rank = data['rank'].title()
        self.phone = data['phone']
        self.specialization = data['specialization']
    
    def __str__(self):
        
        msg = ""
        msg += f"Name         : {self.name}\n"
        msg += f"Branch       : {self.branch}\n"
        msg += f"Designation  : {self.rank}\n"
        msg += f"Email        : {self.email}\n"
        msg += f"Phone        : {self.phone}\n"
        # msg += f"Rank   : {self.rank}\n"

        return msg

class Result():
    def __init__(self, data):
        self.data = data
        self.name = " ".join([i[0].upper()+i[1:].lower() for i in data['name'].split(" ")])
        self.roll = data['roll'].upper()
        self.cgpi = data['cgpi']

        self.sems : list = []

        for d in data['summary']:
            d['subjects'] = []
            self.sems.append(d)

        for d in data['result']:
            self.sems[d['sem']-1]['subjects'].append(d)


    def parse(self):
        msg     = ["```\n"]
        msg[0] += f"Name : {self.name}\n"
        msg[0] += f"Roll : {self.roll}\n"
        msg[0] += f"CGPI : {self.cgpi}\n"
        msg[0] += "\n```"

        for i, sem in enumerate(self.sems):
            msg.append("```\n")
            msg[i+1] += f"Semester: {i+1}\n"
            table = PrettyTable()
            table.field_names = ["Subject Code","Point", "Sub GP", "Grade"]
            for subject in sem['subjects']:
                table.add_row([subject['subject_code'], subject['sub_point'], f"{subject['sub_gp']:2}", f"{subject['grade']:2s}"])
            msg[i+1] += str(table)
            msg[i+1] += "\n\n"
            msg[i+1] += f"SGPI: {sem['sgpi']}\n"
            msg[i+1] += "```"


        return msg

class ResultNew():
    def __init__(self, data):
        self.data = data
        self.name = " ".join([i[0].upper()+i[1:].lower() for i in data['name'].split(" ")])
        self.roll = data['rollno'].upper()
        self.cgpi = data['cgpi']

        self.sems = data['semester']

    def parse(self):
        msg     = ["```\n"]
        msg[0] += f"Name : {self.name}\n"
        msg[0] += f"Roll : {self.roll}\n"
        msg[0] += f"CGPI : {self.cgpi}\n"
        msg[0] += "\n```"

        for i in self.sems:
            sem = sems[i]
            msg.append("```\n")
            msg[i+1] += f"Semester: {i}\n"
            table = PrettyTable()
            table.field_names = ["Subject Code","Credit", "Pointer", "Sub GP"]
            for subject in sem['subject']:
                table.add_row([subject['subject_code'], subject['credit'], f"{subject['pointer']:2}", f"{int(subject['credit']) * int(subject['pointer']):2s}"])
            msg[i+1] += str(table)
            msg[i+1] += "\n\n"
            msg[i+1] += f"SGPI: {sem['sgpi']}\n"
            msg[i+1] += "```"


        return msg