"""
Функции для работы со словами и БД.
"""
import random
from django.db import connection


def add_training(success):
    """
    Добавление в таблицу Trainings числа успешных/неуспешных повторений
    """
    with connection.cursor() as cursor:
        cursor.execute(''' SELECT Successful_tr, Unsuccessful_tr FROM Trainings''')
        trainings = cursor.fetchall()
        sucs_tr = int(trainings[0][0])
        unsucs_tr = int(trainings[0][1])
        if success == 1:
            sucs_tr += 1
            cursor.execute("UPDATE Trainings SET Successful_tr = %s "
                           "WHERE id = 1;", (sucs_tr,))
        else:
            unsucs_tr += 1
            cursor.execute("UPDATE Trainings SET Unsuccessful_tr = %s "
                           "WHERE id = 1;", (unsucs_tr,))


def get_word_for_table():
    words = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID, Character, Pinyin, Translation FROM Words')
        for cnt, (id, character, pinyin, translation) in enumerate(cursor.fetchall(), start=1):
            words.append([cnt, character, pinyin, translation])
    return words

def add_user (user_name, user_email, user_phone = ""):
    """
    Добавление нового пользователя в БД
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID, User_name, User_email, User_phone FROM Users '
                       'WHERE User_name = %s AND User_email = %s', (user_name, user_email))
        row = cursor.fetchone()
        cursor.execute('SELECT MAX(ID) FROM Users')
        max_id_row = cursor.fetchone()
        if max_id_row[0] is None:
            user_id = 1
        else:
            user_id = max_id_row[0] + 1
        if row is None:
            cursor.execute(''' INSERT INTO Users(ID, User_name, User_email, User_phone)
            VALUES(%s, %s, %s, %s)''',
                    (user_id, user_name, user_email, user_phone))
        else:
            user_id = row[0]
    return user_id

def write_word(new_word, new_translation, user_id, new_pinyin = ""):
    """
        Подсчет количества слов в БД.
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT MAX(ID) FROM Words')
        last_row = cursor.fetchone()
        if last_row:
            new_id = last_row[0]+1
        else:
            new_id = 1
        cursor.execute('''
        INSERT INTO Words (ID, character, pinyin, translation, user_id) 
        VALUES (%s, %s, %s, %s, %s)''',
        (new_id, new_word, new_pinyin, new_translation, user_id))

def train_word ():
    """
        Генерация иероглифа и вариантов ответа для повторения в тренажере
    """
    words = get_word_for_table()
    rand_num1 = random.randint(1, len(words)-1)
    train_character = words[rand_num1][1]
    train_translation = words[rand_num1][3]
    rand_num2 = random.randint(1, len(words) - 1)
    rand_num3 = random.randint(1, len(words) - 1)
    if (rand_num1 == rand_num2) or (rand_num1 == rand_num3) or (rand_num2 == rand_num3):
        while (rand_num1 == rand_num2) or (rand_num1 == rand_num3) or (rand_num2 == rand_num3):
            rand_num2 = random.randint(1, len(words) - 1)
            rand_num3 = random.randint(1, len(words) - 1)
    false_translation1 = words[rand_num2][3]
    false_translation2 = words[rand_num3][3]
    train_words = [train_translation, false_translation1, false_translation2]
    random.shuffle(train_words)
    index_true = train_words.index(train_translation)+1
    train_words.append(train_character)
    train_words.append(index_true)
    train_words.append(train_translation)
    return train_words


def get_words_stats():
    words_all = get_word_count()
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM Users;')
        users_all = cursor.fetchone()[0]
        cursor.execute(("SELECT COUNT(*) FROM Words WHERE User_id IS NOT NULL"))
        words_added = cursor.fetchone()[0]
        words_db = int(words_all)-int(words_added)
        cursor.execute(("SELECT Successful_tr, Unsuccessful_tr FROM Trainings"))
        trainings = cursor.fetchall()
        successful_tr_cnt = trainings[0][0]
        unsuccessful_tr_cnt = trainings[0][1]
        stats = {
            "words_all": words_all,
            "words_db": words_db,
            "words_added": words_added,
            "users_all": users_all,
            "sucs_tr": successful_tr_cnt,
            "unsucs_tr": unsuccessful_tr_cnt,
        }
    return stats

def get_word_count():
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT() AS cnt FROM Words')
        cnt = int(cursor.fetchone()[0])
    return cnt
