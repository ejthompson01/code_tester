from datetime import datetime as dt
from glob import glob
import pandas as pd
import inspect
import os

# Imports all code in the student_code directory
import student_code

# Imports the StudentFunction (which should really be named something like "PreparedFunction") [_]
from src.student import StudentFunction

# Imports the professor's answer key
import key

# If determining timeouts dynamically,
# they will be the professor's runtime 
# multiplied by this value
DFLT_TIMEOUT_MULT = 10

# Path to logs
PATH_LOGS = 'logs'
PATH_LOG = os.path.join(PATH_LOGS, 'log')

# Path to reports (student and professor)
PATH_REPORTS = 'reports'
PATH_SUMMARY = os.path.join(PATH_REPORTS, '_summary.csv')

# For identifying code to skip/include
KEY_SKIP = '_'
KEY_QUESTION = 'q'

# Names of columns in the student reports
COL_ARGS = 'Args'
COL_KWARGS = 'Kwargs'
COL_OUTPUT = 'Output'
COL_EXPECTED = 'Expected'
COL_MATCH = 'Match'
COL_RUNTIME = 'Runtime'
COL_CLEAN_EXIT = 'CleanExit'

# Columns above organized as an ordered list.
COLS = [COL_ARGS,
        COL_KWARGS,
        COL_OUTPUT,
        COL_EXPECTED,
        COL_MATCH,
        COL_RUNTIME,
        COL_CLEAN_EXIT
        ]

def timestamp() -> str:
    '''
    Function for adding unique timestamps
    to things like entries in log files.
    '''
    t = str(dt.now())
    for char in [' ', ':', '.']:
        t = t.replace(char, '-')
    return t

