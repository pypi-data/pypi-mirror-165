import json
import numpy as np



class HMMParam:
    def __init__(self, state_names, starting_probabilities, transitions, emissions): 
        self.state_names = np.array(state_names)
        self.starting_probabilities = np.array(starting_probabilities)
        self.transitions = np.array(transitions)
        self.emissions = np.array(emissions)


    def __str__(self):
        out = f'state_names = {self.state_names.tolist()}\n'
        out += f'starting_probabilities = {self.starting_probabilities.tolist()}\n'
        out += f'transitions = {self.transitions.tolist()}\n'
        out += f'emissions = {self.emissions.tolist()}'
        return out

    def __repr__(self):
        return f'{self.__class__.__name__}({self.state_names}, {self.starting_probabilities}, {self.transitions}, {self.emissions})'
        

def read_HMM_parameters_from_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)

    state_names = data['state_names']
    starting_probabilities = data['starting_probabilities']
    transitions = data['transitions']
    emissions = data['emissions']
    return HMMParam(state_names, starting_probabilities, transitions, emissions)

def get_default_HMM_parameters():
    state_names = ['Human', 'Archaic']
    starting_probabilities = [0.98, 0.02]
    transitions = [[0.9999,0.0001],[0.02,0.98]]
    emissions = [0.04, 0.4]
    return HMMParam(state_names, starting_probabilities, transitions, emissions)

def write_HMM_to_file(hmmparam, outfile):
    data = {key: value.tolist() for key, value in vars(hmmparam).items()}
    json_string = json.dumps(data, indent = 2) 
    with open(outfile, 'w') as out:
        out.write(json_string)




myhmm = read_HMM_parameters_from_file('Initialguesses.json')

# --------------


# def Make_HMM_parameters(state_names, starting_probabilities, transitions, emissions, outfile):
#     '''Saves parameters to a file'''
#     json_string = json.dumps({
#                 'state_names' : state_names.tolist(),
#                 'starting_probabilities' : starting_probabilities.tolist(),
#                 'transitions' : transitions.tolist(),
#                 'emissions' : emissions.tolist(),
#              }, indent = 2)

#     Make_folder_if_not_exists(outfile)
#     with open(outfile, 'w') as out:
#         out.write(json_string)


# def Load_HMM_parameters(markov_param):
#     '''Loads parameters to a file'''
#     if markov_param is None:
#         state_names, transitions, emissions, starting_probabilities = get_default_HMM_parameters()
#     else:
#         with open(markov_param) as json_file:
#             data = json.load(json_file)

#         state_names, starting_probabilities, transitions, emissions = data['state_names'], data['starting_probabilities'], data['transitions'], data['emissions']


#     # convert into numpy arrays
#     transitions, starting_probabilities, emissions, state_names = np.array(transitions), np.array(starting_probabilities), np.array(emissions), np.array(state_names)

#     return state_names, transitions, emissions, starting_probabilities







