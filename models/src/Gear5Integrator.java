
public class Gear5Integrator implements Integrator {

    // Coeficientes Gear predictor-corrector orden 5 (fuerza depende solo de r)
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

        // 1) Predicción (Taylor hasta orden 5)
        for (Particle pi : p) {
            Vector rp = pi.r
                    .add(pi.v.mul(dt))
                    .add(pi.r2.mul(dt2 / 2.0))
                    .add(pi.r3.mul(dt3 / 6.0))
                    .add(pi.r4.mul(dt4 / 24.0))
                    .add(pi.r5.mul(dt5 / 120.0));

            Vector r1p = pi.v
                    .add(pi.r2.mul(dt))
                    .add(pi.r3.mul(dt2 / 2.0))
                    .add(pi.r4.mul(dt3 / 6.0))
                    .add(pi.r5.mul(dt4 / 24.0));

            Vector r2p = pi.r2
                    .add(pi.r3.mul(dt))
                    .add(pi.r4.mul(dt2 / 2.0))
                    .add(pi.r5.mul(dt3 / 6.0));

            Vector r3p = pi.r3
                    .add(pi.r4.mul(dt))
                    .add(pi.r5.mul(dt2 / 2.0));

            Vector r4p = pi.r4.add(pi.r5.mul(dt));

            Vector r5p = new Vector(pi.r5.x, pi.r5.y, pi.r5.z);

            // guardo los predichos en el propio objeto
            pi.r.set(rp);
            pi.v.set(r1p);
            pi.r2.set(r2p);
            pi.r3.set(r3p);
            pi.r4.set(r4p);
            pi.r5.set(r5p);
        }

        // 2) Evaluar fuerzas en posiciones predichas
        fc.computeForces(p);

     // 3) Corrección
        for (Particle pi : p) {
            // delta2 = a_actual - r2p
            // pi.r2 todavía contiene el valor predicho r2p
            Vector delta2 = pi.a.sub(pi.r2);

            // Se aplican las correcciones a las derivadas de la posición
            // r, v, r2, r3, r4, r5 usando las fórmulas estándar de Gear.
            // Los valores predichos (almacenados en pi.r, pi.v, etc.) se actualizan.
            pi.r  = pi.r.add(delta2.mul(A0 * dt * dt / 2.0));
            pi.v  = pi.v.add(delta2.mul(A1 * dt / 2.0));
            pi.r2 = pi.r2.add(delta2.mul(A2));
            pi.r3 = pi.r3.add(delta2.mul(A3 * 3.0 / dt));
            pi.r4 = pi.r4.add(delta2.mul(A4 * 12.0 / (dt * dt)));
            pi.r5 = pi.r5.add(delta2.mul(A5 * 60.0 / (dt * dt * dt)));

            // Se asegura que la aceleración de la partícula sea consistente con la derivada segunda corregida (r2).
            // Dado que A2 = 1, pi.r2 ahora es igual a la aceleración recién calculada pi.a.
            pi.a.set(pi.r2);
        }
    }

    @Override
    public String name() {
        return "Gear5";
    }

    /**
     * Inicializa r2..r5 de acuerdo a la fuerza del oscilador amortiguado
     * F = -k r - gamma v
     */
    public static void initializeOscillatorDerivatives(Particle p, double k, double gamma) {
        double m = p.m;
        // r2 = a = F/m
        p.r2.set(p.a);

        // r3 = -k/m * v - gamma/m * a
        p.r3.set(p.v.mul(-k / m).add(p.a.mul(-gamma / m)));

        // r4 = -k/m * a - gamma/m * r3
        p.r4.set(p.a.mul(-k / m).add(p.r3.mul(-gamma / m)));

        // r5 = -k/m * r3 - gamma/m * r4
        p.r5.set(p.r3.mul(-k / m).add(p.r4.mul(-gamma / m)));
    }
}




