'''grades = [
    {"name": "Alice", "score": 88},
    {"name": "Bob", "score": 75},
    {"name": "Charlie", "score": 92},
    {"name": "Diana", "score": 85}
]

def analyze_grades(grades, threshold=80):
    # Filtrar los estudiantes con puntaje mayor al umbral
    high_scorers = [student for student in grades if student["score"] > threshold]
    
    # Lista de puntajes
    scores = [student["score"] for student in grades]
    
    # Calcular promedio y máximo
    average_score = sum(scores) / len(scores)
    max_score = max(scores)
    
    # Ordenar
    sorted_by_score = sorted(grades, key=lambda s: s["score"], reverse=True)
    sorted_by_name = sorted(grades, key=lambda s: s["name"])
    
    # Contar estudiantes con puntaje >= 85
    count_high_scorers = sum(1 for s in grades if s["score"] >= 85)
    
    # Nombre y puntaje del mejor estudiante
    top_student = max(grades, key=lambda s: s["score"])
    
    return {
        "high_scorers": high_scorers,
        "average_score": average_score,
        "max_score": max_score,
        "sorted_by_score": sorted_by_score,
        "sorted_by_name": sorted_by_name,
        "count_high_scorers": count_high_scorers,
        "top_student": {"name": top_student["name"], "score": top_student["score"]}
    }

# Ejemplo de uso
result = analyze_grades(grades, threshold=80)
print(result)'''


grades = [
    {"name": "Alice", "score": 88},
    {"name": "Bob", "score": 75},
    {"name": "Charlie", "score": 92},
    {"name": "Diana", "score": 85}
]

def analyze_grades(grades, threshold=80):
    scores = [s["score"] for s in grades]
    top_student = max(grades, key=lambda s: s["score"])
    return {
            "high_scorers": [s for s in grades if s["score"] > threshold],
            "average_score": sum(scores) / len(scores),
            "max_scores": max(scores),
            "sorted_by_score": sorted(grades, key=lambda s: s["score"], reverse= True),
            "sorted_by_name": sorted(grades, key=lambda s: s["name"]),
            "count_high_scorers": sum(s["score"] >= 85 for s in grades),
            "top_student":{"name": top_student["name"], "score":top_student["score"]}
        }

#print(analyze_grades(grades, threshold=80))

results = analyze_grades(grades, threshold=80)

# Imprimir con salto de línea por cada elemento
for key, value in results.items():
    print(f"{key}: {value}\n")