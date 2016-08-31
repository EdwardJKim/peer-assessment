import os
import yaml
from IPython.display import display, Javascript


class Rubric():
    
    def __init__(self, nb_name, yml_path=None, nproblems=3, **kwargs):
        
        """Constructor"""
        
        self.nproblems = nproblems

        week, assignment = nb_name.split('/')
        assignment = assignment.split('.')[0]
        problem = '_'.join(assignment.split('_')[:3])
        student = '_'.join(assignment.split('_')[-3:])

        self.student = student
        self.problem = problem

        assignments = [f.split('.')[0] for f in os.listdir(os.getcwd()) if f.endswith('.ipynb')]
        self.all_problems = list(set(['_'.join(a.split('_')[:3]) for a in assignments]))
        self.all_students = ['_'.join(a.split('_')[-3:]) for a in assignments]
        
        if yml_path is None:
            self.yml_path = os.path.join('{}.yml'.format(os.getcwd().split('/')[-1]))

            
    def getname(self):
        display(Javascript('''
            var nb = IPython.notebook;
            var kernel = IPython.notebook.kernel;
            var command = "NOTEBOOK_FULL_PATH = '" + nb.base_url + nb.notebook_path + "'";
            kernel.execute(command);
            '''
        ))
        return NOTEBOOK_FULL_PATH

    
    def _display_table(self, table, title):
        
        for idx, row in enumerate(table):
            if idx < 1:
                left = title
            else:
                left = ' ' * len(title)
                
            print('{} | {} points | {}'.format(left, row, table[row]))
        print()
            
        
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
        self.correctness_value = eval(input('Enter your score for correctness: '))
        
        print('-' * 80)
        self._display_table(self.readability, 'Readability')
        self.readability_value = eval(input('Enter your score for readability: '))

        print('-' * 80)
        
        self.comments_value = input('Enter any comments: ')
        
        print('-' * 80)
        print('Assessment submitted')
        print('To change your assessment, simply run the code cell again.')
        
        self._save_submitted(self.yml_path)
        self._on_validate_clicked()
        
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

    def _on_validate_clicked(self):

        if not os.path.exists(self.yml_path):
            print("No data found. You haven't graded any peers.")
            return

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
     
        print('\nSubmitted')
        print('---------')
        for s in sorted(done):
            print('{}: {}'.format(s, ', '.join(done[s])))
        print('')
        print('Remaining tasks')
        print('---------------')
        for s in sorted(todo):
            print('{}: {}'.format(s, ', '.join(todo[s])))
