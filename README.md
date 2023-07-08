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
- Change the connection config inside main() function
```
connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='test',
        cursorclass=pymysql.cursors.DictCursor
    )
```
- Replace 'COM3' with the actual port name you found in Device Manager (Inside initialize_scanner() function)
```
f = pyfp.PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)
```