# Python3 + SQLAlchemy + Sqlite3 實現 ORM 教程
# 參考網站
# https://www.cnblogs.com/lsdb/p/9835894.html
# https://www.itread01.com/content/1546084449.html
# https://codertw.com/%E8%B3%87%E6%96%99%E5%BA%AB/10142/

# How to install sqlalchemy?
# Type these words in ternimal
# >>> pip install sqlalchemy

# Sqlite3 是 Python3 標準庫不需要另外安裝，只需要安裝 SQLAlchemy 即可

# How to check to version of the sqlalchemy?
# type python3 in terminal
# >>> import sqlalchemy
# >>> sqlalchemy.__version__ 
# '1.4.15'
# >>> quit()

# 建立數據庫連接本文中有時會稱為「建立數據庫引擎」

# 以相對路徑形式，建立資料庫：
# 在當前目錄下創建數據庫格式如下：
# engine = create_engine('sqlite:///database.db')
# 在當前目錄下的目錄創建數據庫格式如下：
# engine = create_engine('sqlite:////fold/database.db')

# 創建資料庫連接
# 在當前位置創建資料庫為例，資料庫名稱：test.db
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db?check_same_thread=False', echo=True)
# 在 create_engine 中多了兩樣東西
# 一個是check_same_thread=False
# 一個是echo=Ture
# echo 默認為 False，表示不打印執行的 SQL 語句等較詳細的執行信息，改為 Ture 表示讓其打印
# 由於 sqlite 默認建立的對像只能讓建立該對象的線程使用
# 而 sqlalchemy 是多線程的所以我們需要指定 check_same_thread=False 來讓建立的對象任意線程都可使用，否則不時就會報錯

# 繫結元資訊
from sqlalchemy import MetaData
metadata = MetaData(engine)

# 建立表格，初始化資料庫
# 建立 table 名稱為 test_user
from sqlalchemy import Table, Column, Integer, String
user = Table('test_user', metadata,
    Column('id', Integer, primary_key = True),
    Column('first_name', String(40)),
    Column('second_name', String(40)))

# 建立資料庫檔案，如果檔案存在則系統會自動忽視
# 檔案名稱為 test.db
metadata.create_all(engine)

# ===============================================================
# 到目前為止，在 terminal 執行 python3 test.py 後會得到
# 2021-07-23 12:55:21,823 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2021-07-23 12:55:21,824 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("test_user")
# 2021-07-23 12:55:21,824 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2021-07-23 12:55:21,826 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("test_user")
# 2021-07-23 12:55:21,826 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2021-07-23 12:55:21,826 INFO sqlalchemy.engine.Engine 
# CREATE TABLE test_user (
#         id INTEGER NOT NULL, 
#         first_name VARCHAR(40), 
#         second_name VARCHAR(40), 
#         PRIMARY KEY (id)
# )
#
#
# 2021-07-23 12:55:21,826 INFO sqlalchemy.engine.Engine [no key 0.00005s] ()
# 2021-07-23 12:55:21,828 INFO sqlalchemy.engine.Engine COMMIT
# ===============================================================

