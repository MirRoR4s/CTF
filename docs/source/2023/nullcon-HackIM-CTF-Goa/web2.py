import sqlite3

# 连接到数据库
conn = sqlite3.connect('database.db')

# 创建游标对象
cursor = conn.cursor()

# 执行查询语句
cursor.execute("SELECT * FROM users")  # 替换table_name为实际表的名称

# 获取所有查询结果
results = cursor.fetchall()

# 遍历结果
for row in results:
    print(row)

# 关闭游标和连接
cursor.close()
conn.close()
