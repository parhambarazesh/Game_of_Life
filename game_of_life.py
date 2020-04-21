class Game_of_life():
    def __init__(self, rows, columns,data):
        self.row=rows
        self.column=columns
        self.number_of_generation=0
        self.data=data
        self.generate()
        
    def draw(self):
        """
        Draws the result cells
        -------
        None.

        """
        for i in range(0,self.row):
            for j in range(0,self.column):
                print(self.grid[i][j].get_status(),end=' ')
            print()

    def generate(self):
        """
        Generate the grids initialized with the data included in the ods file.
        -------
        None.

        """
        self.grid = [['0' for x in range(self.column)] for y in range(self.row)]
        
        for i in range(0, self.row):
            for j in range(0, self.column):
                if self.data.iloc[i][j]==0:
                    """
                    here we define an instance of Celle class and assign it to each element in self.grid matrix
                    """
                    cell_element=Cell()
                    cell_element.set_dead()
                    self.grid[i][j] = cell_element
                else:
                    cell_element = Cell()
                    cell_element.set_live()
                    self.grid[i][j] = cell_element
        
    def update(self):
        """
        Updates the generation based on the Conway's GOL rules.
        -------
        TYPE
            generation number

        """
        self.number_of_generation=self.number_of_generation+1

        alive_cells_to_die=[]
        dead_cells_to_alive=[]

        for i in range(0,self.row):
            for j in range(0,self.column):
                [number_of_live_neighbors,number_of_neighbors,list_of_neighbors]=self.find_neighbour(i,j)

                if self.grid[i][j].is_live()==True:
                    if number_of_live_neighbors<2 or number_of_live_neighbors>3:
                        
                        alive_cells_to_die.append(self.grid[i][j])
                else:
                    if number_of_live_neighbors==3:
                        dead_cells_to_alive.append(self.grid[i][j])

        for i in range(len(alive_cells_to_die)):
            alive_cells_to_die[i].set_dead()
        for i in range(len(dead_cells_to_alive)):
            dead_cells_to_alive[i].set_live()

        return self.number_of_generation


    def find_living_number(self):
        """
        get the total number of live cells in the whole grid
        -------
        number_of_alive_cells : TYPE
            Total number of live cells.

        """
        number_of_alive_cells=0
        for i in range(0,self.row):
            for j in range(0,self.column):
                if self.grid[i][j].is_live()==True:
                    number_of_alive_cells=number_of_alive_cells+1
        return number_of_alive_cells


    def find_neighbour(self, x, y):
        """
        Parameters
        ----------
        x : int
            index of row
        y : int
            index of column

        Returns
        -------
        number_of_live_neighbors : int
            returns number of live neighbor cells.
        number_of_neighbors : int
            returns number of neighbor cells.
        list_of_neighbors : list of list
            list of neighbor cells.

        """
        number_of_neighbors=0
        number_of_live_neighbors=0
        list_of_neighbors=[]
        for i in [x-1,x,x+1]:
            for j in [y-1,y,y+1]:
                if i==x and j==y:
                    continue
                elif 0<=i<self.row and 0<=j<self.column:
                    if self.grid[i][j].is_live()==True:
                        number_of_live_neighbors=number_of_live_neighbors+1
                    number_of_neighbors=number_of_neighbors+1
                    list_of_neighbors.append([i,j])

        return number_of_live_neighbors,number_of_neighbors,list_of_neighbors

class Cell:
    def __init__(self):
        self.cell=0
    def set_dead(self):
        self.cell=0
    def set_live(self):
        self.cell=1
    def is_live(self):
        if self.cell==1:
            return True
        else:
            return False
    def get_status(self):
        if self.cell==1:
            return 'o'
        else:
            return '.'

from pandas_ods_reader import read_ods
import os
import time
path = "data.ods"
df = read_ods(path, 1, headers=False)
number_of_rows=df.shape[0]
number_of_columns=df.shape[1]
GOL_instance = Game_of_life(number_of_rows,number_of_columns,df)
for i in range(30):
    GOL_instance.draw()
    number_of_generation=GOL_instance.update()
    
    time.sleep(0.5)
    os.system('clear')