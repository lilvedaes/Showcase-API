pronouns_table_command = '''CREATE TABLE IF NOT EXISTS pronouns(
    pronoun_id INT NOT NULL AUTO_INCREMENT,
    pronoun_set VARCHAR(20),
    PRIMARY KEY (pronoun_id)
);'''
pronouns_insert_command = '''REPLACE INTO pronouns
        (pronoun_id, pronoun_set)
    VALUES
        (1, "other"),
        (2, "she/her"),
        (3, "he/him"),
        (4, "they/them"),
        (5, "ve/ver"),
        (6, "xe/xem");'''

union_status_table_command = '''CREATE TABLE IF NOT EXISTS union_statuses(
    union_status_id INT NOT NULL AUTO_INCREMENT,
    union_status VARCHAR(20),
    PRIMARY KEY (union_status_id)
);'''
union_insert_command = '''REPLACE INTO union_statuses
        (union_status_id, union_status)
    VALUES
        (1, "other"),
        (2, "union"),
        (3, "non-union");'''

users_table_command = '''CREATE TABLE IF NOT EXISTS users(
    user_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    profile_image_url VARCHAR(200),
    location VARCHAR(50),
    title VARCHAR(100),
    pronoun_id INT,
    gender VARCHAR(50),
    union_status_id INT,
    height VARCHAR(20),
    weight VARCHAR(20),
    eye_colour VARCHAR(20),
    hair_colour VARCHAR(20),
    age_range_start INT,
    age_range_end INT,
    about_info VARCHAR(1500),
    FOREIGN KEY(pronoun_id) REFERENCES pronouns(pronoun_id),
    FOREIGN KEY(union_status_id) REFERENCES union_statuses(union_status_id),
    PRIMARY KEY (user_id)
);'''

production_type_table_command = '''CREATE TABLE IF NOT EXISTS production_types(
    production_type_id INT NOT NULL AUTO_INCREMENT,
    production_type VARCHAR(100) NOT NULL,
    PRIMARY KEY (production_type_id)
);'''
production_type_insert_command = '''REPLACE INTO production_types
        (production_type_id, production_type)
    VALUES
        (1, "other"),
        (2, "play"),
        (3, "musical"),
        (4, "short film"),
        (5, "feature film"),
        (6, "solo theatre"),
        (7, "audiobook"),
        (8, "TV show");'''

credits_table_command = '''CREATE TABLE IF NOT EXISTS credits(
    user_id INT NOT NULL,
    production_name VARCHAR(100) NOT NULL,
    role VARCHAR (100) NOT NULL,
    start_date VARCHAR(50) NOT NULL,
    end_date VARCHAR(50),
    src_type VARCHAR (50),
    src_url VARCHAR (200),
    production_type VARCHAR(50) NOT NULL,
    director VARCHAR(100),
    producer VARCHAR(100),
    production_link VARCHAR(200),
    description VARCHAR(500) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    PRIMARY KEY(user_id, production_name, role, start_date, end_date)
);'''


ethnicities_table_command = '''CREATE TABLE IF NOT EXISTS ethnicities(
    ethnicity_id INT NOT NULL AUTO_INCREMENT,
    ethnicity VARCHAR (50) NOT NULL,
    PRIMARY KEY (ethnicity_id)
);'''
ethnicities_insert_command = '''REPLACE INTO ethnicities
        (ethnicity_id, ethnicity)
    VALUES
        (1, "other"),
        (2, "Hispanic/Latino"),
        (3, "Asian"),
        (4, "Black/African American"),
        (5, "White"),
        (6, "Native Hawaiian or Other Pacific Islander"),
        (7, "Indian"),
        (8, "Native American");'''

user_ethnicities_table_command = '''CREATE TABLE IF NOT EXISTS user_ethnicities(
    user_id INT NOT NULL,
    ethnicity_id INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(ethnicity_id) REFERENCES ethnicities(ethnicity_id),
    PRIMARY KEY (user_id, ethnicity_id)
);'''

connections_table_command = '''CREATE TABLE IF NOT EXISTS connections(
    user_id1 INT NOT NULL,
    user_id2 INT NOT NULL,
    connection_date DATE NOT NULL,
    PRIMARY KEY (user_id1, user_id2)
);'''

post_types_table_command = '''CREATE TABLE IF NOT EXISTS post_types(
    post_type_id INT NOT NULL,
    post_type VARCHAR (50) NOT NULL,
    PRIMARY KEY (post_type_id)
);'''

