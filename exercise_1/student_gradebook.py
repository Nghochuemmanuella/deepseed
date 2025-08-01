def calculate_average(grades):
    return sum(grades) / len(grades) if grades else 0

def determine_letter_grade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'

def add_student(students):
    name = input("Enter student name: ").strip()
    if name in students:
        print(f"{name} already exists in the gradebook.")
    else:
        students[name] = []
        print(f"Student {name} added.")

def add_grade(students):
    name = input("Enter student name: ").strip()
    if name not in students:
        print(f"{name} is not in the gradebook.")
        return

    try:
        grade = float(input(f"Enter grade for {name}: "))
        if not 0 <= grade <= 100:
            print("Grade must be between 0 and 100.")
            return
        students[name].append(grade)
        print(f"Added grade {grade} for {name}.")
    except ValueError:
        print("Invalid input. Please enter a numeric grade.")

def view_student_report(students):
    name = input("Enter student name: ").strip()
    if name not in students:
        print(f"{name} is not in the gradebook.")
        return

    grades = students[name]
    if not grades:
        print(f"No grades recorded for {name}.")
        return

    avg = calculate_average(grades)
    letter = determine_letter_grade(avg)
    print(f"{name}'s Average: {avg:.1f} (Grade: {letter})")
    print(f"Grades: {grades}")

def class_statistics(students):
    if not students:
        print("No students in the gradebook.")
        return

    all_averages = []
    for name, grades in students.items():
        if grades:
            avg = calculate_average(grades)
            all_averages.append((name, avg))

    if not all_averages:
        print("No grades recorded for any student.")
        return

    # Calculate class average
    class_avg = sum(avg for _, avg in all_averages) / len(all_averages)

    # Find highest and lowest performing students
    highest_student, highest_avg = max(all_averages, key=lambda x: x[1])
    lowest_student, lowest_avg = min(all_averages, key=lambda x: x[1])

    print(f"Class Average: {class_avg:.2f}")
    print(f"Highest Performing Student: {highest_student} ({highest_avg:.2f})")
    print(f"Lowest Performing Student: {lowest_student} ({lowest_avg:.2f})")

def main():
    students = {}
    while True:
        print("\n=== STUDENT GRADEBOOK MANAGER ===")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. View Student Report")
        print("4. Class Statistics")
        print("5. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            add_grade(students)
        elif choice == "3":
            view_student_report(students)
        elif choice == "4":
            class_statistics(students)
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

   

