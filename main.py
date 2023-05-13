import copy
import heapdict
from collections import Counter


class DataClass:
    def __init__(self, data, path):
        self.data = data
        self.path = path


"""
A good heuristic for this problem is : If the fruit is not assigned in the designated column, we add +1 to the score
If the fruit is not in the right position according to the size goal we add +1 to the score
Since in best case scenario, one swap two fruits can come into the right column and the right size states,
the score is divided by 4 to make it admissible
This is a modified manhattan heuristic
"""


def heuristics(current_cost, state, columns, goal):
    score = 0
    for i in range(3):
        for j in range(len(state[0])):
            name, size = state[i][j].split("_")
            if columns[i] != name:
                score += 1
            if name == "apple":
                if int(size) != goal["apple"][j]:
                    score += 1
            elif name == "banana":
                if int(size) != goal["banana"][j]:
                    score += 1
            else:
                if int(size) != goal["orange"][j]:
                    score += 1
    return (score + current_cost) / 4


"""
To find the right order of the columns and minimize column wise swaps, from the initial data the most frequent fruit in 
a column is assigned that column
"""


def getColumnOrder(data):
    orderingData = []
    columnOrder = []
    for i in range(3):
        tempList = []
        for j in range(len(data[0])):
            tempList.append(data[i][j].split("_")[0])
        orderingData.append(tempList)
    for innerList in orderingData:
        # Count the frequency of each item in the sublist
        counts = Counter(innerList)

        # Find the item with the maximum frequency and its count
        max_item, max_count = max(counts.items(), key=lambda x: x[1])

        columnOrder.append(max_item)
    return columnOrder


"""
A standard A star algorithm
"""


def astar(data, goal):
    columns = getColumnOrder(data)
    visited_states = []
    unvisited_states = heapdict.heapdict()
    dataObject = DataClass(data, [])
    unvisited_states[(0, dataObject)] = 0
    # Perform A star until we reach goal state or there are no items in unvisited states
    while unvisited_states:
        # Fetch the top of the heap which is the value with the lowest score
        current_cost, current_state_object = unvisited_states.popitem()[0]
        current_state = current_state_object.data
        path = current_state_object.path
        path.append(current_state)
        visited_states.append(current_state)

        if checkGoal(current_state):
            return current_state, path, current_cost
        # get child nodes
        nextStates = get_next_states(current_state)
        for state in nextStates:

            if state not in visited_states:
                # get heuristics for the state
                heuristic = heuristics(current_cost, state, columns, goal)
                stateObject = DataClass(state, path)
                unvisited_states[(current_cost + 1, stateObject)] = heuristic

    # Return false if no goal is reached
    return False, False, False


def get_next_states(data):
    next_states = []
    # Horizontal swaps
    for i in range(3):
        for j1 in range(len(data[0])):
            for j2 in range(j1 + 1, len(data[0])):
                newData = copy.deepcopy(data)
                newData[i][j1], newData[i][j2] = newData[i][j2], newData[i][j1]
                next_states.append(newData)
    # Vertical swaps
    for i in range(3):
        for j1 in range(len(data[0])):
            for i2 in range(i + 1, 3):
                newData = copy.deepcopy(data)
                newData[i][j1], newData[i2][j1] = newData[i2][j1], newData[i][j1]
                next_states.append(newData)
    return next_states


def checkGoal(data):
    # To verify is goal is reached
    for i in range(3):
        name = data[i][0].split("_")[0]
        for j in range(len(data[0])):
            # if the fruits are not in the right column return false
            if data[i][j].split("_")[0] != name:
                return False
            # if the fruits are not in the right weight order return false
            if j < 9 and int(data[i][j].split("_")[1]) > int(data[i][j + 1].split("_")[1]):
                return False
    # return true if goal is reached
    return True


def main():
    # data = [["orange_1", "orange_5", "apple_3"],
    #         ["apple_4", "apple_5", "orange_7"],
    #         ["banana_2", "banana_10", "banana_18"]]

    data = [
        ["orange_1", "orange_2", "orange_3", "orange_4", "apple_5",
         "orange_6", "orange_7", "orange_8", "orange_9", "orange_10"],

        ["apple_1", "apple_2", "apple_3", "apple_4", "orange_5",
         "banana_6", "apple_7", "apple_8", "apple_9", "apple_10"],

        ["banana_1", "banana_2", "banana_3", "banana_4", "banana_5",
         "apple_6", "banana_7", "banana_8", "banana_9", "banana_10"]
    ]

    apple = []
    banana = []
    orange = []
    # Standard sort to reorder each fruit according to its size to have a goal sorted state for each fruit
    for i in range(3):
        for j in range(len(data[0])):
            # Each fruit is appended into a new list and the size of each fruit is stored
            name, size = data[i][j].split("_")
            if name == "apple":
                apple.append(int(size))
            elif name == "banana":
                banana.append(int(size))
            else:
                orange.append(int(size))
    # Goal provides the size wise ordering of the fruits for each fruit respectively
    goal = {"apple": sorted(apple), "banana": sorted(banana), "orange": sorted(orange)}
    finalState, path, cost = astar(data, goal)
    if path:
        print("Final ", finalState)
        print("Cost ", cost)
        print("Path Taken")
        for pathTaken in path:
            print(pathTaken)
    else:
        print("No Solution")


if __name__ == '__main__':
    main()
