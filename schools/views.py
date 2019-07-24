import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from schools.models import University, Department, Grade


def index(request):
    context = {
        "pub_t": University.objects.filter(public=True, system="技職校院"),
        "pub_u": University.objects.filter(public=True, system="大學校院"),
        "pri_t": University.objects.filter(public=False, system="技職校院"),
        "pri_u": University.objects.filter(public=False, system="大學校院"),
    }

    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def school(request, eid):
    eid = "{:04}".format(eid)
    u = University.objects.get(edu_id=eid)
    data = {
        "edu_id": u.edu_id,
        "name": u.name,
        "public": u.public,
        "system": u.system,
        "description": u.description,
        "building_area": int(u.building_area/10000),
        "campus_area": int(u.campus_area/10000),
        "funding": int(u.funding/(10**6)),
        "project_funding": int(u.project_funding/(10**6)),
        "register_rate": u.register_rate,
        "teachers": u.teachers,
        "students": u.students,
        "M_students": u.M_students,
        "F_students": u.F_students,
        "department": [d.name for d in u.department.all()],
        "field": list(set([d.field for d in u.department.all()])),
        "category": list(set([d.category for d in u.department.all()])),
        "discipline": list(set([d.discipline for d in u.department.all()])),
    }
    if Grade.objects.filter(university=u).exists():
        data["grade"] = json.loads(Grade.objects.get(university=u).data)
    else:
        data["grade"] = [{"department": "無資料", "grade": "無資料"}]
    return JsonResponse(data)


def compare_school(request):
    schools = request.GET["data"].split(',')
    same = {
        "field": set(),
        "category": set(),
        "discipline": set(),
        "department": set(),
    }
    print(schools)
    for idx, school_i in enumerate(schools):
        for school_j in schools[idx+1:]:
            print(school_i, school_j)
            ui = University.objects.get(edu_id=school_i)
            uj = University.objects.get(edu_id=school_j)

            same["field"] |= (set([d.field for d in ui.department.filter(graduate=False)]) & set(
                [d.field for d in uj.department.filter(graduate=False)]))
            same["discipline"] |= (set([d.discipline for d in ui.department.filter(graduate=False)]) & set(
                [d.discipline for d in uj.department.filter(graduate=False)]))
            same["category"] |= (set([d.category for d in ui.department.filter(graduate=False)]) & set(
                [d.category for d in uj.department.filter(graduate=False)]))
            same["department"] |= (set([d.name for d in ui.department.filter(graduate=False)]) & set(
                [d.name for d in uj.department.filter(graduate=False)]))

    different = {
        "field": set(),
        "category": set(),
        "department": set(),
        "discipline": set()
    }
    universe_set = {
        "field": set(),
        "category": set(),
        "department": set(),
        "discipline": set()
    }
    for school_i in schools:
        # 自己 - 兩兩交集
        ui = University.objects.get(edu_id=school_i)

        universe_set["field"] |= set(
            [d.field for d in ui.department.filter(graduate=False)])
        universe_set["category"] |= set(
            [d.category for d in ui.department.filter(graduate=False)])
        universe_set["discipline"] |= set(
            [d.discipline for d in ui.department.filter(graduate=False)])
        universe_set["department"] |= set(
            [d.name for d in ui.department.filter(graduate=False)])

        different["field"] |= set(
            [d.field for d in ui.department.filter(graduate=False)]) - same["field"]
        different["category"] |= set(
            [d.category for d in ui.department.filter(graduate=False)]) - same["category"]
        different["discipline"] |= set(
            [d.discipline for d in ui.department.filter(graduate=False)]) - same["discipline"]
        different["department"] |= set(
            [d.name for d in ui.department.filter(graduate=False)]) - same["department"]

    same = {
        "field": list(same["field"]),
        "category": list(same["category"]),
        "department": list(same["department"]),
        "discipline": list(same["discipline"]),
    }
    different = {
        "field": list(different["field"]),
        "category": list(different["category"]),
        "department": list(different["department"]),
        "discipline": list(different["discipline"]),
    }
    universe_set = {
        "field": list(universe_set["field"]),
        "category": list(universe_set["category"]),
        "department": list(universe_set["department"]),
        "discipline": list(universe_set["discipline"]),
    }

    print("same")
    print(same)
    print("different")
    print(different)

    return JsonResponse({
        "universe": universe_set,
        "same": same,
        "different": different,
    })