class Professor:     
    '''
    Create an instance of this class when the key.py
    and student_code folder are finalized.

    Upon instantiation this class will load the answer key (key.py),
    and create a dictionary containing student code with the name of their
    .py file as keys and their code as values.

    The student code is not actually executed until .check_students() is run.

    Arguments:
        - assignment_name: The name of the assignment. Will be preprended to output files.
        - clear_outputs: If True (default), clears the contents of logs/ and reports/ before running.
        - print_logs: If True (default), all function calls that write to the log file are also printed to the screen.
    '''
    
    def __init__(self,
                 assignment_name: str,
                 clear_outputs: bool =True,
                 print_logs = True
                 ):
        self.assignment_name = assignment_name
        self.print_logs = print_logs

        if clear_outputs:
            self.clear_logs()
            self.clear_reports()
        
        # Load the answer key
        self.init_key()

        # Load the student key
        self.init_students()
        
        # Initialize the log
        self.init_log()
        return
    
    def init_key(self):
        '''
        Load the contents of key.py, run the functions within,
        and store the details in self.results: dict.
        '''
        self.results: dict[str, StudentFunction] = {}

        for qid, q in key.questions.items():
            self.results[qid] = StudentFunction(q.fun, q.args, q.kwargs, None)
            self.results[qid].run_fun()

            # Determine the timeout
            if self.results[qid].timeout_secs is None:
                self.results[qid].timeout_secs = \
                    self.results[qid].runtime.total_seconds()*DFLT_TIMEOUT_MULT

        # Keep a sorted list of question id's
        self.question_ids = list(self.results.keys())
        self.question_ids.sort()
        return
    
    def init_students(self) -> None:
        '''
        Load student code into a dictionary.
        Code must be a .py file and not start with an underscore.
        '''
        self.students = {}
        for name, obj in inspect.getmembers(student_code, predicate=inspect.ismodule):
            if not name.startswith(KEY_SKIP):
                self.students[name] = obj

        # Keep a sorted list of student names
        self.student_names = list(self.students.keys())
        self.student_names.sort()
        return
    
    def init_log(self) -> None:
        '''
        Create a timestamped log file.

        Initial lines written include the number of questions
        found and the number of student submisssions found.
        '''
        self.log_name = PATH_LOG + '_' + timestamp()
        with open(self.log_name, 'w'):
            pass
        self.write_log('Process initialized')
        self.write_log(f'Questions in key: {len(self.results)}')
        self.write_log(f'Submissions found: {len(self.students)}')
        return
    
    def write_log(self, 
                  message: str
                  ) -> None:
        '''
        Write a line to the main log.

        Only include the message. A timestamp will be prepended and newline inserted at the end.
        '''
        message = f'{dt.now()}::{message}'
        if self.print_logs:
            print(message, flush=True)
        with open(self.log_name, 'a') as f:
            f.write(message + '\n')
        return
    
    def check_student(self, 
                      student_name: str
                      ) -> pd.DataFrame:
        '''
        Given a student_name, find the student's submission.
        Then search their submission for each entry in the key,
        run it, compare output, and log results.
        '''

        # Initialize student report
        student_report = pd.DataFrame(index=self.question_ids, columns=COLS)
        student_report.index.name = 'Question'
        
        # Gather student functions
        student_funs = {}
        for name, obj in inspect.getmembers(self.students[student_name], predicate=inspect.isfunction):
            if name.startswith(KEY_QUESTION):
                student_funs[name] = obj
        
        # For each question in the key,
        # search the student's submission for a matching function
        for qid in self.question_ids:
            # If the question was found in the student's submission...
            if qid in student_funs:
                self.write_log(f'{qid} for {student_name} found!')

                # Get the arguments
                args = self.results[qid].args
                kwargs = self.results[qid].kwargs
                # Get the defined timeout
                timeout_secs = self.results[qid].timeout_secs

                # Instantiate a new StudentFunction
                prepared_function = StudentFunction(student_funs[qid], 
                                                    args=args,
                                                    kwargs=kwargs,
                                                    timeout_secs=timeout_secs
                                                    )
                # Run the function
                prepared_function.run_fun()
                
                # Record details
                details = [
                    args,
                    kwargs,
                    prepared_function.result,
                    self.results[qid].result,
                    prepared_function.result == self.results[qid].result,
                    prepared_function.runtime,
                    prepared_function.clean_exit
                    ]
                
                # If the function was sent an interrupt, log it
                if prepared_function.interrupted:
                    self.write_log(f'{qid} for {student_name} triggered an interrupt.')

            else:
                # If the question was not found in the student's submission...
                self.write_log(f'{qid} for {student_name} was NOT found!')

                # Record details
                details = [
                    '',
                    '',
                    'Code not found!',
                    self.results[qid].result,
                    False,
                    '',
                    ''
                    ]
                
            # Add the details for this question to the student's report
            student_report.loc[qid] = details
        
        # Return the student's report
        return student_report
    
    def check_students(self) -> None:
        '''
        Check all student code.

        This function loops over all students and runs check_student() for each.
        '''
        self.write_log('check_students started')

        # Create the main summary
        self.summary = pd.DataFrame(index=self.student_names, 
                                    columns=self.question_ids
                                    )
        self.summary.index.name = 'Student'

        # Loop over all student submissions
        for student in self.student_names:
            self.write_log(f'Started checking code for: {student}')
            
            # Check the student code
            report = self.check_student(student)

            # Save their report
            report.to_csv(os.path.join(PATH_REPORTS, f'{self.assignment_name}_{student}.csv'))

            # Log their overall correct/incorrect result to the main summary
            for qid in self.question_ids:
                self.summary.loc[student, qid] = report.loc[qid, COL_MATCH]
            self.write_log(f'Finished checking code for: {student}')

        # Output the main summary
        self.summary.to_csv(PATH_SUMMARY)
        self.write_log('check_students finished')
        return

    def clear_reports(self) -> None:
        '''
        Clears everything in the reports/ folder.
        '''
        reports = glob(os.path.join(PATH_REPORTS, '*'))
        for report in reports:
            os.remove(report)
        return
    
    def clear_logs(self) -> None:
        '''
        Clears everything in the logs/ folder.
        '''
        logs = glob(PATH_LOG + '*')
        for log in logs:
            os.remove(log)
        return

    