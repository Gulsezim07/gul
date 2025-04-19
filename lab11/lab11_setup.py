import psycopg2

# 1. Байланысу
conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 2. Барлық SQL кодтарды бір-бірлеп орындау

#  1-Тапсырма: search_phonebook
cur.execute("""
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE (
    user_id INTEGER,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    WHERE first_name ILIKE '%' || pattern || '%'
       OR last_name ILIKE '%' || pattern || '%'
       OR phone_number ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
""")

#  2-Тапсырма: upsert_user
cur.execute("""
CREATE OR REPLACE PROCEDURE upsert_user(fname TEXT, lname TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook WHERE first_name = fname AND last_name = lname
    ) THEN
        UPDATE phonebook
        SET phone_number = phone
        WHERE first_name = fname AND last_name = lname;
    ELSE
        INSERT INTO phonebook(first_name, last_name, phone_number)
        VALUES (fname, lname, phone);
    END IF;
END;
$$;
""")

#  3-Тапсырма: insert_many_users
cur.execute("""
CREATE OR REPLACE PROCEDURE insert_many_users(
    fnames TEXT[],
    lnames TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
BEGIN
    WHILE i <= array_length(fnames, 1) LOOP
        IF phones[i] ~ '^[0-9]+$' THEN
            CALL upsert_user(fnames[i], lnames[i], phones[i]);
        ELSE
            RAISE NOTICE '❗ Неверный номер у % %: %', fnames[i], lnames[i], phones[i];
        END IF;
        i := i + 1;
    END LOOP;
END;
$$;
""")

#  4-Тапсырма: get_page
cur.execute("""
CREATE OR REPLACE FUNCTION get_page(limit_n INT, offset_n INT)
RETURNS TABLE (
    user_id INTEGER,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY user_id
    LIMIT limit_n OFFSET offset_n;
END;
$$ LANGUAGE plpgsql;
""")

#  5-Тапсырма: delete_user_data
cur.execute("""
CREATE OR REPLACE PROCEDURE delete_user_data(fname TEXT, lname TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE (first_name = fname AND last_name = lname)
       OR phone_number = phone;
END;
$$;
""")

# 3. Бітті — жабу
conn.commit()
cur.close()
conn.close()

print(" Барлық функциялар мен процедуралар сәтті құрылды!")
