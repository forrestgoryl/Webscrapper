from django.db import models
import bcrypt, re

class UserManager(models.Manager):
    def validate_signup(self, postData):
        first_name = postData['first_name']
        email = postData['email']
        password = postData['password']
        confirm_password = postData['confirm_password']
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(first_name) > 30:
            errors['name'] = "Your first name is longer than 30 characters. Can you shorten it?"
        if len(first_name) < 2:
            errors['name'] = "Please enter more than one character for your name."
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Your email doesn't fit the pattern 'your_email@abc.com'."
        if User.objects.filter(email=email).exists():
            errors['email'] = "Your email is already registered with another account. Try logging in."
        if len(email) > 30:
            errors['email'] = "Your email is too long for the database."
        if len(password) > 30:
            errors['password'] = "Your password is too long. How can you remember that?"
        if password != confirm_password:
            errors['password'] = "Your password doesn't match your password confirmation."
        return errors
    def validate_login(self, postData):
        errors = {}
        if User.objects.filter(email=postData['email']).exists():
            if (bcrypt.checkpw(postData['password'].encode(), User.objects.filter(email=postData['email'])[0].password.encode())):
                pass
            else:
                errors['password_incorrect'] = "Your password didn't match the one in our system."
                return errors
        else:
            errors['email_not_found'] = "Your email address isn't in the system. Please register it."
        return errors
    # def validate_update(self, postData):
    #     errors = {}
    #     if len(postData['first_name']) < 2:
    #         errors['name'] = "Please make your name longer."
    #     EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    #     if not EMAIL_REGEX.match(postData['email']):
    #         errors['email'] = "Your email doesn't fit the pattern 'your_email@abc.com'."
    #     if User.objects.filter(email=postData['email']).exists():
    #         errors['email'] = "Your email is already in the database."
    #     return errors

class User(models.Model):
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Search(models.Model):
    user = models.ForeignKey(User, related_name='searches', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    user = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)