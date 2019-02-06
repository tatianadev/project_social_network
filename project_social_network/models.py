from django.db import models


class Profile(models.Model):
    text = models.CharField(max_length=500)

    def __str__(self):
        if self.member:
            return self.member.username + ": " + self.text
        return self.text


class Member(models.Model):
    username = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=16)
    profile = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
    following = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.username
