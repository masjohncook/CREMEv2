from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone


DDOS_TYPE_CHOICES = [('udp', 'udp'), ('others...', 'others...')]


# Create your models here.

class ProgressData(models.Model):
    objects = models.Manager()
    scenario = models.TextField(max_length=50, default='None')
    stage_1_status = models.IntegerField(default=1)  # 1: off, 2: running, 3: finished
    stage_1_detail = models.TextField(default='None')
    stage_2_status = models.IntegerField(default=1)  # 1: off, 2: running, 3: finished
    stage_2_detail = models.TextField(default='None')
    stage_3_status = models.IntegerField(default=1)  # 1: off, 2: running, 3: finished
    stage_3_detail = models.TextField(default='None')
    stage_4_status = models.IntegerField(default=1)  # 1: off, 2: running, 3: finished
    stage_4_detail = models.TextField(default='None')
    stage_5_status = models.IntegerField(default=1)  # 1: off, 2: running, 3: finished
    stage_5_detail = models.TextField(default='None')
    stage_6_status = models.IntegerField(default=1)  # 1: off, 2: running, 3: finished
    stage_6_detail = models.TextField(default='None')
    stage_7_status = models.IntegerField(default=1)  # 1: off, 2: running, 3: finished
    stage_7_detail = models.TextField(default='None')

    # attack phases
    attack_phase_1_data = models.TextField(default='Attack Phase 1')
    attack_phase_2_data = models.TextField(default='Attack Phase 2')
    attack_phase_3_data = models.TextField(default='Attack Phase 3')


class Testbed(models.Model):
    objects = models.Manager()
    status = models.IntegerField(default=1)  # 1: off, 2: running, 3: finished
    number_of_controller = models.IntegerField(default=1)  # only 1
    number_of_data_logger_server = models.IntegerField(default=1)  # only 1
    number_of_target_server = models.IntegerField(default=1)  # only 1
    number_of_benign_server = models.IntegerField(default=1)  # only 1
    number_of_vulnerable_client = models.IntegerField(default=1)
    number_of_non_vulnerable_client = models.IntegerField(default=2)  # at least 2: 1 for benign, 1 for target server
    number_of_attacker_server = models.IntegerField(default=1)  # only 1
    number_of_malicious_client = models.IntegerField(default=1)  # only 1


class Controller(models.Model):
    objects = models.Manager()
    hostname = models.CharField(max_length=255,default="controller-machine")
    ip = models.CharField(max_length=255,default="192.168.56.111")
    username = models.CharField(max_length=255,default="user")
    password = models.CharField(max_length=255,default="qsefthuk")
    path = models.CharField(max_length=255,default="/home/user")


class DataLoggerServer(models.Model):
    objects = models.Manager()
    hostname = models.CharField(max_length=255,default="data-logger-machine")
    ip = models.CharField(max_length=255,default="192.168.56.121")
    username = models.CharField(max_length=255, default="root")
    password = models.CharField(max_length=255, default="qsefthuk")
    path = models.CharField(max_length=255, default="/root")
    network_interface = models.CharField(max_length=255,default="enp0s3")
    atop_interval = models.IntegerField(default=1)  # second


class TargetServer(models.Model):
    objects = models.Manager()
    hostname = models.CharField(max_length=255,default="target-server")
    ip = models.CharField(max_length=255,default="192.168.56.181")
    username = models.CharField(max_length=255, default="root")
    password = models.CharField(max_length=255, default="qsefthuk")
    path = models.CharField(max_length=255, default="/root")


class BenignServer(models.Model):
    objects = models.Manager()
    hostname = models.CharField(max_length=255,default="benign-server")
    ip = models.CharField(max_length=255,default="192.168.56.171")
    username = models.CharField(max_length=255, default="root")
    password = models.CharField(max_length=255, default="qsefthuk")
    path = models.CharField(max_length=255, default="/root")


class VulnerableClient(models.Model):
    objects = models.Manager()
    hostname = models.CharField(max_length=255, default="vulnerable-machine")
    ip = models.CharField(max_length=255, default="192.168.56.151")
    username = models.CharField(max_length=255, default="root")
    password = models.CharField(max_length=255, default="qsefthuk")
    path = models.CharField(max_length=255, default="/root")


class NonVulnerableClient(models.Model):
    objects = models.Manager()
    hostname = models.CharField(max_length=255, default="non-vulnerable-machine-1")
    ip = models.CharField(max_length=255, default="192.168.56.141")
    username = models.CharField(max_length=255, default="root")
    password = models.CharField(max_length=255, default="qsefthuk")
    path = models.CharField(max_length=255, default="/root")


class AttackerServer(models.Model):
    objects = models.Manager()
    hostname = models.CharField(max_length=255,default="attacker-server")
    ip = models.CharField(max_length=255,default="192.168.56.131")
    username = models.CharField(max_length=255, default="root")
    password = models.CharField(max_length=255, default="qsefthuk")
    path = models.CharField(max_length=255, default="/home/kali/Desktop/reinstall")
    number_of_new_bots = models.IntegerField(default=3)
    DDoS_type = models.CharField(max_length=10, choices=DDOS_TYPE_CHOICES, default="udp")
    DDoS_duration = models.IntegerField(default=30, validators=[MaxValueValidator(1000000), MinValueValidator(10)])


class MaliciousClient(models.Model):
    objects = models.Manager()
    hostname = models.CharField(max_length=255,default="malicious-client")
    ip = models.CharField(max_length=255,default="192.168.56.161")
    username = models.CharField(max_length=255, default="root")
    password = models.CharField(max_length=255, default="qsefthuk")
    path = models.CharField(max_length=255, default="/root")


class AttackScenario(models.Model):
    objects = models.Manager()
    mirai = models.BooleanField(default=True)
    ransomware = models.BooleanField(default=True)
    resource_hijacking = models.BooleanField(default=True)
    disk_wipe = models.BooleanField(default=True)
    end_point_dos = models.BooleanField(default=True)
    data_theft = models.BooleanField(default=False)
    rootkit_ransomware = models.BooleanField(default=False)


class MachineLearningModel(models.Model):
    objects = models.Manager()
    decision_tree = models.BooleanField(default=True)
    naive_bayes = models.BooleanField(default=True)
    extra_tree = models.BooleanField(default=True)
    knn = models.BooleanField(default=True)
    random_forest = models.BooleanField(default=True)
    XGBoost = models.BooleanField(default=True)

class SkipStage(models.Model):
    objects = models.Manager()
    skip_configuration = models.BooleanField(default=False)
    skip_reproduction = models.BooleanField(default=False)
    skip_data_processing = models.BooleanField(default=False)
    skip_ML_training = models.BooleanField(default=False)
    skip_evaluation = models.BooleanField(default=False)




