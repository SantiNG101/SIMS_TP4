public class GravityForce implements ForceCalculator {
    private double G;
    private double h;

    public GravityForce(double G, double h) {
        this.G = G;
        this.h = h;
    }

    @Override
    public void computeForces(Particle[] particles) {

        int n = particles.length;
        for (int i = 0; i < n; i++) particles[i].a.set(new Vector(0, 0, 0));
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                Vector rij = particles[j].r.sub(particles[i].r);
                double dist2 = rij.x*rij.x + rij.y*rij.y + rij.z*rij.z + h*h;
                double inv = 1.0 / Math.pow(dist2, 1.5);
                double mag = G * particles[i].m * particles[j].m * inv;

                // fuerza atractiva
                Vector fij = rij.mul(mag);

                // aplicar a cada partícula
                particles[i].a = particles[i].a.add(fij.mul(1.0 / particles[i].m));
                particles[j].a = particles[j].a.add(fij.mul(-1.0 / particles[j].m));
            }
        }
    }
}



