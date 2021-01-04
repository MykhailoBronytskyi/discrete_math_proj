'''
Знаходження найкоротшого шляху,
за допомогою алгоритму Левіта у двовимірному масиві.

Функція levits_algortihm відповідає
безпосередньо за пошук і повернення шляху.
##########################################
На вхід приймає 'двовимірний' список по типу
[[2,3,4,5...eln1], [3,4,5,6...eln2], [4,5,6,7....eln3]......]

Точки A і B між якими потрібно знайти шлях як 'тапли'
(x1, y1), (x2, y2) (кординати у межах сітки(заданого списку-ландшафту))

і змінну step як число.

На виході видає список індексів для ландшафту.
'''
#Importing very necessary libraries.
import time
from math import sqrt
import numpy as np

#Defining main function.
def levits_algortihm(landscape: list, pointa: tuple,
                     pointb: tuple, step: int = 1):
    '''
    Returns a minimum distance between point A and B
using adaptated Levit's algorithm.
    '''

    def find_ribs(point, size):
        '''
        Returns a list
of the ends of the ribs formed
with point as a start

        >>> list(sorted(list(find_ribs((2,4), (10,10)))))
        [(1, 4), (2, 3), (2, 5), (3, 4)]
        >>> list(sorted(list(find_ribs((2,4), (2,5)))))
        [(1, 4), (2, 3), (3, 4)]
        '''

        #Finding sumizhni rebra of given point.
        ribs = set()
        index_x = point[0]
        index_y = point[1]

        #Finding rebra if the point is on the edge.
        if index_x == size[0] - 1:
            if index_y == 0:
                ribs.add((index_x - 1, index_y))
                ribs.add((index_x, index_y + 1))
            elif index_y == size[1] - 1:
                ribs.add((index_x - 1, index_y))
                ribs.add((index_x, index_y - 1))
            else:
                ribs.add((index_x - 1, index_y))
                ribs.add((index_x, index_y + 1))
                ribs.add((index_x, index_y - 1))
            return ribs

        if index_x == 0:
            if index_y == 0:
                ribs.add((index_x + 1, index_y))
                ribs.add((index_x, index_y + 1))
            elif index_y == size[1] - 1:
                ribs.add((index_x + 1, index_y))
                ribs.add((index_x, index_y - 1))
            else:
                ribs.add((index_x + 1, index_y))
                ribs.add((index_x, index_y + 1))
                ribs.add((index_x, index_y - 1))
            return ribs

        #Finding rebra if the point is inside the grid.
        if index_y == 0:
            ribs.add((index_x + 1, index_y))
            ribs.add((index_x - 1, index_y))
            ribs.add((index_x, index_y + 1))
        elif index_y == size[1] - 1:
            ribs.add((index_x + 1, index_y))
            ribs.add((index_x - 1, index_y))
            ribs.add((index_x, index_y - 1))
        else:
            ribs.add((index_x + 1, index_y))
            ribs.add((index_x - 1, index_y))
            ribs.add((index_x, index_y - 1))
            ribs.add((index_x, index_y + 1))
        return ribs

    def compute_distance(height1, height2, step):
        '''
        Returns a distance between points
using their heights and given step.

        >>> round(compute_distance(50, 60, 2))
        10
        >>> round(compute_distance(100, 200, 5))
        100
        '''

        #Finding distance between points using heights and step.
        distance = sqrt((height1 - height2)**2 + step**2)
        return distance

    def get_minimum(distance1, distance2, ancestors, element):
        '''
        Returns a minimum distance.

        >>> ancestors = [[(2,4), (2,5), (3,7), (4,5)]]
        >>> get_minimum(50, 60, ancestors, (2,2), (0,2))
        60
        >>> print(ancestors)
        [[(2, 4), (2, 5), (2, 2), (4, 5)]]
        >>> ancestors = [[(2,4), (2,5), (3,7), (4,5)]]
        >>> get_minimum(100, 60, ancestors, (2,2), (0,2))
        100
        >>> print(ancestors)
        [[(2, 4), (2, 5), (3, 7), (4, 5)]]
        '''

        #Compares data of distances and returns minimal existing.
        if distance1 is None:
            return distance2
        if distance1 < distance2:
            return distance1
        ancestors[end_cord0][end_cord1] = element
        return distance2

    #Getting size.
    size = landscape.shape

    #Creating empty list distances for storing
    #minimal distances from the given point to a point in the grid
    distances = [[None]*size[1]]*size[0]

    #Creating a list ancestors for storing
    #a point to cross to get to the point in the grid through the shortest path.
    ancestors = [[(index, jindex) for jindex in
                  range(size[1])] for index in range(size[0])]

    #Setting up distance to a starting point as zero.
    distances[pointa[0]][pointa[1]] = 0

    #Creating a list for storing inf about in what array point is included.
    points_ids = [[2 for jindex in
                  range(size[1])] for index in range(size[0])]
    points_ids[pointa[0]][pointa[1]] = 0

    #Creating a list-queue for storing points which are under evaluation.
    under_computation_distances = [pointa]

    #Setting a loop that runs until all distances have been evaluated and
    #the set with points that are being evaluated is empty.
    while len(under_computation_distances) != 0:

        #Getting a point to evaluate.
        #Adding it to the set of evaluated points.
        element = under_computation_distances.pop(0)
        #element = under_computation_distances[0]
        element_cord0 = element[0]
        element_cord1 = element[1]
        points_ids[element_cord0][element_cord1] = 0
        #Finding adjacent points.
        ribs_finishes = find_ribs(element, size)
        #Getting a height of the point.
        height1 = landscape[element_cord0][element_cord1]

        #Iterating through the list of adjacent points.
        for end in ribs_finishes:
            end_cord0 = end[0]
            end_cord1 = end[1]
            #Getting height of an adjacent point and
            #computing distance with the evaluated one.
            height2 = landscape[end_cord0][end_cord1]
            distance = compute_distance(height1, height2, step)

            #If the adjacent point hasn't been evaluated with
            #any other point, compare a stored distance to
            #the other point and the distance with the adjacent one
            #and storing the minimal.
            if points_ids[end_cord0][end_cord1] == 2:
                try:
                    new_distance = distances[element_cord0][element_cord1] + distance
                    distances[end_cord0][end_cord1] = get_minimum(distances[end_cord0]
                                                                           [end_cord1],
                                                                           new_distance,
                                                                           ancestors,
                                                                           element)
                except ValueError:
                    distances[end_cord0][end_cord1] = get_minimum(distances[end_cord0]
                                                                           [end_cord1],
                                                                           distance,
                                                                           ancestors,
                                                                           element)
                #Moving the adjacent point to the set of evaluated points.
                points_ids[end_cord0][end_cord1] = 1
                under_computation_distances.append(end)
                #Changing an ancestor for the adjacent point.
                ancestors[end_cord0][end_cord1] = element

            #If the adjacent point is been evaluated,
            #choose a minimum distance to it.
            elif points_ids[end_cord0][end_cord1] == 1:
                distances[end_cord0][end_cord1] = get_minimum(distances[end_cord0][end_cord1],
                                                distances[element_cord0][element_cord1]
                                                + distance, ancestors, element)


            #If the adjacent point has been previously
            #evaluated and the rib with the the other point
            #hasn't been evaluated yet, running next block.
            elif points_ids[end_cord0][end_cord1] == 0:
                #Getitng an old distance and computing a new one.
                old_distance = distances[end_cord0][end_cord1]
                new_distance = distances[element_cord0][element_cord1] \
                                                    + distance

                #If the adjacent point and an ancestor of the point we are
                #evaluating mathces, we can get a cycled path between the points.
                 #This condition prevents it.
                if new_distance < old_distance and ancestors[element_cord0][element_cord1] != end:
                    distances[end_cord0][end_cord1] = new_distance
                    ancestors[end_cord0][end_cord1] = element
                    points_ids[end_cord0][end_cord1] = 1
                    under_computation_distances.insert(0, end)

    #Computing a path
    path = np.array([pointb])
    to_go_point = ancestors[pointb[0]][pointb[1]]

    #Creating a last visited point for storing
    #a point from which to move back to the pointa
    #on the current iteration.

    last_visited = to_go_point
    path = np.insert(path, 0, [to_go_point],  axis = 0)
    while tuple(to_go_point) != pointa:
        #Finding a next point in the path.
        to_go_point = ancestors[last_visited[0]][last_visited[1]]
        path = np.insert(path, 0, [to_go_point],  axis = 0)
        #Changing the last visited point.
        last_visited = to_go_point

    #Returning the result value.
    return path

if __name__ == '__main__':
    landscape_input, pointA_input, pointB_input, step_input = input(), input(), input(), input()
    start = time.time()
    path_output = levits_algortihm(landscape_input, pointA_input, pointB_input, step_input)
    print('Path:')
    print()
    print(path_output)
    print()
    print(f'Runtime: {time.time() - start}')
    print()
    with open('results__.txt', 'w', encoding='utf-8') as results_file:
        for step_forward in path_output:
            results_file.write(str(step_forward))
