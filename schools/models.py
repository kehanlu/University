from django.db import models


class University(models.Model):
    edu_id = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    public = models.BooleanField()
    system = models.CharField(max_length=200)

    # 107 註冊
    description = models.CharField(max_length=300)
    register_rate = models.FloatField(default=0.)

    building_area = models.IntegerField(default=0)
    campus_area = models.IntegerField(default=0)

    # 106
    funding = models.IntegerField(default=0)  # 全校總經費(單位：元)
    project_funding = models.IntegerField(default=0)  # 全校總經費(單位：元)
    teachers = models.IntegerField(default=0)  # 專任教師數

    # 107
    students = models.IntegerField(default=0)
    M_students = models.IntegerField(default=0)
    F_students = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Department(models.Model):
    university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name="department")
    name = models.CharField(max_length=200)  # 科系名
    field = models.CharField(max_length=200)  # 領域
    discipline = models.CharField(max_length=200)  # 學門
    category = models.CharField(max_length=200)  # 學類
    graduate = models.BooleanField(default=False)

    def __str__(self):
        return "[{}] {}".format(self.university.name, self.name)
