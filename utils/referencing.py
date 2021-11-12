import discord, datetime, ast
from utils import database, definitions
import random


#################AFK & PROFILE HANDLING##################

def fetch_handler(user: discord.Member):
    """fetches the required data for the MySQL server.
    """
    data = database.profile_fetch_user(user)
    if data is None:
        database.profile_insert_user(user=user, date=datetime.datetime.now())
        return database.profile_fetch_user(user)
    else:
        return data

def update_handler(user: discord.Member, var1, var2):
    """fetches the user and then updates the load.
    """
    fetch_handler(user)
    database.profile_update_user(user, var1, var2)
    return

#################POLL HANDLING##################

def poll_handler(user: discord.Member, interaction):
    data = database.poll_fetch_user(user=user,interaction=interaction)
    if data is None:
        database.poll_insert_user(user=user, interaction=interaction)
    else:
        database.poll_update_user(user=user, interaction=interaction)


def poll_end_handler(interaction):
    data = database.poll_fetch_all(interaction=interaction)
    if data is None:
        return False
    x = 0
    y = 0
    z = 0
    for val in data:
        for single in val:
            if single == "Yes":
                x = x + 1
            elif single == "Abstain":
                y = y + 1
            elif single == "No":
                z = z + 1
    raw = {"Yes":x, "Abstain":y, "No":z}
    return raw





            

            