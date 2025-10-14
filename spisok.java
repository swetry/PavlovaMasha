import java.util.LinkedList;
import java.util.Collections;

public class Main {
    public static void main(String[] args) {
        LinkedList<Integer> myList = new LinkedList<>();
        // Добавляем элементы в список
        myList.add(64);
        myList.add(34);
        myList.add(25);
        myList.add(12);
        myList.add(22);
        myList.add(11);
        myList.add(90);
        
        System.out.print("Исходный список: ");
        for (int num : myList) {
            System.out.print(num + " ");
        }
        System.out.println();
        
        // Сортировка списка
        Collections.sort(myList);
        
        System.out.print("После сортировки: ");
        for (int num : myList) {
            System.out.print(num + " ");
        }
        System.out.println();
        
        // Реверс списка
        Collections.reverse(myList);
        
        System.out.print("После реверса: ");
        for (int num : myList) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}