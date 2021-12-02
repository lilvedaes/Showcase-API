from imdb import IMDb
from mysql_insertion import add_skill, add_social, add_credit, create_user
from objects import DBUser, Credit
import random

i = IMDb()
skills = ["Martial arts", "Aerobics", "Pilot", "Rock climbing", "Shooting", "Swimming", "Fencing", "Skateboarding", "Boxing", "Golf", "Tennis", "Cheerleading", "Surfing", "Trampoline"]

def create_user_from_imdb (app, person_id, pronoun_id = 4, title = "Actor"):
    '''
    pronoun_id: 2 - she/her, 3 - he/him, 4 - they/them, etc
    title: e.g. Actor, Director, and Film Enthusiast 
    '''
    # need: first, last, profile_image_url, location, title, pronoun_id, gender, union_status_id
    weight = random.randint(70, 110)
    eye_color = 'brown'
    hair_color = 'brown'
    
    p = i.get_person(str(person_id))
    data = p.data
    
    age = 2021 - int(p['birth date'][:4])

    first_name = p['canonical name'].split(',')[1]
    last_name = p['canonical name'].split(',')[0]
    profile_image_url = data['headshot']
    location = data['birth info']['birth place']
    height = data['height']
    title = title
    pronoun_id = 3 if 'actor' in p['filmography'].keys() else pronoun_id
    pronoun_id = 2 if 'actress' in p['filmography'].keys() else pronoun_id
    gender = ''
    age_range_start = age - 5
    age_range_end = age + 5
    about_info = data['mini biography'][0]

    user = DBUser(None, first_name, last_name, profile_image_url, location, title, pronoun_id, gender, 1, height, weight, eye_color, hair_color, age_range_start, age_range_end, about_info)
    create_user(app, user)
    credits = []
    max = 4

    actor = 'actor' if 'actor' in p['filmography'].keys() else 'actress'
    filmography_options = [actor, 'director', 'writer', 'producer']
    for option in filmography_options:
        count = 0
        if (option not in p['filmography'].keys()): continue
        for credit in p['filmography'][option]:
            if ('status' not in credit.keys() or credit['status'] != 'post-production' or credit._Container__role == None): continue
            m = i.get_movie(credit.movieID)
            production_name = credit['title']
            role = credit._Container__role[0]['name']
            start_date = '' if 'year' not in credit.keys() else credit['year']
            end_date = ''
            src_type = 'image' if 'cover url' in m.keys() else None # or 'video' or None
            src_url = m['cover url'] if 'cover url' in m.keys() else None
            # print(credit['kind'], credit['kind'].capitalize())
            production_type = credit['kind'].capitalize()
            director = m['director'][0]['name'] if 'director' in m.keys() and len(m['director']) > 0 else None
            producer = m['producers'][0]['name'] if 'producers' in m.keys() and len(m['producers']) > 0 else None
            production_link = None
            description = option.capitalize() + ' role in ' + production_name
            credit = Credit(user.user_id, production_name, role, start_date, end_date, src_type, src_url, production_type, director, producer, production_link, description)
            credits.append(credit)
            count += 1
            if (count > max): break

    for credit in credits:
        add_credit(app, credit)
    # add user and credits to database
    add_social(app, user.user_id, 'IMDb', 'https://www.imdb.com/name/nm' + p['imdbID'])
    for skill in list(set(random.choices(skills, k=3))):
        add_skill(app, user.user_id, skill)
    return True
