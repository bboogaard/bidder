from django.contrib.postgres.fields import ArrayField
from django.db import models


class Strategy(models.Model):

    name = models.SlugField(unique=True)

    max_bid = models.IntegerField()

    inc_bid = models.IntegerField()

    dec_bid = models.IntegerField()

    pass_after = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Graph(models.Model):

    created = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='graphs')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.image.url


class AgentProfile(models.Model):

    name = models.SlugField(unique=True)

    max_bid = ArrayField(models.IntegerField(), size=2, null=True, blank=True)

    inc_bid = ArrayField(models.IntegerField(), size=2, null=True, blank=True)

    dec_bid = ArrayField(models.IntegerField(), size=2, null=True, blank=True)

    pass_after = ArrayField(models.IntegerField(), size=2, null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
