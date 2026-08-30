from typing import List, Optional
from .models import Course, Group

def list_professors(course: Course) -> List[str]:
    seen: List[str] = []
    for g in course.groups:
        if g.professor not in seen:
            seen.append(g.professor)
    return seen

def filter_by_professor(
    course: Course,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
) -> Course:

    filtered = Course(code=course.code, name=course.name, credits=course.credits)
    for g in course.groups:
        if include and g.professor not in include:
            continue
        if exclude and g.professor in exclude:
            continue
        new_group = Group(group=g.group, professor=g.professor, gender=g.gender)
        new_group.classTimes = g.classTimes  # فقط خواندنی استفاده می‌شه، نیازی به کپی عمیق نیست
        new_group.examTime = g.examTime
        filtered.add_group(new_group)
    return filtered
