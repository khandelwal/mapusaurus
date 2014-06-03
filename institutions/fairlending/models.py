from django.db import models

class Ethnicity(models.Model):
    slug = models.SlugField(unique=True, null=False)
    description = models.CharField(max_length=128)

class StatisticType(models.Model):
    """ The type of statistic, including an ethnicity indicator 
    and description. """

    slug = models.SlugField(unique=True, null=False)
    description = models.TextField(null=False)
    ethnicity = models.ForeignKey('Ethnicity')

class TractStatistic(models.Model):
    """ Store per-tract statistics here. """

    geoid = models.ForeignKey(
        'geo.StateCensusTract', to_field='geoid', db_index=True)
    statistic_type = models.ForeignKey(StatisticType)
    value = models.FloatField()
    year = models.IntegerField()
