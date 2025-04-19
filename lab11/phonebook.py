import psycopg2

conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="12345", 
    host="localhost",
    port="5432"
)

cur = conn.cursor()


cur.execute('''
    CREATE TABLE IF NOT EXISTS PhoneBook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        phone_number VARCHAR(20)
    );
''')

conn.commit()
cur.close()
conn.close()
print("Таблица PhoneBook успешно создана.")