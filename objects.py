import re


class User:
    connection_dist = -1

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
    def __init__(self, user_id, profession, connection_dist, location, gender, age, skills, languages, union_status):
        self.user_id = user_id
        self.profession = profession
        self.connection_dist = connection_dist
        self.location = location
        self.gender = gender

        self.age = age if age != None else "0-300"
        self.start_age = int(re.search(r'^(\d+)', self.age).group(1))
        self.end_age = re.search(r'(\d+)$', self.age).group(1)
        self.end_age = 300 if self.end_age == '' else int(self.end_age)
        self.skills = skills
        self.languages = languages
        self.union_status = union_status

    def user_applicable(self, user: User, connection_dist):
        if ((self.profession != None and self.profession.lower() not in user.title.lower()) or
                (self.connection_dist != None and self.connection_dist <= connection_dist) or
                (self.gender != None and user.gender.lower() != self.gender.lower()) or
                # (self.union_status != None and self.union user.union_status_id) or # TODO: get union status from user's union status id
                # (self.skills != None and all([s in user.skills for s in self.skills])) # TODO: save user skills
                (self.location != None and self.location.lower() not in user.location.lower()) or
                (self.age != None and (user.age_range_end < self.start_age or self.end_age < user.age_range_start))
        ):
            return False

        return True
