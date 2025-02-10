## code_tester

The purpose of this code is to allow users to submit .py files containing function definitions and compare the output of their functions with an "answer key".

Additionally, this code contains a timeout feature which will attempt to interrupt functions if they run for too long (see below). Note that this is not guaranteed to work in all cases or on all systems.

**DISCLAIMER**: One of the primary functions of this code is to run arbitrary code submitted by others. There are no safeguards built into this code to prevent execution of malicious code (there is only a mild and at best partially effective attempt to gracefully timeout things like infinite loops). You should not use this code unless you understand the risks assocated with running arbitrary code! Ideally, you should set up an isolated machine/environment (whether virtual or physical) and take whatever steps you deem necessary to ensure that potentially malicious code will not be able to access sensitive or private information, launch attacks over the internet, or succesfully engage in nefarious activities. The author of this code is not responsible for any adverse side effects! Additionally, never run any code from anyone under any circumstances unless you trust the author. **Use this code at your own risk.**

### Quick-Start Guide

...explain the setup. explain the sample cases...

---

### Creating an answer key
[`key.py`](key.py) is located in the main directory and contains a single class definition: `Question`. The professor will write their function definitions and define arguments to be passed when the function is run. One instance of this class will be created for each question containing:

- fun: The function
- args: Optional tuple
- kwargs: Optional dictionary
- timeout_secs:
    - None: (Default) The professor's runtime is multiplied by DFLT_TIMEOUT_MULT defined in [`professor.py`](src/professor.py)
    - 0: Timeout is not implemented
    - Any other number defines the amount of time a student's code will run before a KeyboardInterrupt is triggered.

### Usage
Put the students' .py files into the `student_code` folder. All files that end in `.py` and do not start with `_` will be imported. If any files contain errors which prevent a succesful import, a message will be printed later when running the tool.

Once the student code and answer key are in place, run the tool:

```python
from src import professor
prof = professor(assignment_name='your assignment name')
prof.check_students()
```

The output generated will consist of:

YOU ARE HERE

---

### Test Cases Included:

- user1: All code is correct.
- user2: Output for q1 will be incorrect (they add 2 instead of 1).
- user3: Did not submit q3.
- user4: q2 signature is missing an input.
- user5: Wrote an infinite loop for q3.
- user6: Similar to user5, but included their own error handling.
- user7: Similar to user6, but with their try/except inside the loop.
- user8: Syntax error. Module cannot be imported.
- user9: Runs a time.sleep() command which might not respond to the interrupt it will be sent.

<br><br>
---
#### ToDos:

- floats. When comparing answers, consider how different order of ops may lead to different values.

- how lists/tuples/etc are ordered. if we want to extend this to other things, e.g., dbs, consider optional sorting issues like those seen before.

- ...write a compare() method to allow for additional/future flexibility.

