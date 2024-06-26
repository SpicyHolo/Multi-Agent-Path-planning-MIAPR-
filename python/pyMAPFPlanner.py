import MAPF

from typing import Dict, List, Tuple,Set
from queue import PriorityQueue
import numpy as np

# 0=Action.FW, 1=Action.CR, 2=Action.CCR, 3=Action.W

class pyMAPFPlanner:
    def __init__(self, pyenv=None) -> None:
        if pyenv is not None:
            self.env = pyenv.env

        self.reservations = set()  # {(location, timestep)} means that location is occupied at timestep
        self.W = 10
        self.K = 5
        self.goal_reached_in_steps = 6
        self.master_plan = []
        print("pyMAPFPlanner created!  python debug")

    def initialize(self, preprocess_time_limit: int):
        """_summary_

        Args:
            preprocess_time_limit (_type_): _description_
        """
        pass
        print("planner initialize done... python debug")
        return True

    def plan(self, time_limit):
        """_summary_

        Return:
            actions ([Action]): the next actions

        Args:
            time_limit (_type_): _description_
        """
        if self.master_plan == []:
            self.reservations = set()
            self.goal_reached_in_steps = self.K
            for i in range(len(self.env.curr_states)):
                for j in range(self.K):
                    self.reservations.add((self.env.curr_states[i].location, self.env.curr_timestep + j))
            self.master_plan = self.whcr_star(100)
        try:
            actions = self.master_plan.pop()
        except:
            [MAPF.Action.W for i in range(len(self.env.curr_states))] 

        return actions
    
    def whcr_star(self,time_limit):
        print(self.env.curr_timestep)
        actions = [[MAPF.Action.W for i in range(len(self.env.curr_states))] for _ in range(self.K)]
        start_timestep = self.env.curr_timestep

        # Randomize robot priority
        indices = list(range(self.env.num_of_agents))
        np.random.shuffle(indices)

        for i in range(0, self.env.num_of_agents): #indices:
            self.robot_nr = i
            path = []
            if len(self.env.goal_locations[i]) == 0:
                print(i, " does not have any goal left", end=" ")
                path.append(
                    (self.env.curr_states[i].location, self.env.curr_states[i].orientation))
            else:
                # print(" with start and goal: ", end=" ")
                path = self.single_agent_plan(
                    self.env.curr_states[i].location, self.env.curr_states[i].orientation, self.env.goal_locations[i][0][0], start_timestep)

            # print("current location:", path[0][0],
            #       "current direction: ", path[0][1])
            for time in range(self.K):
                if len(path) <= time:
                    break
                if time == 0:
                    if path[time][0] != self.env.curr_states[i].location:
                        actions[time][i] = MAPF.Action.FW
                    elif path[time][1] != self.env.curr_states[i].orientation:
                        incr = path[time][1]-self.env.curr_states[i].orientation
                        if incr == 1 or incr == -3:
                            actions[time][i] = MAPF.Action.CR
                        elif incr == -1 or incr == 3:
                            actions[time][i] = MAPF.Action.CCR
                else:
                    try:
                        if path[time][0] != path[time - 1][0]:
                            actions[time][i] = MAPF.Action.FW
                        elif path[time][1] != path[time-1][1]:
                            incr = path[time][1] - path[time-1][1]
                            if incr == 1 or incr == -3:
                                actions[time][i] = MAPF.Action.CR
                            elif incr == -1 or incr == 3:
                                actions[time][i] = MAPF.Action.CCR
                    except:
                        continue
                        print(path)
                        print(time)
        # print(actions)
        actions = [np.array([int(a) for a in actions[time]], dtype=int) for time in range(self.goal_reached_in_steps)]
        actions.reverse()
        # print(actions)
        return actions
        # print(actions)
        # return np.array(actions, dtype=int)

    def single_agent_plan(self, start: int, start_direct: int, end: int, start_timestep: int):
        # print(start, start_direct, end)
        timestep = start_timestep
        path = []
        # AStarNode (u,dir,t,f)
        open_list = PriorityQueue()
        s = (start, start_direct, 0, self.getManhattanDistance(start, end), timestep)
        open_list.put([0, s])
        all_nodes = dict()
        close_list = set()
        parent = {(start, start_direct): None}
        all_nodes[start*4+start_direct] = s
        while not open_list.empty():    
            curr = (open_list.get())[1]
            timestep = curr[4]
            close_list.add(curr[0]*4+curr[1])
            if curr[0] == end:
                curr = (curr[0], curr[1])
                while curr != None:
                    path.append(curr)
                    curr = parent[curr]
                path.pop()
                path.reverse()
                break

            neighbors = self.getNeighbors(curr[0], curr[1], timestep + 1)  
            # print("neighbors=",neighbors)
            for neighbor in neighbors:
                if (neighbor[0]*4+neighbor[1]) in close_list:
                    continue
                next_node = (neighbor[0], neighbor[1], curr[2]+1,
                             self.getManhattanDistance(neighbor[0], end), curr[4] + 1)
                parent[(next_node[0], next_node[1])] = (curr[0], curr[1])
                open_list.put([next_node[3]+next_node[2], next_node])
            
        timestep_temp = start_timestep
        if len(path) < self.goal_reached_in_steps and len(path) != 0:
            if len(path)== 0:
                self.goal_reached_in_steps = 1
            self.goal_reached_in_steps = len(path)

        for i in range(self.W):
            timestep_temp += 1
            if len(path) > i:
                self.reservations.add((path[i][0], timestep_temp))
                self.reservations.add((path[i][0], timestep_temp - 1))
                self.reservations.add((path[i][0], timestep_temp + 1))
            else:
                try:
                    self.reservations.add((path[-1][0], timestep_temp))
                except:
                    self.reservations.add((start, timestep_temp))
        return path[:self.K]

    def getManhattanDistance(self, loc1: int, loc2: int) -> int:
        loc1_x = loc1//self.env.cols
        loc1_y = loc1 % self.env.cols
        loc2_x = loc2//self.env.cols
        loc2_y = loc2 % self.env.cols
        return abs(loc1_x-loc2_x)+abs(loc1_y-loc2_y)

    def validateMove(self, loc: int, loc2: int, timestep :int) -> bool:
        loc_x = loc//self.env.cols
        loc_y = loc % self.env.cols

        if(loc_x >= self.env.rows or loc_y >= self.env.cols or self.env.map[loc] == 1):
            return False
        if((loc, timestep) in self.reservations): #check if the loc is occupied by another robot
            return False
        loc2_x = loc2//self.env.cols
        loc2_y = loc2 % self.env.cols
        if(abs(loc_x-loc2_x)+abs(loc_y-loc2_y) > 1):
            return False
        return True

    def getNeighbors(self, location: int, direction: int, timestep: int):
        neighbors = []
        # forward
        candidates = [location+1, location+self.env.cols,
                      location-1, location-self.env.cols]
        forward = candidates[direction]
        new_direction = direction
        if (forward >= 0 and forward < len(self.env.map) and self.validateMove(forward, location, timestep)):
            neighbors.append((forward, new_direction))
        # turn left
        new_direction = direction-1
        if (new_direction == -1):
            new_direction = 3
        neighbors.append((location, new_direction))
        # turn right
        new_direction = direction+1
        if (new_direction == 4):
            new_direction = 0
        neighbors.append((location, new_direction))
        # print("debug!!!!!!!", neighbors)
        return neighbors

    def space_time_plan(self,start: int, start_direct: int, end: int, reservation: Set[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
        print(start, start_direct, end)
        path = []
        open_list = PriorityQueue()
        all_nodes = {}  # loc+dict, t
        parent={}
        s = (start, start_direct, 0, self.getManhattanDistance(start, end))
        open_list.put((s[3], id(s), s))
        # all_nodes[(start * 4 + start_direct, 0)] = s
        parent[(start * 4 + start_direct, 0)]=None

        while not open_list.empty():
            n=open_list.get()
            # print("n=",n)
            _, _, curr = n
        
            curr_location, curr_direction, curr_g, _ = curr

            if (curr_location*4+curr_direction,curr_g) in all_nodes:
                continue
            all_nodes[(curr_location*4+curr_direction,curr_g)]=curr
            if curr_location == end:
                while True:
                    path.append((curr[0], curr[1]))
                    curr=parent[(curr[0]*4+curr[1],curr[2])]
                    if curr is None:
                        break
                    # curr = curr[5]
                path.pop()
                path.reverse()
                break
            
            neighbors = self.getNeighbors(curr_location, curr_direction)

            for neighbor in neighbors:
                neighbor_location, neighbor_direction = neighbor

                if (neighbor_location, -1, curr[2] + 1) in reservation:
                    continue

                if (neighbor_location, curr_location, curr[2] + 1) in reservation:
                    continue

                neighbor_key = (neighbor_location * 4 +
                                neighbor_direction, curr[2] + 1)

                if neighbor_key in all_nodes:
                    old = all_nodes[neighbor_key]
                    if curr_g + 1 < old[2]:
                        old = (old[0], old[1], curr_g + 1, old[3], old[4])
                else:
                    next_node = (neighbor_location, neighbor_direction, curr_g + 1,
                                self.getManhattanDistance(neighbor_location, end))
        
                    open_list.put(
                        (next_node[3] + next_node[2], id(next_node), next_node))
                
                    parent[(neighbor_location * 4 +
                            neighbor_direction, next_node[2])]=curr

        for v in path:
            print(f"({v[0]},{v[1]}), ", end="")
        print()
        return path

    def sample_priority_planner(self,time_limit:int):
        actions = [MAPF.Action.W] * len(self.env.curr_states)
        reservation = set()  # loc1, loc2, t

        for i in range(self.env.num_of_agents):
            print("start plan for agent", i)
            path = []
            if not self.env.goal_locations[i]:
                print(", which does not have any goal left.")
                path.append((self.env.curr_states[i].location, self.env.curr_states[i].orientation))
                reservation.add((self.env.curr_states[i].location, -1, 1))

        for i in range(self.env.num_of_agents):
            print("start plan for agent", i)
            path = []
            if self.env.goal_locations[i]:
                print("with start and goal:")
                path = self.space_time_plan(
                    self.env.curr_states[i].location,
                    self.env.curr_states[i].orientation,
                    self.env.goal_locations[i][0][0],
                    reservation
                )
            
            if path:
                print("current location:", path[0][0], "current direction:", path[0][1])
                if path[0][0] != self.env.curr_states[i].location:
                    actions[i] = MAPF.Action.FW
                elif path[0][1] != self.env.curr_states[i].orientation:
                    incr = path[0][1] - self.env.curr_states[i].orientation
                    if incr == 1 or incr == -3:
                        actions[i] = MAPF.Action.CR
                    elif incr == -1 or incr == 3:
                        actions[i] = MAPF.Action.CCR

                last_loc = -1
                t = 1
                for p in path:
                    reservation.add((p[0], -1, t))
                    if last_loc != -1:
                        reservation.add((last_loc, p[0], t))
                    last_loc = p[0]
                    t += 1

        return actions




if __name__ == "__main__":
    test_planner = pyMAPFPlanner()
    test_planner.initialize(100)
