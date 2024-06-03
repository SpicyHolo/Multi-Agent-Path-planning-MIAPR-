import json
import numpy as np

def main():
    json_file_path = "./test/out.json"
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    n_tasks_finished = data['numTaskFinished']
    avg_planning_time = np.average(data['plannerTimes'])
    max_planning_time = np.max(data['plannerTimes'])
    sum_of_costs = data['sumOfCost']

    print(f"Finished Tasks: {n_tasks_finished}")
    print(f"Planning time (max, avg): {avg_planning_time:.2f}, {max_planning_time:.2f}")
    print(f"Costs sum: {sum_of_costs}")



if __name__ == "__main__":
    main()

