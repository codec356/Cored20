import sys
from datetime import datetime
from io import BytesIO

from PIL import Image
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from tinymce import models as tinymce_models


class LevelMap(models.Model):
    id = models.AutoField(primary_key=True)
    value_from = models.IntegerField(blank=False, null=False)
    value_to = models.IntegerField(blank=False, null=False)
    n_level = models.IntegerField(blank=False, null=False)
    image = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Level settings'

    def __str__(self):
        return "Level №%s (%s - %s)" % (self.n_level, self.value_from, self.value_to)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='user/%Y/%m/%d', blank=True, null=True)
    experience = models.IntegerField(default=1)
    level = models.ForeignKey(LevelMap, on_delete=models.DO_NOTHING, null=True)
    is_fake = models.BooleanField(default=False)
    is_want_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=16, null=True, default=None)
    SEX_CHOICES = (
        ('m', u"남성"),
        ('w', u"여성"),
    )
    sex = models.CharField(max_length=1, verbose_name=u"성별", choices=SEX_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.avatar:
            image = Image.open(self.avatar).convert('RGB')
            output = BytesIO()
            if float(image.size[0]) > float(image.size[1]):
                height = 150
                ratio = (height / float(image.size[1]))
                width = int((float(image.size[0]) * float(ratio)))
            else:
                width = 255
                ratio = (width / float(image.size[0]))
                height = int((float(image.size[1]) * float(ratio)))

            image = image.resize((width, height))
            image.save(output, format='JPEG', quality=100)
            output.seek(0)
            self.avatar = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.avatar.name.split('.')[0],
                                               'image/jpeg',
                                               sys.getsizeof(output), None)
        super(Profile, self).save()

    def calc_level(self, value):
        self.level = LevelMap.objects.get(value_to__gt=self.experience,
                                          value_from__lte=self.experience)
        self.experience += value
        self.save()


