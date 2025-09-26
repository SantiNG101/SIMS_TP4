public class OscillatorForce implements ForceCalculator {
    private double k;
    private double gamma;
    private Vector r0 = new Vector(0, 0,
            0);
    public Particle osc;

    public OscillatorForce(double k, double gamma, Particle osc) {
        this.k = k;
        this.gamma = gamma;
        this.osc = osc;
    }

    @Override
    public void computeForces(Particle[] particles) {
        // único oscilador
        Particle p = osc;

        // F = -k (r - r0) - gamma v
        Vector F = p.r.sub(r0).mul(-k).add(p.v.mul(-gamma));
        p.a = F.mul(1.0 / p.m);
    }
}


