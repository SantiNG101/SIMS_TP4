public class Particle {
    public int id;
    public double m = 1.0;

    public Vector r = new Vector();
    public Vector v = new Vector();
    public Vector a = new Vector();

    // para Beeman
    public Vector a_prev = new Vector();

    // para Gear predictor-corrector
    public Vector r2 = new Vector();
    public Vector r3 = new Vector();
    public Vector r4 = new Vector();
    public Vector r5 = new Vector();

    public Particle(int id) {
        this.id = id;
    }
}
