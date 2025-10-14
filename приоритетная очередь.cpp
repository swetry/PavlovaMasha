#include <iostream>
#include <queue> // Подключение заголовочного файла priority_queue

int main() {
    std::priority_queue<int> pq;
    pq.push(30);
    pq.push(100);
    pq.push(25);
    pq.push(40);

    std::cout << "Элементы приоритетной очереди (по убыванию):" << std::endl;
    while (!pq.empty()) {
        std::cout << pq.top() << " "; // Получаем верхний элемент
        pq.pop();                     
    }
    std::cout << std::endl;

    return 0;
}