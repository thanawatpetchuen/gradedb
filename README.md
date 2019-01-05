# GradeDB

The program that load the CSV file and use them as database. Main function is to Insert / Update / Save course and it's detail and Calculate the GPA from given CSV


## Prerequisites

This program needs Python 3 and following libraries

* [PyInquirer](https://github.com/CITGuru/PyInquirer) - The interactive UI for Python
* [tabulate](https://pypi.org/project/tabulate/) - Pretty table presentation
* [pandas](https://pandas.pydata.org/) - The way of playing with data
* [art](https://pypi.org/project/art/) - Used to generate ASCII art
* [NBLOGIC](https://pypi.org/project/nblogic/) - NBLOGIC for Python by Thanawat Petchuen


### Installing

First, install this project by pip

```
pip install gradedb
```

### Usage

Go to console and run the script

```
gradedb "filename.csv"
```
or use KLOGIC database (require authentication)

```
gradedb
```

## Note

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

The structure (header) of CSV file must be following
| Course Id  | Course Name | Year | Semester | Credit | Section | Grade | Grade(Score) |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 010013001  | INTRODUCTION TO ENGINEERING  | 2559  | 1 | 1 | 1 | B | 3.0 |
| 010123102  | PROGRAMMING FUNDAMENTALS  | 2559  | 1 | 3 | 1 | A | 4.0 |

## Authors

* **Thanawat Petchuen** - [Thanawat(GitHub)](https://github.com/thanawatpetchuen) - [Thanawat(Bitbucket)](https://bitbucket.org/thanawatpetchuen/) 


## License

This project is licensed under the MIT License 

