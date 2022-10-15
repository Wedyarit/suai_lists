from pip._vendor import requests
from bs4 import BeautifulSoup


class Student:
    def __init__(self, id, subject, total, document):
        self.id = id
        self.subject = subject.replace('\n', ';')
        if total == 'Без В/И':
            self.total = 300
        else:
            self.total = int(total) if total else 0
        self.document = document


if __name__ == '__main__':
    students = []
    soup = BeautifulSoup(requests.get('https://priem.guap.ru/_lists/List_1698_14#').text, 'html.parser')
    for tr in soup.find('tbody'):
        tds = tr.find_all('td')
        students.append(Student(tds[0].text, tds[1].text, tds[4].text, tds[6].text))

    sorted_student = sorted(students, key=lambda x: x.total or x.total == 'Без В/И', reverse=True)
    d_sorted_student = [x for x in sorted_student if x.document == 'Да']

    for i, student in enumerate(d_sorted_student):
        common_list_index = sorted_student.index([x for x in sorted_student if x.id == student.id][0]) + 1
        print('>', i + 1, ' ' * (2 - len(str(i + 1))), '|', common_list_index, ' ' * (4 - len(str(common_list_index))), '|', student.id, ' ' * (14 - len(student.id)), '|', student.total) if student.id == 'И0005' else print(i + 1, ' ' * (4 - len(str(i + 1))), '|', common_list_index, ' ' * (4 - len(str(common_list_index))), '|', student.id, ' ' * (14 - len(student.id)), '|', student.total)
    print(soup.select("body > main > div:nth-child(3) > p")[0].text)
