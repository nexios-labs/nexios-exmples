from nexios.auth.base import SimpleUser as BaseUser
from tortoise import fields,Model

class UserEntity(Model,BaseUser):
    username = fields.CharField(max_length = 360)
    
    phone = fields.CharField(max_length = 190)
    
    first_name = fields.CharField(max_length = 120)
    
    last_name = fields.CharField(max_length = 120)
    
    bio = fields.TextField(null = True)
    
    hashed_password = fields.TextField()
    
    
    
    def __str__(self):
        return f"<User {self.username} | {self.phone}"
    
    

    @property
    def display_name(self):
        return self.username or self.phone