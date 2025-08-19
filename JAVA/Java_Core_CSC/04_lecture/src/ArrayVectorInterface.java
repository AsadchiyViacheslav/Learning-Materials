public class ArrayVectorInterface implements VectorOne{
    double[] arr;

    ArrayVectorInterface(double x, double y, double z) {arr = new double[] {x, y, z}; }

    @Override
    public double component(int n) {
        return arr[n];
    }

    @Override
    public double length() {
        return Math.sqrt(Math.pow(arr[0], 2) + Math.pow(arr[1], 2) + Math.pow(arr[2], 2));
    }

    @Override
    public VectorOne plus(VectorOne other){
        return new ArrayVectorInterface(arr[0] + other.component(0),
                                        arr[1] + other.component(1),
                                        arr[2] + other.component(2));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof VectorOne)) return false;
        VectorOne that = (VectorOne) o;
        return this.component(0) == that.component(0) &&
                this.component(1) == that.component(1) &&
                this.component(2) == that.component(2);
    }
}
