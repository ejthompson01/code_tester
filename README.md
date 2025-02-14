## code_tester: Overview

The purpose of this code is to automate comparisons of the output of user-submitted code to the output of an "answer key" and provide useful data about these comparisons.

More specifically, given a [key.py](key.py) containing function definitions and predefined inputs, along with a collection of [user-submitted code](student_code), this code will compare the output of the user-submitted code with the output of the code in the key and create summaries including runtimes, errors, etc.

The intent is to aid educators who need to review code, especially those who have many students. This is not meant to be a replacement to human review, nor to be any type of "auto-grader". It simply runs each user's code, compares the output, and summarizes the results. The educator can then use this information to help focus their efforts when doing their review.

**DISCLAIMER**: **One of the primary goals of this code is to execute code submitted by others without the whole process crashing when it encounters erroneous or malformed code. It is not generally a good idea to run any arbitrary code sent to you. This code contains no safeguards to prevent execution of potentially malicious code. It is your responsibility to review your users' submissions and take whatever safeguards you deem necessary (e.g., run it in an isolated environment, virtual and/or physical, from which access to your own data, the internet, etc. is not possible).**

This code does contain a timeout feature which will attempt to gracefully interrupt functions if they run for too long. It is not guaranteed that this feature will be effective on all systems or in all cases, but it has been tested to ensure that honest mistakes made by honest users will _probably_ be handled (e.g., breaking out of accidental infinite loops). Some such test cases are included in the examples provided.

---

### Quick Start Guide

This repository is already initialized with functional examples; no setup is necessary aside from making sure that you have Python and required libraries installed (this project is managed using [uv](https://docs.astral.sh/uv/), please see [their website](https://docs.astral.sh/uv/) for more information).

For those who wish to just see the code work, all that is needed is to first clone the repository, and then:

```python
from src import professor
prof = professor.Professor(assignment_name='yourAssignmentName')
prof.check_students()
```

Then, inspect the output found in [`logs/`](logs/) and [`reports/`](reports/).

More detailed instructions below.

---

### Creating/Checking a New Assignment

1) Create a key.py file.
2) Place student code in the student_code folder.
3) Run the utility.
4) Inspect the output.

### 1) Create a key.py file

The answer key, [`key.py`](key.py), should be placed in the main directory. Questions are defined as instances of the included class `Question`, which has the following properties:

- `fun`: The function to be run.
- `args`: Optional tuple of arguments that will be passed positionally to the function.
- `kwargs`: Optional dictionary of arguments that will be passed by keyword to the function.
- `timeout_secs`: Optional float that defines the number of seconds before a student's function will be sent a KeyboardInterrupt:
    - `None`: (Default) The timeout will be equal to the professor's runtime multiplied by `DFLT_TIMEOUT_MULT`. (Defined in [`professor.py`](src/professor.py))
    - `0`: No timeout. Not recommended.
    - Any other number defines the number of seconds a student's code will run before a KeyboardInterrupt is sent.

### 2) Place student code in the [student_code](student_code) folder

- The [`__init__.py`](student_code/__init__.py) contains logic to import all files ending in `.py` and not starting with `_`. This file should not be edited or removed.
- Each student's submission should be a `.py` file whose name does not start with `_`.
- If any student's submission contains syntax or other errors which prevent a succesful import this _should_ be automatically reported at runtime and not prevent the rest of the process from running.

### 3) Run the utility

- Instantiate a `src.professor.Professor()`. Arguments include:
    - `assignment_name`: Provide a string to name the assignment (required)
    - `clear_outputs`: If True (default), existing files in `logs/` and `reports/` are deleted first.
    - `print_logs`: If True (default), information written to the log is also printed to the screen. The log will be saved in `logs/` either way.

### 4) Inspect the Output

- `logs/` will contain a timestamped file starting with `log_` containing general information related to runtimes and whether or not each question was found in each student's code.

- `reports/` will contain:
    - `_summary.csv`: A grid of booleans with students on one axis and questions on the other. Values are `True` if the student's output matched the key, and `False` otherwise.
    - Individual reports for each student named like `yourAssignmentName_student.csv`. Each question is listed as a row, and columns contain information such as the arguments provided, runtimes, and whether or not the function succesfully ran without error (work in progress).

---

### Test Cases

The following test cases are included in [`student_code`](student_code/) and are not advertised as an exhaustive suite of tests! Please let me know if you find any interesting cases and/or recommendations about how to catch errors I haven't anticipated.

- user1: All code is correct.
- user2: Output for q1 will be incorrect (they add 2 instead of 1).
- user3: Did not submit q3.
- user4: q2 signature is missing an input.
- user5: Wrote an infinite loop for q3.
- user6: Similar to user5, but included their own error handling.
- user7: Similar to user6, but with their try/except inside the loop.
- user8: Syntax error. Module cannot be imported.
- user9: Runs a time.sleep() command which might not respond to the interrupt it will be sent.

