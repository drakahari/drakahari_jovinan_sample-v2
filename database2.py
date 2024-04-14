import mysql.connector


conn = mysql.connector.connect(
  user='drak',
  password='Thispassword!!',
  database='drakaharicareers',
  host='drakahari.mysql.database.azure.com',
  ssl_ca='/var/www/html/DigiCertGlobalRootCA.crt.pem'

)

print(conn)