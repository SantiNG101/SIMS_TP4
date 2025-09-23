import java.util.List;

public interface Integrator {
    void step(List<Particle> particles, ForceCalculator forceCalculator, double dt);
}

