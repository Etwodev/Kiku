import discord, datetime

from discord.user import Profile
from utils import database

class ProfileHeader:
    def __init__(self, user: discord.User):
        self.user = user

        profile = database.fetch_one(sql="SELECT * FROM tbl_profile WHERE user_id = %s", values=(self.user.id,))
        if not profile:
            profile = profile_initiate(user)

        self.date = profile[1]
        self.marriage_id = profile[2]
        self.marriage_status = int(profile[3])
        self.afk_status = int(profile[4])
        self.afk_message = profile[5]

    def is_afk(self) -> bool:
        return self.afk_status == 1

    def is_married(self) -> bool:
        return self.marriage_status >= 1

    def set_afk(self, message: str):
        sql = "UPDATE tbl_profile SET afk_message = %s, is_afk = %s WHERE user_id = %s"
        values = (message, 1, self.user.id,)
        database.insert(sql=sql, values=values)
        self.afk_status == 1
        self.afk_message == message
    
    def remove_afk(self, message="User is afk."):
        sql = "UPDATE tbl_profile SET afk_message = %s, is_afk = %s WHERE user_id = %s"
        values = (message, 0, self.user.id,)
        database.insert(sql=sql, values=values)
        self.afk_status == 0
        self.afk_message == message

    def set_marriage(self, mention) -> bool:
        if self.is_married() or mention.is_married():
            return False
        sql = "UPDATE tbl_profile SET married_to = %s, is_married = %s WHERE user_id = %s"
        values = (mention.user.id, 1, self.user.id,)
        database.insert(sql=sql, values=values)
        values = (self.user.id, 1, mention.user.id)
        database.insert(sql=sql, values=values)
        self.marriage_status == 1
        self.marriage_id == mention.user.id
        mention.marriage_status == 1
        mention.marriage_id == mention.user.id
        return True

    def remove_marriage(self, message="Nobody") -> bool:
        if not self.is_married():
            return False
        sql = "UPDATE tbl_profile SET married_to = %s, is_married = %s WHERE user_id = %s"
        values = (message, 0, self.user.id,)
        database.insert(sql=sql, values=values)
        sql = "UPDATE tbl_profile SET married_to = %s, is_married = %s WHERE married_to = %s"
        database.insert(sql=sql, values=values)
        self.marriage_status == 0
        self.marriage_id == message
        return True

def profile_initiate(user: discord.User):
    sql = "INSERT INTO tbl_profile(user_id, created_at) VALUES(%s, %s)"
    values = (user.id, datetime.datetime.now(),)
    database.insert(sql=sql, values=values)
    sql = "SELECT * FROM tbl_profile WHERE user_id = %s"
    values = (user.id,)
    return database.fetch_one(sql=sql, values=values)

class HaremHeader:
    def __init__(self, user: discord.User):
        self.user = user

        profile = database.fetch_one(sql="SELECT * FROM tbl_harem WHERE user_id = %s", values=(self.user.id,))
        if not profile:
            profile = harem_initiate(user)
        
        self.status = int(profile[1])
        self.owner = profile[2]

    def in_harem(self) -> bool:
        return self.status == 1
    
    def is_owner(self) -> bool:
        return self.owner == str(self.user.id)

    def count(self) -> int:
        if not self.in_harem():
            return None
        sql = "SELECT * FROM tbl_harem WHERE harem_owner = %s"
        values = (self.owner,)
        return len(database.fetch_all(sql=sql, values=values)) - 1

    def users(self) -> list:
        if not self.in_harem():
            return None
        sql = "SELECT user_id FROM tbl_harem WHERE harem_owner = %s"
        values = (self.owner,)
        return [e for i in database.fetch_all(sql=sql, values=values) for e in i]

    def add(self, mention):
        if not self.is_owner() or mention.in_harem():
            return False
        elif self.count() == 5:
            return False
        sql = "UPDATE tbl_harem SET harem_owner = %s, is_harem = %s WHERE user_id = %s"
        values = (self.user.id, 1, mention.user.id,)
        database.insert(sql=sql, values=values)
        mention.status == 1
        mention.owner == self.user.id
        return True
    
    def leave(self, message="Nobody"):
        if self.is_owner() or not self.in_harem():
            return False
        sql = "UPDATE tbl_harem SET harem_owner = %s, is_harem = %s WHERE user_id = %s"
        values = (message, 0, self.user.id,)
        database.insert(sql=sql, values=values)
        self.status == 0
        self.owner == message
        return True        
    
    def end(self, message="Nobody"):
        if not self.is_owner():
            return False
        elif self.count() != 0:
            return False
        sql = "UPDATE tbl_harem SET harem_owner = %s, is_harem = %s WHERE user_id = %s"
        values = (message, 0, self.user.id,)
        database.insert(sql=sql, values=values)
        self.status == 0
        self.owner == message
        return True

    def create(self):
        if self.is_owner() or self.in_harem():
            return False
        sql = "UPDATE tbl_harem SET harem_owner = %s, is_harem = %s WHERE user_id = %s"
        values = (self.user.id, 1, self.user.id,)
        database.insert(sql=sql, values=values)
        self.status == 1
        self.owner == self.user.id
        return True        

def harem_initiate(user: discord.User):
    sql = "INSERT INTO tbl_harem(user_id) VALUES(%s)"
    values = (user.id,)
    database.insert(sql=sql, values=values)
    sql = "SELECT * FROM tbl_harem WHERE user_id = %s"
    values = (user.id,)
    return database.fetch_one(sql=sql, values=values)


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
    '''This is the handler for the interaction in ending a poll. Returns a dictionary.
    '''
    data = database.poll_fetch_all(interaction=interaction)
    if data is None:
        return False
    a = sum(value.count("Yes") for value in data)
    b = sum(value.count("Abstain") for value in data)
    c = sum(value.count("No") for value in data)
    return {"Yes":a, "Abstain":b, "No":c}





            

            