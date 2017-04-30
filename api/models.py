from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30,primary_key=True, blank=False, unique=True)
    token = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return "Name: "+self.name


def contact_default():
    return User("Raspi", "NoPass")


class Log(models.Model):
    COMMANDS = (
        ('1', 'TakePhoto'),
        ('2', 'Shutdown'),
        ('3', 'Activate'),
    )

    # Fields
    user = models.ForeignKey(User, on_delete=models.SET(contact_default), default=contact_default, related_name="logs")
    date = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=15, choices=COMMANDS, default='TakePhoto')

    def __str__(self):
        return self.order + self.date.__str__()