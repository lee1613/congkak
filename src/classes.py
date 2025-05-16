import numpy as np


class Player:
    score = 0

    def __init__(self, name):
        self.name = name

    def change_name(self, new_name):
        self.name = new_name
# The rules of this gameplay comes from the following website: https://www.scribd.com/document/92355008/Peraturan-Permainan-Tradisional-Congkak
class Congkak:

    # Attributes set up
    player0 = None
    player1 = None
    houses = np.array([[7] * 7] * 2)
    storehouses = [0, 0]

    def __init__(self, timer):
        self.timer = timer

    # Set up function
    def add_player(self, player):
        if self.player0 is None:
            self.player0 = player
        elif self.player1 is None:
            self.player1 = player
        else:
            return "This Board is currently full, please find another game!"

    def remove_player(self, player: Player):
        """

        :param player:  The player object
        :return: A string indicating the player name has been removed
        """
        if self.player0 == player:
            self.player0 = None
            return f"Player {player.name} has been removed"
        elif self.player1 == player:
            self.player1 = None
            return f"Player {player.name} has been removed"
        else:
            return "This player is currently not in this board"

    def reset_game(self):
        self.storehouses = [0] * 2
        self.houses = [[7] * 7] * 2

    def clear_board(self):
        self.remove_player(self.player0)
        self.remove_player(self.player1)
        self.reset_game()






    # Gameplay function
    def turn_ended(self, player_site, ending_site, house):
        # The player turns ended if it landed on an empty shell
        if house == 7:
            return False
        else:
            if self.houses[ending_site][house] == 1:
                if ending_site == player_site:
                    self.storehouses[player_site] += self.houses[1 - player_site][house]
                    self.houses[1 - player_site][house] = 0
                return True
            else:
                return False

    def distribute_marble(self, starting_site, house):
        """
        :param starting_site: The site which the player pick up the marble from. (0 or 1)
        :param house: The index of the house ranging from 0 - 6 where the n value indicates the (n + 1)th house from the right
        :return: A tuple of values indicating where the last marble is being placed with the first value being the site while the second value indicate the indices of the site (0 - 6 are the houses index while 7 means it landed last on the storehouse of that site)
        """
        marble_count = self.houses[starting_site][house]
        self.houses[starting_site][house] = 0
        iter = 0
        if marble_count <= (6 - house):
            for i in range(house + 1, house + 1 + marble_count):
                self.houses[starting_site][i] += 1

            marble_count -= (6 - house)

            return starting_site, 6 - house
        else:
            # For if the marble just nice ended in the storehouse after the first iteration
            if marble_count == 1:
                self.storehouses[starting_site] += 1
                return starting_site, 7

            site = 1 - starting_site

            while marble_count > 0:

                # The number to be marble to be distributed to the corresponding site
                if marble_count > 7:
                    iter_marble = marble_count % 7
                else:
                    iter_marble = marble_count
                for i in range(iter_marble):
                    self.houses[site][i] += 1

                marble_count -= iter_marble

                # The player will only be able to place marble inside their storehouse but not their opponent
                if site == starting_site and marble_count > 0:
                    self.storehouses[site] += 1
                    marble_count -= 1

                site = 1 - site

            return site, iter_marble

    def start_game(self, player_turn):

        # The storehouse is always on the left to the player when they are sitting in front of the board
        # The gameplay is going on a clockwise direction
        """

        :param player_turn: 0 or 1 indicating which player is going to start first
        :return: Winner of the game (0 / 1)
        """

        if self.player0 is None or self.player1 is None:
            print("There isn't sufficient player, please add more player to the game")
        else:
            ending_site = player_turn
            while not self.game_ended(player_turn):
                try:
                    starting_house = int(input(f"Player{player_turn}, please choose which house to take your marble from")) - 1

                    # The condition imposed to validate the input
                    if starting_house < 0 or starting_house > 6:
                        print("Please enter a number between 1 and 7")
                        continue

                    if self.houses[player_turn][starting_house] == 0:
                        print("Please choose a house with at least a marble")
                        continue

                    # Always distribute in the first run, additional statement to avoid directly taking opponents marble if the player starts with the house that have only 1 marble (Algorithm due to how turn_ended has implemented)
                    ending_site, starting_house = self.distribute_marble(ending_site, starting_house)

                    while not self.turn_ended(player_turn, ending_site, starting_house):
                        ending_site, starting_house = self.distribute_marble(ending_site, starting_house)

                except ValueError:
                    print("Invalid Input! Please enter a valid integer")

                player_turn = 1 - player_turn

    def tally_score(self):
        self.player0.score += self.storehouses[0]
        self.player1.score += self.storehouses[1]


    def game_ended(self, player_turn):
        if sum(self.houses[player_turn]) == 0:
            self.storehouses[1 - player_turn] += sum(self.houses[1 - player_turn])
            self.tally_score()
            self.reset_game()
            return True
        else:
            return False












