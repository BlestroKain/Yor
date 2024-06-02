import pandas as pd
import random
import os
import datetime
import logging
import platform

def log_event(message):
    # Reemplazamos la funcionalidad de log_event con print para pruebas
    print(message)

# Encabezado del log con información del sistema y usuario
#user_name = os.getlogin()
system_info = platform.uname()
#print(f"Usuario: {user_name}")
print(f"Sistema: {system_info.system}")
print(f"Nodo: {system_info.node}")
print(f"Release: {system_info.release}")
print(f"Versión: {system_info.version}")
print(f"Máquina: {system_info.machine}")
print(f"Procesador: {system_info.processor}")
print(f"_____________________________________________________________________________________")
# Función para leer nombres y apellidos de los archivos proporcionados
def read_names(file):
    return pd.read_csv(file, header=None, skiprows=1, encoding='utf-8').squeeze().tolist()

# Generación de datos únicos para los estudiantes
def generate_students(num_students, first_names, last_names):
    students = []
    unique_names = set()
    while len(students) < num_students:
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        if full_name not in unique_names:
            unique_names.add(full_name)
            students.append({'Nombre Completo': full_name})
    return students

# Distribución de estudiantes entre los semestres
def distribute_students(students):
    distribution = [0.14, 0.13, 0.12, 0.11, 0.10, 0.10, 0.09, 0.08, 0.07, 0.06]
    semester_counts = [int(len(students) * p) for p in distribution]
    semesters = []
    for i, count in enumerate(semester_counts):
        semesters.extend([i + 1] * count)
    random.shuffle(semesters)
    for student, semester in zip(students, semesters):
        student['Semestre'] = semester
    return students

# Función para obtener las iniciales del curso
def obtener_iniciales(nombre):
    palabras_comunes = {"DE", "LA", "DEL", "Y", "EL", "LOS", "LAS"}
    palabras = nombre.split()
    iniciales = [palabra[:3] for palabra in palabras if palabra.upper() not in palabras_comunes]
    return "".join(iniciales).upper()[:3]

# Función para calcular HTD y HTI basadas en los créditos
def calcular_horas(creditos):
    if creditos == 4:
        return 96, 120
    if creditos == 3:
        return 64, 80
    if creditos == 2:
        return 32, 64
    if creditos == 1:
        return 16, 32
    return 0, 0

# Generar el código único para cada materia
def generar_codigo(nombre, nivel, creditos, consecutivo):
    iniciales = obtener_iniciales(nombre)
    return f"{iniciales}{nivel}{creditos}{consecutivo}"

# Crear archivos de cursos
def create_course_files(students, courses, folder_path):
    start_time = datetime.datetime.now()
    log_event("Inicio de la creación de archivos de cursos")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    grouped = {course: [] for course in courses}

    for student in students:
        for course, info in courses.items():
            if student['Semestre'] in info['Semestres']:
                grouped[course].append(student)

    for course, data in grouped.items():
        course_path = os.path.join(folder_path, f"Semestre {courses[course]['Semestres'][0]}", course)
        if not os.path.exists(course_path):
            os.makedirs(course_path)
        num_groups = len(data) // courses[course]['Cupo'] + (1 if len(data) % courses[course]['Cupo'] else 0)
        for i in range(num_groups):
            group_data = data[i * courses[course]['Cupo']:(i + 1) * courses[course]['Cupo']]
            if group_data:
                df = pd.DataFrame(group_data)[['Nombre Completo']]
                code = course
                course_name = courses[course]['Nombre'].replace(" ", "").capitalize()
                student_count = len(group_data)
                group_code = i + 1
                filename = f"{code}-{course_name}-{student_count}-{group_code}"
                filepath_csv = os.path.join(course_path, f"{filename}.csv")
                filepath_excel = os.path.join(course_path, f"{filename}.xlsx")
              # Crear archivo CSV
                csv_start_time = datetime.datetime.now()
                df.to_csv(filepath_csv, index=False, encoding='utf-8-sig')
                csv_end_time = datetime.datetime.now()
                csv_time_taken = csv_end_time - csv_start_time
                log_event(f'Creado archivo CSV: {filepath_csv}. Tiempo: {csv_time_taken}')

                # Crear archivo Excel
                excel_start_time = datetime.datetime.now()
                df.to_excel(filepath_excel, index=False)
                excel_end_time = datetime.datetime.now()
                excel_time_taken = excel_end_time - excel_start_time
                log_event(f'Creado archivo Excel: {filepath_excel}. Tiempo: {excel_time_taken}')

    end_time = datetime.datetime.now()
    total_time_taken = end_time - start_time
    log_event(f"Fin de la creación de archivos de cursos. Tiempo total: {total_time_taken}")


