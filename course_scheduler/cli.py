from typing import List, Tuple

from .catalog import find_course, find_courses_by_name, load_catalog
from .engine import find_valid_schedules, print_schedule, schedule_total_credits
from .filters import filter_by_professor, list_professors
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
                problems.append(f"کد درس «{tok}» تو کاتالوگ پیدا نشد.")
                continue

        elif tok.isdigit() and 1 <= int(tok) <= len(catalog):
            course = catalog[int(tok) - 1]

        else:
            matches = find_courses_by_name(catalog, tok)
            if len(matches) == 1:
                course = matches[0]
            elif len(matches) == 0:
                problems.append(f"هیچ درسی با نام «{tok}» پیدا نشد.")
                continue
            else:
                names = "، ".join(f"{m.name} ({m.code})" for m in matches)
                problems.append(
                    f"«{tok}» با چند درس مچ شد و نمی‌دونم منظورت کدومه: {names}. "
                    f"لطفاً کد ۷ رقمی دقیق رو وارد کن."
                )
                continue

        if course in selected:
            continue
        selected.append(course)

    return selected, problems


def _parse_professor_tokens(raw: str, professors: List[str]) -> Tuple[List[str], List[str]]:
    names: List[str] = []
    problems: List[str] = []
    for tok in [t.strip() for t in raw.split(",") if t.strip()]:
        if tok.isdigit() and 1 <= int(tok) <= len(professors):
            names.append(professors[int(tok) - 1])
        elif tok in professors:
            names.append(tok)
        else:
            problems.append(tok)
    return names, problems


def ask_professor_filters(wanted: List[Course]) -> List[Course]:
    print(
        "\n--- فیلتر استاد (اختیاری) ---\n"
        "برای هر درسی که چند استاد داره می‌تونی بگی فقط کدوم استاد(ها) رو می‌خوای یا کدوم‌ها رو نمی‌خوای.\n"
        "فرمت: include:1,2  یا  exclude:3   (شماره از لیست استادهای همون درس، یا خودِ اسم استاد)\n"
        "برای رد شدن از این درس فقط Enter بزن.\n"
    )

    result: List[Course] = []
    for course in wanted:
        professors = list_professors(course)
        if len(professors) <= 1:
            result.append(course)
            continue

        print(f"\n«{course.name}» — اساتید موجود:")
        for i, p in enumerate(professors, start=1):
            print(f"   {i}) {p}")

        raw = input("فیلتر تو (Enter = بدون فیلتر): ").strip()
        if not raw:
            result.append(course)
            continue

        mode = None
        if raw.lower().startswith("include:"):
            mode, rest = "include", raw.split(":", 1)[1]
        elif raw.lower().startswith("exclude:"):
            mode, rest = "exclude", raw.split(":", 1)[1]
        else:
            print("⚠️  فرمت شناخته نشد (باید با include: یا exclude: شروع بشه)؛ بدون فیلتر ادامه می‌دیم.")
            result.append(course)
            continue

        names, problems = _parse_professor_tokens(rest, professors)
        if problems:
            print(f"⚠️  این موردها شناسایی نشدن و نادیده گرفته شدن: {', '.join(problems)}")
        if not names:
            print("⚠️  هیچ استاد معتبری داده نشد؛ بدون فیلتر ادامه می‌دیم.")
            result.append(course)
            continue

        filtered = filter_by_professor(
            course,
            include=names if mode == "include" else None,
            exclude=names if mode == "exclude" else None,
        )
        if not filtered.groups:
            print(
                f"⚠️  این فیلتر همه‌ی گروه‌های «{course.name}» رو حذف کرد "
                f"(یعنی این درس دیگه هیچ گروه قابل‌انتخابی نداره)؛ فیلتر نادیده گرفته شد."
            )
            result.append(course)
            continue

        kept = [g.professor for g in filtered.groups]
        print(f"   ✅ فیلتر اعمال شد — گروه‌های باقی‌مانده با استاد: {', '.join(sorted(set(kept)))}")
        result.append(filtered)

    return result


def interactive_main(json_path: str):
    catalog = load_catalog(json_path)
    print(f"کاتالوگ بارگذاری شد: {len(catalog)} درس.")
    print_catalog(catalog)

    print(
        "\nحالا دروسی که می‌خوای بگیری رو وارد کن.\n"
        "می‌تونی از شماره‌ی ردیف بالا، کد ۷ رقمی درس، یا بخشی از نام درس استفاده کنی — با کاما جدا کن.\n"
        "مثال: 1, 18, 3106103, مدار منطقی\n"
    )

    while True:
        raw = input("انتخاب تو: ")
        wanted, problems = parse_selection(raw, catalog)

        if problems:
            print("\n⚠️  این موردها درست شناسایی نشدن:")
            for p in problems:
                print(f"   - {p}")
            if wanted:
                print("\nدروسی که درست پیدا شدن:")
                for c in wanted:
                    print(f"  - {c.name} ({c.code})")
            retry = input(
                "\nمی‌خوای دوباره کل لیست رو وارد کنی تا مطمئن بشیم هیچی جا نمونده؟ "
                "(y = دوباره وارد کن / n = همین چند تا که پیدا شد رو ادامه بده): "
            ).strip().lower()
            if retry != "n":
                continue

        if not wanted:
            print("هیچ درسی انتخاب نشد. برنامه بسته می‌شه.")
            return
        break

    print("\n✅ دروس نهایی که وارد موتور می‌شن:")
    for c in wanted:
        print(f"  - {c.name} ({c.code}) | {c.credits} واحد | {len(c.groups)} گروه")

    wanted = ask_professor_filters(wanted)

    all_options = find_valid_schedules(wanted)

    if not all_options:
        print(
            "\n❌ هیچ چینش بدون تداخلی برای این دروس پیدا نشد.\n"
            "یعنی با هر ترکیبی از گروه‌ها، حداقل دو درس با هم تداخل کلاسی یا امتحانی دارن.\n"
            "(همه‌ی دروس بالا اجباری در نظر گرفته می‌شن؛ اگه یکی‌شونو حذف کنی شاید جواب پیدا بشه.)"
        )
        return

    print(f"\n✅ تعداد چینش‌های ممکن بدون تداخل: {len(all_options)}\n")
    for i, sched in enumerate(all_options, start=1):
        assert {c.code for c, _ in sched} == {c.code for c in wanted}
        print(f"=== گزینه {i} (مجموع واحد: {schedule_total_credits(sched)}) ===")
        print_schedule(sched)
