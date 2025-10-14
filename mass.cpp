#include <iostream>
using namespace std;

int main() {
    const int SIZE = 6;
    int arr[SIZE] = {12, 7, 25, 8, 3, 14};
    
    cout << "Чётные числа: ";
    for (int i = 0; i < SIZE; i++) {
        if (arr[i] % 2 == 0) {
            cout << arr[i] << " ";
        }
    }
    cout << endl;
    
    cout << "Нечётные числа: ";
    for (int i = 0; i < SIZE; i++) {
        if (arr[i] % 2 != 0) {
            cout << arr[i] << " ";
        }
    }
    cout << endl;
    
    int evenSum = 0;
    for (int i = 0; i < SIZE; i++) {
        if (arr[i] % 2 == 0) {
            evenSum += arr[i];
        }
    }
    cout << "Сумма чётных чисел: " << evenSum << endl;
    
    return 0;
}