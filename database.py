import sqlite3

from scripts_utils.logs_manager import logs

# Initialiser la base de données SQLite
# def init_db():
#     conn = sqlite3.connect(
#         'bot_database.db')  # Créez la base de données SQLite
#     cursor = conn.cursor()

#     # Créez la table "onlines" si elle n'existe pas, avec les nouveaux champs
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS onlines (
#             user_id TEXT PRIMARY KEY,
#             registered_id TEXT,
#             quest_completed INTEGER,
#             vote1_completed INTEGER DEFAULT 0,
#             vote2_completed INTEGER DEFAULT 0,
#             pets_checked TEXT
#         )
#     ''')

#     conn.commit()
#     conn.close()


# Ajouter un utilisateur à la base de données
def add_user(user_id, registered_id, quest_completed=False):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO onlines (user_id, registered_id, quest_completed) VALUES (?, ?, ?)',
        (user_id, registered_id, quest_completed))
    conn.commit()
    conn.close()


# Récupérer tous les utilisateurs
def get_all_users():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM onlines')
    results = cursor.fetchall()
    conn.close()

    # Crée un dictionnaire à partir des résultats
    return {
        row[0]: {
            "registered_id": row[1],
            "quest_completed": row[2]
        }
        for row in results
    }


# Mettre à jour l'état de la quête pour un utilisateur
def update_quest_status(user_id, updates):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Mettre à jour les champs "registered_id" et "quest_completed" si fournis dans 'updates'
    if 'registered_id' in updates and 'quest_completed' in updates:
        cursor.execute(
            '''
            UPDATE onlines
            SET registered_id = ?, quest_completed = ?
            WHERE user_id = ?
        ''', (updates['registered_id'], updates['quest_completed'], user_id))

    elif 'registered_id' in updates:
        cursor.execute(
            '''
            UPDATE onlines
            SET registered_id = ?
            WHERE user_id = ?
        ''', (updates['registered_id'], user_id))

    elif 'quest_completed' in updates:
        cursor.execute(
            '''
            UPDATE onlines
            SET quest_completed = ?
            WHERE user_id = ?
        ''', (updates['quest_completed'], user_id))

    conn.commit()
    conn.close()


# Mettre à jour l'état des votes pour un utilisateur
def update_vote_status(user_id, vote_data):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE onlines 
        SET vote1_completed = ?, vote2_completed = ?
        WHERE user_id = ?
    ''', (vote_data.get('vote1_completed', False),
          vote_data.get('vote2_completed', False), user_id))
    conn.commit()
    conn.close()


# Mettre à jour l'heure du dernier rappel des "pets" pour un utilisateur
def update_pets_status(user_id, last_pets_time):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE onlines 
        SET last_pets_time = ?
        WHERE user_id = ?
    ''', (last_pets_time, user_id))
    conn.commit()
    conn.close()


# Vérifier si un utilisateur existe dans la base de données
# def user_exists(user_id):
#     conn = sqlite3.connect('bot_database.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT 1 FROM onlines WHERE user_id = ?', (user_id, ))
#     exists = cursor.fetchone() is not None
#     conn.close()
#     return exists


# Récupérer un utilisateur spécifique à partir de la base de données
def get_user(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM onlines WHERE user_id = ?', (user_id, ))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "user_id": result[0],
            "registered_id": result[1],
            "quest_completed": result[2],
            "vote1_completed": result[3],
            "vote2_completed": result[4],
            "last_pets_time": result[5]
        }
    return None


