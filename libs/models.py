import json 
from prettytable import PrettyTable

"""
    To format the api response
"""

class Student():
    def __init__(self, data):
        self.name = data['name'].title()
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
        self.name = data['name'].title()
        self.roll = data['rollno'].upper()
        self.cgpi = data['cgpi']

        self.sems = []
        for i in data["semester"]:
            self.sems.append(data["semester"][i])

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
            table.field_names = ["Subject Code","Credit", "Sub GP", "Pointer"]
            for subject in sem['subject']:
                table.add_row([subject['subject_code'], subject['credit'], f"{int(subject['credit']) * int(subject['pointer']):2}", f"{int(subject['pointer']):2}"])
            msg[i+1] += str(table)
            msg[i+1] += "\n\n"
            msg[i+1] += f"SGPI: {sem['sgpi']}\n"
            msg[i+1] += "```"


        return msg