
import sqlite3
w = []
with sqlite3.connect('Chinese_words.db') as connection:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Words')
    for cnt, (id_, character, pinyin, translation, picture) in enumerate(cursor.fetchall(), start=1):
        w.append([cnt, character, pinyin, translation, picture])
connection.close()
print (w)




with sqlite3.connect('Chinese_words.db') as connection:
    cursor = connection.cursor()
    cursor.execute('''DELETE FROM Words WHERE ID IN (
    SELECT ID FROM Words
    ORDER BY ID DESC
    LIMIT 2)''')
connection.commit()
connection.close()