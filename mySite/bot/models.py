from django.db import models
from django.contrib.auth.models import User as USR

class User(models.Model):
    user = models.ForeignKey(USR, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150,null=True,blank=True)
    passkey = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.user.username} - {self.phone_number} - your pass key : {self.passkey}'


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.TextField()
    status = models.CharField(max_length=50, default='Open')
    remark = models.CharField(max_length=150,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_by_user = models.BooleanField(default=False)

    def __str__(self):
        if self.remark!='':
            return f"TicketId {self.id} raised by {self.user.user.username} for {self.issue}: remark by admin {self.remark} : status {self.status}"
        return f"TicketId {self.id} raised by {self.user.user.username} for {self.issue}: {self.status}"