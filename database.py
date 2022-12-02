import sqlite3


def select_from_user():
    conn = sqlite3.connect('db/vpn.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user')
    res = cur.fetchall()
    print(res)
    cur.close()


def select_user(telegram_id: int):
    conn = sqlite3.connect('db/vpn.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM user WHERE telegram_id = {telegram_id}')
    res = cur.fetchone()
    cur.close
    return res


def insert_into_user(data: tuple):
    conn = sqlite3.connect('db/vpn.db')
    cur = conn.cursor()
    try:
        # cur.execute('INSERT INTO user(telegram_id, username, firstname, lastname) VALUES (?, ?, ?, ?)', yar)
        cur.execute('INSERT INTO user(telegram_id, username, firstname, lastname) VALUES (?, ?, ?, ?)', data)
    except sqlite3.IntegrityError:
        pass
    else:
        conn.commit()
    finally: cur.close()


def update_user(data: tuple):
    conn = sqlite3.connect('db/vpn.db')
    cur = conn.cursor()
    try:
        cur.execute(f"UPDATE user SET username = '{data[1]}', firstname = '{data[2]}', lastname = '{data[3]}' WHERE telegram_id = '{data[0]}'")
    except Exception as e:
        pass
    else:
        conn.commit()
    finally: cur.close()
#update_user((605360923, 'yarche', None, None))


def delete_all_from_user():
    conn = sqlite3.connect('db/vpn.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM user')
    conn.commit()
    cur.close()
#delete_all_from_user()


def select_all_from_accesskey(telegram_id: int):
    conn = sqlite3.connect('db/vpn.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM access_key WHERE user_id = (SELECT id FROM user WHERE telegram_id = {telegram_id})')
    res = cur.fetchone()
    cur.close()
    return res
#print(select_all_from_accesskey(605360923))

def select_from_subcription_by_id(telegram_id: int):
    conn = sqlite3.connect('db/vpn.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM subscription WHERE user_id = (SELECT id FROM user WHERE telegram_id = {telegram_id})')
    res = cur.fetchone()
    cur.close()
    return res
#print(select_user(2036666795))
# == (14, 605360923, 'porridgeX', 'yaroslav', None)
# x = select_user(1)
# print(x)

# conn = sqlite3.connect('db/vpn.db')
# cur = conn.cursor()
# cur.execute('SELECT * from access_key')
# res = cur.fetchall()
# print(res)
# cur.close()