class Towns(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Town'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Regions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    id_town = models.ForeignKey('Towns', on_delete=models.CASCADE, related_query_name='regions', related_name='regions')

    class Meta:
        verbose_name = 'Region'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = 'Categories'
        ordering = ('name',)

    def natural_key(self):
        return {
            'name': self.name,
        }

    def __str__(self):
        return self.name


class Discounts(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField()
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Discount'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        im = Image.open(self.image)
        im = im.convert('RGBA')
        output = BytesIO()
        im = im.resize((110, 110))
        im.save(output, format='PNG', quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.image.name.split('.')[0], 'image/png',
                                          sys.getsizeof(output), None)
        super(Discounts, self).save()


class Offers(models.Model):
    id = models.AutoField(primary_key=True)
    name_offer = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    author = models.ForeignKey(User, models.DO_NOTHING)
    town = models.ForeignKey(Towns, models.DO_NOTHING, db_column='town', blank=True, null=True)
    region = models.ForeignKey(Regions, models.DO_NOTHING, db_column='region', blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category', blank=True, null=True)
    is_new = models.BooleanField(default=False)
    discount = models.ForeignKey(Discounts, models.DO_NOTHING, db_column='discount', blank=True, null=True)
    html_content = tinymce_models.HTMLField()
    time_work = models.CharField(max_length=50, blank=False, null=False)
    dt_created = models.DateTimeField(null=False, auto_now=True)
    dt_start = models.DateTimeField(null=True)
    dt_expiration = models.DateTimeField(null=True)
    dt_updated = models.DateTimeField(null=False, auto_now=True)
    is_fake = models.BooleanField(null=False, default=False)
    ext_ident = models.IntegerField(null=True, blank=True)
    is_published = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.name_offer

    def get_init_dict(self):
        return self.__dict__


class OfferComments(models.Model):
    id = models.AutoField(primary_key=True)
    offer = models.ForeignKey(Offers, models.DO_NOTHING)
    author = models.ForeignKey(User, models.DO_NOTHING)
    html_content = RichTextField(max_length=512, blank=True, null=False)
    dt_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comments'

    @staticmethod
    def get_comments_by_offer(offer_inst):
        return OfferComments.objects.filter(offer=offer_inst).order_by('dt_created')


class OfferReviews(models.Model):
    id = models.AutoField(primary_key=True)
    offer = models.ForeignKey(Offers, models.DO_NOTHING)
    author = models.ForeignKey(User, models.DO_NOTHING)
    title = models.CharField(max_length=128, blank=False, null=False)
    html_content = RichTextField(max_length=4096, blank=False, null=False)
    dt_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reviews'


class RateType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = 'Types of rates'

    def natural_key(self):
        return {
            'name': self.name
        }

    def __str__(self):
        return self.name


class OfferReviewRates(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(OfferReviews, on_delete=models.DO_NOTHING)
    rate_type = models.ForeignKey(RateType, on_delete=models.DO_NOTHING)
    n_rate = models.IntegerField(default=0, blank=False, null=False)

    def natural_key(self):
        return {
            'name_rate': self.rate_type.name,
            'n_rate': self.n_rate
        }


class OfferReviewComments(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(OfferReviews, models.DO_NOTHING)
    author = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    html_content = RichTextField(max_length=1000, blank=True, null=False)
    dt_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review comments'


class BalanceType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    icon = models.CharField(max_length=100, blank=False, null=False)


class Balances(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(BalanceType, on_delete=models.DO_NOTHING)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'User balances'

    def create_balance(self, user, type):
        self.user = user
        self.type = type
        self.value = 0
        self.save()

    def add_balance(self, value):
        self.value += value
        Profile.calc_level(self.user.profile, value)
        self.save()

    def cut_balance(self, value):
        self.value -= value
        self.save()

    def __str__(self):
        return "User: %s, balance value: %s" % (self.user.username, self.value)


class TypesIncomes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    action = models.CharField(max_length=60, blank=False, null=False)
    value = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name = 'Type of incomes'

    def __str__(self):
        return "Name type: %s, value: %s" % (self.name, self.value)


class BalanceMovements(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user')
    dt_income = models.DateTimeField(auto_now=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(TypesIncomes, on_delete=models.DO_NOTHING, db_column='type')


class SectionType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    type = models.ForeignKey(SectionType, on_delete=models.DO_NOTHING, null=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Section forum'

    def __str__(self):
        return self.title


class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    title = models.CharField(max_length=150, blank=True, null=True)
    content = RichTextField(blank=True, null=False)
    dt_created = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(Section, models.DO_NOTHING)
    is_fixed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Topic'

    def __str__(self):
        return '[%(section)s] %(title)s' % {'section': self.section.title, 'title': self.title}


class TopicComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    topic = models.ForeignKey(Topic, models.DO_NOTHING)
    content = RichTextField(blank=True, null=False)
    dt_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Topic comment'


class ResortType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=False, null=False)

    class Meta:
        verbose_name = 'Типы обращений'

    def __str__(self):
        return '%(name)s' % {'name': self.name}


class Resort(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    type = models.ForeignKey(ResortType, models.DO_NOTHING)
    title = models.CharField(max_length=128, blank=False, null=False)
    solved = models.BooleanField(default=False)
    dt_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Обращения'

    def __str__(self):
        return '[%(type)s] %(title)s' % {'type': self.type.name, 'title': self.title}


class ResortMessages(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    resort = models.ForeignKey(Resort, models.DO_NOTHING)
    content = RichTextField(blank=False, null=False)
    dt_created = models.DateTimeField(auto_now=True)


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    offer = models.ForeignKey(Offers, models.DO_NOTHING)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=512)
    start_price = models.IntegerField(blank=False, null=False)
    current_price = models.IntegerField(blank=False, null=False)
    dt_created = models.DateTimeField(auto_now=True)
    dt_expiration = models.DateTimeField(auto_now=False)
    user_winner = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='user_winner')
    secret_key = models.CharField(max_length=64, null=True)

    class Meta:
        verbose_name = 'Auction'

    def update_auction(self, user, amount):
        self.user_winner = user
        self.current_price = amount
        self.save()


class AuctionBets(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    amount = models.IntegerField()
    dt_created = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Bets'

    def save(self, *args, **kwargs):
        if Auction.objects.filter(auction=self.auction, auction__current_price__lt=self.amount,
                                  dt_expiration__gte=datetime.utcnow()).count() != 0:

            cancel_bet = TypesIncomes.objects.get(action='cancel_bet')
            betting = TypesIncomes.objects.get(action='bet')

            expense = BalanceMovements.objects.create(user=self.user,
                                                      dt_income=datetime.utcnow(),
                                                      value=-self.amount,
                                                      type=betting)
            expense.save()

            Balances.objects.filter(user=self.user)[0].cut_balance(self.amount)

            Auction.objects.get(id=self.auction.id).update_auction(self.user, self.amount)

            for rec in AuctionBets.objects.filter(auction=self.auction):
                apv = BalanceMovements(user=rec.user, dt_income=datetime.now(), value=rec.amount, type=cancel_bet)
                apv.save()
                usr = Balances.objects.filter(user=rec.user)[0]
                usr.add_balance(rec.amount)
            self.save()
