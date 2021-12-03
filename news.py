import uuid


class News:
    def __init__(self):
        self.id = str(uuid.uuid1())
        self.optional_info = "N/A"
        self.image = "N/A"
        pass

    def set_values(self, title, image, countries, topic, optional_info):
        self.title = title
        self.image = image
        self.countries = countries
        self.topic = topic
        self.optional_info = optional_info


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)