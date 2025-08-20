public class Test {
    static class MyException extends Exception{

    }

    static void test() throws MyException {
        throw new MyException();
    }

    public static void main(String[] args) throws MyException {
        test();
    }

    public static void main2(String[] args) {
        try {
            test();
        }
        catch (MyException ex) {
            ex.printStackTrace();
        }
    }
}
