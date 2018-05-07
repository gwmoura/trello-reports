import os

from datetime import datetime
from trello import TrelloApi, Boards, Cards

from settings import BOARD_ID, TRELLO_APP_KEY, TRELLO_APP_TOKEN

def get_lead_time(actions):
    lead_time = None
    d1 = get_first_action(actions)
    d2 = get_last_action(actions)
    if(d1 is not None and d2 is not None):
        lead_time = d2 - d1

    return lead_time

def get_action_by_pos(actions, pos):
    if len(actions) > 0:
        date = datetime.strptime(actions[pos]['date'][0:10], "%Y-%m-%d")
        return date

def get_first_action(actions):
    return get_action_by_pos(actions, -1)

def get_last_action(actions):
    return get_action_by_pos(actions, 0)

def get_actions(card_id):
    card = Cards(TRELLO_APP_KEY, TRELLO_APP_TOKEN)
    actions =  card.get_action(card_id)
    update_actions = []
    get_lead_time(actions)
    for action in actions:
        if action['type'] != 'commentCard':
            update_actions.append(action)
            list_before = action['data']['listBefore']['name']
            list_after = action['data']['listAfter']['name']
    return update_actions

def get_members(card_id):
    card = Cards(TRELLO_APP_KEY, TRELLO_APP_TOKEN)
    members = card.get_member(card_id)
    return members

def get_cards(borad_id):
    board = Boards(TRELLO_APP_KEY, TRELLO_APP_TOKEN)
    cards = board.get_card(borad_id, filter={'closed'})
    return cards

def get_cards_as_csv(board_id):
    cards = get_cards(board_id)
    for card in cards:
        actions = get_actions(card['id'])
        lead_time = get_lead_time(actions)
        start = get_first_action(actions)
        end = get_last_action(actions)
        members = get_members(card['id'])
        qtd_members = len(members)
        members_names = ''
        for member in members:
            members_names += member['fullName'] + " "

        if lead_time is None:
            lead_time = 0
        else:
            lead_time = lead_time.days

        card_name = card['name'].replace(";", "").replace("	", " ").replace("\t", " ").replace("\n", " ")
        lead_time = str(lead_time)

        if start is None or end is None:
            last_activity = datetime.strptime(card['dateLastActivity'][0:10], "%Y-%m-%d")
            start_date = last_activity.strftime('%d/%m/%Y')
            end_date = last_activity.strftime('%d/%m/%Y')
        else:
            start_date = start.strftime('%d/%m/%Y')
            end_date = end.strftime('%d/%m/%Y')

        print "%s (%s);%s;%s;%s;%s;%s" % (card_name, card['id'], members_names, qtd_members, start_date, end_date, lead_time)

board_id = BOARD_ID
cards = get_cards(board_id)
print "Card;Membros;Qtd Membros;Data Inicio;Data Entrega;Lead Time"
get_cards_as_csv(board_id)
