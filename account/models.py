from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from userauth.models import User
# add django signals
from django.db.models.signals import post_save

ACCOUNT_STATUS = (
    ("active", "Active"),
    ("in-active", "In-active")
)

GENDER = (
    ("male","Male"),
    ("female","Female"),
    ("other","Other")
)

MARITAL_STATUS = (
    ("married","Married"),
    ("single","Single"),
    ("other","Other")
)

IDENTITY_TYPE = (
    ("national id","National ID"),
    ("passport","PassPort"),
    ("driving lincenses","Driving Lincenses"),
)


def user_directory_path(instance,filename):
    extension = filename.split(".")[-1]
    filename = "%s_%s"% (instance.id,extension)
    return "user_{0}/{1}".format(instance.user.id, filename)


class Account(models.Model):
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    account_number = ShortUUIDField(unique=True ,length=10,max_length=25,prefix="718",alphabet="1234567890")
    account_id = ShortUUIDField(unique=True,length=7,max_length=25,prefix="DAN",alphabet="1234567890")
    account_pin_number = ShortUUIDField(unique=True, length=4,max_length=7,alphabet="1234567890")
    ref_code = ShortUUIDField(unique=True,length=10,max_length=20,alphabet="abcdefghijklmn1234567890")
    account_status = models.CharField(max_length=100,choices=ACCOUNT_STATUS,default="in-active")
    date = models.DateField(auto_now=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User,on_delete=models.DO_NOTHING, blank=True,null=True, related_name="recommended_by")

    class Meta:
        ordering=['-date']

        def __str__(self):
            try:
                return str(self.user)
            except:
                return "Account Model"

class KYC(models.Model):
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="kyc",default="default.jpg")
    marital_status = models.CharField(max_length=50,choices=MARITAL_STATUS)
    gender = models.CharField(choices=GENDER, max_length=50)
    next_of_keen = models.CharField(max_length=100)
    identity_type = models.CharField(max_length=120,choices=IDENTITY_TYPE)
    date_of_birth = models.DateField(auto_now=False)
    signature = models.ImageField(upload_to="kyc")

    # Address
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # Contact details
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)







# IMPLEMENT AUTO ACCOUNT CREATION BY USE OF SIGNALS ON SIGNUP
# django signals to create an account when an account is created
def create_account(sender,instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

def save_account(instance, **kwargs):
    # save the account that has been created
    instance.account.save()

post_save.connect(create_account,sender=User)
post_save.connect(save_account,sender=User)
