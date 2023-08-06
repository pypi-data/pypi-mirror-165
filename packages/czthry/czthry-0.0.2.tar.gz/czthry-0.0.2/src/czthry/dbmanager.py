from sqlalchemy import create_engine
from sqlalchemy import text
from urllib.parse import quote_plus as urlquote


# 数据已存在时的操作
ea_ignore = 'ignore'
ea_replace = 'replace'


class DBManager(object):
    def __init__(self, connstr):
        self.engine = create_engine(connstr, echo=False, encoding='utf8')

    def insert(self, table, data, exist_action=ea_ignore):
        """
        :param table: 表名
        :param data: 数据
            dict 类型 是一条数据，key就是字段名，所以 key 很重要
            list 类型 是N条数据，是dict类型的数组，最终会转换成元组，批量执行
        :param exist_action:
            如果此条数据已存在，采取何种方式去插入：
                ignore: 'insert ignore into ...' 此次插入不执行
                replace: 'replace into ...' 替换现有记录（先delete 后insert。id会自增，不同于update）
                其他: 'insert into...' 直接插入。如果没有唯一索引，就会重复插入
        :return:

        """
        if not data:
            return None
        if type(data) == list:
            if len(data) == 0:
                return None
            keys = list(data[0].keys())
        else:
            keys = list(data.keys())
        fields = ','.join(keys)  # 使用data的keys作为字段名
        pre_values = ','.join([':%s' % k for k in keys])  # 前缀加":"
        if exist_action == ea_replace:
            pre_sql = 'replace into %s (%s) values(%s)' % (table, fields, pre_values)
        elif exist_action == ea_ignore:
            pre_sql = 'insert ignore into %s (%s) values(%s)' % (table, fields, pre_values)
        else:
            pre_sql = 'insert into %s (%s) values(%s)' % (table, fields, pre_values)
        session = None
        bind_sql = None
        try:
            bind_sql = text(pre_sql)
            session = self.engine.connect()
            if type(data) == list:
                resproxy = session.execute(bind_sql, *data)  # 对于数组，批量执行，效率非常高
            else:
                resproxy = session.execute(bind_sql, data)
            return resproxy
        except Exception as e:
            if bind_sql:
                self.engine.logger.error('插入insert操作（%s）发生错误：%s' % (bind_sql, e))
            return None
        finally:
            if session:
                session.close()

    def execute(self, sql):
        session = None
        try:
            session = self.engine.connect()
            result = session.execute(sql)
            hasResult = 'select' in sql.lower()
            if hasResult:
                rows = result.fetchall()
                return rows
        except Exception as e:
            self.engine.logger.error('执行sql语句（%s）发生错误：%s' % (sql, e))
            return None
        finally:
            if session:
                session.close()

    def exists(self, table, fields, data):
        condition = ''
        if fields:
            fmt = ' and '.join([f'{f}="%({f})s"' for f in fields])
            condition = 'where ' + fmt % data
        sql = f'select * from {table} {condition} limit 1'
        try:
            result = self.execute(sql)
            count = len(result)
            return count > 0
        except Exception as e:
            self.engine.logger.error('查询exists发生错误：%s' % e)
            return None

    def close(self):
        self.engine.dispose()


if __name__ == '__main__':
    # print(ea_ignore)
    pass
