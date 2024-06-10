import json
import numpy as np
import os
import matplotlib.pyplot as plt

def load_json_files(directory):
    json_data = {}
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Check if the path is a file and not a directory
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                try:
                    # Load the JSON data from the file
                    json_dict = json.load(file)
                    # Add the data to the dictionary with the filename as key
                    json_data[filename] = json_dict
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {filename}: {e}")
    return json_data




def plot(x, y, label):
    data = np.array(list(zip(x, y)))
    sorted_data = data[data[:, 0].argsort()]
    x, y = sorted_data[:, 0], sorted_data[:, 1]

    plt.plot(x, y, label=label)


def main():
    datas = load_json_files('./tests')
    output_data = {}

    wh       = {'sizes': [], 'tasks': [], 't_avg': [], 't_max': [], 'cost': [], 'errors': []}
    wh_st    = {'sizes': [], 'tasks': [], 't_avg': [], 't_max': [], 'cost': [], 'errors': []}
    rand     = {'sizes': [], 'tasks': [], 't_avg': [], 't_max': [], 'cost': [], 'errors': []}
    rand_st  = {'sizes': [], 'tasks': [], 't_avg': [], 't_max': [], 'cost': [], 'errors': []}

    for fname, data in datas.items():

        tasks = data['numTaskFinished']
        t_avg = np.average(data['plannerTimes'])
        t_max = np.max(data['plannerTimes'])
        cost = data['sumOfCost']
        errors = len(data['errors'])
        print(fname)
        fname = fname.replace('.json', '')

        spacetime = False
        if 'spacetime' in fname:
            spacetime = True
            fname = fname.replace('_spacetime', '')
        if "warehouse" in fname and spacetime == False:
            wh['sizes'].append(int(fname.split('_')[-1]))
            wh['tasks'].append(tasks)
            wh['t_avg'].append(t_avg)
            wh['t_max'].append(t_max)
            wh['cost'].append(cost)
            wh['errors'].append(errors) 

        if "warehouse" in fname and spacetime == True:
            wh_st['sizes'].append(int(fname.split('_')[-1]))
            wh_st['tasks'].append(tasks)
            wh_st['t_avg'].append(t_avg)
            wh_st['t_max'].append(t_max)
            wh_st['cost'].append(cost)
            wh_st['errors'].append(errors) 

        if "random" in fname and spacetime == False:
            rand['sizes'].append(int(fname.split('_')[-1]))
            rand['tasks'].append(tasks)
            rand['t_avg'].append(t_avg)
            rand['t_max'].append(t_max)
            rand['cost'].append(cost)
            rand['errors'].append(errors) 

        if "random" in fname and spacetime == True:
            rand_st['sizes'].append(int(fname.split('_')[-1]))
            rand_st['tasks'].append(tasks)
            rand_st['t_avg'].append(t_avg)
            rand_st['t_max'].append(t_max)
            rand_st['cost'].append(cost)
            rand_st['errors'].append(errors)    
    fig = plt.figure(figsize=(10, 6))
    for i,field in enumerate(['tasks', 't_avg', 'cost', 'errors']):
        plt.subplot(2, 2, i+1)
        plot(rand['sizes'], rand[field], 'WHCA*')
        plot(rand_st['sizes'], rand_st[field], 'spacetime')
        plt.legend()
        plt.grid()
        plt.xlim((20,800))
        plt.xlabel("number of agents")
        plt.ylabel(field)
        plt.suptitle('Random map')
    
        # Ticks
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        # Legend
        plt.legend(fontsize=10)
        plt.tight_layout()
    plt.show()
    fig.savefig(f'./figs/rand.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    main()