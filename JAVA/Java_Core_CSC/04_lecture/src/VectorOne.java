/**
 * Class Vector
 */

public interface VectorOne {
    /**
     * Returns a vector component
     * @param n component number, must be 0 (X) 1 (Y) or 2 (Z)
     * @return a value of the corresponding vector component
     */
    double component(int n);
    /**
     * @return a vector length
     */
    double length();
    /**
     * Sums of two vectors
     * @param other another vector
     */
    VectorOne plus(VectorOne other);
}
