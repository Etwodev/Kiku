from utils import startup
import mysql.connector
import discord

class MySQL:
    def __init__(self):
        self.connection = None
        self.config = startup.get("config.json")

    def __enter__(self):
        self.connection = mysql.connector.connect(user=self.config.sql.user, password=self.config.sql.password, db=self.config.sql.database, host=self.config.sql.host, autocommit=True)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type or exc_val or exc_tb:
                    self.connection.rollback()
                    self.connection.close()
            else:
                self.connection.close()
        except:
            self.connection.close()


##################AFK & PROFILE HANDLING##################

def profile_fetch_user(user: discord.Member, *args, **kwargs):
    """Queries the main server and fetches one response.
    This should **NOT** be used in tandem with UPDATE or INPUT,
    as it can create some desync problems. All operations should be done in **ONE** go.
    """
    data = "SELECT * FROM tbl_profile WHERE user_id = %s"
    values = (user.id,)
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(data, values)
        return db.fetchone()


def profile_update_user(user: discord.Member, var1, var2:int):
    """Updates the main server based upon the specified data load.
    Calls should happen just within this section, as it will be cancelled upon exit.
    Load (the user's profile) -> should be converted into a string for updating LONGTEXT().
    """
    data = "UPDATE tbl_profile SET afk_message = %s, is_afk = %s WHERE user_id = %s"
    values = (var1, var2, user.id,)
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(data, values)
        return

def profile_insert_user(user: discord.Member, date: str):
    """Inserts into main server for first-time users.
    This should be called if fetch_user() returns None.
    """
    sql = "INSERT INTO tbl_profile(user_id, created_at) VALUES(%s, %s)"
    val = (user.id, date,)
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(sql, val)
        return

##################POLL HANDLING##################

def poll_fetch_user(user: discord.Member, interaction):
    data = "SELECT * FROM tbl_polls WHERE user_id = %s AND message_id = %s"
    values = (user.id, interaction.message.id,)
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(data, values)
        return db.fetchone()

def poll_update_user(user: discord.Member, interaction):
    data = "UPDATE tbl_polls SET vote_id = %s WHERE user_id = %s AND message_id = %s"
    values = (interaction.custom_id, user.id, interaction.message.id,)
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(data, values)
        return

def poll_insert_user(user: discord.Member, interaction):
    sql = "INSERT INTO tbl_polls(user_id, message_id, vote_id) VALUES(%s, %s, %s)"
    val = (user.id, interaction.message.id, interaction.custom_id,)
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(sql, val)
        return

def poll_fetch_all(interaction):
    data = "SELECT * FROM tbl_polls WHERE message_id = %s"
    delt = "DELETE FROM tbl_polls WHERE message_id = %s"
    values = (interaction.message.id,)
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(data, values)
        data = db.fetchall()
        db.execute(delt, values)
        return data