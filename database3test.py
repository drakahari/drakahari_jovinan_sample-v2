from sqlalchemy import create_engine, text

# Replace with your actual connection string
db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string)

# Open a connection
with engine.connect() as connection:
    # Execute a simple query
    result = connection.execute(text("SELECT * FROM jobs"))

    # Fetch all rows from the result
    rows = result.fetchall()

    # Print each row
    for row in rows:
        print(row)