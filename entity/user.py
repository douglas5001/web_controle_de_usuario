

class User():
    def __init__(self, name, email, password, profile_id, is_admin):
        self.__name = name 
        self.__email = email 
        self.__password = password
        self.__is_admin = is_admin
        self.__profile_id = profile_id
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.__email = email
    
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def is_admin(self):
        return self.__is_admin
    
    @is_admin.setter
    def is_admin(self, is_admin):
        self.__is_admin = is_admin
        
    @property
    def profile_id(self):
        return self.__profile_id

    @profile_id.setter
    def profile_id(self, profile_id):
        self.__profile_id = profile_id