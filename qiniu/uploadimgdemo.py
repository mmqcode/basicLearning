# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import os
import psycopg2
import uuid
import datetime
import time

#需要填写你的 Access Key 和 Secret Key
access_key = ''
secret_key = ''

#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'heartstoneimg'

dir = "D:/python/heartstoneimg/Knights_of_the_Frozen_Throne_full_art"

conn = psycopg2.connect(database="mydb", user="mmq", password="123456", host="", port="5432")

cur = conn.cursor()


insertsql = "INSERT INTO blz_img(id, img_name, img_url, img_size, img_group, img_source, create_time) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s)"

selectsql = "SELECT * FROM blz_img WHERE img_name = %s"

datas = []
files = [x for x in os.listdir(dir)]
count = 0
for imgfile in files:
    print(imgfile)
    cur.execute(selectsql, (imgfile,))
    temp = cur.fetchone()
    if isinstance(temp, tuple):
        print("exists!pass")
        continue
    key = 'img/hs/Knights_of_the_Frozen_Throne/'+imgfile
    token = q.upload_token(bucket_name, key, 3600)
    localfile = dir+"/"+imgfile
    filesize = os.path.getsize(localfile)
    print("uploading..")
    try:
        ret, info = put_file(token, key, localfile)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
    except TypeError:
        print("tpyerror occur, uploadfail")
        continue
    if info.status_code == 200:
        data = (str(uuid.uuid5(uuid.NAMESPACE_DNS, imgfile + str(time.time()))), imgfile, "img/hs/Knights_of_the_Frozen_Throne/"+imgfile, filesize, "Knights_of_the_Frozen_Throne", "heartstone", datetime.datetime.now())
        cur.execute(insertsql, data)
        conn.commit()
        print("success!")
    count += 1
    print(count)
cur.close()
conn.close()



#上传到七牛后保存的文件名
#
# #生成上传 Token，可以指定过期时间等
# token = q.upload_token(bucket_name, key, 3600)
#
# #要上传文件的本地路径
# localfile = 'D:/python/heartstoneimg/basic_full_art/Sprint_full.png'
#
# ret, info = put_file(token, key, localfile)
# print(info)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)
