from email.policy import default
import json
from operator import mod
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Monitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        null=False,
        blank=False,
    )
    type = models.CharField(
        max_length=255,
        verbose_name=_("Type"),
        null=False,
        blank=False,
        default="http",
        choices=[
            ("http", "Http(s)"),
            ("ping", "Ping"),
            ("dns", "DNS"),
            ("tcp", "TCP")
        ]
    )
    timeout = models.IntegerField(
        verbose_name=_("Timeout"),
        null=False,
        blank=True,
        default=10
    )
    url = models.URLField(
        verbose_name=_("URL"),
        null=True,
        blank=True
    )
    hostname = models.CharField(
        max_length=255,
        verbose_name=_("Hostname"),
        null=True,
        blank=True,
    )
    port = models.IntegerField(
        verbose_name=_("Port"),
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(65535),
            MinValueValidator(0)
        ]
    )
    interval = models.IntegerField(
        verbose_name=_("Interval"),
        null=False,
        blank=True,
        default=60
    )
    retry_interval = models.IntegerField(
        verbose_name=_("Retry Interval"),
        null=False,
        blank=True,
        default=30
    )
    options = models.JSONField(
        verbose_name=_("Options"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Monitor")
        verbose_name_plural = _("Monitors")

    def __str__(self):
        return self.name

class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monitor = models.ForeignKey(Monitor, verbose_name=_("Monitor"), blank=False, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=255,
        verbose_name=_("Type"),
        null=False,
        blank=False,
        choices=[
            ("pass", "Passed"),
            ("fail", "Failed")
        ]
    )
    rtt = models.DecimalField(   
        verbose_name=_("Response Time"),     
        null=False,
        blank=False,
        decimal_places=9,
        max_digits=13
    )
    result = models.JSONField(
        verbose_name=_("result"),
        null=True,
        blank=True,
        default={}
    )

    def set_pass(self):
        self.status = "pass"

    def set_fail(self):
        self.status = "fail"  

    class Meta:
        verbose_name = _("Result")
        verbose_name_plural = _("Results")

    def __str__(self):
        return str(self.id)
