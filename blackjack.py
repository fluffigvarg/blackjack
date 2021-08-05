# Enter name, number of decks to use
# Create deck
# Player places bet
# Dealer deals cards
# Dealer calculates hands of player and dealer
    # if bj, check players cards
        # if bj, push
        # else, dealer wins
    # if not, play normally
# player hits, double down, split, stand
# if cards get down to 25%, deck is shuffled

import random

class Cards():
    def __init__(self):
        self.deck = []
        self.suits = ['H', 'C', 'D', 'S']
        self.num_of_decks = None
    
    def create_deck(self):
        for i in range (2, 15):
            for suit in self.suits:
                card = f'{i}{suit}'
                self.deck.append(card)
        self.deck = self.deck * self.num_of_decks
    
    def get_decks(self):
        while True:
            try:
                self.num_of_decks = int(input('How many decks would you like to use? 1-8: '))
                if self.num_of_decks > 0 and self.num_of_decks < 9:
                    break
                else:
                    print('Invalid number, try again!')
                    continue
            except:
                print('Invalid number, try again!')
                continue
    
    def shuffle_decks(self):
        self.deck = []
        self.create_deck()

class Player():
    def __init__(self):
        self.name = ''
        self.money = 1000
        self.hand = []
        self.hand_value = 0
        self.bet = 0
    
    def get_name(self):
        self.name = input('What is your name? ')

    def place_bet(self):
        while True:
            try:
                self.bet = int(input(f'How much do you want to bet? You have {self.money}: '))
                if self.bet > 0 and self.bet <= self.money:
                    break
                else:
                    print('Invalid bet, try again!')
                    continue
            except:
                print('Invalid bet, try again!')


class Dealer():
    def __init__(self):
        self.name = 'Dealer'
        self.dealer_hand = []
        self.dealer_hand_value = 0
        self.card_value = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, '10': 10, '11': 10, '12': 10, '13': 10, '14': 1} 
        self.card_name = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
            '8': '8', '9': '9', '10': '10', '11': 'Jack', '12': 'Queen', '13': 'King', '14': 'Ace'}
        self.card_suit = {'H': 'Hearts', 'S': 'Spades', 'D': 'Diamonds', 'C': 'Clubs'}
        
    def initial_deal(self, deck, hand):
        for i in range(2):
            card = random.choice(deck)
            deck.remove(card)
            hand.append(card)
            
    def hit(self, deck, hand):
        card = random.choice(deck)
        deck.remove(card)
        hand.append(card)
        return card

    def calculate_hand(self, hand):
        hand_value = 0
        for card in hand:
            hand_value += self.card_value[card[:-1]]
        for card in hand:
            if card[:-1] == '14': # Conditions for Ace
                if (hand_value + 10) <= 21:
                    hand_value += 10
                else:
                    pass
        return hand_value

    def translate_hand(self, hand):
        name = ''
        suit = ''
        number_of_cards = len(hand)
        card_count = 0
        hand_translated = []
        for card in hand:
            name = self.card_name[card[:-1]]
            suit = self.card_suit[card[-1]]
            hand_translated.append(name + ' of ' + suit)
            card_count += 1
            if card_count < number_of_cards:
                hand_translated.append('and')
            else:
                pass
        return ' '.join(hand_translated)

    def check_bust(self, hand_value):
        if hand_value > 21:
            return True
        else:
            return False
    
    def check_blackjack(self, hand, hand_value):
        if hand_value == 21 and len(hand) == 2:
            return True
        else:
            return False
    
    def determine_winner(self, player_name, hand_value, dealer_name, dealer_hand_value):
        if hand_value == dealer_hand_value:
            return "Push"
        elif hand_value > dealer_hand_value:
            return player_name
        else:
            return dealer_name

