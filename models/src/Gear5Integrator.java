
public class Gear5Integrator implements Integrator {
// coeficiente gear5
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

        // 1) Predicción por Taylor hasta r5
        for (int i = 0; i < n; i++) {
            Particle pi = p[i];
            // r = r + r1*dt + r2*(dt^2)/2 + r3*(dt^3)/6 + r4*(dt^4)/24 + r5*(dt^5)/120
            Vector rp = pi.r
                    .add(pi.v.mul(dt))
                    .add(pi.r2.mul(dt2 / 2.0))
                    .add(pi.r3.mul(dt3 / 6.0))
                    .add(pi.r4.mul(dt4 / 24.0))
                    .add(pi.r5.mul(dt5 / 120.0));
            // r1 = v + r2*dt + r3*(dt^2)/2 + r4*(dt^3)/6 + r5*(dt^4)/24
            Vector r1p = pi.v
                    .add(pi.r2.mul(dt))
                    .add(pi.r3.mul(dt2 / 2.0))
                    .add(pi.r4.mul(dt3 / 6.0))
                    .add(pi.r5.mul(dt4 / 24.0));
            // r2 = r2 + r3*dt + r4*(dt^2)/2 + r5*(dt^3)/6
            Vector r2p = pi.r2
                    .add(pi.r3.mul(dt))
                    .add(pi.r4.mul(dt2 / 2.0))
                    .add(pi.r5.mul(dt3 / 6.0));
            // r3 = r3 + r4*dt + r5*(dt^2)/2
            Vector r3p = pi.r3
                    .add(pi.r4.mul(dt))
                    .add(pi.r5.mul(dt2 / 2.0));
            // r4 = r4 + r5*dt
            Vector r4p = pi.r4.add(pi.r5.mul(dt));
            // r5 stays the same
            Vector r5p = new Vector(pi.r5.x, pi.r5.y, pi.r5.z);
            // store predictors in temporary fields (reuse r,r1,r2... fields as "predicted")
            pi.r.set(rp);
            pi.v.set(r1p);
            pi.r2.set(r2p);
            pi.r3.set(r3p);
            pi.r4.set(r4p);
            pi.r5.set(r5p);
        }

        // 2) Evaluar fuerzas en las posiciones predichas -> fc debe fijar pi.a = a_actual
        fc.computeForces(p);

        // 3) Corrección: Δa = a_actual - r2pred
        for (int i = 0; i < n; i++) {
            Particle pi = p[i];
            Vector delta2 = pi.a.sub(pi.r2); //a_actual - r2p
            // aplicar correcciones según la teórica
            // r = rp + A0 * Δa * dt^2
            pi.r = pi.r.add(delta2.mul(A0 * dt2));

            // v = v_p + A1 * Δa * dt
            pi.v = pi.v.add(delta2.mul(A1 * dt));

            // r2 = r2p + A2 * Δa
            pi.r2 = pi.r2.add(delta2.mul(A2));

            // r3 = r3p + A3 * Δa / dt
            pi.r3 = pi.r3.add(delta2.mul(A3 / dt));

            // r4 = r4p + A4 * Δa / dt^2
            pi.r4 = pi.r4.add(delta2.mul(A4 / dt2));

            // r5 = r5p + A5 * Δa / dt^3
            pi.r5 = pi.r5.add(delta2.mul(A5 / dt3));

            // actualizar la aceleración almacenada (r2) para consistencia
            // y dejar pi.a = r2 (la aceleración corregida)
            pi.a.set(pi.r2);
        }
    }

    @Override
    public String name() {
        return "Gear5";
    }
}



