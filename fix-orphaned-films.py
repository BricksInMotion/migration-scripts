import records


# Fill these in with proper credentials
DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_DBNAME = ""
OP_USER_ID = 141084

# Connect to the database
print("Connecting to database...")
conn_str = "mysql+pymysql://{}:{}@{}/{}".format(
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOST,
    DB_DBNAME
)
db = records.Database(conn_str)

with db.transaction() as tx:
    # Start by getting the films whose directors don't exist as forum users
    print("Getting orphaned films...")
    orphaned_films = tx.query("""
    SELECT id
    FROM films
    WHERE id NOT IN (
        SELECT films.id
        FROM films
        INNER JOIN forums_users ON films.user_id = forums_users.id
    )
    ORDER BY id
    """)
    for film in orphaned_films:
        # Reassign the films to Mouldy
        tx.query("""
        UPDATE films
        SET user_id = :mouldy
        WHERE id = :film_id
        """,
                 mouldy=OP_USER_ID,
                 film_id=film.id)
        print(f"Film {film.id} reassigned to user ID {OP_USER_ID}")

    print("Successfully reassigned director for orphaned films")