def reset_game(player, dealer):
    global next_move, game_status, player_status, dealer_status, player_bust, dealer_bust, play_again, winner, current_card
    next_move = ''
    game_status = True
    player_status = True
    dealer_status = True
    player_bust = False
    dealer_bust = False
    winner = ''
    play_again = ''
    current_card = []
    player.hand = []
    player.hand_value = 0
    dealer.dealer_hand = []
    dealer.dealer_hand_value = 0


if __name__ == '__main__':
    c = Cards()
    p = Player()
    d = Dealer()

    print(f'Welcome to Blackjack! Standard rules apply, dealer stands on 17.')
    c.get_decks()
    p.get_name()
    c.create_deck()

    next_move = ''
    current_card = []
    game_status = True
    player_status = True
    dealer_status = True
    player_bust = False
    dealer_bust = False
    winner = ''
    play_again = ''

    # As long as the player wants to keep playing
    # Deal cards
    # Check for bj
        # if dealer has it, game ends
        # if player has it, game ends
    # Show two cards of player one of dealers
    # either hit or stand
        # if busts, game ends
    # dealer hits on 16 or less, stands on 17 or more
    # compare values, determine winner


    while game_status: # Main game loop
        print(f'You currently have {p.money} chips.')
        p.place_bet()
        d.initial_deal(c.deck, p.hand)
        d.initial_deal(c.deck, d.dealer_hand)
        p.hand_value = d.calculate_hand(p.hand)
        d.dealer_hand_value = d.calculate_hand(d.dealer_hand)
        print(f'{p.name} has {d.translate_hand(p.hand)} for {p.hand_value} and {d.name} has {d.translate_hand(d.dealer_hand)} for {d.dealer_hand_value}')
        # TODO: need to check for blackjack
        while player_status: # players moves
            next_move = input('What would you like to do? (h)it or (s)tand? ') # TODO: add split and doubledown
            if next_move == 'h':
                current_card.append(d.hit(c.deck, p.hand))
                print(f'{p.name} hits and gets a {d.translate_hand(current_card)}!')
                current_card.pop()
                p.hand_value = d.calculate_hand(p.hand)
                print(f'{p.name} has {d.translate_hand(p.hand)} for {p.hand_value} and {d.name} has {d.translate_hand(d.dealer_hand)} for {d.dealer_hand_value}')
                if d.check_bust(p.hand_value):
                    player_status = False
                    player_bust = True
                    dealer_status = False
                continue              
            elif next_move == 's':
                print(f'{p.name} stands!')
                player_status = False
            else:
                print('Invalid input, try again!')
                continue
        
        if player_bust:
            print(f'{p.name} busts! {d.name} wins!')
            p.money -= p.bet
            pass
        else:
            while dealer_status:
                if d.dealer_hand_value < 17:
                    current_card.append(d.hit(c.deck, d.dealer_hand))
                    print(f'{d.name} hits and gets a {d.translate_hand(current_card)}!')
                    current_card.pop()
                    d.dealer_hand_value = d.calculate_hand(d.dealer_hand)
                    print(f'{p.name} has {d.translate_hand(p.hand)} for {p.hand_value} and {d.name} has {d.translate_hand(d.dealer_hand)} for {d.dealer_hand_value}')
                    if d.check_bust(d.dealer_hand_value):
                        dealer_status = False
                        dealer_bust = True
                        print(f'{d.name} busts! {p.name} wins!')
                        p.money += p.bet
                else:
                    print(f'{d.name} stands!')
                    dealer_status = False

        if player_bust == False and dealer_bust == False:
            winner = d.determine_winner(p.name, p.hand_value, d.name, d.dealer_hand_value)
            if winner == p.name:
                print(f'{p.name} wins!')
                p.money += p.bet
            elif winner == d.name:
                print(f'{d.name} wins!')
                p.money -= p.bet
            else:
                print('It\'s a tie!')
            # payout for win

        while True:
            play_again = input('Would you like to play again? (y)es or (n)o? ')
            if play_again == 'y':
                reset_game(p, d)
                break
            elif play_again == 'n':
                print('Thanks for playing!')
                game_status = False
                break
            else:
                print('Invalid input, try again!')