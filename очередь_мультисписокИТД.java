// Создание мультисписка на языке java
public class Node {
    int data;
    Node prev;
    Node next;
    public Node(int data)
    {
        this.data = data;
        this.prev = null;
        this.next = null;
    }
}
public class DoublyLinkedList {
    Node head;
    Node tail;
    public DoublyLinkedList()
    {
        this.head = null;
        this.tail = null;
    }
}


// Создание очереди на языке java
import java.util.LinkedList;
import java.util.Queue;

public class FruitQueue {
    public static void main(String[] args) {
        Queue<String> queue = new LinkedList<>();
        queue.add("арбуз");
        queue.add("драгонфрукт");
        queue.add("личи");

        System.out.println("Очередь: " + queue);
    }
}


// Реализация дека на языке java
import java.util.ArrayDeque;
import java.util.Deque;

public class Deque {
    public static void main(String[] args) {
        Deque<Integer> stack = new ArrayDeque<>();

        stack.push(3);
        stack.push(5);
        stack.push(4);

        while (!stack.isEmpty()) {
            System.out.println("Извлек: " + stack.pop());
        }
    }
}


// Создание приоритетной очереди на языке java
import java.util.PriorityQueue;
import java.util.Comparator;

public class PriorityQueue {
    public static void main(String[] args) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.offer(33);
        minHeap.offer(13);
        minHeap.offer(1);
        minHeap.offer(290);
        while (!minHeap.isEmpty()) {
            System.out.println(minHeap.poll());
        }
    }
}