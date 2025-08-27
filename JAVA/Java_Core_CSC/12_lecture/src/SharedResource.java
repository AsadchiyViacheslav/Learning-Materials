import java.util.concurrent.locks.ReentrantLock;

class SharedResource {
    private final ReentrantLock lock = new ReentrantLock();
    private int counter = 0;

    public void increment() {
        lock.lock(); // блокировка
        try {
            counter++;
        } finally {
            lock.unlock(); // обязательно освобождать!
        }
    }

    public int getCounter() {
        return counter;
    }
}
