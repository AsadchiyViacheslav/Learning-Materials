public class SyncExample {
    private static int counter = 0;

    // синхронизированный метод
    public synchronized static void increment() {
        counter++;
    }

    public static void main(String[] args) throws InterruptedException {
        Runnable task = () -> {
            for (int i = 0; i < 1000; i++) {
                increment(); // только один поток может зайти
            }
        };

        Thread t1 = new Thread(task);
        Thread t2 = new Thread(task);

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("Итог: " + counter); // всегда 2000
    }
}
