import sqlite3

# Initialiser la base de données SQLite
def init_db():
    conn = sqlite3.connect('bot_database.db')  # Créez la base de données SQLite
    cursor = conn.cursor()

    # Créez la table "onlines" si elle n'existe pas, avec les nouveaux champs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS onlines (
            user_id TEXT PRIMARY KEY,
            registered_id TEXT,
            quest_completed INTEGER,
            vote1_completed INTEGER DEFAULT 0,
            vote2_completed INTEGER DEFAULT 0,
            pets_checked TEXT
        )
    ''')

    conn.commit()
    conn.close()
# Ajouter un utilisateur à la base de données
def add_user(user_id, registered_id, quest_completed=False):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO onlines (user_id, registered_id, quest_completed) VALUES (?, ?, ?)', 
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
    return {row[0]: {"registered_id": row[1], "quest_completed": row[2]} for row in results}

# Mettre à jour l'état de la quête pour un utilisateur
def update_quest_status(user_id, updates):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Mettre à jour les champs "registered_id" et "quest_completed" si fournis dans 'updates'
    if 'registered_id' in updates and 'quest_completed' in updates:
        cursor.execute('''
            UPDATE onlines
            SET registered_id = ?, quest_completed = ?
            WHERE user_id = ?
        ''', (updates['registered_id'], updates['quest_completed'], user_id))

    elif 'registered_id' in updates:
        cursor.execute('''
            UPDATE onlines
            SET registered_id = ?
            WHERE user_id = ?
        ''', (updates['registered_id'], user_id))

    elif 'quest_completed' in updates:
        cursor.execute('''
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
    cursor.execute('''
        UPDATE onlines 
        SET vote1_completed = ?, vote2_completed = ?
        WHERE user_id = ?
    ''', (vote_data.get('vote1_completed', False), vote_data.get('vote2_completed', False), user_id))
    conn.commit()
    conn.close()

# Mettre à jour l'heure du dernier rappel des "pets" pour un utilisateur
def update_pets_status(user_id, last_pets_time):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE onlines 
        SET last_pets_time = ?
        WHERE user_id = ?
    ''', (last_pets_time, user_id))
    conn.commit()
    conn.close()

# Vérifier si un utilisateur existe dans la base de données
def user_exists(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM onlines WHERE user_id = ?', (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Récupérer un utilisateur spécifique à partir de la base de données
def get_user(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM onlines WHERE user_id = ?', (user_id,))
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
    cursor.execute('DELETE FROM onlines WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()