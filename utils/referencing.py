import discord, datetime, ast
from utils import database
import random


#################AFK & PROFILE HANDLING##################

def fetch_handler(user: discord.Member):
    '''fetches the required data for the MySQL server.
    '''
    data = database.profile_fetch_user(user)
    if data is None:
        database.profile_insert_user(user=user, date=datetime.datetime.now())
        return database.profile_fetch_user(user)
    else:
        return data

def update_handler(user: discord.Member, var1, var2):
    '''fetches the user and then updates the load.
    '''
    fetch_handler(user)
    database.profile_update_user(user, var1, var2)
    return

#################POLL HANDLING##################

def poll_handler(user: discord.Member, interaction):
    '''This is triggered by every interaction from the bot, poll vote is updated accordingly
    '''
    data = database.poll_fetch_user(user=user,interaction=interaction)
    if data is None:
        database.poll_insert_user(user=user, interaction=interaction)
    else:
        database.poll_update_user(user=user, interaction=interaction)


def poll_handler_end(interaction):
    '''This is the handler for the interaction in ending a poll. Returns a tuple.
    '''
    data = database.poll_fetch_all(interaction=interaction)
    if data is None:
        return False
    a = sum(data.count("Yes") for x in data)
    b = sum(data.count("Abstain") for x in data)
    c = sum(data.count("No") for x in data)
    return {"Yes":a, "Abstain":b, "No":c}





            

            