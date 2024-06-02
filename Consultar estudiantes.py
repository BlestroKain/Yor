# Función para buscar un estudiante y sus cursos
def buscar_estudiante(nombre_completo, students, courses):
    estudiante = next((est for est in students if est['Nombre Completo'] == nombre_completo), None)
    if estudiante is None:
        return f"Error: El estudiante {nombre_completo} no existe."

    semestre = estudiante['Semestre']
    cursos_matriculados = [info['Nombre'] for code, info in courses.items() if semestre in info['Semestres']]
    cursos_str = "\n".join(cursos_matriculados)
    return f"Estudiante: {nombre_completo}\nSemestre: {semestre}\nCursos matriculados:\n{cursos_str}"

# Pedir al usuario el nombre del estudiante
nombre_estudiante = input("Ingrese el nombre completo del estudiante: ")
resultado = buscar_estudiante(nombre_estudiante, students, courses)
print(resultado)