# 先建立基本映射類(class)，後邊真正的映射類都要繼承它
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
# 定義映射類 User，其繼承上一步創建的 Base
class TestUser(Base):
    # 指定本類映射到 users 表格(table)
    __tablename__ = 'test_user'
    # 如果有多個類指向同一張表格，那麼在後面的類需要把 extend_existing 設成 True，表示在已有列基礎上進行擴展
    # 或者换句话说，sqlalchemy 允許類是表的字集
    # __table_args__ = {'extend_existing': True}
    # 如果表在同一個數據庫服務（datebase）的不同數據庫中（schema），可使用 schema 參數近一步指定數據庫
    # __table_args__ = {'schema': 'test_database'}
    
    # 個變量名一定要與表格的各字段名一样，因為相同的名字是他们之間的唯一關聯關係
    # 從語法上來說，個變量類型和表格的類型可以不完全一致，如表格字段是 String(40)，這裡可改定義為 String(20)
    # 但為了避免造成不必要的錯誤，變量的类類型和其對應的表格的字段的類型還是要一致
    # sqlalchemy 强制要求必須要有主鍵字段不然會報錯，如果要映射一張已存在且没有主鍵的表格，那麼可行的做法是將所有字段都設為 primary_key=True
    # 不要看隨便將一個非主鍵字段設為 primary_key，然後似乎就沒抱錯就能使用了，sqlalchemy 在接收到查詢結果後還會自己根據主鍵進行一次去重
    # 指定 id 映射到 id 字段; id 字段為整型，為主鍵，自動增長（其實整型主鍵默認就自動增長）
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定 name 映射到 name 字段; name 字段為字符串類型
    first_name = Column(String(40))
    second_name = Column(String(40))

    def __init__(self, first_name, second_name):
        self.first_name = first_name
        self.second_name = second_name

# 建立對話
from sqlalchemy.orm import sessionmaker
# 這裡的 engine 就是創建資料庫連接時的 engine
Session = sessionmaker(bind=engine)
# 建立類實例
session01 = Session()

# # CRUD's Create 增查改刪 的 增
# # 運用 class 來新增 records
# # Add one record
# iteam01 = TestUser('Tom', 'Smith')
# session01.add(iteam01)
# session01.commit()
# session01.close()

# # Add many records
# session02 = Session()
# session02.add_all(
#     [TestUser('Wendy', 'Williams'),
#     TestUser('Mary', 'Contrary'),
#     TestUser('Fred', 'Flinstone')]
# )
# session02.commit()
# session02.close()

# ===============================================================
# 2021-07-23 13:25:34,645 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2021-07-23 13:25:34,645 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("test_user")
# 2021-07-23 13:25:34,645 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2021-07-23 13:25:34,647 INFO sqlalchemy.engine.Engine COMMIT
# 2021-07-23 13:25:34,679 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2021-07-23 13:25:34,680 INFO sqlalchemy.engine.Engine INSERT INTO test_user (first_name, second_name) VALUES (?, ?)
# 2021-07-23 13:25:34,681 INFO sqlalchemy.engine.Engine [generated in 0.00009s] ('Tom', 'Smith')
# 2021-07-23 13:25:34,682 INFO sqlalchemy.engine.Engine COMMIT
# 2021-07-23 13:25:34,683 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2021-07-23 13:25:34,683 INFO sqlalchemy.engine.Engine INSERT INTO test_user (first_name, second_name) VALUES (?, ?)
# 2021-07-23 13:25:34,684 INFO sqlalchemy.engine.Engine [cached since 0.003263s ago] ('Wendy', 'Williams')
# 2021-07-23 13:25:34,684 INFO sqlalchemy.engine.Engine INSERT INTO test_user (first_name, second_name) VALUES (?, ?)
# 2021-07-23 13:25:34,684 INFO sqlalchemy.engine.Engine [cached since 0.003839s ago] ('Mary', 'Contrary')
# 2021-07-23 13:25:34,684 INFO sqlalchemy.engine.Engine INSERT INTO test_user (first_name, second_name) VALUES (?, ?)
# 2021-07-23 13:25:34,684 INFO sqlalchemy.engine.Engine [cached since 0.003945s ago] ('Fred', 'Flinstone')
# 2021-07-23 13:25:34,684 INFO sqlalchemy.engine.Engine COMMIT
# ===============================================================

# CRUD's Read 增查改刪 的 查
# Query records by filter
session02 = Session()
data01 = session02.query(TestUser).filter(TestUser.id > 2).all()
for i in range(len(data01)):
    print(data01[i].id, ' ', data01[i].first_name, data01[i].second_name)
session01.close()
# 3   Mary Contrary
# 4   Fred Flinstone

