from django.db import connection

w = []
with connection.cursor() as cursor:
    cursor.execute('SELECT ID, Character, Pinyin, Translation FROM Words')
    for cnt, (id_, character, pinyin, translation) in enumerate(cursor.fetchall(), start=1):
        w.append([cnt, character, pinyin, translation])
print (w)
