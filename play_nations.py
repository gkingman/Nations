import requests
from bs4 import BeautifulSoup


game_id = '88285'
game_url = f"http://www.mabiweb.com/modules.php?name=GM_Nations&g_id={game_id}&op=view_game_reset"

def get_players(soup):
    '''
        This function parses the HTML to extract the current turn order and determines the current player to move
    '''
    header = str(soup).split("Players:")[1].split("<br/></div><hr/>")[0].split(" <img src=")[1:]
    current_player = None
    players = []
    for player in header:
        player = ''.join(player.split('>')[1:]).strip('\xa0\xa0')
        if '<' not in player: # Name is parsed correctly
            players.append(player)
        else: # It is this player's turn
            player = player[2:-3]
            players.append(player)
            current_player = player
    return players, current_player
    
def get_available_cards(soup):
    cards = str(soup).split('<div id="nations-game">')[1].split('<div id="nations-tracks')[0]
    cards = cards.split(' src=modules/GM_Nations/images/Progress_Cards/')[1:-1] # The first one is header, the last is war
    available = [[], [], [], []] # Index is the cost of the card. No cards go in zero index
    for card in cards:
        name = card.split('.')[0].replace('_', ' ')

        height = card.split('top: ')[1].split(';')[0]
        if height == '386':
            cost = 1
        elif height == '208':
            cost = 2
        elif height == '30':
            cost = 3
        available[cost].append(name)
    return available

def get_board(url):
    response=requests.post(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    
    # First scrape the board to get key pieces of information
    turn_order, to_move = get_players(soup)
    available = get_available_cards(soup)

    ### TO DO

    # Get war strength (if any)
    # Get passed players
    # Get turmoil remaining
    # Get architects remaining
    # Get individual player tableaus
    # Get individual player resources
    
    #print(soup) ### Use this command to reveal the raw HTML to get ideas on how to scrape the next target



get_board(game_url)