# Query all records
# 方法ㄧ
session03 = Session()
data02 = session03.query(TestUser).all()
for i in range(len(data02)):
    print(data02[i].id, ' ', data02[i].first_name, data02[i].second_name)
session03.close()
# 1   Tom Smith
# 2   Wendy Williams
# 3   Mary Contrary
# 4   Fred Flinstone

# 方法二
session03 = Session()
data03 = session03.query(TestUser.id, TestUser.first_name, TestUser.second_name).all()
print(data03)
# [(1, 'Tom', 'Smith'), (2, 'Wendy', 'Williams'), (3, 'Mary', 'Contrary'), (4, 'Fred', 'Flinstone')]
for i in range(len(data03)):
    print(data03[i])
# (1, 'Tom', 'Smith')
# (2, 'Wendy', 'Williams')
# (3, 'Mary', 'Contrary')
# (4, 'Fred', 'Flinstone')

# 特定查詢 ==
# 方法一
session04 = Session()
data04 = session04.query(TestUser).filter(TestUser.first_name == 'Mary').all()
print(data04[0].id, ' ', data04[0].first_name, data04[0].second_name)
session04.close()
# 3   Mary Contrary

# 方法二
session04 = Session()
data042 = session04.query(TestUser).filter(TestUser.id == 4).first()
print(data042.id, ' ', data042.first_name, data042.second_name)
session04.close()
# 4   Fred Flinstone

# 模糊查詢 .like
session05 = Session()
data05 = session05.query(TestUser).filter(TestUser.first_name.like('T%')).all()
for i in range(len(data05)):
    print(data05[i].id, ' ', data05[i].first_name, data05[i].second_name)
session05.close()
# 1   Tom Smith

# 多條件查詢 .filter().filter()
session06 = Session()
data06 = session06.query(TestUser).filter(TestUser.id > 1).filter(TestUser.id < 4).all()
for i in range(len(data06)):
    print(data06[i].id, ' ', data06[i].first_name, data06[i].second_name)
session06.close()
# 2   Wendy Williams
# 3   Mary Contrary

# 多條件查詢 and_ or_
from sqlalchemy import and_, or_
session07 = Session()
data07 = session06.query(TestUser).filter(and_(TestUser.id > 1, TestUser.first_name.like('%e%'))).all()
for i in range(len(data07)):
    print(data07[i].id, ' ', data07[i].first_name, data07[i].second_name)
session07.close()
# 2   Wendy Williams
# 4   Fred Flinstone

# CRUD's Update 增查改刪 的 改
# 方法一
# 修改 id == 1 使用者的 first_name
session08 = Session()
data08 = session08.query(TestUser).filter(TestUser.id == 1).update({TestUser.first_name: 'Jerry'})
session08.commit()
data08 = session08.query(TestUser).all()
for i in range(len(data08)):
    print(data08[i].id, ' ', data08[i].first_name, data08[i].second_name)
session08.close()
# 1   Jerry Smith       <------ 由 Tom Smith 變成 Jerry Smith
# 2   Wendy Williams
# 3   Mary Contrary
# 4   Fred Flinstone

# 方法二
# 修改 id == 2 使用者的 first_name
session09 = Session()
data09 = session09.query(TestUser).filter(TestUser.id == 2).first()
data09.first_name = 'Cathy'
session09.commit()
data09 = session09.query(TestUser).all()
for i in range(len(data09)):
    print(data09[i].id, ' ', data09[i].first_name, data09[i].second_name)
session09.close()

# CRUD's Update 增查改刪 的 刪
# 為避免資料庫出錯誤，先增加一個 record 來刪除
session10 = Session()
iteam02 = TestUser('Bob', 'Takahashi')
session10.add(iteam02)
session10.commit()
# .delete
session10.query(TestUser).filter(TestUser.first_name == 'Bob').delete()
session10.commit()
session10.close()

# 統計數量
# .count()
session11 = Session()
data11 = session11.query(TestUser).filter(TestUser.second_name.like('%i%')).count()
print(data11)
session11.close()
# 3
