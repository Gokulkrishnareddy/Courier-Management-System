from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    manager=models.BooleanField(default=False,null=True)
    worker=models.BooleanField(default=False,null=True)
    email=models.EmailField(unique=True,null=True)
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username


class Courier(models.Model):
    name=models.CharField(max_length=20)
    customer= models.ForeignKey(User, on_delete=models.CASCADE)
    destination=models.TextField()
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    courier_id=models.CharField(max_length=50,default=uuid.uuid4)
    created=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,default="In Transit")
    delivery_by=models.CharField(max_length=20,default=None,null=True,blank=True)
    def __str__(self):
        return self.name[:20]
    
class Report(models.Model):
    report= models.TextField(null=True)
    created=models.DateTimeField(auto_now=True)
    courier=models.ForeignKey(Courier, on_delete=models.CASCADE,null=True)
    customer= models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    report_id=models.CharField(max_length=50,default=uuid.uuid4)
    def __str__(self):
        return self.customer.username[:20]

class Branch(models.Model):
    name=models.CharField(max_length=20)
    manager=models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.TextField()
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    branch_id=models.CharField(max_length=50,default=uuid.uuid4)
    couriers=models.ManyToManyField(Courier,related_name="couriers",blank=True)
    delivery=models.ManyToManyField(User,related_name="deliverys",blank=True)
    reports=models.ManyToManyField(Report,related_name="reports",blank=True)
    def __str__(self):
        return self.name[:20]


class Tracker(models.Model):
    courier=models.ForeignKey(Courier, on_delete=models.CASCADE,null=True)
    customer= models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    present= models.ForeignKey(Branch, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.courier.name[:20]


@receiver(post_save,sender=Courier)
def create_tracker(sender,instance,created,**kwargs):
    if created:
        Tracker.objects.create(courier=instance,customer=instance.customer)


