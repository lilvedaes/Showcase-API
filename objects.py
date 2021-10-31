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
