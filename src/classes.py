import numpy as np
from bots import Bot


class Player:

    def __init__(self, name):
        self.score = 0
        self.name = name

    def change_name(self, new_name):
        self.name = new_name
# The rules of this gameplay comes from the following website: https://www.scribd.com/document/92355008/Peraturan-Permainan-Tradisional-Congkak
class Congkak:

    def __init__(self, timer):
        self.timer = timer
        self.players = np.array([None] * 2)
        self.is_bot = np.array([False] * 2)
        self.houses = np.array([[7] * 7] * 2)
        self.storehouses = np.array([0, 0])

    # Set up function
    def add_player(self, player):
        if self.players[0] is None:
            self.players[0] = player
            self.is_bot[0] = isinstance(player, Bot)
        elif self.players[1] is None:
            self.players[1] = player
            self.is_bot[1] = isinstance(player, Bot)
        else:
            return "This Board is currently full, please find another game!"
        

    def remove_player(self, player: Player):
        """

        :param player:  The player object
        :return: A string indicating the player name has been removed
        """
        if self.players[0] == player:
            self.players[0] = None
            return f"Player {player.name} has been removed"
        elif self.players[1] == player:
            self.players[1] = None
            return f"Player {player.name} has been removed"
        else:
            return "This player is currently not in this board"

    def reset_game(self):
        self.storehouses = np.array([0] * 2)
        self.houses = np.array([[7] * 7] * 2)

    def clear_board(self):
        self.players = np.array([None] * 2)
        self.reset_game()

    def visualise_board(self):
        print(self.houses)
        print(self.storehouses)

    def get_board(self):
        """
        Return the current state of the board
        :return: A numpy array of shape (2,7) representing the current state of the board
        """
        return self.houses






    # Gameplay function
    def turn_ended(self, player_site, ending_site, house):
        # The player turns ended if it landed on an empty shell
        if house == 7:
            self.visualise_board()
            return False
        else:
            if self.houses[ending_site][house] == 1:
                if ending_site == player_site:
                    self.storehouses[player_site] += self.houses[1 - player_site][house]
                    self.houses[1 - player_site][house] = 0
                    self.houses[player_site][house] = 0
                self.visualise_board()
                return True
            else:
                self.visualise_board()
                return False

    def distribute_marble(self,player_turn, site, house):
        """
        :param site: The site which the player pick up the marble from. (0 or 1)
        :param house: The index of the house ranging from 0 - 6 where the n value indicates the (n + 1)th house from the right
        :return: A tuple of values indicating where the last marble is being placed with the first value being the site while the second value indicate the indices of the site (0 - 6 are the houses index while 7 means it landed last on the storehouse of that site)
        """
        marble_count = self.houses[site][house]
        self.houses[site][house] = 0
        first_iteration_ending_house = min(house + marble_count, 6)

        # Distribute the marble to the first iteration where the marble count could be less than the amount of remanining house on the player site
        for i in range(house + 1, first_iteration_ending_house + 1):
            self.houses[site][i] += 1

        marble_count -= first_iteration_ending_house - house
        # The index of the house where the last marble is being placed
        ending_house = first_iteration_ending_house

        if site == player_turn and marble_count >= 1:
            self.storehouses[player_turn] += 1
            marble_count -= 1
            ending_house = 7

        while marble_count > 0:
            site = 1 - site

            # ending_house is The number of marble to be distributed to the corresponding site
            ending_house = min(marble_count - 1, 6)
            for i in range(ending_house + 1):
                self.houses[site][i] += 1

            marble_count -= ending_house + 1

            # For if the marble just nice ended in the storehouse 
            # The player will only be able to place marble inside their storehouse but not their opponent
            if site == player_turn and marble_count > 0:
                self.storehouses[player_turn] += 1
                marble_count -= 1
                ending_house = 7
                    
        return site, ending_house
        
    def request_human_action(self, player_turn): 
        if None in self.players:
            print("There isn't sufficient player, please add more player to the game")
        else:
            player_name = self.players[player_turn]
        answer = int(input(f"{player_name}, please choose which house to take your marble from\n")) - 1

        # The condition imposed to validate the input
        if answer < 0 or answer > 6:
            print("Please enter a number between 1 and 7")
            return self.request_human_action(player_turn)

        if self.houses[player_turn][answer] == 0:
            print("Please choose a house with at least a marble")
            return self.request_action(player_turn)
        
        return answer
    
    def request_agent_action(self, agent_site):
        """
        Request an action from the agent for the given site.
        
        :param agent: The agent that will make the action decision.
        :param agent_site: The site (0 or 1) where the agent is playing.
        :return: The house index (0 to 6) chosen by the agent to pick up marbles.
        :raises AssertionError: If the agent chooses an out-of-range number or an empty house.
        """
        state = self.get_board()
        answer = self.players[agent_site].make_action(state, agent_site)
        # The condition imposed to validate the input
        if answer < 0 or answer > 6:
            raise AssertionError("Agent chose a number out of range")

        if self.houses[agent_site][answer] == 0:
            raise AssertionError("Agent chose an empty house")
        
        return answer
    
    def request_action(self, player_turn):
        if self.is_bot[player_turn]: 
            return self.request_agent_action(player_turn)
        else:
            return self.request_human_action(player_turn)



    def play_game(self, player_turn):
        # The storehouse is always on the left to the player when they are sitting in front of the board
        # The gameplay is going on a clockwise direction
        """

        :param player_turn: 0 or 1 indicating which player is going to start first
        :return: Winner of the game (0 / 1)
        """

        if None in self.players:
            print("There isn't sufficient player, please add more player to the game")
        else:
            while not self.game_ended(player_turn):
                try:
                    ending_site = player_turn
                    starting_house = self.request_action(player_turn)

                    # Always distribute in the first run, additional statement to avoid directly taking opponents marble if the player starts with the house that have only 1 marble (Algorithm due to how turn_ended has implemented)
                    ending_site, starting_house = self.distribute_marble(player_turn,ending_site, starting_house)
                    print(ending_site, starting_house)

                    while not self.turn_ended(player_turn, ending_site, starting_house):
                        if starting_house == 7:
                            starting_house = self.request_action(player_turn)
                        ending_site, starting_house = self.distribute_marble(player_turn, ending_site, starting_house)
                    

                except ValueError:
                    print("Invalid Input! Please enter a valid integer")

                player_turn = 1 - player_turn

    def tally_score(self):
        if None in self.players:
            print("There isn't sufficient player, please add more player to the game")
        else:
            self.players[0].score += self.storehouses[0]
            self.players[1].score += self.storehouses[1]


    def game_ended(self, player_turn):
        if sum(self.houses[player_turn]) == 0:
            self.storehouses[1 - player_turn] += sum(self.houses[1 - player_turn])
            self.tally_score()
            self.reset_game()
            return True
        else:
            return False







if False:
    JY = Player("Jun Yuan")
    cd =  Player("CD")
    congkak = Congkak(5)
    congkak.add_player(JY)
    congkak.add_player(cd)
    congkak.play_game(0)




