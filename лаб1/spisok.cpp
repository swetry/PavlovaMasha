#include <iostream>
#include <list>
using namespace std;

int main() {
    list<int> myList = {64, 34, 25, 12, 22, 11, 90};
    
    cout << "Исходный список: ";
    for (int num : myList) {
        cout << num << " ";
    }
    cout << endl;
    
    // Сортировка списка
    myList.sort();
    
    cout << "После сортировки: ";
    for (int num : myList) {
        cout << num << " ";
    }
    cout << endl;
    
    // Реверс списка
    myList.reverse();
    
    cout << "После реверса: ";
    for (int num : myList) {
        cout << num << " ";
    }
    cout << endl;
    
    return 0;
}
