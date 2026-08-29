from typing import List, Optional

#minuts after midnight
def _to_minutes(hhmm: str) -> int:
    h, m = hhmm.strip().split(":")
    return int(h) * 60 + int(m)


class ClassTime:
    def __init__(self, day, startingHour, endingHour):
        self.day = day
        self.startingHour = startingHour
        self.endingHour = endingHour

    def overlaps(self, other: "ClassTime") -> bool:
        if self.day != other.day:
            return False
        
        s1, e1 = _to_minutes(self.startingHour), _to_minutes(self.endingHour)
        s2, e2 = _to_minutes(other.startingHour), _to_minutes(other.endingHour)
        
        return s1 < e2 and s2 < e1

    def __repr__(self):
        return f"{self.day} {self.startingHour}~{self.endingHour}"


class ExamTime:
    def __init__(self, date, startingHour, endingHour):
        self.date = date
        self.startingHour = startingHour
        self.endingHour = endingHour

    def overlaps(self, other: "ExamTime") -> bool:
        if self.date != other.date:
            return False
        
        s1, e1 = _to_minutes(self.startingHour), _to_minutes(self.endingHour)
        s2, e2 = _to_minutes(other.startingHour), _to_minutes(other.endingHour)
        
        return s1 < e2 and s2 < e1

    def __repr__(self):
        return f"{self.date} {self.startingHour}~{self.endingHour}"


class Group:
    def __init__(self, group, professor, gender="مختلط"):
        self.group = group
        self.professor = professor
        self.gender = gender
        self.classTimes: List[ClassTime] = []
        self.examTime: Optional[ExamTime] = None
        self.course: Optional["Course"] = None

    def conflicts_with(self, other: "Group") -> bool:
        if self.examTime and other.examTime and self.examTime.overlaps(other.examTime):
            return True
        
        for ct1 in self.classTimes:
            for ct2 in other.classTimes:
                if ct1.overlaps(ct2):
                    return True
        return False

    def __repr__(self):
        return f"گروه {self.group} ({self.professor})"


class Course:
    def __init__(self, code, name, credits):
        self.code = code
        self.name = name
        self.credits = credits
        self.groups: List[Group] = []

    def add_group(self, group: Group):
        group.course = self
        self.groups.append(group)

    def __repr__(self):
        return f"{self.name} ({self.code})"
