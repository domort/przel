from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class EmailBasedUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), blank=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Product(models.Model):
    slug = models.SlugField(null=False, blank=False, unique=True)

    name = models.CharField(null=False, blank=False, unique=True, verbose_name='Name', max_length=255)
    unit_weight = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, verbose_name='Unit weight')
    unit_description = models.TextField(null=False, blank=True, verbose_name='Unit Description')
    category = models.CharField(null=False, blank=True, verbose_name='Name', max_length=255)

    protein = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, verbose_name='Protein')
    carb = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, verbose_name='Carbs')
    fat = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, verbose_name='Fat')
    energy = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, verbose_name='Energy')

    fat_sat = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, verbose_name='Fat saturated')
    fiber = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, verbose_name='Fiber')
    salt = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, verbose_name='Salt')

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return '{} [{}]'.format(self.name or "<Unnamed Item>", self.category or '<Uncategorized>')

    def _get_unique_slug(self):
        slug = slugify(self.name[:30])
        unique_slug = slug
        num = 1
        while self.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Product, self).save(*args, **kwargs)


class Meal(models.Model):
    user = models.OneToOneField(EmailBasedUser, null=False, blank=False, related_name="meal")


class MealElement(models.Model):
    meal = models.ManyToManyField(Meal, related_name="meal_elements")
    product = models.OneToOneField(Product, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=1)
    in_grams = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Product: {}, Amount: {}, In grams: {}'.format(self.product, self.amount, self.in_grams)
