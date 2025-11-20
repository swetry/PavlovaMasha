#вариант 5 джава
import java.util.Scanner;
import java.util.Random;

public class SimulatedAnnealing {

    public static double saSquare(double temp, double cooling) {
        Random random = new Random();
        double x = random.nextDouble() * 20 - 10; // случайное начальное значение в [-10, 10]
        double energy = x * x;

        while (temp > 1e-6) {
            // Генерируем новое решение в окрестности текущего
            double xNew = x + (random.nextDouble() * 2 - 1) * temp;
            // Ограничиваем xNew диапазоном [-10, 10]
            if (xNew < -10) xNew = -10;
            if (xNew > 10) xNew = 10;

            double energyNew = xNew * xNew;

            // Критерий Метрополиса: принимаем новое решение, если оно лучше
            // или с вероятностью exp(-(energyNew - energy) / temp), если хуже
            if (energyNew < energy || 
                Math.random() < Math.exp(-(energyNew - energy) / temp)) {
                x = xNew;
                energy = energyNew;
            }

            temp *= cooling; // уменьшаем температуру
        }

        return x;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите начальную температуру (например, 100.0): ");
        double initialTemp = scanner.nextDouble();

        System.out.print("Введите коэффициент охлаждения (например, 0.99): ");
        double coolingRate = scanner.nextDouble();

        scanner.close();

        double optimalX = saSquare(initialTemp, coolingRate);
        double optimalValue = optimalX * optimalX;

        System.out.printf("Оптимальное значение x: %.6f%n", optimalX);
        System.out.printf("Значение функции f(x) = x²: %.6f%n", optimalValue);
    }
}
'''пример работы консоли:
Введите начальную температуру (например, 100.0): 100.0
Введите коэффициент охлаждения (например, 0.99): 0.99
Оптимальное значение x: 0.001234
Значение функции f(x) = x²: 0.000002'''
