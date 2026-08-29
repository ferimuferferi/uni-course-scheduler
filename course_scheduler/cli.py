from typing import List, Tuple

from .catalog import find_course, find_courses_by_name, load_catalog
from .engine import find_valid_schedules, print_schedule, schedule_total_credits
from .models import Course


def print_catalog(catalog: List[Course]):
    print("\n" + "=" * 70)
    print(f"{'#':<4}{'کد درس':<12}{'واحد':<6}{'تعداد گروه':<12}نام درس")
    print("=" * 70)
    for i, c in enumerate(catalog, start=1):
        print(f"{i:<4}{c.code:<12}{c.credits:<6}{len(c.groups):<12}{c.name}")
    print("=" * 70)


def parse_selection(raw: str, catalog: List[Course]) -> Tuple[List[Course], List[str]]:
    tokens = [t.strip() for t in raw.replace("،", ",").split(",") if t.strip()]
    selected: List[Course] = []
    problems: List[str] = []

    for tok in tokens:
        course = None

        if tok.isdigit() and len(tok) == 7:
            course = find_course(catalog, code=tok)
            if course is None:
                problems.append(f"course with code <{tok}> wasn't found in catalog")
                continue

        elif tok.isdigit() and 1 <= int(tok) <= len(catalog):
            course = catalog[int(tok) - 1]

        else:
            matches = find_courses_by_name(catalog, tok)
            if len(matches) == 1:
                course = matches[0]
            elif len(matches) == 0:
                problems.append(f"no course with the name <{tok}> was found")
                continue
            else:
                names = "، ".join(f"{m.name} ({m.code})" for m in matches)
                problems.append(
                    f"«{tok}» با چند درس مچ شد و نمی‌دونم منظورت کدومه: {names}. "
                    f"enter the code correctly!"
                )
                continue

        if course in selected:
            continue
        selected.append(course)

    return selected, problems


def interactive_main(json_path: str):
    catalog = load_catalog(json_path)
    print(f"catalog uploaded: {len(catalog)} درس.")
    print_catalog(catalog)

    print(
        "\nenter the courses you want\n"
        "you can use the number of the row, the 7 digited code, or part of the course's name. use commas.\n"
        "مثال: 1, 18, 3106103, مدار منطقی\n"
    )

    while True:
        raw = input("your choices: ")
        wanted, problems = parse_selection(raw, catalog)

        if problems:
            print("\n couldn't find these:")
            for p in problems:
                print(f"   - {p}")
            if wanted:
                print("\nfound ones: ")
                for c in wanted:
                    print(f"  - {c.name} ({c.code})")
            retry = input(
                "\nمی‌خوای دوباره کل لیست رو وارد کنی تا مطمئن بشیم هیچی جا نمونده؟ "
                "(y = دوباره وارد کن / n = همین چند تا که پیدا شد رو ادامه بده): "
            ).strip().lower()
            if retry != "n":
                continue

        if not wanted:
            print("no course selected.")
            return
        break

    print("\n finilized courses: ")
    for c in wanted:
        print(f"  - {c.name} ({c.code}) | {c.credits} واحد | {len(c.groups)} گروه")

    all_options = find_valid_schedules(wanted)

    if not all_options:
        print(
            "\nno possible non overlaping state was available\n"
            "یعنی با هر ترکیبی از گروه‌ها، حداقل دو درس با هم تداخل کلاسی یا امتحانی دارن.\n"
            "(همه‌ی دروس بالا اجباری در نظر گرفته می‌شن؛ اگه یکی‌شونو حذف کنی شاید جواب پیدا بشه.)"
        )
        return

    print(f"\n تعداد چینش‌های ممکن بدون تداخل: {len(all_options)}\n")
    for i, sched in enumerate(all_options, start=1):
        assert {c.code for c, _ in sched} == {c.code for c in wanted}
        print(f"=== گزینه {i} ( credits sum: {schedule_total_credits(sched)}) ===")
        print_schedule(sched)
