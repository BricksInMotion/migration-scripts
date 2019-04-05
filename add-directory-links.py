import records


# Fill these in with proper credentials
DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_DBNAME = ""

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
    # Start by getting all releases topics before
    # the directory was modified to add the link
    # directly to the post
    print("Getting topic info...")
    film_topics = tx.query("""
    SELECT ft.film_id, fp.id AS post_id, fp.message, ft.id AS topic_id
    FROM forums_topics ft JOIN forums_posts fp
        ON ft.id = fp.topic_id
    WHERE ft.forum_id = 3  /* this must be in the releases category */
        AND ft.film_id IS NOT NULL  /* this must be a film, not a trailer or normal topic */
        AND ft.id < 26111  /* don't get topics with link in it already */
        AND ft.first_post_id = fp.id  /* only get op */
        AND fp.poster_id != 140674  /* take out Mouldy */
    ORDER BY fp.id DESC  /* newest films first */
    LIMIT 1000;  /* there's over 9000 rows, only do 1000 at a time */
        """)
    for topic in film_topics:
        print(f"\nCurrent topic: {topic.topic_id}")

        # Build a link to the directory page
        # and add it to the existing topic content
        dir_link = "[url=https://bricksinmotion.com/films/view/{}]Directory Link[/url]\n\n".format(
            topic.film_id
        )
        new_msg = f"{dir_link}{topic.message}"

        # Taking the post OP ID, go to the posts table
        # and replace the content with our revised version
        print("Updating OP with directory link...")
        tx.query("""
UPDATE `forums_posts`
SET `message` = :new_message
WHERE `id` = :post_id""",
                 new_message=new_msg,
                 post_id=topic.post_id)

    print("Successfully added directory links into posts")
