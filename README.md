Dormitory Management System (CLI)
===

## Install & Dependence
- pyfingerprint
```
pip install pyfingerprint
```
- pymysql
```
pip install pymysql
```
- Change the connection config inside main function
```
connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='test',
        cursorclass=pymysql.cursors.DictCursor
    )
```