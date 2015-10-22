import requests
import time
from player import Player

# DEALER_URL = 'http://ec2-52-25-237-207.us-west-2.compute.amazonaws.com'
DEALER_URL = 'http://localhost:5000'
myPlayer = Player()
playerId = ''
gameId = ''

def main():
    global playerId, gameId
    registerResp = requests.post(DEALER_URL + '/player?name={}'.format(myPlayer.name))
    respJson = registerResp.json()
    playerId = respJson['playerId']
    gameId = respJson['game']['id']

    # wait for game to start
    # while not requests.get(DEALER_URL + '/game/{}'.format(gameId)).json()['active']:
    #     time.sleep(1)
    requests.get(DEALER_URL + '/start')
    wait_for_turn()
    while requests.get(DEALER_URL + '/game/{}'.format(gameId)).json()['active']:
        myPlayer.hand_count = 0
        myPlayer.hand_total = 0
        myPlayer.soft = False

        wait_for_turn()

        gameInfo = requests.get(DEALER_URL + '/game/{}'.format(gameId))
        revealedCards = gameInfo.json()['revealedCards']
        myPlayer.count = 0
        for card in revealedCards:
            myPlayer.view_card(card)

        playerInfoResp = requests.get(DEALER_URL + '/player/{}'.format(playerId))
        playerInfo = playerInfoResp.json()
        myPlayer.chips = playerInfo['chips']
        wager = myPlayer.get_wager()
        requests.get(DEALER_URL + '/setWager?playerId={}&wager={}'.format(playerId, wager))

        wait_for_turn()

        playerInfoResp = requests.get(DEALER_URL + '/player/{}'.format(playerId))
        playerInfo = playerInfoResp.json()
        gameInfo = requests.get(DEALER_URL + '/game/{}'.format(gameId))
        upCard = gameInfo.json()['dealerUpCard']['value']
        print playerInfo
        myPlayer.add_card(playerInfo['hand']['cards'][0])
        myPlayer.add_card(playerInfo['hand']['cards'][1])
        print 'player hand: {} / {}  , dealer up card: {}'.format(myPlayer.hand_total, myPlayer.soft, upCard)
        if myPlayer.double_down(upCard):
            print 'double'
            resp = requests.get(DEALER_URL + '/doubleDown?playerId={}'.format(playerId))
            card = resp.json()
            myPlayer.add_card(card)
            continue

        while myPlayer.hit(upCard) and myPlayer.hand_total <= 21:
            wait_for_turn()
            print 'hit'
            resp = requests.get(DEALER_URL + '/hit?playerId={}'.format(playerId))
            card = resp.json()
            print 'got {}'.format(card['value'])
            myPlayer.add_card(card)

        if myPlayer.hand_total <= 21:
            wait_for_turn()
            print 'stand'
            requests.get(DEALER_URL + '/stand?playerId={}'.format(playerId))



def wait_for_turn():
    resp = None
    respJson = None
    try:
        resp = requests.get(DEALER_URL + '/myTurn?playerId={}'.format(playerId))
        respJson = resp.json()
        while not respJson['myTurn']:
            time.sleep(.1)
            resp = requests.get(DEALER_URL + '/myTurn?playerId={}'.format(playerId))
            respJson = resp.json()
    except Exception as e:
        print e
        print resp
        print respJson





if __name__ == '__main__':
    main()