import enum

class MalEntryUserStatus(enum.Enum):
    watching = 1
    completed = 2
    on_hold = 3
    dropped = 4
    plan_to_watch = 6


class MalEntryAiringStatus(enum.Enum):
    airing = 1
    aired = 2
    not_aired = 3


class MalEntry():

    def __init__(self, username):
        self.username = username
        self.anime_id = None
        self.title = None
        self.user_status = None
        self.airing_status = None
        self.watched_episodes = None
        self.total_episodes = None
        self.user_score = None

    def to_string(self):
        return {"username":self.username, "anime_id":self.anime_id, "title": self.title, "user_status":self.user_status, "airing_status": self.airing_status, "watched_episodes":self.watched_episodes, "total_episodes":self.total_episodes, "user_score":self.user_score}

class MalUser():
    def __init__(self, username):
        self.username = username
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)


