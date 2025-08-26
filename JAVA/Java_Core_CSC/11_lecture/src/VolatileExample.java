public class VolatileExample {
    private static volatile boolean running = true;

    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            while (running) { // всегда читаем из памяти
            }
            System.out.println("Stopped");
        });

        t.start();
        Thread.sleep(1000);
        running = false; // сразу видно в другом потоке
    }
}
