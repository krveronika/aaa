from collections import defaultdict

PATH = "./Corp_Summary.csv"


def _read_dept_info_from_file(
    filepath: str, sep: str = ";", count_first_skip_lines: int = 1
) -> tuple[dict, dict]:
    """
    Чтение файла и созранение в словари нужных данных
    :param filepath: путь до файла
    :param sep: разделитель
    :param count_first_skip_lines: кол-во пропускаемых строк в начале 1-название колонки
    :return: словарь с командами и словарь с зарплатами
    """

    def update_salary_dict(salary_by_dept: dict, dept: str, salary: int) -> None:
        if dept not in salary_by_dept:
            salary_by_dept[dept] = {
                "c_empl": 1,
                "min_salary": salary,
                "max_salary": salary,
                "sum_salary": salary,
            }
            return
        salary_by_dept[dept]["c_empl"] += 1
        salary_by_dept[dept]["min_salary"] = min(
            salary_by_dept[dept]["min_salary"], salary
        )
        salary_by_dept[dept]["max_salary"] = max(
            salary_by_dept[dept]["max_salary"], salary
        )
        salary_by_dept[dept]["sum_salary"] += salary
        return

    tree_dept = defaultdict(set)
    salary_by_dept = {}
    with open(filepath) as file:
        for iline, line in enumerate(file):
            if iline < count_first_skip_lines:
                continue
            _, dept_name, sub_dept_name, _, _, string_salary = line.split(sep)
            salary: int = int(string_salary.replace("\n", ""))
            update_salary_dict(salary_by_dept, dept_name, salary)
            tree_dept[dept_name].add(sub_dept_name)
    return tree_dept, salary_by_dept


def print_tree_dept(tree_dept: dict) -> None:
    """
    Вывод на экран
    :param tree_dept: Заполненный словарь
    :return:
    """
    for dept, subdepts in tree_dept.items():
        print(f"Департамент: {dept} ({len(subdepts)})")
        print(f"Команды: {subdepts}")
        print(50 * "-")


def create_row(dept: str, stat: dict) -> list:
    """
    Список строки отчета: кол-во, вилка, средняя ЗП
    :param dept: Название депатамента
    :param stat: Статистики
    :return:
    """
    return [
        dept,
        f'{stat["c_empl"]}',
        f'{stat["min_salary"]}-{stat["max_salary"]}',
        f'{round(stat["sum_salary"] / stat["c_empl"], 2)}',
    ]


def print_dept_report(salary_by_dept: dict, sep: str = "\t| ") -> None:
    """
    Вывод на экран
    :param salary_by_dept: Словарь со статистикой по департаментам
    :param sep: разделитель для вывода на экран
    :return:
    """
    col_names = [
        "Название департамента",
        "Численность",
        '"вилка" зарплат',
        "Средняя зарплата",
    ]
    print(sep.join(col_names))
    print(80 * "-")
    for dept, stat in salary_by_dept.items():
        row = create_row(dept, stat)
        print(sep.join(row))
    print(80 * "-")


def to_csv_dept_report(
    salary_by_dept: dict, filename: str = "./dept_report.csv", sep: str = ";"
) -> None:
    """
    Сохранение отчета
    :param salary_by_dept: Словарь со статистикой по департаментам
    :param filename: путь до файла
    :param sep: разделитель для вывода на экран
    :return:
    """
    col_names = [
        "Название департамента",
        "Численность",
        '"вилка" зарплат',
        "Средняя зарплата",
    ]
    count_row = 0
    with open(filename, "w") as file:
        file.write(sep.join(col_names) + "\n")
        for dept, stat in salary_by_dept.items():
            row = create_row(dept, stat)
            file.write(sep.join(row) + "\n")
            count_row += 1
    print(f"create file in {filename}, #row={count_row}")


if __name__ == "__main__":
    tree_dept, salary_by_dept = _read_dept_info_from_file(PATH)
    print(f"data is loaded, #dept={len(tree_dept)}")
    _exit = False
    while not _exit:
        print("Меню, введите номер команды:")
        print("1. \tВывести в понятном виде иерархию команд")
        print("2. \tВывести сводный отчёт по департаментам")
        print("3. \tСохранить сводный отчёт из предыдущего пункта в виде csv-файла")
        option = input()
        if option == "1":
            print_tree_dept(tree_dept)
        elif option == "2":
            print_dept_report(salary_by_dept)
        elif option == "3":
            to_csv_dept_report(salary_by_dept)
        else:
            break

    print("До встречи!")
