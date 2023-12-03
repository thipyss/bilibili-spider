import pymysql

class Database:
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='123456',
                                  db='test',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def create_table(self, table):
        sql = f'''
        create table if not exists {table}
        (
            comment_id bigint not null primary key,
            bv varchar(20),
            uid bigint,
            likes int,
            ip varchar(20),
            publish_time datetime,
            root_id bigint,
            parent_id bigint,
            content varchar(1000),
        )
        '''
        try:
            self.cursor.execute(sql)
            print('Successful')
            self.db.commit()
        except:
            print('Failed')
            self.db.rollback()

    def insert(self, table, data):
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql_query = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        try:
            if self.cursor.execute(sql_query, tuple(data.values())):
                print('Successful')
                self.db.commit()
        except:
            print('Failed')
            self.db.rollback()

    def close(self):
        self.db.close()