# Lista de materias con información
materias = [
    {"nivel": 1, "nombre": "INGLÉS I", "creditos": 1},
    {"nivel": 1, "nombre": "INTRODUCCIÓN A LA INGENIERÍA INDUSTRIAL", "creditos": 1},
    {"nivel": 1, "nombre": "ÁLGEBRA Y TRIGONOMETRÍA", "creditos": 3},
    {"nivel": 1, "nombre": "GEOMETRÍA VECTORIAL Y ANALÍTICA", "creditos": 3},
    {"nivel": 1, "nombre": "CÁLCULO DIFERENCIAL", "creditos": 3},
    {"nivel": 1, "nombre": "LECTOESCRITURA", "creditos": 3},
    {"nivel": 1, "nombre": "VIVAMOS LA UNIVERSIDAD", "creditos": 1},
    {"nivel": 2, "nombre": "INGLÉS II", "creditos": 1},
    {"nivel": 2, "nombre": "GESTIÓN DE LAS ORGANIZACIONES", "creditos": 3},
    {"nivel": 2, "nombre": "HABILIDADES GERENCIALES", "creditos": 3},
    {"nivel": 2, "nombre": "ÁLGEBRA LINEAL", "creditos": 3},
    {"nivel": 2, "nombre": "CÁLCULO INTEGRAL", "creditos": 3},
    {"nivel": 2, "nombre": "DESCUBRIENDO LA FÍSICA", "creditos": 3},
    {"nivel": 3, "nombre": "INGLÉS III", "creditos": 1},
    {"nivel": 3, "nombre": "GESTIÓN CONTABLE", "creditos": 3},
    {"nivel": 3, "nombre": "TEORÍA GENERAL DE SISTEMAS", "creditos": 3},
    {"nivel": 3, "nombre": "PROBABILIDAD E INFERENCIA ESTADÍSTICA", "creditos": 3},
    {"nivel": 3, "nombre": "ALGORITMIA Y PROGRAMACIÓN", "creditos": 3},
    {"nivel": 3, "nombre": "FÍSICA MECÁNICA", "creditos": 3},
    {"nivel": 4, "nombre": "INGLÉS IV", "creditos": 1},
    {"nivel": 4, "nombre": "GESTIÓN DE MÉTODOS Y TIEMPOS", "creditos": 4},
    {"nivel": 4, "nombre": "INGENIERÍA ECONÓMICA", "creditos": 3},
    {"nivel": 4, "nombre": "DISEÑO DE EXPERIMENTOS Y ANÁLISIS DE REGRESIÓN", "creditos": 3},
    {"nivel": 4, "nombre": "OPTIMIZACIÓN", "creditos": 3},
    {"nivel": 5, "nombre": "INGLÉS V", "creditos": 1},
    {"nivel": 5, "nombre": "DINÁMICA DE SISTEMAS", "creditos": 3},
    {"nivel": 5, "nombre": "GESTIÓN POR PROCESOS", "creditos": 3},
    {"nivel": 5, "nombre": "GESTIÓN FINANCIERA", "creditos": 3},
    {"nivel": 5, "nombre": "MUESTREO Y SERIES DE TIEMPO", "creditos": 3},
    {"nivel": 5, "nombre": "PROCESOS ESTOCÁSTICOS Y ANÁLISIS DE DECISIÓN", "creditos": 3},
    {"nivel": 6, "nombre": "INGLÉS VI", "creditos": 1},
    {"nivel": 6, "nombre": "GESTIÓN TECNOLÓGICA", "creditos": 3},
    {"nivel": 6, "nombre": "NORMALIZACIÓN Y CONTROL DE CALIDAD", "creditos": 3},
    {"nivel": 6, "nombre": "SIMULACIÓN", "creditos": 3},
    {"nivel": 6, "nombre": "SEGURIDAD Y SALUD EN EL TRABAJO", "creditos": 3},
    {"nivel": 7, "nombre": "GESTIÓN AMBIENTAL", "creditos": 3},
    {"nivel": 7, "nombre": "FORMULACIÓN Y EVALUACIÓN DE PROYECTOS", "creditos": 3},
    {"nivel": 7, "nombre": "GESTIÓN LOGÍSTICA Y DE LA CADENA DE SUMINISTRO", "creditos": 3},
    {"nivel": 7, "nombre": "MODELACIÓN DE SISTEMAS Y SIMULACIÓN DE PROCESOS", "creditos": 3},
    {"nivel": 8, "nombre": "GESTIÓN DEL TALENTO HUMANO", "creditos": 3},
    {"nivel": 8, "nombre": "GESTIÓN DE SERVICIOS", "creditos": 3},
    {"nivel": 8, "nombre": "PLANIFICACIÓN Y CONTROL DE LA PRODUCCIÓN", "creditos": 3},
    {"nivel": 8, "nombre": "PLANEACIÓN ESTRATÉGICA", "creditos": 3},
    {"nivel": 9, "nombre": "INVESTIGACIÓN DE MERCADOS Y ANÁLISIS DE LA COMPETENCIA", "creditos": 3},
    {"nivel": 9, "nombre": "PRÁCTICAS PROFESIONALES", "creditos": 3},
]

# Cursos y su configuración
courses = {}
consecutivo = 1
for materia in materias:
    codigo = generar_codigo(materia['nombre'], materia['nivel'], materia['creditos'], consecutivo)
    courses[codigo] = {
        'Semestres': [materia['nivel']],
        'Cupo': 30 if materia['nivel'] < 4 else 25 if materia['nivel'] < 7 else 20,
        'HTD': calcular_horas(materia['creditos'])[0],
        'HTI': calcular_horas(materia['creditos'])[1],
        'Nombre': materia['nombre']
    }
    consecutivo += 1

# Archivos de nombres y apellidos
first_names = read_names('nombres.csv')
last_names = read_names('apellidos.csv')

# Generar y distribuir estudiantes
students = generate_students(1000, first_names, last_names)
students = distribute_students(students)

# Crear archivos de cursos
create_course_files(students, courses, 'Ruta Trabajo Final')

# Finalizar el log de eventos con un resumen
total_files = sum([len(files) for r, d, files in os.walk('Ruta Trabajo Final')])
print(f"Total de archivos creados: {total_files}")
print(f"Total de acciones realizadas: {total_files * 2}")  # Cada archivo implica crear CSV y Excel, así que se multiplica por 2
