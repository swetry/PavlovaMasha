//пирамидальная сортировка
#include <iostream>
using namespace std;

// Функционал для построения max-кучи (перестановка элементов сверху вниз)
void heapify(int arr[], int n, int root) {
    int largest = root;      // Начнем с предположения, что корень - максимальный элемент
    int leftChild = 2 * root + 1; // Левый ребенок узла
    int rightChild = 2 * root + 2; // Правый ребенок узла

    // Проверяем, существует ли левый ребёнок и является ли он больше корня
    if (leftChild < n && arr[leftChild] > arr[largest])
        largest = leftChild;

    // Проверяем, существует ли правый ребёнок и является ли он больше текущего наибольшего
    if (rightChild < n && arr[rightChild] > arr[largest])
        largest = rightChild;

    // Если самый большой элемент не равен корню, производим обмен
    if (largest != root) {
        swap(arr[root], arr[largest]); // Переставляем элементы местами
        heapify(arr, n, largest); // Рекурсивно восстанавливаем кучу снизу вверх
    }
}

// Основная процедура пирамидальной сортировки
void heapSort(int arr[], int n) {
    // Строим max-кучу из входящего массива
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);

    // Один за другим извлекаем корни из кучи
    for (int i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]); // Перемещение максимального элемента в конец массива
        heapify(arr, i, 0); // Восстанавливаем кучу снова
    }
}

// Процедура печати массива
void printArray(int arr[], int size) {
    for (int i=0; i<size; ++i)
        cout << arr[i] << " ";
    cout << endl;
}

// Точка входа в программу
int main() {
    int arr[] = {12, 11, 13, 5, 6, 7};
    int n = sizeof(arr)/sizeof(arr[0]);

    cout << "Исходный массив:\n";
    printArray(arr, n);

    heapSort(arr, n); // Сортируем массив методом Heap Sort

    cout << "\nОтсортированный массив:\n";
    printArray(arr, n);

    return 0;
}
/////////////////////////////////////////////////////////////////////////////////////////////
//бинарный поиск
#include <iostream>
using namespace std;

// Функция binarySearch реализует алгоритм бинарного поиска
int binarySearch(int arr[], int left, int right, int target) {
    while (left <= right) {                       // Пока диапазон поиска не пуст
        int mid = left + (right - left) / 2;      // Вычисляем середину диапазона
        
        if (arr[mid] == target)                   // Если центральный элемент равен целевому числу
            return mid;                           // Возвращаем индекс центрального элемента
        
        if (arr[mid] < target)                    // Если целевой элемент больше среднего
            left = mid + 1;                       // Продолжаем искать в правой половине
        else                                      // Иначе цель находится в левой половине
            right = mid - 1;                      // Уменьшаем правую границу
    }
    return -1;                                    // Если элемент не найден, возвращаем -1
}

// Главная функция для демонстрации работы алгоритма
int main() {
    int arr[] = {2, 3, 4, 10, 40};              // Отсортированный массив
    int n = sizeof(arr) / sizeof(arr[0]);        // Размер массива
    int target = 10;                             // Целевой элемент для поиска
    int result = binarySearch(arr, 0, n - 1, target); // Вызов функции бинарного поиска
    
    if(result == -1)                             // Если элемент не найден
        cout << "Элемент не найден." << endl;
    else                                         // Если элемент найден
        cout << "Элемент найден на индексе " << result << "." << endl;
    
    return 0;
}
///////////////////////////////////////////////////////////////////////////////////////////////////////
//интерполирующий поиск
#include <iostream>
using namespace std;

// Интерполирующий поиск по отсортированному массиву
int interpolationSearch(int arr[], int left, int right, int target) {
    while ((arr[right] != arr[left]) && (target >= arr[left]) && (target <= arr[right])) {
        // Рассчитываем приблизительную позицию искомого элемента
        int pos = left + (((double)(right - left) /
                        (arr[right] - arr[left])) *
                            (target - arr[left]));

        // Если элемент найден
        if (arr[pos] == target)
            return pos;

        // Если элемент меньше ожидаемого, смещаем правые границы
        if (arr[pos] < target)
            left = pos + 1;
        // Если элемент больше ожидаемого, смещаем левые границы
        else
            right = pos - 1;
    }

    // Последняя проверка, если целевой элемент равен последнему элементу массива
    if (target == arr[left])
        return left;

    // Если элемент не найден
    return -1;
}

// Главная функция для демонстрации работы алгоритма
int main() {
    int arr[] = {10, 12, 13, 16, 18, 19, 20, 21, 22, 23, 24, 33, 35, 42, 47};
    int n = sizeof(arr) / sizeof(arr[0]); // Вычисление размера массива
    int target = 18; // Цель поиска

    // Вызов функции интерполирующего поиска
    int index = interpolationSearch(arr, 0, n - 1, target);

    // Вывод результата
    if(index != -1)
        cout << "Индекс элемента " << target << ": " << index << endl;
    else
        cout << "Элемент не найден." << endl;

    return 0;
}
///////////////////////////////////////////////////////////////////////////////////////////////////////