# Supprimer un utilisateur de la base de données
def remove_user(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM onlines WHERE user_id = ?', (user_id, ))
    conn.commit()
    conn.close()


#
#
#
#
#
#
#

from datetime import datetime

import pytz

tz = pytz.timezone('Europe/Paris')


# Initialiser la base de données SQLite
def init_db() -> bool:
    """
    ### Creating the db

    **Returns :**
    - *bool* (False = failure, True = success)
    """
    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()

        query = "CREATE TABLE IF NOT EXISTS onlines (user_id TEXT PRIMARY KEY, pseudo TEXT, registered_id TEXT, quest_completed INTEGER, vote1_completed INTEGER DEFAULT 0, vote2_completed INTEGER DEFAULT 0, last_pets_time TEXT)"

        cursor.execute(query)

        conn.commit()
        conn.close()
    except Exception as e:
        logs("db_initError", {"error": e})
        return False
    return True


def user_exists_db(user_id):
    """
    ### Search a user in the db
    **Arguments :**
    - user_id: *str* (discord user id)

    **Returns :**
    - *object* (None = failure, True = success)
    """
    try:
        verification = get_user_db(user_id)
        if verification:
            return True
        logs("db_userExistsError2", {
            "user_id": user_id,
            "verification": verification
        })
        return False
    except Exception as e:
        logs("db_userExistsError1", {"user_id": user_id, "error": e})
        return False


def user_dont_exist_db(user_id):
    """
    ### Search a user not in the db
    **Arguments :**
    - user_id: *str* (discord user id)

    **Returns :**
    - *object* (None = success, True = failure)
    """
    try:
        verification = get_user_db(user_id)
        if verification:
            logs("db_userDontExistError2", {
                "user_id": user_id,
                "verification": verification
            })
            return False
        return True
    except Exception as e:
        logs("db_userDontExistError1", {"user_id": user_id, "error": e})
        return False


def add_user_db(user_id: int, pseudo: str) -> bool:
    """
    ### Adding a user to the db
    **Arguments :**
    - user_id: *int* (discord user id)
    - pseudo: *str* (minecraft pseudo)

    **Returns :**
    - *bool* (False = failure, True = success)
    """
    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()

        query = "INSERT INTO onlines (user_id, pseudo, registered_id, quest_completed,  vote1_completed, vote2_completed, last_pets_time) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (user_id, pseudo, None, False, False, False,
                  datetime.now(tz).isoformat())

        cursor.execute(query, values)
        conn.commit()
        conn.close()
    except Exception as e:
        logs("db_addUserError", {
            "user_id": user_id,
            "pseudo": pseudo,
            "error": e
        })
        return False
    return True


def update_user_db(user_id: int, value: dict) -> bool:
    """
    ### Edit a user's information in the database
    **Arguments :**
    - user_id: *int* (discord user id)
    - value: *dict* (ex: {"vote1_completed": False, "vote2_completed": False})

    **Returns :**
    - *bool* (False = failure, True = success)
    """
    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()

        query = "UPDATE onlines SET " + ", ".join(
            f"{key} = ?" for key in value) + " WHERE user_id = ?"

        values = list(value.values()) + [user_id]
        cursor.execute(query, values)

        conn.commit()
        conn.close()
    except Exception as e:
        logs("db_updateUserError", {
            "user_id": user_id,
            "value": value,
            "error": e
        })
        return False
    return True


def remove_user_db(user_id: int) -> bool:
    """
    ### Removing a user from the db
    **Arguments :**
    - user_id: *int* (discord user id)

    **Returns :**
    - *bool* (False = failure, True = success)
    """
    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        query = "DELETE FROM onlines WHERE user_id = ?"
        values = [user_id]
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    except Exception as e:
        logs("db_removeUserError", {"user_id": user_id, "error": e})
        return False
    return True


def get_user_db(user_id: int) -> dict:
    """
    ### Retrieve a user from the db
    **Arguments :**
    - user_id: *int* (discord user id)
    
    **Returns :**
    - *dict* (None = failure)

    `{"user_id": id[0], 
    "pseudo": id[1],
    "registered_id": id[2], 
    "quest_completed": id[3], 
    "vote1_completed": id[4], 
    "vote2_completed": id[5], 
    "last_pets_time": id[6]}`

    """
    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        query = "SELECT * FROM onlines WHERE user_id = ?"
        values = [user_id]
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.close()

        if result:
            user = {
                "user_id": result[0],
                "pseudo": result[1],
                "registered_id": result[2],
                "quest_completed": result[3],
                "vote1_completed": result[4],
                "vote2_completed": result[5],
                "last_pets_time": result[6]
            }
            if user:
                print("")
                print(f"> [SUCCESS] > database.py -> get_user_db({user_id})")
                print(f"-> {query}")
                print(f"-> {values}")
                print(f"-> Return: {user}")
                print("")
                return user
    except Exception as e:
        logs("db_getUserError", {"error": e})
        return None
    return None


def get_all_users_db() -> dict:
    """
    ### Retrieve all users from the db
    **Returns :**
    - *dict* (None = failure)

    `{"user_id":
    {"user_id": id[0],
    "pseudo": id[1],
    "registered_id": id[2],
    "quest_completed": id[3],
    "vote1_completed": id[4],
    "vote2_completed": id[5],
    "last_pets_time": id[6]}`

    """
    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM onlines')
        results = cursor.fetchall()
        conn.close()

        all_users = {
            id[0]: {
                "user_id": id[0],
                "pseudo": id[1],
                "registered_id": id[2],
                "quest_completed": id[3],
                "vote1_completed": id[4],
                "vote2_completed": id[5],
                "last_pets_time": id[6]
            }
            for id in results
        }

    except Exception as e:
        logs("db_getAllUsersError", {"error": e})
        return None
    return all_users


# MAKE : Init & UserExists
