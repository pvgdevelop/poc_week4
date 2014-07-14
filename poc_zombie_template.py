"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui
# import poc_simpletest
# import test


# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []


    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        location = (row, col)
        self._zombie_list.append(location)


    def remove_zombie(self, row, col):
        """
        Remove zombie from the zombie list
        """
        location = (row, col)
        self._zombie_list.remove(location)

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)


    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        location = (row, col)
        self._human_list.append(location)

    def remove_human(self, row, col):
        """
        Remove human from the human list
        """
        location = (row, col)
        self._human_list.remove(location)

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human


    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        height = self.get_grid_height()
        width = self.get_grid_width()

        # Create a new grid of the same size as the obstacle grid
        visited = poc_grid.Grid(height, width)
        visited.clear()

        # Create a 2D list of the same size as the grid and initialize its entries to be (heigth * width).
        max_distance = height * width
        distance_field = [[max_distance for dummy_col in range(width)]
                      for dummy_row in range(height)]

        # Create a queue that is a copy entity_type
        boundary = poc_queue.Queue()

        if entity_type == ZOMBIE:
            entity_type = self.zombies()
        elif entity_type == HUMAN:
            entity_type = self.humans()
        else:
            print "ERROR: Entity type is incorrect"
        for entity in entity_type:
            boundary.enqueue(entity)

        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0

        # Updates a 2D distance field computed using the four-way distance to entities of the given type
        while len(boundary) != 0:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0], cell[1])
            # #neighbors = self.eight_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]) and \
                        visited.is_empty(neighbor[0], neighbor[1]):
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
        return distance_field


    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        # queue = poc_queue.Queue()
        # [queue.enqueue(dummy_turn) for dummy_turn in self.num_humans()]
        temp_list = []
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0], human[1])
            neighbors.append(human) # Add human position to the list of neighbors

            # Get maximal distance from zombies
            max_distance = max(zombie_distance[dummy_row][dummy_col] for dummy_row, dummy_col in neighbors)
            max_distances = []

            for cell in neighbors:
                if zombie_distance[cell[0]][cell[1]] == max_distance:
                    max_distances.append(cell)

            distance_choice = random.choice(max_distances)
            temp_list.append(distance_choice)
        self._human_list = temp_list

    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        temp_list = []
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            neighbors.append(zombie) # Add zombie position to the list of neighbors

            # Get minimal distance to humans
            min_distance = min(human_distance[dummy_row][dummy_col] for dummy_row, dummy_col in neighbors)
            min_distances = []

            for cell in neighbors:
                if human_distance[cell[0]][cell[1]] == min_distance:
                    min_distances.append(cell)
            distance_choice = random.choice(min_distances)
            temp_list.append(distance_choice)
        self._zombie_list = temp_list


# Start up gui for simulation - You will need to write some code above
# before this will work without errors 123qweasd

# poc_zombie_gui.run_gui(Zombie(30, 40))

# test.phase1_test(Zombie)
# test.phase2_test(Zombie)
# test.phase3_test(Zombie)

