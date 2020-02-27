from django.db import models


class BaseInfo(models.Model):
    """An abstract base class model that provides common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=256)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    slug = models.SlugField(max_length=256, editable=False)  # Used to find the web URL

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """the output will be, for example, '/customers/enrolmentrequest/test/1/'"""
        try:
            return reverse(
                f"{self._meta.app_label}:{self._meta.model_name}.detail_view",
                args=[self.slug, self.id]
            )
        except NoReverseMatch:
            assert False, vars(self)

    class Meta:
        abstract = True


class User(BaseInfo, AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('user', 'user'),
        ('anonymous', 'anonymous'),
    ]

    name = models.CharField(max_length=256, editable=False)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='user')

    def save(self, app_label=None, model_name=None, *args, **kwargs):
        if self.first_name:
            self.name = self.first_name
        else:
            self.name = self.username

        if self.last_name and self.first_name:
            self.name += f" {self.last_name}"

        super().save(*args, **kwargs)


class EnrolmentRequest(BaseInfo):
    name = models.CharField(max_length=256, editable=False)
    account_name = models.CharField(max_length=256)
    company_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=256)

    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

    terms_confirmation = models.BooleanField(default=False)
    review_pending = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    phone_confirmed = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        self.name = f'{self.email} | {self.phone}'
        super().save(*args, **kwargs)
