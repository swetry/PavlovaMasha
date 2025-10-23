#include <iostream>
#include <set>
#include <algorithm>

int main() {
    std::multiset<int> myMultiset;

    myMultiset.insert(10);
    myMultiset.insert(20);
    myMultiset.insert(10);
    myMultiset.insert(30);
    myMultiset.insert(20);

    std::cout << "Элементы мультисписка:" << std::endl;
    for (int val : myMultiset) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    myMultiset.erase(10);

    std::cout << "Элементы после удаления одного 10:" << std::endl;
    for (int val : myMultiset) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    return 0;
}
