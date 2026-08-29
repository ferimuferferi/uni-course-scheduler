import os

from course_scheduler.cli import interactive_main

if __name__ == "__main__":
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "courses_data.json")
    interactive_main(json_path)