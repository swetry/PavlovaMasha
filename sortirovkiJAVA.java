//сортировка выбором

public class SelectionSort {
    
    // Метод для сортировки массива целых чисел
    public static void selectionSort(int[] array) {  
        
        int n = array.length;           // Получаем длину массива

        for (int i = 0; i < n - 1; i++) {   // Внешний цикл проходит по каждому элементу массива
            
            int minIndex = i;               // Предположительно минимальный индекс на каждом этапе
            
            // Внутренний цикл ищет наименьший элемент среди оставшихся элементов
            for (int j = i + 1; j < n; j++) {
                if (array[j] < array[minIndex]) {   
                    minIndex = j;          // Обновляем индекс минимального элемента
                }
            }
            
            // Меняем местами найденный минимум с элементом на текущей позиции
            swap(array, i, minIndex);      
        }
    }

    // Вспомогательная функция для обмена двух элементов массива
    private static void swap(int[] arr, int a, int b) {
        int temp = arr[a];                  // Сохраняем значение первого элемента
        arr[a] = arr[b];                    // Перезаписываем первый элемент вторым
        arr[b] = temp;                      // Второй элемент заменяется сохранённым значением
    }

    // Основной метод для проверки работоспособности сортировки
    public static void main(String[] args) {
        int[] data = {64, 25, 12, 22, 11};  // Исходный массив для тестирования
        
        System.out.println("Исходный массив:");
        printArray(data);                   // Печать исходного массива перед сортировкой
        
        selectionSort(data);                // Запуск сортировки методом выбора
        
        System.out.println("\nОтсортированный массив:");
        printArray(data);                   // Печать отсортированного массива
    }

    // Функция печати массива для вывода результата
    private static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");  // Проходим по всему массиву и выводим каждый элемент
        }
    }
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////
//сортировка обменом (пузырек)

public class BubbleSort {

    // Метод для сортировки массива целочисленных значений
    public static void bubbleSort(int[] array) {
        int n = array.length;              // Определяем размер массива
        
        boolean swapped;                   // Флаг для отслеживания наличия перестановок
        
        // Внешний цикл проходит по массиву столько раз, сколько элементов в нём
        for (int i = 0; i < n - 1; i++) {
            swapped = false;              // Изначально считаем, что перестановок нет
            
            // Внутренний цикл сравнивает соседние пары элементов
            for (int j = 0; j < n - i - 1; j++) {
                
                // Если левый элемент больше правого, меняем их местами
                if (array[j] > array[j + 1]) {
                    int temp = array[j];       // Создаем временную переменную для обмена
                    array[j] = array[j + 1];   // Левый элемент становится равным правому
                    array[j + 1] = temp;       // Правый элемент принимает старое левое значение
                    
                    swapped = true;            // Отмечаем, что произошла перестановка
                }
            }
            
            // Если ни одна пара не была поменяна местами, значит массив уже отсортирован
            if (!swapped) break;               // Выходим досрочно из внешнего цикла
        }
    }

    // Вспомогательный метод для отображения массива
    public static void printArray(int[] array) {
        for (int num : array) {
            System.out.print(num + " ");       // Выводим каждый элемент массива
        }
        System.out.println();                  // Переход на новую строку
    }

    // Основная точка входа в программу
    public static void main(String[] args) {
        int[] data = {64, 34, 25, 12, 22, 11, 90};
        
        System.out.println("Исходный массив:");
        printArray(data);                     // Показываем исходный массив
        
        bubbleSort(data);                     // Сортируем массив методом пузырьковой сортировки
        
        System.out.println("Отсортированный массив:");
        printArray(data);                     // Показываем отсортированный массив
    }
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
//сортировка слиянием
// Реализация сортировки слиянием на Java

public class MergeSort {
    
    // Основной метод сортировки
    public static void mergeSort(int[] array) {     
        if (array.length > 1) {   // Если массив больше одного элемента, выполняем рекурсивную сортировку
            int mid = array.length / 2;      // Определяем середину массива
            
            // Разделяем исходный массив на две части
            int[] leftArray = new int[mid];       // Левый подмассив
            int[] rightArray = new int[array.length - mid];     // Правый подмассив
            
            for (int i = 0; i < mid; i++) {           // Копируем элементы левой половины
                leftArray[i] = array[i];
            }
            
            for (int i = mid; i < array.length; i++) { // Копируем элементы правой половины
                rightArray[i - mid] = array[i];
            }
            
            // Рекурсивно сортируем обе половинки
            mergeSort(leftArray);                      // Сортируем левую половину
            mergeSort(rightArray);                     // Сортируем правую половину
            
            // После сортировки обеих частей объединяем их обратно
            merge(array, leftArray, rightArray);
        }
    }
    
    // Метод объединения двух отсортированных подмассивов
    private static void merge(int[] result, int[] leftArray, int[] rightArray) {
        int i = 0;                 // Индекс левого подмассива
        int j = 0;                 // Индекс правого подмассива
        int k = 0;                 // Индекс результирующего массива
        
        while (i < leftArray.length && j < rightArray.length) {  // Пока оба подмассива не исчерпаны
            if (leftArray[i] <= rightArray[j]) {               // Если элемент слева меньше или равен элементу справа
                result[k++] = leftArray[i++];                  // Добавляем левый элемент в итоговый массив
            } else {
                result[k++] = rightArray[j++];                 // Иначе добавляем правый элемент
            }
        }
        
        // Добавляем оставшиеся элементы из левого подмассива, если они остались
        while (i < leftArray.length) {
            result[k++] = leftArray[i++];
        }
        
        // Добавляем оставшиеся элементы из правого подмассива, если они остались
        while (j < rightArray.length) {
            result[k++] = rightArray[j++];
        }
    }
}
public static void main(String[] args) {
    int[] array = {8, 4, 2, 1};
    System.out.println("Исходный массив:");
    printArray(array);

    mergeSort(array);                  // Выполняем сортировку

    System.out.println("\nОтсортированный массив:");
    printArray(array);
}

private static void printArray(int[] arr) {
    for (int num : arr) {
        System.out.print(num + " ");
    }
}
////////////////////////////////////////////////////////////////////////////////////////////////////////

public class ShellSort {
    
    // Метод для сортировки массива методом Шелла
    public static void shellSort(int[] array) {
        
        int n = array.length; // Получаем длину массива
        
        for (int gap = n / 2; gap > 0; gap /= 2) { // Начальное значение шага (gap)
            // Проходим массив начиная с текущего значения шага (gap)
            for (int i = gap; i < n; i++) {
                int temp = array[i]; // Берём элемент для вставки
                
                // Перемещаемся назад через элементы, пока находим меньшие числа
                int j = i;
                while (j >= gap && array[j - gap] > temp) {
                    array[j] = array[j - gap]; // Смещение элемента вперёд
                    j -= gap;                  // Переход к предыдущему элементу с шагом gap
                }
                
                array[j] = temp; // Ставим нужный элемент на своё место
            }
        }
    }

    // Тестируем алгоритм на примере массива чисел
    public static void main(String[] args) {
        int[] arr = {23, 12, 8, 15, 34};
        System.out.println("Исходный массив:");
        printArray(arr);
        
        shellSort(arr); // Сортируем массив
        
        System.out.println("\nОтсортированный массив:");
        printArray(arr);
    }

    // Вспомогательная функция вывода элементов массива
    private static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");
        }
    }
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
