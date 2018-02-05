from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def register(self, name, username, date_hired, password, confirm_password):
        print "inside the models", name, username, date_hired, password, confirm_password
        response = {
            "errors": [],
            "valid": True,
            "user": None
        }
# check if name is entered and matches right format
        if len(name) < 3:
            response["valid"] = False
            response["errors"].append("A valid name of 3 or more letters is required")
        if len(username) < 3:
            response["valid"] = False
            response["errors"].append("A valid username of 3 or more letters is required")

# check if date of hire is older than today
        if len(date_hired) < 1:
            response["errors"].append("Date of hire is required")
        else:
            date_hired = datetime.strptime(date_hired, '%Y-%m-%d')
            today = datetime.now()
            if date_hired > today:
                response["errors"].append("Date of hire must be in the past")

# check whether password has at least 8 characters
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Your password must be at least 8 characters")
        if confirm_password != password:
            response["valid"] = False
            response["errors"].append("Be careful. Your password must match Confirm Password")
        
# If the response is valid this will replace none in the respose.user dictionary.
        if response["valid"]:
            response["user"] = User.objects.create(
                name=name,
                username=username,
                date_hired=date_hired,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
            )
        return response

    def login(self, username, password):
        response = {
            "errors": [],
            "valid": True,
            "user": None
        }

        if len(username) < 2:
            response['errors'].append("Username longer than two characters is required!")
        else:
            uname = User.objects.filter(username=username)
            if len(uname) == 0:
                response["errors"].append("Invalid username/password!")
        if len(password) < 8:
            response['errors'].append("Password must be 8 characters long!")
        if len(response['errors']) == 0:
            if bcrypt.checkpw(password.encode(), uname[0].password.encode()):
                response['user'] = uname[0]
            else:
                response["errors"].append("Invalid username/password!")
        
        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Wish(models.Model):
    wish = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_wishing = models.ManyToManyField(User, related_name="wish_list")

    def __str__(self):  
        return self.name
