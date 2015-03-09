from Tkinter import *
from player import Human, RandomPlayer, MinimaxPlayer
from connect4 import ConnectFour
from utility import SimpleUtility, WithColumnUtility
import itertools


class Connect4GUI(Frame):

    def __init__(self, parent):

        parent.title("Connect Four")

        self.parent = parent
        self.parent.geometry('600x600')

        # Frames for different elements of the game
        self.menu_frame = Frame(self.parent)
        self.menu_frame.grid(row=0, column=0)
        self.game_frame = Frame(self.parent)
        self.game_frame.grid(row=0, column=4)

        # Function to setup game, will eventually run the game
        self.setup()

    def setup(self):
        # User options for player types
        player_options = ('Human', 'Random', 'Minimax')

        # Selector for player 1 type
        self.p1_variable = StringVar()
        player1_label = Label(self.menu_frame, text="Player 1: ")
        player1_label.grid(row=1, column=0)
        player1_opts = OptionMenu(self.menu_frame, self.p1_variable, *player_options)
        player1_opts.grid(row=1, column=1)

        # Selector for player 2 type
        self.p2_variable = StringVar()
        player2_label = Label(self.menu_frame, text="Player 2: ")
        player2_label.grid(row=2, column=0)
        player2_opts = OptionMenu(self.menu_frame, self.p2_variable, *player_options)
        player2_opts.grid(row=2, column=1)

        # Button to check users choices
        check = Button(self.menu_frame, text="Continue", command=self.check_setup)
        check.grid(row=6, column=0)

    # This function makes sure choices are valid, and then calls another
    # function to check if minimax options need to be set.
    def check_setup(self):

        # Make sure both player options are not empty
        if self.p1_variable.get() == '' or self.p2_variable.get() == '':
            message = Label(self.menu_frame, text="Must have two players!")
            message.grid(row=0, column=2)

        # Make sure at least one of the players is of type 'Human'
        elif self.p1_variable.get() != 'Human' and self.p2_variable.get() != 'Human':
            message = Label(self.menu_frame, text="At least one player must be Human!")
            message.grid(row=0, column=2)

        # Everything is okay, clear the canvas and check if minimax values need
        # to be set.
        else:
            self.remove()
            self.minimax_options()

    # This function checks to see if one of the players is 'Minimax', if so
    # brings up options menu, otherwise goes to next step.
    def minimax_options(self):

        # Check if a player is 'Minimax'
        if self.p1_variable.get() == "Minimax" or self.p2_variable.get() == "Minimax":
            message = Label(self.menu_frame, text="Wait! We must set minimax variables.")
            message.grid(row=0, column=0)

            # Choose ply depth
            depth_label = Label(self.menu_frame, text="ply_depth")
            depth_label.grid(row=1, column=0)
            self.depth_num = Spinbox(self.menu_frame, from_=1, to=5)
            self.depth_num.grid(row=1, column=1)

            # Set three in a row utility value
            three_score_label = Label(self.menu_frame, text="three_score")
            three_score_label.grid(row=2, column=0)
            self.three_score = Spinbox(self.menu_frame, from_=3, to=9)
            self.three_score.grid(row=2, column=1)

            # Set two in a row utility value
            two_score_label = Label(self.menu_frame, text="two_score")
            two_score_label.grid(row=3, column=0)
            self.two_score = Spinbox(self.menu_frame, from_=1, to=5)
            self.two_score.grid(row=3, column=1)

            # Button that will call function to draw the game board
            start_game = Button(self.menu_frame, text="Begin Game", command=self.create_board)
            start_game.grid(row=4, column=0)

        else:
            # No Minimax player, move to board creation
            self.create_board()

    # This function will draw the game board
    def create_board(self):
        # Clear the grid
        self.remove()

        # Buttons to play in each column
        self.btn_list = []
        for i in range(7):
            btn = Button(self.game_frame, text="Column" + str(i))
            btn.bind("<Button>", self.play_turn)
            btn.grid(row=0, column=i)
            self.btn_list.append(btn)

        # Data structure to store the board.
        self.board = []
        for y in range(6):
            row = []
            for x in range(7):
                row.append(None)
            self.board.append(row)

            # Creates a new Canvas Widget at each board position.
        for y in range(6):
            for x in range(7):
                self.board[y][x] = Canvas(self.game_frame, width=80, height=80, bg='white')
                self.board[y][x].grid(row=y + 1, column=x)

        self.initialize()

    # Controls Moves for each player

    #sets game variables
    def initialize(self):
        # Set Player 1
        self.p1_string = self.p1_variable.get()
        self.p2_string = self.p2_variable.get()

        #determine if minimax variables are needed
        if self.p1_string != 'Human' or self.p2_string != 'Human':
            if self.p1_string != 'Random' and self.p2_string != 'Random':
                two_score = int(self.two_score.get())
                three_score = int(self.three_score.get())
                ply_depth = int(self.depth_num.get())
        
        #set player 1
        if self.p1_string == 'Minimax':
            self.player1 = MinimaxPlayer(playernum=1, ply_depth=ply_depth, utility=WithColumnUtility(three_score, two_score, [1,2,3,4,3,2,1]))
        elif self.p1_string == 'Random':
            self.player1 = RandomPlayer(playernum=1)
        else:
            self.player1 = Human(playernum=1)

        #set player 2
        if self.p2_string == 'Minimax':
            self.player2 = MinimaxPlayer(playernum=2, ply_depth=ply_depth, utility=WithColumnUtility(three_score, two_score, [1,2,3,4,3,2,1]))
        elif self.p2_string == 'Random':
            self.player2 = RandomPlayer(playernum=2)
        else:
            self.player2 = Human(playernum=2)


        #board for gui to match to
        self.logic_board = ConnectFour()

        self.new_pos = None
        self.prev_pos = None

        #stores visited positions for highlighting
        self.visited = {}
        for y in range(6):
            for x in range(7):
                self.visited[str(y)+str(x)] = False

        #some variables to let play_turn method know who's turn it is
        self.turn_num = StringVar()
        self.turn_display = Label(self.game_frame, textvariable=self.turn_num)
        self.turn_display.grid(row=8, column=3)
        self.turn_ctrl = itertools.cycle([1,2]).next
        self.playernum = self.turn_ctrl()
        self.turn_num.set("Player: " + str(self.playernum))

        #if first player is not human, play computer turn first since play turn is only called by clicking a column button
        if self.p1_variable.get() != 'Human':
            self.player1.play_turn(self.logic_board)
            self.match_board(self.logic_board, True)
            self.playernum = self.turn_ctrl()

    #controls players moves
    def play_turn(self, event):
        #gets column number of button pressed
        btn = event.widget
        col = int(btn.cget("text")[-1])

        if self.playernum == 1:
            #we only want to call the play turn method if the game is not over, between each turn we will check if the game is over or if the board is full and update the values
            if self.p1_string == 'Human' and self.is_game_over() == False:
                self.player1.play_turn(self.logic_board, col)
                self.match_board(self.logic_board, False)
                self.board_full()

                if self.p2_string != 'Human' and self.is_game_over() == False:
                    self.player2.play_turn(self.logic_board)
                    self.match_board(self.logic_board, True)
                    self.board_full()

                else:
                    self.playernum = self.turn_ctrl()
            else:
                if self.is_game_over() == False:
                    self.player1.play_turn(self.logic_board)
                    self.match_board(self.logic_board, True)
                    self.playernum = self.turn_ctrl()
                    self.board_full()

        elif self.playernum == 2:
            if self.p2_string == 'Human' and self.is_game_over() == False:
                self.player2.play_turn(self.logic_board, col)
                self.match_board(self.logic_board, False)
                self.board_full()

                if self.p1_string != 'Human' and self.is_game_over() == False:
                    self.player1.play_turn(self.logic_board)
                    self.match_board(self.logic_board, True)
                    self.board_full()

                else:
                    self.playernum = self.turn_ctrl()
            else:
                if self.is_game_over() == False:
                    self.player2.play_turn(self.logic_board)
                    self.match_board(self.logic_board, True)
                    self.playernum = self.turn_ctrl()
                    self.board_full()

        else:
            self.turn_num.set("Player " + str(self.playernum))

        self.game_over()

        return

    def board_full(self):
        if self.logic_board.is_board_full():
            self.turn_num.set("Board Full!")
            self.exit = Button(self.game_frame, text="Quit", command=self.exit)
            self.exit.grid(row=9, column=3)
        else:
            pass

    #function to check if game is over
    def is_game_over(self):
        if self.logic_board.is_game_over():
            return True
        else:
            return False

    #called if game is over
    def game_over(self):
        if self.logic_board.is_game_over():
            win = self.logic_board.is_game_over()
            
            for btn in self.btn_list:
                btn.unbind("<Button>", funcid = None)

            self.mark_winning_four(self.logic_board)

            #Display message to show winner
            self.turn_num.set("Winner" + str(self.playernum))
            #Create button to exit game
            self.exit = Button(self.game_frame, text="Quit", command=self.exit)
            self.exit.grid(row=9, column=3)

            return True
        else:
            pass
    
    #function to match gui to logic board 
    def match_board(self, board, bot):
        #iterate through each column and row
        for col in range(7):
            for row in range(6):
                if board.get_position(row, col) != None:
                    #conditions to match up the logic board to the gui board
                    if board.get_position(row, col) == 1:
                        self.board[5-row][col].create_oval(0,0,80,80,fill="black")
                    else:
                        self.board[5-row][col].create_oval(0,0,80,80,fill="red")

                    #Finds last move made by computer and highlights it
                    if self.p2_string != 'Human':
                        if bot and board.get_position(row, col) == 2:

                            #we must define previous position if it is not defined
                            if self.prev_pos == None:
                                self.new_pos = self.board[5-row][col]
                                self.new_pos.configure(bg="green")
                                self.prev_pos = self.new_pos
                                self.visited[str(5-row)+str(col)] = True

                            #set new and previous position with new properties
                            elif self.visited[str(5-row)+str(col)] == False:
                                self.prev_pos.configure(bg="white")
                                self.new_pos = self.board[5-row][col]
                                self.new_pos.configure(bg="green")
                                self.prev_pos = self.new_pos
                                self.visited[str(5-row)+str(col)] = True

                    if self.p1_string != 'Human':
                        if bot and board.get_position(row, col) == 1:

                            if self.prev_pos == None:
                                self.new_pos = self.board[5-row][col]
                                self.new_pos.configure(bg="green")
                                self.prev_pos = self.new_pos
                                self.visited[str(5-row)+str(col)] = True

                            elif self.visited[str(5-row)+str(col)] == False:
                                self.prev_pos.configure(bg="white")
                                self.new_pos = self.board[5-row][col]
                                self.new_pos.configure(bg="green")
                                self.prev_pos = self.new_pos
                                self.visited[str(5-row)+str(col)] = True
                    
    #this method is called in the game_over method, if the game is over, it will mark the winning four in a row
    def mark_winning_four(self, board):
        #these directions will be used for the match_in_direction function from connect4.py
        direction_dict = {'E': (0,1), 'W': (0,-1), 'N':(1,0), 'S':(-1,0), 'NE':(1,1), 'NW':(1,-1), 'SE':(-1,1), 'SW':(-1,-1)}
        
        #make an empty list to fill with winning positions
        positions_to_mark = []

        #iterate over board to determine where the winning four in a row is
        for row in range(6):
            for col in range(7):
                for direction in direction_dict:
                    rowdir = direction_dict[direction][0]
                    coldir = direction_dict[direction][1]
                    if board.match_in_direction(row, col, rowdir, coldir) >= 4:
                        for i in range(4):
                            positions_to_mark.append(self.board[5 - (row + i*rowdir)][col + i*coldir])

        #draw an 'x' through the winning four in a row
        for position in positions_to_mark:
            self.draw_x(position)

    # This function is used to clear off the Menu Frame between menu stages.
    def remove(self):
        self.menu_frame.grid_remove()
        self.menu_frame = Frame(self.parent)
        self.menu_frame.grid()

    def draw_x(self, position):
        position.create_line(0,0,80,80, fill="white")
        position.create_line(0,80,80,0, fill="white")

    #exit the game
    def exit(self):
        self.parent.quit()

parent = Tk()
Connect4GUI(parent)
parent.mainloop()
