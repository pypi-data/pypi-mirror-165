"""
作者:陈泊文
日期:2022年09月02日
"""
import sqlite3

class Sql:
    def __init__(self,DB_FILE):
        FILE_PATH = DB_FILE
        self.con = sqlite3.connect(FILE_PATH)
        self.cursor = self.con.cursor()


    def create_table(self,TABLE_NAME,VALUE_LIST):
        """
        :param TABLE_NAME: 创建的表名称
        :param VALUE_LIST: 所有的type均为text 需为一个列表
        :return:
        """
        try:
            text = ''
            for i in VALUE_LIST:
                value = str(i) + ' text,'
                text += value
            text = text[:-1]
            sql = f"CREATE TABLE {TABLE_NAME}({text})"
            self.cursor.execute(sql)
            return True
        except:
            return False


    def insert_row(self,TABLE_NAME,VALUE_LIST):
        """
        :param TABLE_NAME: 插入值的table名称
        :param VALUE_LIST:必须为表格且与type一致
        :return:只能整行插入而不能单个插入
        """
        list_ziduan = []
        keys1 = ''
        keys2 = ''
        self.cursor.execute(f'PRAGMA table_info({TABLE_NAME})')
        values1 = self.cursor.fetchall()
        for value1 in values1:
            list_ziduan.append(value1[1])
        for ziduan in list_ziduan:
            keys1 += ziduan + ','
        keys1 = keys1[:-1]
        for l1 in VALUE_LIST:
            keys2 += '"' + l1 + '"' + ','
        keys2 = keys2[:-1]
        sql = f'insert into {TABLE_NAME}({keys1})values({keys2})'
        self.cursor.execute(sql)
        self.con.commit()


    def select_all(self,TABLE_NAME):
        """
        将从数据库中拿取该表的所有数据
        :param TABLE_NAME:
        :return: 元组集 返回的是列表 [(  ), (  )]
        """
        sql = f'select * from {TABLE_NAME}'
        self.cursor.execute(sql)
        value = self.cursor.fetchall()
        return value


    def delete_by_tag(self,TABLE_NAME,TAG_NAME,TAG_VALUE):
        """
        根据tag_name来删除所有tag_value所在的某一行数据
        当有多个tag_name的值为tag_value时 将会删除所有的相关数据
        :param TABLE_NAME:
        :param TAG_NAME: 所需删除的type值
        :param TAG_VALUE: 所对应某一行的数据值
        :return: None
        """
        sql = f'delete from {TABLE_NAME} where {TAG_NAME} = "{TAG_VALUE}"'
        self.cursor.execute(sql)
        self.con.commit()

    def search_by_tag(self,TABLE_NAME,TAG_NAME,TAG_VALUE):
        """
        获取tag_name为tag_value的某一行数据
        当有多行数据的tag_name的值相同时返回的将是元组集包含在列表中
        :param TABLE_NAME:
        :param TAG_NAME: 所需tag名
        :param TAG_VALUE: tag值
        :return: 返回的是元组集包含在列表中 [ (  ) , (  ) ]
        """
        sql = f'select * from {TABLE_NAME} where {TAG_NAME}="{TAG_VALUE}"'
        self.cursor.execute(sql)
        value = self.cursor.fetchall()
        return value

    def update_by_name(self,TABLE_NAME,TARGET_NAME,CHANGED_TAG,TARGET_VALUE,CHANGED_VALUE):
        """
        根据tag替换某一个数据值
        如果有多行数据一样，将会更改所有满足条件的数据
        :param TABLE_NAME:
        :param TARGET_NAME: 参照tag名称
        :param CHANGED_TAG: 需要更改的tag名称
        :param TARGET_VALUE: 参照tag值
        :param CHANGED_VALUE: 需要更改的tag值
        :return: None
        """
        sql = f'update {TABLE_NAME} set {CHANGED_TAG} = "{CHANGED_VALUE}" where {TARGET_NAME} = "{TARGET_VALUE}"'
        self.cursor.execute(sql)
        self.con.commit()
