from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
#importing regex
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# View page will call model method, which is built into the model manager class
class UserManager(models.Manager):
# method to handle user validations
# post_data is the information from request.POST
    def validate_user(self, post_data):
        # dictionary to contain user data from models.py
        response_to_views = {}
        # list to gather up errors:
        errors = []
        print("In model method:", post_data)

        # add validations:
# name
        if not post_data['name']:#python returns an empty string as false
            errors.append('Name is required')
        if not len(post_data['name']) >= 2:
            errors.append('Name must be at least 2 characters')

# alias
        if not post_data['alias']:#python returns an empty string as false
            errors.append('Alias is required')
        if not len(post_data['alias']) >= 2:
            errors.append('Alias must be at least 2 characters')

# email
        # sends post_data into regex to be checked for match
        if not EMAIL_REGEX.match(post_data['email']):
            errors.append('Enter a valid email')
# password
        if len(post_data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if not post_data['password'] == post_data['confirmPW']:
            errors.append('Passwords must match')

# date of birth; date object from datetime changed to string:
        if not post_data['dob'] < str(date.today()):
            errors.append("Your date of birth cannot be in the future")
        if not post_data['dob']:
            errors.append("Please enter a date of birth")

# check that submitted email is unique (non-duplicate) before other validations, because users log in with their emails
# filter will return false if list is empty, true if not empty
        if self.filter(email = post_data['email']):
            errors.append('Email is already in use')

# checking the errors for failed validations
# if any validations fail, user cannot be logged in
# error messages will be returned
# status and errors are keys in the dictionary response_to_views
        if errors: #failed validations
            response_to_views['status'] = False
            response_to_views['errors'] = errors
        else: #passed validations
            response_to_views['status'] = True

            #hash the password with bcrypt
            hashed_password = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())

            #create new user, saves data in a variable (user):
            user = self.create(name = post_data['name'], alias = post_data['alias'], email = post_data['email'], password = hashed_password, dob = post_data['dob'])
            # user object is saved as a key in list and returned:
            response_to_views['user'] = user
#return response data
        return response_to_views

# finding a user in the database with the user's email:
    def login_user(self, post_data):
        print("This is login_user method in models.py")
        #will be true if email found, false if it isn't:
        response_to_views = {}
        #filter will return only 1 object & won't generate error if email doesn't exist
        user = self.filter(email = post_data['email'])
        print("User:", user)

        if user:#if user email is in the database:
# checks whether submitted password matches one in the database
# submitted pw is hashed with same formula as db password
# because filter returns only 1 object at a time, the user is always user[0]
# bcrypt.checkpw returns a boolean, true or false
            if bcrypt.checkpw(post_data['password'].encode(), user[0].password.encode()):#if boolean is true:
            # user object is saved in response_to_views
                response_to_views['status'] = True
                response_to_views['user'] = user[0]#will be returned & saved in session

            else:#if password is invalid
                response_to_views['status'] = False
                response_to_views['errors'] = "Invalid email/password combination"

        else:#if user email is not found in database:
            response_to_views['status'] = False
            response_to_views['errors'] = "Invalid email"

#return response data
        return response_to_views


# author
        if not post_data['author']:#python returns an empty string as false
            errors.append('Author name is required')
        if not len(post_data['author']) > 3:
            errors.append('Author name must be at least 3 characters')

# quote
        if not post_data['quote']:#python returns an empty string as false
            errors.append('Quote is required')
        if not len(post_data['quote']) > 10:
            errors.append('Quote must be at least 10 characters')


#return response data
        return response_to_views


# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=60)
    alias=models.CharField(max_length=45)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=25)
    dob=models.DateField(default=datetime.today, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

# links UserManager to User, by overwriting the objects hidden key that all models have
    objects = UserManager()

class Quote(models.Model):
# link to user who posts a quote
    post_id=models.ForeignKey(User, related_name="quotes", null=True)
# link to users to add a posted quote
    add_id=models.ManyToManyField(User, related_name="addquotes")
    author=models.CharField(max_length=100)
    quote=models.CharField(max_length=255)
