#альтернативное решение задания с помощью Реализации алгоритма Дейкстры на Python
import heapq

def dijkstra_with_path(graph, start, end):
    # Инициализация расстояний
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    previous_vertices = {vertex: None for vertex in graph}
    
    # Очередь с приоритетами
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Если достигли конечной вершины, можно остановиться
        if current_vertex == end:
            break
            
        # Если текущее расстояние больше сохраненного, пропускаем
        if current_distance > distances[current_vertex]:
            continue
            
        # Обход соседей
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            
            # Если найден более короткий путь
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # Восстановление пути
    path = []
    current_vertex = end
    
    while previous_vertices[current_vertex] is not None:
        path.insert(0, current_vertex)
        current_vertex = previous_vertices[current_vertex]
    
    if path:
        path.insert(0, start)
    
    return distances[end], path

def print_route_info(graph, start, end):
    distance, path = dijkstra_with_path(graph, start, end)
    
    print(f"Кратчайший путь от {start} до {end}:")
    print(f"Расстояние: {distance} км")
    print(f"Маршрут: {' → '.join(path)}")
    
    # Детали маршрута
    print("\nДетали маршрута:")
    for i in range(len(path) - 1):
        from_city = path[i]
        to_city = path[i + 1]
        distance_segment = graph[from_city][to_city]
        print(f"  {from_city} → {to_city}: {distance_segment} км")

# Заданный граф
graph = {
    'A': {'B': 4, 'C': 7},
    'B': {'A': 4, 'D': 2, 'E': 8},
    'C': {'A': 7, 'D': 2, 'E': 5},
    'D': {'B': 2, 'C': 2, 'E': 1, 'F': 4},
    'E': {'C': 5, 'D': 1, 'F': 11},
    'F': {'B': 8, 'D': 4, 'E': 11}
}

# Решение задачи
print("=" * 50)
print("ПРАКТИЧЕСКАЯ ЗАДАЧА: ПОИСК КРАТЧАЙШЕГО ПУТИ")
print("=" * 50)

start_city = 'A'
end_city = 'F'

print_route_info(graph, start_city, end_city)

# Дополнительно: расстояния от A до всех городов
print("\n" + "=" * 50)
print("РАССТОЯНИЯ ОТ ГОРОДА A ДО ВСЕХ ОСТАЛЬНЫХ:")
print("=" * 50)

def dijkstra_all_distances(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_vertex]:
            continue
            
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

all_distances = dijkstra_all_distances(graph, 'A')
for city, dist in sorted(all_distances.items()):
    print(f"A → {city}: {dist} км")

|||Результат выполнения:
text
==================================================
ПРАКТИЧЕСКАЯ ЗАДАЧА: ПОИСК КРАТЧАЙШЕГО ПУТИ
==================================================
Кратчайший путь от A до F:
Расстояние: 10 км
Маршрут: A → B → D → F

Детали маршрута:
  A → B: 4 км
  B → D: 2 км
  D → F: 4 км

==================================================
РАССТОЯНИЯ ОТ ГОРОДА A ДО ВСЕХ ОСТАЛЬНЫХ:
==================================================
A → A: 0 км
A → B: 4 км
A → C: 7 км
A → D: 6 км
A → E: 7 км
A → F: 10 км|||
