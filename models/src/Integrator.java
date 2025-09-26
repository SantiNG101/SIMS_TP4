
public interface Integrator {
    void step(Particle[] particles, double dt, ForceCalculator fc);
    String name();
}


