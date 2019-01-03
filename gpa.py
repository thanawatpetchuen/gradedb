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
        # Load CSV file to DataFrame

        self.db = pd.read_csv(file_name, encoding='utf8',
                              dtype={'Course Id': 'str', 'Grade(Score)': 'float',
                                     'Credit': 'int', 'Year': 'str','Semester': 'str'})

        # Print logo text
        art.tprint("GradeDB", font="roman")

    def check_int(self, text):
        # Check the input text if it's int
        try:
            if int(text):
                return True
        except ValueError:
            return False

    def singlepoint(self, n):
        # Check the number if have 1 floating point
        gpa = str(n)
        if gpa[::-1].find('.') == 1:
            return True
        return False

    def update_row_with_dict(self, dictionary, index):
        # Update DataFrame with index by dictionary
        for key in dictionary.keys():
            self.db.loc[index, key] = dictionary.get(key)

    def main(self):
        # Main function to call

        main_menu_questions = [
            {
                'type': 'list',
                'name': 'todo',
                'message': 'What do you want to do?',
                'choices': [
                    'Insert',
                    'Update',
                    'Summary',
                    'Calculate GPA',
                    'Save and Close',
                    'Close'
                ]
            }
        ]

        main_menu_answers = prompt(main_menu_questions, style=custom_style_2)
        while main_menu_answers['todo'] != "Save and Close":
            if main_menu_answers['todo'] == "Insert":
                insert_questions = [
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
                insert_answers = prompt(insert_questions, style=custom_style_2)   # Get the answer
                insert_answers["Grade(Score)"] = self.grade_table[insert_answers['Grade']]  # Map Grade to score

                self.db = self.db.append(insert_answers, ignore_index=True)  # Append the new course to DB

            elif main_menu_answers['todo'] == "Update":
                pprint(self.db)  # Show current DB
                update_questions = [
                    {
                        'type': 'input',
                        'name': 'course',
                        'message': 'Which year and semester do you want?',
                         'validate': lambda text: int(text) <= self.db.tail(1).index.item(),
                    }
                ]

                update_answers = prompt(update_questions, style=custom_style_2)
                course_info = self.db.iloc[int(update_answers['course'])]  # Find selected course from answer

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

                update_course_questions = [
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

                update_course_answers = prompt(update_course_questions, style=custom_style_2)
                update_course_answers["Grade(Score)"] = self.grade_table[update_course_answers['Grade']]  # Map Grade from score

                self.update_row_with_dict(update_course_answers, int(update_answers['course']))  # Update DB from answer

            elif main_menu_answers['todo'] == "Summary":
                pprint(self.db)  # Show DB

            elif main_menu_answers['todo'] == "Calculate GPA":

                year_semester = self.db[["Year", "Semester"]]  # Select only Year and Semester coloumn
                year_semester = year_semester.drop_duplicates()  # Drop the duplicate value
                # Get the unique Year and Semester pair
                year_ = ["Year {} Semester {}".format(row[1]['Year'], row[1]['Semester']) for row in year_semester.iterrows()]

                select_term_questions = [
                    {
                        'type': 'list',
                        'name': 'term',
                        'message': 'Which year and semester do you want?',
                        'choices': ['Total'] + year_
                    }
                ]

                select_term_answers = prompt(select_term_questions, style=custom_style_2)

                if select_term_answers['term'] == 'Total':
                    self.db = self.db.astype({'Credit': int})  # Cast credit column to int
                    # (After update mode will cause conflict!)
                    sp = self.db['Grade(Score)'] * self.db['Credit']  # Calculate Product of Score and Credit
                    gpa = sp.sum() / self.db['Credit'].sum()  # Calculate SumProduct / Sum of Credit
                    if not self.singlepoint(gpa):  # Avoid round down if there is one floating point
                        gpa = gpa // 0.01 / 100
                    art.tprint("GPA = {}".format(gpa))  # Print the GPA
                else:
                    #  Calculate specific term
                    year_split = select_term_answers['term'].split(" ")  # Extract the selected term
                    year = year_split[1]  # Get the year
                    semester = year_split[3]  # Get the semester
                    # Filter the db by given Year and Semester
                    db_filter = self.db[(self.db["Year"] == year) & (self.db["Semester"] == semester)]
                    db_filter = db_filter.astype({'Credit': int})  # Cast credit column to int (same as above)
                    sp = db_filter['Grade(Score)'] * db_filter['Credit']  # Calculate Product of Score and Credit
                    gpa = sp.sum() / db_filter['Credit'].sum()  # Calculate SumProduct / Sum of Credit
                    if not self.singlepoint(gpa):  # Avoid round down if there is one floating point
                        gpa = gpa // 0.01 / 100
                    art.tprint("GPA = {}".format(gpa))  # Print the GPA

            main_menu_answers = prompt(main_menu_questions, style=custom_style_2)  # Loop the main menu question

        if (main_menu_answers['todo'] == "Save and Close"):
            # Save current state of db to csv and close
            print("Saveing....")
            self.db.to_csv('GPA.csv', encoding='utf-8', index=False)
            print("Complete!")
            art.tprint("Goodbye")
        else:
            art.tprint("Goodbye")

if __name__ == "__main__":
    csv = CSVdb()
    csv.load('GPA.CSV')
    csv.main()

