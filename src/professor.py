from typing import Callable
from types import ModuleType

from datetime import datetime as dt
from glob import glob
import pandas as pd
import inspect
import os

import student_code
from src.student import StudentFunction

import key

PATH_LOGS = 'logs'
PATH_LOG = os.path.join(PATH_LOGS, 'log')

PATH_REPORTS = 'reports'
PATH_SUMMARY = os.path.join(PATH_REPORTS, '_summary.csv')

# For identifying code to skip/include
KEY_SKIP = '_'
KEY_QUESTION = 'q'

# Student report columns
COL_ARGS = 'Args'
COL_KWARGS = 'Kwargs'
COL_OUTPUT = 'Output'
COL_EXPECTED = 'Expected'
COL_MATCH = 'Match'
COL_RUNTIME = 'Runtime'
COL_CLEAN_EXIT = 'CleanExit'
COLS = [COL_ARGS,
        COL_KWARGS,
        COL_OUTPUT,
        COL_EXPECTED,
        COL_MATCH,
        COL_RUNTIME,
        COL_CLEAN_EXIT
        ]

def timestamp() -> str:
    t = str(dt.now())
    for char in [' ', ':', '.']:
        t = t.replace(char, '-')
    return t

class Professor:
    DFLT_TIMEOUT_MULT = 2
    
    #__slots__ = ()
    
    def __init__(self,
                 assignment_name: str,
                 clear_outputs=True,
                 print_logs = True
                 ):
        self.assignment_name = assignment_name
        self.print_logs = print_logs

        if clear_outputs:
            self.clear_logs()
            self.clear_reports()
        
        self.init_key()
        self.init_students()
        self.init_log()
        return
    
    def init_key(self):
        self.results: dict[str, StudentFunction] = {}
        self.timeouts: dict[str, float] = {}

        for qid, q in key.questions.items():
            self.results[qid] = StudentFunction(q.fun, None, q.args, q.kwargs)
            self.results[qid].run_fun()
            
            # HELD FIXED FOR TESTING [_]
            self.timeouts[qid] = 1

        self.question_ids = list(self.results.keys())
        self.question_ids.sort()
        return
    
    def init_students(self) -> None:
        self.students = {}
        for name, obj in inspect.getmembers(student_code, predicate=inspect.ismodule):
            if not name.startswith(KEY_SKIP):
                self.students[name] = obj
        self.student_names = list(self.students.keys())
        self.student_names.sort()
        return
    
    def init_log(self) -> None:
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
        Write to the main log. Timestamp and newline automatically included.
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
        # Initialize report
        student_report = pd.DataFrame(index=self.question_ids, columns=COLS)
        student_report.index.name = 'Question'
        # Gather student functions
        student_funs = {}
        for name, obj in inspect.getmembers(self.students[student_name], predicate=inspect.isfunction):
            if name.startswith(KEY_QUESTION):
                student_funs[name] = obj

        for qid in self.question_ids:
            if qid in student_funs:
                self.write_log(f'{qid} for {student_name} found!')

                args = self.results[qid].args
                kwargs = self.results[qid].kwargs

                prepared_function = StudentFunction(student_funs[qid], 
                                                    timeout_secs=self.timeouts[qid],
                                                    args=args,
                                                    kwargs=kwargs
                                                    )
                prepared_function.run_fun()
                details = [
                    args,
                    kwargs,
                    prepared_function.result,
                    self.results[qid].result,
                    prepared_function.result == self.results[qid].result,
                    prepared_function.runtime,
                    prepared_function.clean_exit
                    ]
                
                if prepared_function.interrupted:
                    self.write_log(f'{qid} for {student_name} triggered an interrupt.')

            else:
                self.write_log(f'{qid} for {student_name} was NOT found!')
                details = [
                    '',
                    '',
                    'Code not found!',
                    self.results[qid].result,
                    False,
                    '',
                    ''
                    ]
            student_report.loc[qid] = details
        return student_report
    
    def check_students(self) -> None:
        self.write_log('check_students started')

        self.summary = pd.DataFrame(index=self.student_names, 
                                    columns=self.question_ids
                                    )
        self.summary.index.name = 'Student'
        for student in self.student_names:
            self.write_log(f'Started checking code for: {student}')
            report = self.check_student(student)
            report.to_csv(os.path.join(PATH_REPORTS, f'{self.assignment_name}_{student}.csv'))
            for qid in self.question_ids:
                self.summary.loc[student, qid] = report.loc[qid, COL_MATCH]
            self.write_log(f'Finished checking code for: {student}')

        self.summary.to_csv(PATH_SUMMARY)
        self.write_log('check_students finished')
        return

    def clear_reports(self) -> None:
        reports = glob(os.path.join(PATH_REPORTS, '*'))
        for report in reports:
            os.remove(report)
        return
    
    def clear_logs(self) -> None:
        logs = glob(PATH_LOG + '*')
        for log in logs:
            os.remove(log)
        return

    