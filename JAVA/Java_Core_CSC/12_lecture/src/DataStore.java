import java.util.concurrent.locks.ReentrantReadWriteLock;

class DataStore {
    private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
    private String data = "init";

    public void write(String newData) {
        rwLock.writeLock().lock();
        try {
            data = newData;
        } finally {
            rwLock.writeLock().unlock();
        }
    }

    public String read() {
        rwLock.readLock().lock();
        try {
            return data;
        } finally {
            rwLock.readLock().unlock();
        }
    }
}
