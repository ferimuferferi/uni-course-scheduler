from typing import List, Tuple

from .models import Course, Group

Schedule = List[Tuple[Course, Group]]


def find_valid_schedules(wanted_courses: List[Course]) -> List[Schedule]:
    courses_sorted = sorted(wanted_courses, key=lambda c: len(c.groups))

    results: List[Schedule] = []
    chosen: Schedule = []

    def backtrack(index: int):
        if index == len(courses_sorted):
            results.append(list(chosen))
            return
        course = courses_sorted[index]
        for group in course.groups:
            if all(not group.conflicts_with(g) for _, g in chosen):
                chosen.append((course, group))
                backtrack(index + 1)
                chosen.pop()

    backtrack(0)
    return results


def schedule_total_credits(schedule: Schedule) -> int:
    return sum(course.credits for course, _ in schedule)


def print_schedule(schedule: Schedule):
    print("-" * 50)
    for course, group in schedule:
        print(f"{course.name} | گروه {group.group} | استاد {group.professor}")
        for ct in group.classTimes:
            print(f"    کلاس: {ct}")
        if group.examTime:
            print(f"    امتحان: {group.examTime}")
    print("-" * 50)
