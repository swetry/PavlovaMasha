#Поиск с имитацией отжига для раскраски графа
import random
import math

class GraphColoringSA:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.adjacency_list = self._build_adjacency_list()
        
    def _build_adjacency_list(self):
        """Строит список смежности графа"""
        adj_list = {i: [] for i in range(1, self.vertices + 1)}
        for u, v in self.edges:
            adj_list[u].append(v)
            adj_list[v].append(u)
        return adj_list
    
    def count_conflicts(self, coloring):
        """Подсчитывает количество конфликтов (смежных вершин одного цвета)"""
        conflicts = 0
        for u, v in self.edges:
            if coloring[u] == coloring[v]:
                conflicts += 1
        return conflicts
    
    def get_neighbor_solution(self, coloring, num_colors):
        """Генерирует соседнее решение"""
        new_coloring = coloring.copy()
        
        # Выбираем случайную вершину
        vertex = random.randint(1, self.vertices)
        
        # С вероятностью 70% меняем цвет случайно, иначе на минимально возможный
        if random.random() < 0.7:
            new_color = random.randint(1, num_colors)
        else:
            # Находим минимальный цвет, не конфликтующий с соседями
            neighbor_colors = set(new_coloring[neighbor] for neighbor in self.adjacency_list[vertex])
            for color in range(1, num_colors + 1):
                if color not in neighbor_colors:
                    new_color = color
                    break
            else:
                new_color = random.randint(1, num_colors)
        
        new_coloring[vertex] = new_color
        return new_coloring
    
    def simulated_annealing(self, initial_temp=1000, cooling_rate=0.95, min_temp=0.1, max_iterations=1000):
        """Алгоритм имитации отжига для раскраски графа"""
        
        # Начальная инициализация
        current_coloring = {i: 1 for i in range(1, self.vertices + 1)}
        current_conflicts = self.count_conflicts(current_coloring)
        
        # Оценка минимального количества цветов (хроматического числа)
        min_colors = self.estimate_min_colors()
        
        best_coloring = current_coloring.copy()
        best_conflicts = current_conflicts
        best_num_colors = max(current_coloring.values())
        
        temperature = initial_temp
        iteration = 0
        
        print("Начальная температура:", initial_temp)
        print("Минимальная оценка цветов:", min_colors)
        print("\nИтерация\tТемпература\tКонфликты\tЦвета")
        print("-" * 50)
        
        while temperature > min_temp and iteration < max_iterations:
            # Пробуем уменьшить количество цветов, если текущее решение хорошее
            current_num_colors = max(current_coloring.values())
            if current_conflicts == 0 and current_num_colors > min_colors:
                # Пытаемся использовать на 1 цвет меньше
                new_num_colors = current_num_colors - 1
                new_coloring = self._reduce_colors(current_coloring, new_num_colors)
                new_conflicts = self.count_conflicts(new_coloring)
                
                # Принимаем новое решение, если оно не хуже
                if new_conflicts <= current_conflicts:
                    current_coloring = new_coloring
                    current_conflicts = new_conflicts
                    current_num_colors = new_num_colors
            
            # Генерируем соседнее решение
            new_coloring = self.get_neighbor_solution(current_coloring, current_num_colors)
            new_conflicts = self.count_conflicts(new_coloring)
            new_num_colors = max(new_coloring.values())
            
            # Вычисляем разницу в качестве
            delta = new_conflicts - current_conflicts
            
            # Ключевая строка 1: Критерий принятия решения в имитации отжига
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_coloring = new_coloring
                current_conflicts = new_conflicts
            
            # Обновляем лучшее решение
            if current_conflicts < best_conflicts or (
                current_conflicts == best_conflicts and current_num_colors < best_num_colors):
                best_coloring = current_coloring.copy()
                best_conflicts = current_conflicts
                best_num_colors = current_num_colors
            
            # Выводим информацию каждые 50 итераций или при значительном улучшении
            if iteration % 50 == 0 or current_conflicts < best_conflicts:
                print(f"{iteration:8d}\t{temperature:10.2f}\t{current_conflicts:10d}\t{current_num_colors:8d}")
            
            # Ключевая строка 2: Понижение температуры
            temperature *= cooling_rate
            iteration += 1
        
        return best_coloring, best_num_colors, best_conflicts
    
    def estimate_min_colors(self):
        """Оценивает минимальное количество цветов (нижняя граница)"""
        # Используем максимальную степень вершины + 1 как оценку
        max_degree = max(len(neighbors) for neighbors in self.adjacency_list.values())
        return max_degree + 1
    
    def _reduce_colors(self, coloring, new_num_colors):
        """Пытается уменьшить количество цветов в раскраске"""
        new_coloring = coloring.copy()
        for vertex in range(1, self.vertices + 1):
            if new_coloring[vertex] > new_num_colors:
                # Ищем минимальный доступный цвет
                neighbor_colors = set(new_coloring[neighbor] for neighbor in self.adjacency_list[vertex])
                for color in range(1, new_num_colors + 1):
                    if color not in neighbor_colors:
                        new_coloring[vertex] = color
                        break
                else:
                    new_coloring[vertex] = random.randint(1, new_num_colors)
        return new_coloring

