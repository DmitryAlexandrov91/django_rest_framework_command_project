import csv
import sqlite3

con = sqlite3.connect("db.sqlite3")

cur = con.cursor()

with open('category.csv', encoding='utf-8') as file:
    data = csv.DictReader(file)
    to_base = [(i['id'], i['name'], i['slug']) for i in data]
    for i in to_base:
        cur.executemany(
            "INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);",
            i)
# con.commit()
# con.close()
