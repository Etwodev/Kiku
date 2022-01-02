from utils import config
import mysql.connector
import discord

class MySQL:
    def __init__(self):
        self.connection = None
        self.config = config.get("config.json")

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

def fetch_one(sql: str, values: tuple) -> tuple:
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(sql, values)
        return db.fetchone()

def fetch_all(sql: str, values: tuple) -> tuple:
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(sql, values)
        return db.fetchall()

def insert(sql: str, values: tuple):
    with MySQL() as connection:
        db = connection.cursor()
        db.execute(sql, values)
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