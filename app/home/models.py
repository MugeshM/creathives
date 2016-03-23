from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from datetime import datetime

class UserManager(BaseUserManager):
    def _create_user(self, email, user_name, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model( email=email, user_name=user_name, is_staff=is_staff,
                          is_active=False, is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def _create_super_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model( email=email, is_staff=is_staff,
                          is_active=False, is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_user(self, email=None, user_name=None, password=None, **extra_fields):
        if 'username' in extra_fields:
            extra_fields.pop('username')
        return self._create_user(email, user_name, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_super_user( email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

    def update_user_details(self, email,  user_name):
        user = User.objects.get(email=email)
        if user is not None:
            user.first_name = user_name
            user.save
            return user
        return None


class User(AbstractBaseUser):
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True,
        related_name="tmp_user_set", related_query_name="user")
    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_('user permissions'), blank=True,
        related_name="tmp_user_set", related_query_name="user")
    user_name = models.CharField(_('user name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    date_of_birth = models.DateField(null=True)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=30, null=True)

    MALE = '1'
    FEMALE = '2'
    OTHER = '3'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,null=True)
    profile_url=models.CharField(max_length=200,default="/static/images/user.png")
    wallimg_url=models.CharField(max_length=250,null=True,default="/static/images/banner1.png")
    aboutme=models.CharField(max_length=300)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    is_superuser = models.BooleanField(_('active'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    activation_key = models.CharField(max_length=40, blank="True")
    reset_password_key = models.CharField(max_length=40, blank="True")
    key_expires = models.DateTimeField(default=datetime.now())
    is_email_verified = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email',]
    class Meta:
        db_table = "creativesaccount"

    def get_full_name(self):
        full_name = '%s' % (self.user_name)
        return full_name.strip()

    def get_short_name(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class projects(models.Model):
    project_title=models.CharField(max_length=100,default="Project Title")
    project_desc=models.CharField(max_length=350,default="Project Description")
    # user_email = models.ForeignKey(User,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    posted_date = models.DateTimeField('date posted',default=timezone.now)
    thumbnail_url = models.CharField(max_length=200,default=None)
    project_url = models.CharField(max_length=200,default=None)
    project_type=models.CharField(max_length=100,default=None)
    def __str__(self):
        return self.project_title

    def was_posted_recently(self):
        return self.posted_date >= timezone.now() - datetime.timedelta(days=1)
