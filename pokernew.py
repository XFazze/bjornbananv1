import random, copy, math
deck = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'a12', 'a13', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13']



'''
setup game
game loop:
1. small and big deal
2. show/deal cards
3. first betting round
4. pop
5. second betting
6. 4th card
6. third betting
7. final card
8. last and forth betting
9. reward and reset
'''

# player class
class player:
    def __init__(self, name):
        self.name = name
        self.money = 500
        self.cards = []
        self.bet = 0


class bot:
    def __init__(self, name):
        self.name = name
        self.money = 500
        self.cards = []
        self.bet = 0


def number_of_players():
    question = "how many players?(there will be a total of 8 participants this asks how many real players)"
    amount = None
    while amount is None:
        try:
            amount = int(input(question))
        except:
            pass
    return amount

bot_names = ["XQC", "Glen", "peppapig", "Wille", "Emelie från stockholm", "poggers", "monkaS", "nip"]
bots = []
players = []
def create_bots_players(player_amount):
    number_of_bots = 8-player_amount
    for i in range(number_of_bots):
        bots.append(bot(bot_names[i]))
    
    for i in range(player_amount):
        players.append(player(input("Whats ur callsign?")))

    return bots, players

def place_players(bot_player, player_amount):
    seats = bots
    places = [0,1,2,3,4,5,6,7]
    player_seats = []
    for i in range(player_amount):
        r = 8
        while r not in places:
            r = random.randint(0,len(places))
        seats.insert(places[r], bot_player[1][i])
        places.remove(r)
        player_seats.append(r)

    return seats, player_seats
 
def deal(seats):
    tempdeck = copy.deepcopy(deck)
    for i in seats:
        for _ in range(2):
            card = tempdeck[random.randint(0, len(tempdeck)-1)]
            tempdeck.remove(card)
            i.cards.append(card)
    return seats, tempdeck  

def betting(seats, pot):
    for i in seats:
        if type(i) == bot:
            x = random.randint(0, i.money)
            amount = math.floor(x/2)
            i.money -= amount
            i.bet += amount
            print(i.name, "bets", amount)
        else:
            question = "You have "+str(i.money)+ " how much do you want to bet?"
            amount = None
            while amount is None:
                try:
                    amount = math.floor(int(input(question)))
                except:
                    pass
            
            i.money -= amount
            i.bet += amount


    for i in seats:
        pot += i.bet
    print("This are the bets this round\n the total pot is:", pot)

def flop(tempdeck):
    open_cards = []
    for _ in range(3):
        x = random.randint(0, len(tempdeck)-1)
        open_cards.append(tempdeck[x])
        tempdeck.remove(tempdeck[x])
    print("\n\nThe flop is ", open_cards)
    return open_cards, tempdeck

def fourth_card(tempdeck, open_cards):
    x = random.randint(0, len(tempdeck)-1)
    open_cards.append(tempdeck[x])
    tempdeck.remove(tempdeck[x])
    return open_cards, tempdeck


def round(seats, player_seats):
    pot = 0
    seats[0].money -= 10
    seats[1].money -= 20
    for i in seats:
        i.cards = []
    x = deal(seats)
    seats = x[0]
    tempdeck = x[1]
    print("\n\n")
    print(seats[0].name, "is small blind") 
    print(seats[1].name, "is big blind")
    
# Setup complete

    betting(seats, pot)
    x = flop(tempdeck)
    open_cards = x[0]
    tempdeck = x[1]
    betting(seats, pot)
    x = fourth_card(tempdeck, open_cards)
    open_cards = x[0]
    tempdeck = x[1]
    betting(seats, pot)
    return seats

def one_lap(seats, player_seats):
    for i in range(8):
        newseats = [0,0,0,0,0,0,0,0]
        newseats[0]=seats[1]
        newseats[1]=seats[2]
        newseats[2]=seats[3]
        newseats[3]=seats[4]
        newseats[4]=seats[5]
        newseats[5]=seats[6]
        newseats[6]=seats[7]
        newseats[7]=seats[0]
        seats = copy.deepcopy(newseats)

        seats = round(seats, player_seats)
        print("\n\nmoney situation now is:")
        for p in seats:
            print(p.name, "got", p.money)
    return seats
    

def play():
    player_amount = number_of_players()
    print("Starting a poker game with {} real players".format(player_amount))
    print("Everybody starts with 200 \nSmall and big are 10 and 20\n\n")
    seats, player_seats = place_players(create_bots_players(player_amount),player_amount)
# Done with seats and player setup
    one_lap(seats, player_seats)





play()    
