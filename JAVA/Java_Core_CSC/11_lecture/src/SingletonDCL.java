public class SingletonDCL {
    private static volatile SingletonDCL instance; // volatile важно!

    private SingletonDCL() {}

    public static SingletonDCL getInstance() {
        if (instance == null) {  // 1-я проверка (без блокировки)
            synchronized (SingletonDCL.class) {
                if (instance == null) { // 2-я проверка (с блокировкой)
                    instance = new SingletonDCL();
                }
            }
        }
        return instance;
    }
}