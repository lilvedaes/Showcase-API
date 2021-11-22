import re


class User:
    connection_dist = -1

    def __init__(self, user_id: int, first_name: str, last_name: str, profile_image_url: str,
                 location: str, title: str, pronoun: str, gender: str, union_status: str,
                 height: int, weight: int, eye_colour: str, hair_colour: str, age_range_start: int,
                 age_range_end: int, about_info: str):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.profile_image_url = profile_image_url
        self.location = location
        self.title = title
        self.pronoun = pronoun
        self.gender = gender
        self.union_status = union_status
        self.height = height
        self.weight = weight
        self.eye_colour = eye_colour
        self.hair_colour = hair_colour
        self.age_range_start = age_range_start
        self.age_range_end = age_range_end
        self.about_info = about_info

    def get_values(self):
        # Used for insertion into MySQL database
        return (self.user_id, self.first_name, self.last_name, self.profile_image_url,
        self.location, self.title, self.pronoun, self.gender, self.union_status,
        self.height, self.weight, self.eye_colour, self.hair_colour, self.age_range_start,
        self.age_range_end, self.about_info)
    
    def get_connection_dist(self):
        return self.connection_dist

class DBUser:
    def __init__(self, user_id: int, first_name: str, last_name: str, profile_image_url: str,
                 location: str, title: str, pronoun_id: int, gender: str, union_status_id: int,
                 height: int, weight: int, eye_colour: str, hair_colour: str, age_range_start: int,
                 age_range_end: int, about_info: str):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.profile_image_url = profile_image_url
        self.location = location
        self.title = title
        self.pronoun_id = pronoun_id
        self.gender = gender
        self.union_status_id = union_status_id
        self.height = height
        self.weight = weight
        self.eye_colour = eye_colour
        self.hair_colour = hair_colour
        self.age_range_start = age_range_start
        self.age_range_end = age_range_end
        self.about_info = about_info

    def get_values(self):
        # Used for insertion into MySQL database
        return (self.user_id, self.first_name, self.last_name, self.profile_image_url,
                self.location, self.title, self.pronoun_id, self.gender, self.union_status_id,
                self.height, self.weight, self.eye_colour, self.hair_colour, self.age_range_start,
                self.age_range_end, self.about_info)

    def get_connection_dist(self):
        return self.connection_dist


class Network_Filter:
    def __init__(self, user_id, professions, connection_dists, locations, genders, age, skills, languages, union_statuses):
        self.user_id = user_id
        self.professions = professions
        self.connection_dists = connection_dists
        self.locations = locations
        self.genders = genders

        self.age = age if age != None else "0-300"
        self.start_age = int(re.search(r'^(\d+)', self.age).group(1))
        self.end_age = re.search(r'(\d+)$', self.age).group(1)
        self.end_age = 300 if self.end_age == '' else int(self.end_age)
        self.skills = skills
        self.languages = languages
        self.union_statuses = union_statuses


    def user_applicable(self, user: User, connection_dist):
        if ((self.professions != None and all([p.lower() not in user.title.lower() for p in self.professions])) or
                (self.connection_dists != None and all([cd <= connection_dist for cd in self.connection_dists])) or
                (self.genders != None and all([user.gender.lower() != g.lower() for g in self.genders])) or
                # (self.union_status != None and self.union user.union_status_id) or # TODO: get union status from user's union status id
                # (self.skills != None and all([s in user.skills for s in self.skills])) # TODO: save user skills
                (self.locations != None and all([l.lower() not in user.location.lower() for l in self.locations])) or
                (self.age != None and (user.age_range_end < self.start_age or self.end_age < user.age_range_start))
        ):
            return False

        return True


class Post:
    def __init__(self, post_id: int, user_id: int, post_type_id: id, posted_date: str, caption: str,
                 likes: int, media_url: str):
        self.post_id = post_id
        self.user_id = user_id
        self.post_type_id = post_type_id
        self.posted_date = posted_date
        self.caption = caption
        self.likes = likes
        self.media_url = media_url


class Comment:
    def __init__(self, comment_id: int, user_id: int, post_id: id, comment_date: str, comment: str, likes: int):
        self.comment_id = comment_id
        self.user_id = user_id
        self.post_id = post_id
        self.comment_date = comment_date
        self.comment = comment
        self.likes = likes

class Credit:
    def __init__(self, user_id: int, production_name: str, role: str, start_date: str, end_date: str, src_type: str, src_url: str, production_type: str, director: str, producer: str, production_link: str, description: str):
        self.user_id = int(user_id)
        self.production_name = production_name
        self.role = role
        self.start_date = start_date
        self.end_date = end_date or ""
        self.src_type = src_type or ""
        if (self.src_type != ""):
            self.src_type = self.src_type.capitalize()
        self.src_url = src_url or ""
        self.production_type = production_type
        self.director = director or ""
        self.producer = producer or ""
        self.production_link = production_link or ""
        self.description = description or ""

    def get_values(self):
        # Used for insertion into MySQL database
        return (self.user_id, self.production_name, self.role, self.start_date,
        self.end_date, self.src_type, self.src_url, self.production_type, self.director,
        self.producer, self.production_link, self.description)

class Education:
    def __init__(self, user_id: int, title: str, start_date: str, end_date: str, institution: str, institution_logo_url: str):
        self.user_id = user_id
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.institution = institution
        self.institution_logo_url = institution_logo_url

    def get_values(self):
        # Used for insertion into MySQL database
        return (self.user_id, self.title, self.start_date, self.end_date,
        self.institution, self.institution_logo_url)
