public class Gear5Integrator implements Integrator {

    // Coeficientes Gear predictor-corrector orden 5
    private static final double A0 = 3.0 / 16.0;
    private static final double A1 = 251.0 / 360.0;
    private static final double A2 = 1.0;
    private static final double A3 = 11.0 / 18.0;
    private static final double A4 = 1.0 / 6.0;
    private static final double A5 = 1.0 / 60.0;

@Override
public void step(Particle[] p, double dt, ForceCalculator fc) {
    int n = p.length;

    double dt2 = dt * dt;
    double dt3 = dt2 * dt;
    double dt4 = dt3 * dt;
    double dt5 = dt4 * dt;

    // Guardar las derivadas actuales para la predicción
    for (Particle pi : p) {
        pi.r_prev = new Vector(pi.r.x, pi.r.y, pi.r.z);
        pi.v_prev = new Vector(pi.v.x, pi.v.y, pi.v.z);
        pi.r2_prev = new Vector(pi.r2.x, pi.r2.y, pi.r2.z);
        pi.r3_prev = new Vector(pi.r3.x, pi.r3.y, pi.r3.z);
        pi.r4_prev = new Vector(pi.r4.x, pi.r4.y, pi.r4.z);
        pi.r5_prev = new Vector(pi.r5.x, pi.r5.y, pi.r5.z);
    }

    // 1) Predicción
    for (Particle pi : p) {
        Vector rp = pi.r_prev
                .add(pi.v_prev.mul(dt))
                .add(pi.r2_prev.mul(dt2 / 2.0))
                .add(pi.r3_prev.mul(dt3 / 6.0))
                .add(pi.r4_prev.mul(dt4 / 24.0))
                .add(pi.r5_prev.mul(dt5 / 120.0));

        Vector r1p = pi.v_prev
                .add(pi.r2_prev.mul(dt))
                .add(pi.r3_prev.mul(dt2 / 2.0))
                .add(pi.r4_prev.mul(dt3 / 6.0))
                .add(pi.r5_prev.mul(dt4 / 24.0));

        Vector r2p = pi.r2_prev
                .add(pi.r3_prev.mul(dt))
                .add(pi.r4_prev.mul(dt2 / 2.0))
                .add(pi.r5_prev.mul(dt3 / 6.0));

        Vector r3p = pi.r3_prev
                .add(pi.r4_prev.mul(dt))
                .add(pi.r5_prev.mul(dt2 / 2.0));

        Vector r4p = pi.r4_prev.add(pi.r5_prev.mul(dt));
        Vector r5p = pi.r5_prev; // La predicción de r5 es r5_prev

        // Asignar los valores predichos a las variables de la partícula
        pi.r.set(rp);
        pi.v.set(r1p);
        pi.r2.set(r2p);
        pi.r3.set(r3p);
        pi.r4.set(r4p);
        pi.r5.set(r5p);
    }

    // 2) Evaluar fuerzas (usa la posición predicha)
    fc.computeForces(p);

    // 3) Corrección
    for (Particle pi : p) {
        // Usa la aceleración calculada y la aceleración predicha para el delta
        Vector delta2 = pi.a.sub(pi.r2);

            // La implementación es correcta para estos coeficientes A_k
            pi.r  = pi.r.add(delta2.mul(A0 * dt * dt / 2.0));
            pi.v  = pi.v.add(delta2.mul(A1 * dt));
            pi.r2 = pi.r2.add(delta2.mul(A2));
            pi.r3 = pi.r3.add(delta2.mul(A3 / dt));
            pi.r4 = pi.r4.add(delta2.mul(A4 / (dt * dt)));
            pi.r5 = pi.r5.add(delta2.mul(A5 / (dt * dt * dt)));

            pi.a.set(pi.r2); // consistencia
        }
    }

    @Override
    public String name() {
        return "Gear5";
    }

public static void initializeOscillatorDerivatives(Particle p, double k, double gamma) {
        double m = p.m;
        p.r2.set(p.a);
        p.r3.set(p.v.mul(-k / m).add(p.a.mul(-gamma / m)));
        p.r4.set(p.a.mul(-k / m).add(p.r3.mul(-gamma / m)));
        p.r5.set(p.r3.mul(-k / m).add(p.r4.mul(-gamma / m)));
    }
}





