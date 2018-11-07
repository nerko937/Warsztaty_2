from models import create_connection, close_connection
from models.parser import run


(cnx, cursor) = create_connection()

run(cursor)

close_connection(cnx, cursor)
