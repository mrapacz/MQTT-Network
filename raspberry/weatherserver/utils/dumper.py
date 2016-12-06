import psycopg2
from datetime import datetime


def dump_data(chip_id, temperature):
    conn = psycopg2.connect(database="temperatures", user="admin", password="adminpassword")
    cur = conn.cursor()
    cur.execute('INSERT INTO temperatures_probe (node_id, temperature, timestamp) VALUES (%s, %s, %s);',
                (chip_id, temperature, datetime.now()))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    temp = float(input())
    id = "123456"
    dump_data(id, temp)
