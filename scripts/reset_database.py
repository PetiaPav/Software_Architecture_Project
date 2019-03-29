import sys

from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'soen344'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ubersante'
app.config['MYSQL_DATABASE_DB'] = 'ubersante'
app.config['MYSQL_DATABASE_HOST'] = 'mydbinst.ccaem9daeat5.us-east-2.rds.amazonaws.com'

if len(sys.argv) > 1:
    if sys.argv[1] == 'test':
        app.config['MYSQL_DATABASE_DB'] = 'ubersante_test'

mysql.init_app(app)
connection = mysql.connect()
c = connection.cursor()

fd = open('../sql/db_structure.sql', 'r')
sqlFile = fd.read()
fd.close()

fl = open('../sql/db_data.sql', 'r')
sqlFile2 = fl.read()
fl.close()

# all SQL commands (split on ';')
sqlCommands = sqlFile.split(';')
sqlCommands2 = sqlFile2.split(';')

# Execute every command from the input file
print('Reseting table structures...')
for command in sqlCommands:
    # This will skip and report errors
    try:
        c.execute(command)
    except:
        if command != '':
            print(command)
            print('Command skipped')

print('Repopulating tables...')
for command in sqlCommands2:
    # This will skip and report errors
    try:
        c.execute(command)
    except:
        if command == '':
            print(command)
            print('Command skipped')
connection.commit()
c.close()
print('All tables reset and repopulated')
        
