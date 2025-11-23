//Блочная (корзинная) сортировка
def insertion_sort(arr):
    """Простая сортировка вставками"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def bucket_sort(arr):
    """
    Блочная (корзинная) сортировка.
    
    :param arr: Список чисел для сортировки
    :return: Отсортированный список
    """
    if not arr or len(arr) <= 1:
        return arr

    # Определяем минимальное и максимальное значение списка
    min_val = min(arr)
    max_val = max(arr)
    
    # Количество корзин выбирается равным длине списка
    num_buckets = len(arr)
    buckets = [[] for _ in range(num_buckets)]

    # Распределение элементов по корзинам
    for value in arr:
        index = int((value - min_val) / (max_val - min_val) * (num_buckets - 1))  # Нормализуем индекс
        buckets[index].append(value)

    # Сортируем каждую отдельную корзину
    sorted_arr = []
    for bucket in buckets:
        sorted_bucket = insertion_sort(bucket)
        sorted_arr.extend(sorted_bucket)

    return sorted_arr


if __name__ == "__main__":
    input_list = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    print("Исходный список:", input_list)
    sorted_list = bucket_sort(input_list)
    print("Отсортированный список:", sorted_list)
//вывод из консоли: Исходный список: [0.78, 0.17, 0.39, 0.26, 0.72, 0.9399999999999999, 0.21, 0.12, 0.23, 0.68]
//Отсортированный список: [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.9399999999999999]

//блинная сортировка
def flip(arr, k):
    # Переворот первых k элементов массива
    arr[:k+1] = arr[:k+1][::-1]

def find_max_idx(arr, n):
    # Поиск индекса максимального элемента среди первых n элементов
    max_idx = 0
    for i in range(n):
        if arr[i] > arr[max_idx]:
            max_idx = i
    return max_idx

def pancake_sort(arr):
    curr_size = len(arr)
    
    while curr_size > 1:
        # Шаг 1: находим индекс максимального элемента в текущем сегменте
        max_idx = find_max_idx(arr, curr_size)
        
        if max_idx != curr_size - 1:
            # Если максимум не находится в конце сегмента,
            # сначала поднимаем его вверх, потом опускаем в конец
            
            # Шаг 2: переворачиваем отрезок до максимума включительно
            flip(arr, max_idx)
            
            # Шаг 3: переворачиваем весь текущий сегмент
            flip(arr, curr_size - 1)
        
        # Уменьшаем размер обрабатываемого сегмента
        curr_size -= 1
    
    return arr

# Тестирование
arr = [3, 6, 2, 4, 5, 1]
sorted_arr = pancake_sort(arr)
print("Отсортированный массив:", sorted_arr)
//Отсортированный массив: [1, 2, 3, 4, 5, 6]

//Сортировка бусинами (гравитационная)
def bead_sort(arr):
    """
    Сортировка бусинами (гравитационная сортировка)
    Работает только с неотрицательными целыми числами
    """
    if not arr:
        return arr
    
    # Проверяем, что все элементы неотрицательные
    if any(x < 0 for x in arr):
        raise ValueError("Сортировка бусинами работает только с неотрицательными числами")
    
    if len(arr) <= 1:
        return arr
    
    max_val = max(arr)
    beads = [[0] * max_val for _ in range(len(arr))]
    
    # Размещаем бусины на рейках
    for i in range(len(arr)):
        for j in range(arr[i]):
            beads[i][j] = 1
    
    print("Исходное расположение бусин:")
    for row in beads:
        print(' '.join('●' if x else '○' for x in row))
    print()
    
    # Симулируем падение бусин
    for j in range(max_val):
        beads_count = 0
        for i in range(len(arr)):
            beads_count += beads[i][j]
            beads[i][j] = 0
        
        for i in range(len(arr) - beads_count, len(arr)):
            beads[i][j] = 1
    
    print("После 'падения' бусин:")
    for row in beads:
        print(' '.join('●' if x else '○' for x in row))
    print()
    
    result = [sum(row) for row in beads]
    return result

# Тестирование алгоритма
def test_bead_sort():
    print("=== ТЕСТИРОВАНИЕ СОРТИРОВКИ БУСИНАМИ ===\n")
    
    # Всего один тестовый список из 7 элементов
    test_arr = [3, 1, 4, 1, 5, 2, 3]
    
    print(f"Исходный массив: {test_arr}")
    print(f"Ожидаемый результат: {sorted(test_arr)}")
    print("\nПроцесс сортировки:")
    
    sorted_arr = bead_sort(test_arr.copy())
    
    print(f"Полученный результат: {sorted_arr}")
    
    # Проверяем корректность
    if sorted_arr == sorted(test_arr):
        print("✓ Тест пройден! Сортировка работает корректно")
    else:
        print("✗ Тест не пройден! Ошибка в сортировке")

# Демонстрация работы алгоритма
def demo_bead_sort():
    print("=== ДЕМОНСТРАЦИЯ СОРТИРОВКИ БУСИНАМИ ===\n")
    
    # Демонстрационный список из 6 элементов
    demo_arr = [2, 4, 1, 3, 2, 1]
    
    print(f"Демонстрационный массив: {demo_arr}")
    print("\nПроцесс сортировки:")
    
    result = bead_sort(demo_arr.copy())
    print(f"Итоговый результат: {result}")

# Основная программа
if __name__ == "__main__":
    # Демонстрация
    demo_bead_sort()
    
    print("\n" + "="*50 + "\n")
    
    # Тестирование
    test_bead_sort()
    
    # Дополнительная проверка на другом наборе
    print("\n" + "="*50)
    print("\nДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА:")
    another_arr = [1, 3, 2, 2, 1, 4, 2]
    print(f"Массив: {another_arr}")
    result = bead_sort(another_arr.copy())
    print(f"Результат: {result}")
    print(f"Проверка: {'✓ Верно' if result == sorted(another_arr) else '✗ Ошибка'}")
//Результат: [1, 1, 2, 2, 2, 3, 4]

//Поиск скачками (Jump Search)
import math

def jump_search(arr, x):
    n = len(arr)
    
    # Определяем размер шага ("jump")
    step = int(math.sqrt(n))
    
    prev = 0
    
    # Находим блок, где элемент находится (если вообще присутствует)
    while arr[min(step, n)-1] < x:
        prev = step
        step += int(math.sqrt(n))
        
        if prev >= n:
            return None  # Элемент отсутствует
            
    # Линейный поиск внутри блока
    for i in range(prev, min(step, n)):
        if arr[i] == x:
            return i  # Возвращаем индекс найденного элемента
            
    return None  # Если элемент не найден

# Тестируем алгоритм
arr = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
x = 13

result = jump_search(arr, x)
if result is not None:
    print(f'Элемент {x} найден на индексе {result}')
else:
    print('Элемент не найден')
//Элемент 13 найден на индексе 7

//Экспоненциальный поиск (Exponential Search) 
def binary_search(arr, left, right, x):
    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def exponential_search(arr, n, x):
    # Проверяем первый элемент
    if arr[0] == x:
        return 0

    i = 1
    # Удвоение индекса пока значение меньше искомого элемента
    while i < n and arr[i] <= x:
        i *= 2

    # Возвращаемся назад, если вышли за пределы массива
    last_idx = min(i, n)
    
    # Применяем бинарный поиск в диапазоне от предыдущего значения до текущего удвоенного
    return binary_search(arr, i//2, last_idx-1, x)


# Тестируем алгоритм
arr = sorted([10, 12, 13, 16, 18, 19, 20, 21, 22, 23, 24, 33, 35, 42, 47])
n = len(arr)
target = 22

result = exponential_search(arr, n, target)
if result != -1:
    print(f'Элемент {target} найден на индексе {result}')
else:
    print('Элемент не найден')
//Элемент 22 найден на индексе 8
