public class FieldVectorInterface implements VectorOne{
    double x, y, z;

    FieldVectorInterface(double x, double y, double z){
        this.x = x;
        this.y = y;
        this.z = z;
    }

    @Override
    public double component(int n){
        return switch (n) {
            case 0 -> x;
            case 1 -> y;
            case 2 -> z;
            default -> throw new IllegalArgumentException();
        };
    }

    @Override
    public double length() {
        return Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2) + Math.pow(z, 2));
    }

    @Override
    public VectorOne plus(VectorOne other){
        return new ArrayVectorInterface(x + other.component(0),
                y + other.component(1),
                z + other.component(2));
    }
}
