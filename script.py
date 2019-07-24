import json
import pandas as pd
from schools.models import University, Department, Grade

DATA_FOLDER = "data/"


def is_public(s):
    if s == "公立(含市立)":
        return True
    else:
        return False


def is_graduate(s):
    if "研究所" in s or "MBA" in s or "EMBA" in s:
        return True
    else:
        return False


df = pd.read_csv(DATA_FOLDER+"/106ulistdepartmentlist01.csv")
school = ""
for idx, row in df.iterrows():
    if school != row["學校代碼"]:
        print(row["學校名稱"])
        u = University.objects.create(edu_id="{:04}".format(int(
            row["學校代碼"])), name=row["學校名稱"], public=is_public(row["公私立"]), system=row["學校體制"])
    school = row["學校代碼"]

    Department.objects.create(university=u,
                              name=row["科系名稱"],
                              field=row["領域名稱"],
                              discipline=row["學門名稱"],
                              category=row["學類名稱"],
                              graduate=is_graduate(row["科系名稱"]))

# 研1.學校承接各單位資助「各類計畫經費」及其每師平均承接金額-以「校」統計.csv
df = pd.read_csv(DATA_FOLDER+"/研1.學校承接各單位資助「各類計畫經費」及其每師平均承接金額-以「校」統計.csv")
df = df[df["年度"] == "106"]

for idx, row in df.iterrows():
    if University.objects.filter(edu_id=row["學校統計處代碼"]).exists():
        University.objects.filter(edu_id=row["學校統計處代碼"]).update(
            teachers=int(row["專任教師數"]),
            funding=int(row["全校總經費(單位：元)"]),
            project_funding=int(row["學校承接計畫經費(單位：元)-小計"]),
        )


# 學1-2.正式學籍在學學生人數-以「校(含學制班別)」統計.csv
df = pd.read_csv(DATA_FOLDER+"/學1-2.正式學籍在學學生人數-以「校(含學制班別)」統計.csv")
df = df[df["學年度"] == "107"].groupby(["學校統計處代碼", "學校名稱"]).sum().reset_index()

for idx, row in df.iterrows():
    if University.objects.filter(edu_id=row["學校統計處代碼"]).exists():
        University.objects.filter(edu_id=row["學校統計處代碼"]).update(
            students=int(row["在學學生數小計"]),
            M_students=int(row["在學學生數男"]),
            F_students=int(row["在學學生數女"]),
        )

# 學12-3.新生(含境外學生)註冊率-以「校」統計.csv
df = pd.read_csv(DATA_FOLDER+"/學12-3.新生(含境外學生)註冊率-以「校」統計.csv")
df = df[df["學年度"] == "107"]

for idx, row in df.iterrows():
    if University.objects.filter(edu_id=row["學校統計處代碼"]).exists():
        University.objects.filter(edu_id=row["學校統計處代碼"]).update(
            description=row["全校招生特色說明"],
            register_rate=row["當學年度全校新生註冊率"]
        )

# 校7.校舍及校地面積-以「校」統計.csv
df = pd.read_csv(DATA_FOLDER+"/校7.校舍及校地面積-以「校」統計.csv")
df = df[df["學年度"] == "107"].groupby(["學校統計處代碼", "學校名稱"]).sum().reset_index()
for idx, row in df.iterrows():
    if University.objects.filter(edu_id=row["學校統計處代碼"]).exists():
        University.objects.filter(edu_id=row["學校統計處代碼"]).update(
            building_area=row["校舍總樓地板面積"],
            campus_area=row["校地面積總計"]
        )

# 最低錄取分
U = json.load(open(DATA_FOLDER+"/uni.json"))
for uni, grade in U.items():
    if uni:
        if University.objects.filter(name__contains=uni).exists():
            u = University.objects.filter(name__contains=uni)[0]
            if not Grade.objects.filter(university=u).exists():
                Grade.objects.create(university=u, data=json.dumps(grade))

U = json.load(open(DATA_FOLDER+"/tech_uni.json"))
for uni, grade in U.items():
    if uni:
        if University.objects.filter(name__contains=uni).exists():
            u = University.objects.filter(name__contains=uni)[0]
            if not Grade.objects.filter(university=u).exists():
                Grade.objects.create(university=u, data=json.dumps(grade))

print("Done!")
