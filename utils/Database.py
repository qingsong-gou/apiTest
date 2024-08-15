"""
1. 将 pymysql 进行一个封装
    预期的结果 :
        调用 方法 就可以得到结果

        fetchall()   execute()  帮我执行写操作
"""
# 1. 导入 pymysql
import pymysql


class Database(object):
    # 属性
    def __init__(self, password, database, host="localhost", user="root", charset="utf8",
                 port=3306):  # 绑定初始化属性  对象被创建的时候自动调用执行
        # 2. 创建连接对象
        self.cnn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port
        )

    # 方法
    def fetchall(self, sql, args=None):
        # 3. 通过连接对象创建游标对象
        with self.cnn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            # 4. 使用游标对象执行sql语句
            cursor.execute(sql, args)
            # 5. 如果是查询语句 使用游标对象获取查询结果
            data = cursor.fetchall()
        return data

    def fetchone(self, sql, args=None):
        # 3. 通过连接对象创建游标对象
        with self.cnn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            # 4. 使用游标对象执行sql语句
            data =cursor.execute(sql, args)
            # 5. 如果是查询语句 使用游标对象获取查询结果
            data = cursor.fetchone()
        return data

    def execute(self, sql, args=None):
        """
        执行 有受影响的行数的 sql语句
        :param sql:
        :param args:
        :return:
        """
        # 创建游标对象 执行 sql
        with self.cnn.cursor() as cursor:
            num = cursor.execute(sql, args)
        if num == 1:
            self.cnn.commit()
            return True
        else:
            self.cnn.rollback()
            return False

    def executemany(self, sql, args):
        """
        执行 多条返回受影响的行数的sql 语句
        :param sql:
        :param args:
        :return:
        """
        # 创建游标对象 执行 sql
        with self.cnn.cursor() as cursor:
            num = cursor.executemany(sql, args)
        if num == len(args):
            self.cnn.commit()
            return True
        else:
            self.cnn.rollback()
            return False

    def create(self, sql, args=None):
        try:
            with self.cnn.cursor() as cursor:
                cursor.execute(sql, args)
        except Exception as e:
            print("创建表失败", e)

    # def __del__(self):  # 对象被销毁的时候 自动调用执行
    #     # 7. 关闭连接对象
    #     self.cnn.close()


if __name__ == '__main__':
    # db = Database("root", "test")
    # sql = "select * from student where stu_name=%s and stu_id=%s"
    # args = ["曹操", 1]
    # res = db.fetchone(sql, args)
    # print(res)
    # res = db.fetchone(sql, args)
    # print(res)

    # 实例化数据库操作对象
    db = Database("root", "test")
    # 准备sql语句
    sql = "INSERT INTO student (stu_no,stu_name,money,class_id) VALUES (%s,%s,%s,%s)"
    args = [["itsrc-015", "大乔", 2500, 11], ["itsrc-016", "二乔", 2500, 11], ["itsrc-017", "三乔", 2500, 11],
            ["itsrc-018", "四乔", 2500, 11]]
    db.executemany(sql, args)
    # sql = "select * from student"
    # # 执行
    # res = db.fetchall(sql)
    # print(res)
