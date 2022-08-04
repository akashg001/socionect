from distutils import text_file
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now
from django.conf import settings
from django.db.models.fields import UUIDField
from datetime import date,datetime
from django.db.models import Max
class userprofile(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    followers = models.ManyToManyField(User,related_name="followers",null=True)
    following = models.ManyToManyField(User,related_name="following",null=True)
    total_followers = models.IntegerField(default = 0,null=True)
    total_followings = models.IntegerField(default = 0,null=True)
    #dob = models.DateTimeField(auto_now_add=True)
    dp = models.ImageField(upload_to="dp/")
    def __str__(self):
        return f'{self.user.username}'
    

class posts(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_by = models.ForeignKey(userprofile, on_delete=models.CASCADE,null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    pic = models.ImageField( upload_to="media/")
    caption = models.TextField(null=True)
    comments = models.TextField(default="",null=True)
    liked_by = models.ManyToManyField(User,related_name="liked_by",null=True)
    likes = models.IntegerField(default = 0,null=True)
    

class Message(models.Model):
    msguser = models.ForeignKey(userprofile, on_delete=models.CASCADE, related_name="msguser")
    sender = models.ForeignKey(userprofile, on_delete=models.CASCADE, related_name="from_user")
    reciepient = models.ForeignKey(userprofile, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def sender_message(from_user, to_user, body):
        sender_message = Message(
            msguser=from_user,
            sender = from_user,
            reciepient = to_user,
            body = body,
            is_read = True
            )
        sender_message.save()
    
        reciepient_message = Message(
            msguser=to_user,
            sender = from_user,
            reciepient = from_user,
            body = body,
            is_read = True
            )
        reciepient_message.save()
        return sender_message

    def get_message(user):
        users = []
        messages = Message.objects.filter(msguser=user).values('reciepient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': userprofile.objects.get(pk=message['reciepient']),
                'last': message['last'],
                'unread': Message.objects.filter(msguser=user, reciepient__pk=message['reciepient'], is_read=False).count()
            })
        return users