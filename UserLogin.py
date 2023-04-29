import users


class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.get_data_by_id(user_id)
        return self

    def create_user(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonnymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])

    def get_user(self):
        return self.__user
