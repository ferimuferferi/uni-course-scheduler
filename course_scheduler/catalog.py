import json
from typing import List, Optional

from .models import Course, Group, ClassTime, ExamTime


def load_catalog(json_path: str) -> List[Course]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_courses: List[Course] = []
    for c in data["courses"]:
        course = Course(code=c["code"], name=c["name"], credits=c["credits"])
        for g in c["groups"]:
            group = Group(
                group=g["group"],
                professor=g["professor"],
                gender=g.get("gender", "مختلط"),
            )
            group.classTimes = [
                ClassTime(ct["day"], ct["start"], ct["end"]) for ct in g["classTimes"]
            ]
            if g.get("examTime"):
                et = g["examTime"]
                group.examTime = ExamTime(et["date"], et["start"], et["end"])
            course.add_group(group)
        all_courses.append(course)
    return all_courses


def find_course(all_courses: List[Course], code: str = None) -> Optional[Course]:
    if code:
        for c in all_courses:
            if c.code == code:
                return c
    return None


def find_courses_by_name(all_courses: List[Course], query: str) -> List[Course]:
    normalized_query = " ".join(query.strip().split())
    for c in all_courses:
        if " ".join(c.name.split()) == normalized_query:
            return [c]

    words = normalized_query.split()
    if not words:
        return []
    return [c for c in all_courses if all(w in c.name for w in words)]
