class User(object):
    def __init__(self, id, properties):
        self.id = id
        self.properties = properties

    def __str__(self):
        return 'User(id={}, properties={})'.format(self.id, self.properties)


class HackleUser(object):
    def __init__(self, id=None, user_id=None, device_id=None, identifiers=None, properties=None):
        self.id = id
        self.user_id = user_id
        self.device_id = device_id
        self.identifiers = identifiers
        self.properties = properties

    def __str__(self):
        return 'HackleUser(id={}, user_id={}, device_id={}, identifiers={}, properties={})'.format(self.id,
                                                                                                   self.user_id,
                                                                                                   self.device_id,
                                                                                                   self.identifiers,
                                                                                                   self.properties)

    @staticmethod
    def of(user):
        return HackleUser(user.id, None, None, None, user.properties)


class Event(object):
    def __init__(self, key, value, properties):
        self.key = key
        self.value = value
        self.properties = properties


class Hackle:
    @staticmethod
    def user(id, **kwargs):
        return User(id, kwargs)

    @staticmethod
    def event(key, value=None, **kwargs):
        return Event(key, value, kwargs)
