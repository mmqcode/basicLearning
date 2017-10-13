import psycopg2
import datetime
import uuid

conn = psycopg2.connect(database="mydb", user="mmq", password="123456", host="127.0.0.1", port="")

cur = conn.cursor()

sql = "INSERT INTO blz_img(id, img_name, img_url, img_size, img_group, img_source, create_time) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s)"

data = (str(uuid.uuid5(uuid.NAMESPACE_DNS, "Vilespine_Slayer_full.jpg")), "Vilespine_Slayer_full.jpg", "img/hs/Journey_to_UnGoro/Vilespine_Slayer_full.jpg", 7000000, "Journey_to_UnGoro", "heartstone", datetime.datetime.now())

cur.execute(sql, data)

conn.commit()

