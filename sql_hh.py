import sqlite3 as sq

# Подключение к базе данных
conn = sq.connect('my_base_hh.db')

cursor = conn.cursor()
print('*' * 50)
print(('Команда cursor.execute(\'SELECT * from city\') '))
print()
cursor.execute('SELECT * from city')
result = cursor.fetchall()
print(result)
print('*' * 50)

print('Команда cursor.execute(\'SELECT * from vacancy\') ')
print()
cursor.execute('SELECT * from vacancy')
result = cursor.fetchall()
print(result)

print('*' * 50)
print('Команда cursor.execute(\'SELECT v.name, c.name as city_name from vacancy v, city c where v.city_id == c.id\')')
print()
cursor.execute('SELECT v.name, c.name as city_name from vacancy v, city c where v.city_id == c.id')
result = cursor.fetchall()
print(result)

print('*' * 50)
print('Команда cursor.execute(\'SELECT * from city where name=?\', (\'Москва\'))')
print()
cursor.execute('SELECT * from city where name=?', ('Москва',))
result = cursor.fetchall()
print(result)

print('*' * 50)
print('Команда insert into vacancykey_skills (vacansy_id, key_skills_id) values (?, ?), (5, 3)')
cursor.execute('insert into vacancykey_skills (vacansy_id, key_skills_id) values (?, ?)', (5, 3))
cursor.execute('insert into vacancykey_skills (vacansy_id, key_skills_id) values (?, ?)', (5, 4))
print()

print('*' * 50)
print('Команда select * from vacancykey_skills')
print()
cursor.execute('select * from vacancykey_skills')
result = cursor.fetchall()
print(result)

# cursor.execute('insert into city (name) values (\'Чердаклы\')')
cursor.execute('SELECT * from city')
result = cursor.fetchall()
print(result)
print()

print('*' * 50)

query = ('SELECT '\
    'vk.id, v.name, k.name, c.name '\
    'FROM vacancy v, skill k, vacancykey_skills vk, city c '\
    'WHERE vk.vacansy_id = v.id AND '\
    'vk.key_skills_id = k.id AND '\
    'v.city_id = c.id')
cursor.execute(query)

result = cursor.fetchall()

for item in result:
    print('')
    for item1 in range(int(len(item))):
        print(f'{item[item1]:>20}|', end='')
print('')
query_insert_city = ('insert into city (name) values (\'Чердаклы\')')
query_delite = ('delete from city where name = "Сочи"')

query_insert = ('insert into vacancy (name, city_id) values (?, ?)', ('java developer', 4))

# cursor.execute(query_insert_city)

conn.commit()
conn.close()

conn = sq.connect('my_base_hh_homeworks.db')
cursor = conn.cursor()




sql_params = 'INSERT INTO city (name) VALUES(?);'

total_city = [('Кострома'), ('Москва'), ('Санкт-Петербург'), ('Ульяновск'), ('Чердаклы'),]

for row in total_city:
    print(row)
    cursor.execute("insert into city (name) VALUES (?)", (row,))



conn.commit()
conn.close()
