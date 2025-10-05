import psycopg2
from psycopg2.extras import DictCursor

def connect():
    study = {
        'user' : 'postgres',
        'password' : 'aSd_vbnm001',
        'host' : 'localhost',
        'port' : '5432'
    }
    return psycopg2.connect(**study)

# выдача студента по id
def get_student(id_student):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT f00l_name FROM students WHERE id_student = %s', (id_student, ))
            return cur.fetchone()

# выдача предметов по курсу в хронологическом порядке       
def get_discipline(number_course):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT name_discipline FROM disciplines WHERE number_course = %s ORDER BY weekday, number_class', (number_course, ))
            return cur.fetchall()

# выдача студентов по номеру курса в алфавитном порядке
def get_students(course_number):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT f00l_name FROM students WHERE course_number = %s ORDER BY f00l_name', (course_number, ))
            return cur.fetchall()

# вывод полного рассписания со всеми полями
def get_disciplines():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM disciplines')
            return cur.fetchall()

# добавление студента       
def put_student(f00l_name, course_number):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO students (f00l_name, course_number) VALUES(%s, %s) RETURNING id_student', (f00l_name, course_number, ))
            id_students = cur.fetchone()[0]
            conn.commit()
            return id_students

# добавление предмета     
def put_discipline(name_discipline, weekday, number_class, number_course, ):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO disciplines (name_discipline, weekday, number_class, number_course) VALUES(%s, %s, %s, %s) RETURNING id_discipline', (name_discipline, weekday, number_class, number_course, ))
            id_discipline = cur.fetchone()[0]
            conn.commit()
            return id_discipline

# удаление студента по id     
def delete_student(id_student):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM students WHERE id_student = %s', (id_student, ))
            conn.commit()

# удаление предмета по id
def delete_discipline(id_discipline):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM disciplines WHERE id_discipline = %s', (id_discipline, ))
            conn.commit()

def main():
    while True:
        inp = input('введите команду: ').strip().split()
        if not inp:
            continue
        if inp[0].lower() == 'exit':
            break
        command = inp[0].lower()

        if command == 'get':
            if inp[1] == 'student':
                student = get_student(int(inp[2]))
                if student:
                    print(*student)
                else:
                    print('студент не найден')

            elif inp[1] == 'discipline':
                discipline = get_discipline(int(inp[2]))
                for d in discipline:
                    print(*d)

            elif inp[1] == 'students':
                students = get_students(int(inp[2]))
                for s in students:
                    print(*s)
            
            elif inp[1] == 'disciplines':
                disciplines = get_disciplines()
                for ds in disciplines:
                    print(*ds)

        elif command == 'put':
            if inp[1] == 'student':
                course_number = int(inp[-1])
                student_name = " ".join(inp[2:-1])
                new_student = put_student(student_name, course_number)
                print(f'студент с id {new_student} добавлен')

            elif inp[1] == 'discipline':
                name_discipline = " ".join(inp[2:-3])
                weekday = inp[-3]
                number_class = int(inp[-2])         
                number_course = int(inp[-1])
                new_discipline = put_discipline(name_discipline, weekday, number_class, number_course)
                print(f'предмет с id {new_discipline} добавлен')

        elif command == 'delete':
            if inp[1] == 'student':
                delete_student(inp[2])
                print('студент удален')

            elif inp[1] == 'discipline':
                delete_discipline(inp[2])
                print('предмет удален')

if __name__ == '__main__':
    main()

        

    
