# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Shang-Tse Chen (stchen@csie.ntu.edu.tw) on 03/03/2022

"""
This is the main entry point for HW1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)


class Node:
    def __init__(self, position, forward_cost, backward_cost):
        self.position = position
        self.forward_cost = forward_cost
        self.backward_cost = backward_cost
        self.total_cost = forward_cost + backward_cost

class BinaryHeap:
    def __init__(self):
        self.heap_list = [Node((0, 0), 0, 0)]
        self.current_size = 0

    def insert(self, item):
        self.heap_list.append(item)
        self.current_size += 1
        self.perc_up(self.current_size)

    def perc_up(self, i):
        while i // 2 > 0:
            if self.heap_list[i].total_cost < self.heap_list[i // 2].total_cost:
                temp = self.heap_list[i // 2]
                self.heap_list[i // 2] = self.heap_list[i]
                self.heap_list[i] = temp
            i //= 2

    def del_min(self):
        ret_val = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size -= 1
        self.heap_list.pop()
        self.perc_down(1)
        return ret_val

    def perc_down(self, i):
        while (i * 2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i].total_cost > self.heap_list[mc].total_cost:
                temp = self.heap_list[i]
                self.heap_list[i] = self.heap_list[mc]
                self.heap_list[mc] = temp
            i = mc

    def min_child(self, i):
        if i * 2 + 1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i * 2].total_cost < self.heap_list[i * 2 + 1].total_cost:
                return i * 2
            else:
                return i * 2 + 1

def calc_manhattan(pos1, pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def calc_heuristic(problem, maze, position):
    if problem == "base":
        return calc_manhattan(position, maze.getObjectives()[0])

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    queue = []
    table = {} # saving the ancestor (descendant, ancestor)
    queue.append(maze.getStart()) # enqueue start node

    table[maze.getStart()] = maze.getStart()
    flag = 0
    while len(queue) != 0:
        curr = queue.pop(0)
        for _, i in enumerate(maze.getNeighbors(*curr)): # fringe expansion
            if(table.get(i) is not None):
                continue
            queue.append(i)
            table[i] = curr
            if maze.getObjectives()[0] == i: # goal test
                ans = []
                trace_back = maze.getObjectives()[0]
                ans.insert(0, trace_back)
                while trace_back is not maze.getStart():
                    trace_back = table[trace_back]
                    ans.insert(0, trace_back)

                return ans

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    fringe = BinaryHeap()
    table = {}
    fringe.insert(
        Node(
            maze.getStart(), 
            0, 
            calc_heuristic("base", maze, maze.getStart())
        )
    )
    table[maze.getStart()] = maze.getStart()
    # print(maze.getObjectives()[0])

    flag = 0
    while fringe.current_size != 0:
        curr = fringe.del_min()
        # print(f"{curr.position} {curr.forward_cost} {curr.backward_cost}")
        for _, i in enumerate(maze.getNeighbors(*curr.position)): # fringe expansion
            if(table.get(i) is not None):
                continue
            # a = calc_heuristic("base", maze, i)
            # print(f"{maze.getObjectives()[0]} {i} {a}")
            fringe.insert(
                Node(
                    i, 
                    curr.forward_cost+1, 
                    calc_heuristic("base", maze, i)
                )
            )
            table[i] = curr.position
            if maze.getObjectives()[0] == i: # goal test
                ans = []
                trace_back = maze.getObjectives()[0]
                ans.insert(0, trace_back)
                while trace_back is not maze.getStart():
                    trace_back = table[trace_back]
                    ans.insert(0, trace_back)

                return ans

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    return []

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
