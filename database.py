
import MySQLdb
import json

from bson import json_util


class Database:

    tmp = None

    def __init__(self):
        self.db = MySQLdb.connect("localhost", "pi", "poziom9", "pi")
        self.cursor = self.db.cursor()

    def get_all_files(self):

        if self.tmp is None:
            return json.dumps(self.tmp)

        sql = "SELECT * FROM files WHERE user_id=%s LIMIT 10" % self.tmp["user_id"]
        self.cursor.execute(sql)
        fetched_data = self.cursor.fetchall()

        data = []

        for row in fetched_data:
            t = {
                    'id': row[0],
                    'name': row[1],
                    'type': row[2],
                    'size': row[3],
                    'path': row[4],
                    'date': row[6].strftime('%s')
            }
            data.append(t)

        return json.dumps(data)

    def get_file(self, file_id):
        sql = "SELECT * FROM files " \
                "LEFT JOIN users ON files.user_id = users.user_id " \
                "WHERE files.file_id = %s" % file_id
        self.cursor.execute(sql)
        data = self.cursor.fetchone()

        prepared_data = {
                'file_id': data[0],
                'filename': data[1],
                'type': data[2],
                'size': data[3],
                'path': data[4],
                'user_id': data[5],
                'date_added': data[6],
                'name': data[8],
                'surname': data[9]
        }

        return json.dumps(prepared_data, default=json_util.default)

    def get_shared_files(self):

        if self.tmp is None:
            return json.dumps(self.tmp)

        sql = "select f.*, u.* " \
              "from shared_files as sf " \
              "left join files as f on f.file_id = sf.file_id " \
              "left join users as u on f.user_id = u.user_id " \
              "where sf.user_id = %s or sf.user_id is null " \
              "and f.user_id != %s" % (self.tmp["user_id"], self.tmp["user_id"])

        self.cursor.execute(sql)
        fetched_data = self.cursor.fetchall()

        data = []

        for row in fetched_data:
            t = {
                    'id': row[0],
                    'name': row[1],
                    'type': row[2],
                    'size': row[3],
                    'path': row[4],
                    'date': row[6].strftime('%s'),
                    'user_user_id': row[7],
                    'owner_name': row[8],
                    'owner_surname': row[9],
            }
            data.append(t)

        return json.dumps(data)

    def share_file(self, file_id, user_id):

        if self.tmp is None:
            return json.dumps(self.tmp)

        if user_id != '0':
            sql = "INSERT INTO `shared_files` (`file_id`, `user_id`) VALUES (%s, %s)" % (file_id, user_id)
        else:
            sql = "INSERT INTO `shared_files` (`file_id`) VALUES (%s)" % file_id

        self.cursor.execute(sql)
        self.db.commit()

        return "OK"

    def user_principal(self):
        return json.dumps(self.tmp)

    def user_list(self):
        if self.tmp is None:
            return json.dumps(self.tmp)

        sql = "SELECT * FROM users WHERE user_id!=%s" % self.tmp["user_id"]
        self.cursor.execute(sql)
        fetched_data = self.cursor.fetchall()

        data = []

        for row in fetched_data:
            t = {
                    'user_id': row[0],
                    'name': row[1],
                    'surname': row[2]
            }
            data.append(t)

        return json.dumps(data)

    def user_login(self):
        self.tmp = {
            'user_id': 2,
            'username': 'Przykladowy'
        }
        return 'OK'

    def user_logout(self):
        self.tmp = None
        return 'OK'


