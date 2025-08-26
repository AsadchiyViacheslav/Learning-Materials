class MyThread1 extends Thread {
    public void run() {
        System.out.println("Привет из потока " + Thread.currentThread().getName());
    }
}