post_types_insert_command = '''REPLACE INTO post_types
        (post_type_id, post_type)
    VALUES
        (1, "Text"),
        (2, "Video"),
        (3, "Image"),
        (4, "Audio"),
        (5, "File");'''

posts_table_command = '''CREATE TABLE IF NOT EXISTS posts(
    post_id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    post_type_id INT,
    posted_date VARCHAR(30) NOT NULL,
    caption VARCHAR(500),
    likes INT,
    media_url VARCHAR(1000),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(post_type_id) REFERENCES post_types(post_type_id),
    PRIMARY KEY (post_id)
);'''

comments_table_command = '''CREATE TABLE IF NOT EXISTS comments(
    comment_id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    post_id INT,
    comment_date DATE NOT NULL,
    comment VARCHAR(500),
    likes INT,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(post_id) REFERENCES posts(post_id),
    PRIMARY KEY (comment_id)
);'''
demo_reels_table_command = '''CREATE TABLE IF NOT EXISTS demo_reels(
    user_id INT NOT NULL,
    title VARCHAR(100),
    src_url VARCHAR(500) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    PRIMARY KEY (user_id, src_url)
);'''

socials_table_command = '''CREATE TABLE IF NOT EXISTS socials(
    label VARCHAR(50) NOT NULL,
    icon VARCHAR(50) NOT NULL,
    PRIMARY KEY (label)
);'''
socials_insert_command = '''REPLACE INTO socials
        (label, icon)
    VALUES
        ("other", ""),
        ("IMDb", "fab fa-imdb"),
        ("Instagram", "fab fa-instagram"),
        ("YouTube", "fab fa-youtube"),
        ("Facebook", "fab fa-facebook"),
        ("Twitter", "fab fa-twitter"),
        ("Snapchat", "fab fa-snapchat"),
        ("TikTok", "fab fa-tiktok"),
        ("Website", ""),
        ("Backstage", ""),
        ("Actors Access", "");'''

user_socials_table_command = '''CREATE TABLE IF NOT EXISTS user_socials(
    user_id INT NOT NULL,
    label VARCHAR(50) NOT NULL,
    social_link VARCHAR(200) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(label) REFERENCES socials(label),
    PRIMARY KEY (user_id, social_link)
);'''

skills_table_command = '''CREATE TABLE IF NOT EXISTS skills(
    user_id INT NOT NULL,
    skill VARCHAR(100) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    PRIMARY KEY (user_id, skill)
);'''

education_table_command = '''CREATE TABLE IF NOT EXISTS education(
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    start_date VARCHAR(50) NOT NULL,
    end_date VARCHAR(50),
    institution VARCHAR(150) NOT NULL,
    institution_logo_url VARCHAR(200),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    PRIMARY KEY (user_id, title, institution)
);'''

connection_requests_table_command = '''CREATE TABLE IF NOT EXISTS connection_requests(
    user_id INT NOT NULL,
    user_requested VARCHAR(100) NOT NULL,
    request_date VARCHAR(50) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    PRIMARY KEY (user_id, user_requested)
);'''

headshots_table_command = '''CREATE TABLE IF NOT EXISTS headshots(
    user_id INT NOT NULL,
    headshot_url VARCHAR(100) NOT NULL,
    priority INT,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    PRIMARY KEY (user_id, headshot_url)
);'''

messages_table_command = '''CREATE TABLE IF NOT EXISTS messages(
    user_from INT NOT NULL,
    user_to INT NOT NULL,
    time_sent VARCHAR(100) NOT NULL,
    time_recieved VARCHAR(100),
    msg MEDIUMTEXT NOT NULL,
    FOREIGN KEY(user_from) REFERENCES users(user_id),
    FOREIGN KEY(user_to) REFERENCES users(user_id),
    PRIMARY KEY(user_from, user_to, time_sent)
);'''

likes_table_command = '''CREATE TABLE IF NOT EXISTS likes(
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    time_liked VARCHAR(100) NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(post_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    PRIMARY KEY(post_id, user_id)
);'''

comment_likes_table_command = '''CREATE TABLE IF NOT EXISTS comment_likes(
    post_id INT NOT NULL,
    comment_id INT NOT NULL,
    user_id INT NOT NULL,
    time_liked VARCHAR(100) NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(post_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(comment_id) REFERENCES comments(comment_id),
    PRIMARY KEY(post_id, user_id)
);'''