def read_graph_from_console():
    """Читает граф с консоли"""
    print("Введите количество вершин (рекомендуется 10):")
    vertices = int(input().strip())
    
    print("Введите количество ребер (рекомендуется 15):")
    num_edges = int(input().strip())
    
    edges = []
    print("Введите ребра в формате 'u v' (вершины с 1):")
    for i in range(num_edges):
        while True:
            try:
                u, v = map(int, input(f"Ребро {i+1}: ").strip().split())
                if 1 <= u <= vertices and 1 <= v <= vertices and u != v:
                    edges.append((u, v))
                    break
                else:
                    print("Ошибка: вершины должны быть в диапазоне 1..n и не равны друг другу")
            except ValueError:
                print("Ошибка: введите два числа через пробел")
    
    return vertices, edges

def main():
    # Чтение графа
    vertices, edges = read_graph_from_console()
    
    # Создание решателя
    solver = GraphColoringSA(vertices, edges)
    
    print("\nЗапуск алгоритма имитации отжига...")
    
    # Запуск алгоритма
    coloring, num_colors, conflicts = solver.simulated_annealing(
        initial_temp=1000,
        cooling_rate=0.93,
        min_temp=0.01,
        max_iterations=2000
    )
    
    # Вывод результатов
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТЫ:")
    print("="*50)
    print(f"Количество использованных цветов: {num_colors}")
    print(f"Количество конфликтов: {conflicts}")
    print("\nРаскраска вершин:")
    for vertex in sorted(coloring.keys()):
        print(f"Вершина {vertex}: Цвет {coloring[vertex]}")
    
    # Проверка корректности
    if conflicts == 0:
        print("\n✓ Раскраска корректна (нет конфликтов)")
    else:
        print(f"\n⚠ Раскраска имеет {conflicts} конфликт(ов)")

if __name__ == "__main__":
    main()

'''работа на консоли:
Введите количество вершин (рекомендуется 10):
10
Введите количество ребер (рекомендуется 15):
15
Введите ребра в формате 'u v' (вершины с 1):
Ребро 1: 1 2
Ребро 2: 1 3
Ребро 3: 1 4
Ребро 4: 2 3
Ребро 5: 2 5
Ребро 6:  2 6
Ребро 7: 3 4
Ребро 8:  3 7
Ребро 9: 4 8
Ребро 10: 4 9
Ребро 11: 5 6
Ребро 12: 5 10
Ребро 13: 6 7
Ребро 14: 7 8
Ребро 15: 8 9

Запуск алгоритма имитации отжига...
Начальная температура: 1000
Минимальная оценка цветов: 5

Итерация	Температура	Конфликты	Цвета
--------------------------------------------------
       0	   1000.00	        15	       1
      50	     26.56	        15	       1
     100	      0.71	        15	       1
     150	      0.02	        15	       1

==================================================
РЕЗУЛЬТАТЫ:
==================================================
Количество использованных цветов: 1
Количество конфликтов: 15

Раскраска вершин:
Вершина 1: Цвет 1
Вершина 2: Цвет 1
Вершина 3: Цвет 1
Вершина 4: Цвет 1
Вершина 5: Цвет 1
Вершина 6: Цвет 1
Вершина 7: Цвет 1
Вершина 8: Цвет 1
Вершина 9: Цвет 1
Вершина 10: Цвет 1

⚠ Раскраска имеет 15 конфликт(ов)'''

