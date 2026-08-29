# Smart Course Scheduler — Amirkabir University of Technology

A program for finding all possible course schedules where:

* No two classes overlap in terms of day and time.
* No two final exams overlap in terms of date and time.

The course data was manually/visually digitized from Report No. 212 of the Golestan system for the first semester of the 1404–1405 academic year and stored in JSON format.

## Project Structure

```text
course-scheduler/
├── main.py                       # Entry point; run this file
├── course_scheduler/             # Main code as a Python package
│   ├── __init__.py
│   ├── models.py                 # Course, Group, ClassTime, ExamTime classes
│   ├── engine.py                 # Backtracking engine for finding conflict-free schedules
│   ├── catalog.py                # JSON loading and course search
│   └── cli.py                    # Interactive command-line interface
├── data/
│   └── courses_data.json         # Complete course catalog (58 courses, ~250 groups)
├── tests/
│   └── test_engine.py            # Unit tests for conflict detection logic
└── README.md
```

## Installation and Usage

No external packages are required. Python 3.9 or higher is sufficient.

```bash
git clone <uni-course-scheduler>
cd course-scheduler
python3 main.py
```

The program first displays the entire course catalog with row numbers and then asks which courses you want to select.

You can enter any combination of the following three formats, separated by commas:

* Row number from the list (e.g. `1`)
* 7-digit course code (e.g. `3106103`)
* Part of the course name (e.g. `مدارهای منطقی`)

Example:

```text
Your selection: 1, 18, 3106103, مدارهای منطقی
```

The program then outputs all possible schedules in which none of the selected courses have class or exam conflicts, along with the total number of credits for each schedule.

## Running the Tests

```bash
python3 -m unittest discover -s tests -v
```

## Updating the Catalog for Future Semesters

To update the catalog for a future semester, simply replace:

```text
data/courses_data.json
```

with the course data from the new Golestan report.

Each course follows this structure:

```json
{
  "code": "1234567",
  "name": "Course Name",
  "credits": 3,
  "groups": [
    {
      "group": "01",
      "professor": "Professor Name",
      "gender": "Mixed",
      "classTimes": [
        {
          "day": "Saturday",
          "start": "10:00",
          "end": "12:00"
        }
      ],
      "examTime": {
        "date": "1405/10/20",
        "start": "09:00",
        "end": "12:00"
      }
    }
  ]
}
```

If a course does not have a final exam, such as a workshop or laboratory course, set:

```json
"examTime": null
```

## Data Accuracy and Limitations

The current data was manually extracted from images of the report rather than using automated OCR.

Nevertheless, before final course registration, make sure to verify your selected courses against the official Golestan system.

## License

MIT — use, modify, and distribute as you wish.
