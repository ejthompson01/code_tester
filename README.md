## code_tester

The purpose of this code is to allow users to submit .py files containing function definitions and compare the output of their functions with an "answer key".

**DISCLAIMER**: One of the primary functions of this code is to run arbitrary code submitted by others. There are no safeguards built into this code to prevent execution of malicious code (there is only a mild and at best partially effective attempt to gracefully timeout things like infinite loops). You should not use this code unless you understand the risks assocated with running arbitrary code! Ideally, you should set up an isolated machine/environment (whether virtual or physical) and take whatever steps you deem necessary to ensure that potentially malicious code will not be able to access sensitive or private information, launch attacks over the internet, or succesfully engage in nefarious activities. The author of this code is not responsible for any adverse side effects! Additionally, never run any code from anyone under any circumstances unless you trust the author! **Use this code at your own risk.**

**ADDITIONALLY**: While I normally espouse thorough documentation and commenting of code, this code is intentionally lacking in that regard. This is to reinforce the fact that you should not be using this code unless you know exactly why you are using it and what it does! **Use this code at your own risk.**

### Quick-Start Guide

...explain the setup. explain the sample cases...

### The Key
...explain how the key works...

### Test Cases Included:

- user1: All code is correct.
- user2: Output for q1 will be incorrect (they add 2 instead of 1).
- user3: Did not submit q3.
- user4: q2 signature is missing an input.
- user5: Wrote an infinite loop for q3.
- user6: Similar to user5, but included their own error handling.
- user7: Similar to user6, but with their try/except inside the loop.
- user8: Syntax error. Module cannot be imported.

<br><br>
---
#### ToDos:

- floats. When comparing answers, consider how different order of ops may lead to different values.

- how lists/tuples/etc are ordered. if we want to extend this to other things, e.g., dbs, consider optional sorting issues like those seen before.

- write a compare() method to allow for additional/future flexibility.

