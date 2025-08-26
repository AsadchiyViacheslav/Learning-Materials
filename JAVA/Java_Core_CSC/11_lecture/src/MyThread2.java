class MyThread2 implements Runnable {
    public void run() {
        System.out.println("Выполняется задача в " + Thread.currentThread().getName());
    }
}