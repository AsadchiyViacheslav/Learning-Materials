public class BankAccount {
    private String owner;
    private double balance;
    public static String bankName = "Sber";
    public static int accountCount;
    private final int accountId;

    public BankAccount(String owner, double balance){
        this.owner = owner;
        this.balance = balance;

        this.accountId = accountCount + 1;
        accountCount++;
    }

    public void deposit(double amount){
        if (amount > 0) {
            balance += amount;
        } else {
            System.out.println("Отрицательная сумма!");
        }
    }

    public void withdraw(double amount){
        if (balance - amount >= 0){
            balance -= amount;
        } else {
            System.out.println("Недостаточно средств");
        }
    }

    public final void printInfo(){
        System.out.println("Account info: owner: " + owner + " balance: " + balance + " id: " + accountId);
    }

    public final void printInfo(String extra){
        System.out.println("Account info: owner: " + owner + " balance: " + balance + " id: " + accountId + " extra: " + extra);
    }

    public final void printInfo(int years){
        System.out.println("Account info: owner: " + owner + " balance: " + balance + " id: " + accountId);
        simulateYears(years);
    }

    public static int getAccountCount(){
        return accountCount;
    }

    private void simulateYears(int years){
        for (int year = 1; year <= years; year++){
            balance = balance + balance * 0.5;
            System.out.println("Баланс на год " + year + " после открытия равен " + balance);
        }
    }
}
