# -*- coding: utf-8 -*-
"""
list prompt example
"""
from __future__ import print_function, unicode_literals

from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt, Separator

from examples import custom_style_2
import art
import pandas as pd



class CSVdb:
    def __init__(self):
        self.db = None
        self.grade_table = {
            'A': 4,
            'B+': 3.5,
            'B': 3,
            'C+': 2.5,
            'C': 2,
            'D+': 1.5,
            'D': 1,
            'F': 0
        }

    def load(self, file_name):
        self.db = pd.read_csv(file_name, encoding = 'utf8', dtype={'Course Id': 'str', 'Grade(Score)': 'float', 'Credit': 'int', 'Year': 'str', 'Semester': 'str'})
        art.tprint("GradeDB", font="roman")

    def check_int(self, text):
        try:
            if int(text):
                return True
        except ValueError:
            return False

    def singlepoint(self, n):
        gpa = str(n)
        if gpa[::-1].find('.') == 1:
            return True
        return False

    def update_row_with_dict(self, dictionary, index):
        for key in dictionary.keys():
            self.db.loc[index, key] = dictionary.get(key)

    def main(self):
        questions = [
            {
                'type': 'list',
                'name': 'todo',
                'message': 'What do you want to do?',
                'choices': [
                    'Insert',
                    'Update',
                    'Summary',
                    'Calculate GPA',
                    'Save and Close'
                ]
            }
        ]

        answers = prompt(questions, style=custom_style_2)
        while(answers['todo'] != "Save and Close"):
            if(answers['todo'] == "Insert"):
                questions2 = [
                    {
                        'type': 'input',
                        'name': 'Course Id',
                        'message': 'Course Id:',
                        'validate': lambda text: len(text) == 9,
                    },
                    {
                        'type': 'input',
                        'name': 'Course Name',
                        'message': 'Course Name:',
                        'validate': lambda text: len(text) > 0,
                    },
                    {
                        'type': 'input',
                        'name': 'Year',
                        'message': 'Year:',
                        'validate': lambda text: len(text) > 0 and self.check_int(text),
                    },
                    {
                        'type': 'input',
                        'name': 'Semester',
                        'message': 'Semester:',
                        'validate': lambda text: len(text) > 0,
                    },
                    {
                        'type': 'input',
                        'name': 'Credit',
                        'message': 'Credit:',
                        'validate': lambda text: len(text) > 0,
                    },
                    {
                        'type': 'input',
                        'name': 'Section',
                        'message': 'Section:',
                        'validate': lambda text: len(text) > 0,
                    },
                    {
                        'type': 'list',
                        'name': 'Grade',
                        'message': 'Grade:',
                        'choices': [
                            'A',
                            'B+',
                            'B',
                            'C+',
                            'C',
                            'D+',
                            'D',
                            'F',
                        ]
                    },
                ]
                answers2 = prompt(questions2, style=custom_style_2)
                answers2["Grade(Score)"] = self.grade_table[answers2['Grade']]
                # pprint(answers2)

                self.db = self.db.append(answers2, ignore_index=True)
                # pprint(self.db)

            # pprint(answers)
            elif (answers['todo'] == "Update"):
                pprint(self.db)
                questions4 = [
                    {
                        'type': 'input',
                        'name': 'course',
                        'message': 'Which year and semester do you want?',
                         'validate': lambda text: int(text) <= self.db.tail(1).index.item(),
                    }
                ]

                answers4 = prompt(questions4, style=custom_style_2)
                course_info = self.db.iloc[int(answers4['course'])]

                default_grade = {
                    'A': 0,
                    'B+': 1,
                    'B': 2,
                    'C+': 3,
                    'C': 4,
                    'D+': 5,
                    'D': 6,
                    'F': 7
                }

                questions5 = [
                    {
                        'type': 'input',
                        'name': 'Course Id',
                        'message': 'Course Id:',
                        'default': course_info['Course Id'],
                        'validate': lambda text: len(text) == 9,
                    },
                    {
                        'type': 'input',
                        'name': 'Course Name',
                        'message': 'Course Name:',
                        'default': course_info['Course Name'],
                        'validate': lambda text: len(text) > 0,
                    },
                    {
                        'type': 'input',
                        'name': 'Year',
                        'message': 'Year:',
                        'default': course_info['Year'],
                        'validate': lambda text: len(text) > 0 and self.check_int(text),
                    },
                    {
                        'type': 'input',
                        'name': 'Semester',
                        'message': 'Semester:',
                        'default': course_info['Semester'],
                        'validate': lambda text: len(text) > 0,
                    },
                    {
                        'type': 'input',
                        'name': 'Credit',
                        'message': 'Credit:',
                        'default': str(course_info['Credit']),
                        'validate': lambda text: len(text) > 0,
                    },
                    {
                        'type': 'input',
                        'name': 'Section',
                        'message': 'Section:',
                        'default': str(course_info['Section']),
                        'validate': lambda text: len(text) > 0,
                    },
                    {
                        'type': 'list',
                        'name': 'Grade',
                        'message': 'Grade:',
                        'choices': [
                            'A',
                            'B+',
                            'B',
                            'C+',
                            'C',
                            'D+',
                            'D',
                            'F',
                        ],
                        'default': 5,
                    },
                ]

                answers5 = prompt(questions5, style=custom_style_2)
                answers5["Grade(Score)"] = self.grade_table[answers5['Grade']]


                pprint(answers5)

                self.update_row_with_dict(answers5, int(answers4['course']))

            elif(answers['todo'] == "Summary"):
                pprint(self.db)

            elif (answers['todo'] == "Calculate GPA"):

                yearxsemester = self.db[["Year", "Semester"]]
                yearxsemester = yearxsemester.drop_duplicates()
                year_ = ["Year {} Semester {}".format(row[1]['Year'], row[1]['Semester']) for row in yearxsemester.iterrows()]

                yearxsemester_dict = {}
                # for i
                questions3 = [
                    {
                        'type': 'list',
                        'name': 'term',
                        'message': 'Which year and semester do you want?',
                        'choices': ['Total'] + year_
                    }
                ]

                answers3 = prompt(questions3, style=custom_style_2)

                if(answers3['term'] == 'Total'):

                    self.db = self.db.astype({'Credit': int})
                    sp = self.db['Grade(Score)'] * self.db['Credit']
                    gpa = sp.sum() / self.db['Credit'].sum()
                    art.tprint("GPA = {}".format(gpa // 0.01 / 100))
                else:
                    year_split = answers3['term'].split(" ")
                    year = year_split[1]
                    semester = year_split[3]
                    db_filter = self.db[(self.db["Year"] == year) & (self.db["Semester"] == semester)]
                    db_filter = db_filter.astype({'Credit': int})
                    sp = db_filter['Grade(Score)'] * db_filter['Credit']
                    gpa = sp.sum() / db_filter['Credit'].sum()
                    # print("GPA:", gpa, "sp:", sp.sum(), "credit:", db_filter['Credit'].sum())
                    if not self.singlepoint(gpa):
                        gpa = gpa // 0.01 / 100

                    art.tprint("GPA = {}".format(gpa))

            answers = prompt(questions, style=custom_style_2)

        if (answers['todo'] == "Save and Close"):
            self.db.to_csv('GPA.csv', encoding='utf-8', index=False)
            art.tprint("Goodbye")

if __name__ == "__main__":
    csv = CSVdb()
    csv.load('GPA.CSV')
    csv.main()
    # print(csv.db)
