import os
import mysql.connector
from decorators import once

@once
def connect_to_db(conn=None) -> mysql.connector.connection_cext.CMySQLConnection:
    """Функция подключения к БД"""
    print('Подключение к БД')
    try:
        conn = mysql.connector.connect(user='root',
                                       password=os.getenv("DB_PASSWORD"),
                                       host='127.0.0.1',
                                       database='department_of_information_technology_and_learning')
    except mysql.connector.DatabaseError:
        print(f'Не удалось подключиться к БД')
    return conn

db_handler = connect_to_db()

def read_sql(conn: mysql.connector.connection_cext.CMySQLConnection, table: str, queries_read: list):
    """Функция обработки запросов к БД"""
    print('READ FROM DB')

    values = []
    if ("INSERT INTO" in queries_read):
        sql_read = f"INSERT INTO {table} (id_student, name_student, group_student, sub_group_student, phone_number_student, email) VALUES (%s, %s, %s, %s, %s, %s)"
    elif ("DELETE" in queries_read):
        sql_read = f"DELETE FROM {table} WHERE id_student == %s"
    for _qq in queries_read:
        if ("INSERT INTO" not in _qq and
                "DELETE" not in _qq):
            values.append(_qq)
    print(values)
    cursor = conn.cursor()
    crud_res = cursor.executemany(sql_read, values)


#read_sql(db_handler, table='students', queries_read=[
#  "INSERT INTO",
#  ('4', 'Просвирнина Жанна Владимировна', 1, 1, 89167564433, 'janjac@mail.ru'),
#  ('5', 'Тверской Дмитрий Романович', 2, 2, 89175349022, 'TDR@yandex.ru')
#])
read_sql(db_handler, table='students', queries_read=[
  "DELETE",
  ('4',),
  ('5',)
])
cursor = db_handler.cursor()
cursor.execute("SELECT * FROM students;")
for select in cursor:
    print(select)



