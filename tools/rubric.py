import os
import yaml
from IPython.display import display, Javascript


class Rubric():
    
    def __init__(self, nb_name, yml_path=None, **kwargs):
        """Constructor"""
        
        week, assignment = nb_name.split('/')[-2:]
        assignment = assignment.split('.')[0]
        problem = '_'.join(assignment.split('_')[:2])
        student = '_'.join(assignment.split('_')[-3:])

        self.student = student
        self.problem = problem

        cwd = os.path.join(os.path.expanduser('~'), week)
        assignments = [f.split('.')[0] for f in os.listdir(cwd) if f.endswith('.ipynb')]
        self.all_problems = list(set(['_'.join(a.split('_')[:2]) for a in assignments]))
        self.all_students = ['_'.join(a.split('_')[-3:]) for a in assignments]
        
        if yml_path is None:
            self.yml_path = os.path.join(cwd, '{}.yml'.format(week))

    def _display_table(self, table, title):
        
        for idx, row in enumerate(table):
            if idx < 1:
                left = title
            else:
                left = ' ' * len(title)
                
            print('{} | {} points | {}'.format(left, row, table[row]))
            
        print()
            
    def _get_input(self, name, minimum=0, maximum=5):
        
        value = input("Enter your score for {}: ".format(name))
        
        while True:
            try:
                value = float(value)
                if value >= minimum and value <= maximum:
                    break
            except:
                pass
            
            value = input(
                "Your score must be between 0 and 5. "
                "Enter your score for {}: ".format(name)
            )
        
        return value
            
    def display_rubric(self):

        self.correctness = {
            0: 'Code does not run.',
            2: 'Code runs, but does not produce correct ',
            4: 'Code runs, produces correct output but output is difficult to understand.',
            5: 'Code runs, produces correct output and output is easy to understand.'
        }
        
        self.readability = {
            0: 'Code is not documented and is impossible to understand.',
            2: 'Code is poorly documented, and uses non-recommended practices.',
            4: 'Code is documented, but uses non-recommended practices',
            5: 'Code is fully documented (as appropriate), and uses good programming practices.'
        }
        
        print('Assessment Form\n')
        print('-' * 80)
        
        self._display_table(self.correctness, 'Correctness')
        self.correctness_value = self._get_input('correctness')
        print('-' * 80)
        
        self._display_table(self.readability, 'Readability')
        self.readability_value = self._get_input('readability')
        print('-' * 80)
        
        self.comments_value = input('Enter any comments: ')
        print('-' * 80)
        
        print('Assessment saved. To change your assessment, simply run the code cell again.')
        
        self._save_submitted(self.yml_path)
        self._display_tasks()
        
    def _save_submitted(self, path):

        s = self.student
        p = self.problem

        if os.path.exists(path):
            with open(path) as f:
                data = yaml.load(f)
            os.remove(path)
        else:
            data = {}

        if s not in data:
            data[s] = {}
        if p not in data[s]:
            data[s][p] = {}

        data[s][p]['correctness'] = self.correctness_value
        data[s][p]['readability'] = self.readability_value
        data[s][p]['comments'] = self.comments_value

        with open(path, 'w') as f:
            f.write(yaml.dump(data))

    def _display_tasks(self):

        with open(self.yml_path) as f:
            data = yaml.load(f)

        done = {}
        todo = {}

        for student in self.all_students:
            if student not in data.keys():
                done[student] = ['']
                todo[student] = self.all_problems
                continue
            done[student] = []
            todo[student] = []
            for problem in self.all_problems:
                if problem in data[student].keys():
                    done[student].append(problem)
                else:
                    todo[student].append(problem)
     
        print('\nCompleted tasks')
        print('-' * 80)
        for s in sorted(done):
            print('{}: {}'.format(s, ', '.join(done[s])))
        print('-' * 80)
        print('Remaining tasks')
        print('-' * 80)
     
        # check for any non-empty list, an empty list is False
        if any(todo.values()):
            for s in sorted(todo):
                if todo[s]:
                    print('{}: {}'.format(s, ', '.join(todo[s])))
        # if all empty
        else:
            print('You have no remaining tasks.\n\nYou are ready to submit. Go to Assignments tab and click Submit.')
