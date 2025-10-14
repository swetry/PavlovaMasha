#include <iostream>
#include <deque>

int main() {
    std::deque<int> myDeque;

    myDeque.push_back(10);
    myDeque.push_front(5);
    myDeque.push_back(20);
    myDeque.push_front(2);

    std::cout << "Первый элемент: " << myDeque.front() << std::endl;
    std::cout << "Последний элемент: " << myDeque.back() << std::endl;
    std::cout << "Элемент по индексу 1: " << myDeque[1] << std::endl;

    std::cout << "Все элементы: ";
    for (auto const& element : myDeque) {
        std::cout << element << " ";
    }
    std::cout << std::endl;

    myDeque.pop_back();
    myDeque.pop_front();

    return 0;
}