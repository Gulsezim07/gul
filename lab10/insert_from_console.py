import psycopg2
import csv
from tabulate import tabulate


conn = psycopg2.connect(
    host="localhost",
    dbname="lab10",
    user="postgres",
    password="12345",
    port=5432               
)

cur = conn.cursor()
conn.set_session(autocommit=True)


cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL
);
""")


while True:
    print("""
📘 МЕНЮ:
1 - Вставить контакт вручную
2 - Загрузить контакты из CSV
3 - Показать все контакты
0 - Выйти
""")
    choice = input("Выбери действие: ")

    if choice == "1":
        
        first_name = input("Имя: ")
        last_name = input("Фамилия: ")
        phone = input("Телефон: ")
        cur.execute(
            "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
            (first_name, last_name, phone)
        )
        print(" Контакт добавлен.\n")

    elif choice == "2":
        
        filepath = input("Введите путь к CSV-файлу: ")
        try:
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cur.execute(
                        "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                        (row['first_name'], row['last_name'], row['phone_number'])
                    )
            print("Данные из CSV успешно добавлены.\n")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}\n")

    elif choice == "3":
        
        cur.execute("SELECT * FROM phonebook;")
        rows = cur.fetchall()
        print(tabulate(rows, headers=["ID", "Имя", "Фамилия", "Телефон"], tablefmt="fancy_grid"))

    elif choice == "0":
        print(" Выход из программы.")
        break

    else:
        print(" Неверный ввод. Попробуй снова.")


cur.close()
conn.close()
