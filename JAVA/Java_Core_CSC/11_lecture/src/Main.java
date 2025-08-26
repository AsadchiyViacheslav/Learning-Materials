public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new MyThread1();
        t1.start(); // запускаем поток


        Thread t = new Thread(new MyThread2());
        t.start();

        Thread t2 = new Thread(() -> {
            System.out.println("Выполняется задача через лямбду");
        });
        t2.start();


        // synchronized
        Counter counter = new Counter();

        Thread t3 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) counter.increment();
        });

        Thread t4 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) counter.increment();
        });

        t3.start();
        t4.start();
        t3.join();
        t4.join();

        System.out.println("Результат: " + counter.getCount()); // всегда 2000
    }
}