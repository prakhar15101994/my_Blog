from django.db import models

# Create your models here.


from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an user address')

        user = self.model(
            username=self.normalize_email(username),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
        


from django.contrib.auth.models import  AbstractBaseUser,PermissionsMixin
state_choices = (
    ("Andhra Pradesh","Andhra Pradesh"),
    ("Arunachal Pradesh ","Arunachal Pradesh "),
    ("Assam","Assam"),("Bihar","Bihar"),
    ("Chhattisgarh","Chhattisgarh"),
    ("Goa","Goa"),
    ("Gujarat","Gujarat"),
    ("Haryana","Haryana"),
    ("Himachal Pradesh","Himachal Pradesh"),
    ("Jammu and Kashmir ","Jammu and Kashmir "),
    ("Jharkhand","Jharkhand"),
    ("Karnataka","Karnataka"),
    ("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),("Manipur","Manipur"),
    ("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),
    ("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),
    ("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),
    ("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),
    ("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
    ("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
    ("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),
    ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
    ("Puducherry","Puducherry")
    )



class MyUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    
    first_name=models.CharField(max_length=100,)
    last_name=models.CharField(max_length=100,)
    email=models.EmailField(max_length=50, blank=True)
    address=models.CharField(max_length=100, null=True, blank=True)
    city=models.CharField(max_length=50, null=True, blank=True)
    pincode=models.CharField(max_length=6,null=True, blank=True)
    state = models.CharField(choices=state_choices, max_length=255, null=True, blank=True)
    profile_pic = models.FileField(null=True, blank=True, upload_to='images')
    patient=models.BooleanField(default=False)
    doctor=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True )
    is_superuser = models.BooleanField(default=False)
  
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    # @property
    # def profile_image(self):
    #     if self.profile_pic :
    #         return self.profile_image.url
    #     return ''


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin




CATEGORIES = (('Mental Health', 'Mental Health'),
              ('Heart Disease', 'Heart Disease'),
              ('COVID19', 'COVID19'),
              ('Immunization', 'Immunization'))


class Blog(models.Model):
    myuser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    blog_image = models.FileField(null=True, blank=True, upload_to='images')
    blog_category = models.CharField(choices=CATEGORIES, max_length=100)
    summary = models.TextField(max_length=255)
    content = models.TextField(max_length=255)
    is_draft = models.BooleanField('Is Draft?', default=True)

    def __str__(self):
        return str(self.id)
    
    
    @property
    def my_blog_image(self):
        if self.blog_image :
            return self.blog_image.url
        return ''
    

SPECIALITY = (('Orthopedics', 'Orthopedics'),
              ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'),
              ('Dermatology', 'Dermatology'),
              ('Pediatrics', 'Pediatrics'),
              ('Internal Medicine', 'Internal Medicine'))


class Appointment(models.Model):
    doctor_name = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='%(class)s_requests_doctor')
    patient_name = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='%(class)s_requests_patient')
    app_date = models.DateField()
    app_time = models.TimeField()
    end_time = models.TimeField()
    speciality = models.CharField(choices=SPECIALITY, max_length=100)

    def __str__(self):
        return str(self.id)



