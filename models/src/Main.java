import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.sql.Timestamp;
import java.util.Random;
import java.util.Timer;


public class Main {

    // Parameters
    static String mode = "gravity"; // "oscillator" or "gravity"
    static String integrators[] = {"verlet"}; // "verlet", "beeman", "gear5"
    static double dt[] = {0.001};
    static double tf = 1.0;
    static double dt2 = 0.01; // for writing output only
    static int N[] = {100};
    static int runs = 5;
    public static void main(String[] args) throws IOException {
        for (int i = 0; i < runs; i++) {
            for (String integrator : integrators) {
                for (double deltaT : dt) {
                    for (int n : N) {
                        if (mode.equalsIgnoreCase("oscillator")) {
                            runOscillator(integrator, deltaT, dt2, tf);
                        } else if (mode.equalsIgnoreCase("gravity")) {
                            runGravity(integrator, deltaT, tf, n, runs>1);
                        } else {
                            throw new IllegalArgumentException("Unknown mode: " + mode);
                        }
                    }
                }
            }
        }
    }

    static Integrator buildIntegrator(String integratorName) {
        if (integratorName.equalsIgnoreCase("verlet")) {
            return new VerletIntegrator();
        } else if (integratorName.equalsIgnoreCase("beeman")) {
            return new BeemanIntegrator();
        } else if (integratorName.equalsIgnoreCase("gear5")) {
            return new Gear5Integrator();
        } else {
            throw new IllegalArgumentException("Unknown integrator: " + integratorName);
        }
    }

    static void runOscillator(String integratorName, double dt, double dt2, double tf) throws IOException {
        String folder = "outputs/oscillator/sim_results/";
        new File(folder).mkdirs();

        String out = Paths.get(folder, integratorName + "_" + dt + "_out.csv").toString();
        String eout = Paths.get(folder, integratorName + "_" + dt + "_energy.csv").toString();

        Particle p = new Particle(0);
        p.m = 70.0;
        p.r.set(1.0, 0, 0);

        double k = 1e4;
        double gamma = 100.0;
        double A = 1.0;
        p.v.set(-A * gamma / (2.0 * p.m), 0, 0);

        Particle[] arr = new Particle[]{p};
        ForceCalculator fc = new OscillatorForce(k, gamma, p);
        Integrator integrator = buildIntegrator(integratorName);

        // 👉 Inicialización de derivadas solo si es Gear5
        if (integrator instanceof Gear5Integrator) {
            // primero calculo aceleración inicial con la fuerza
            fc.computeForces(arr);
            p.a.set(p.a); // redundante, pero deja claro que ya está calculada
            // ahora inicializo r2..r5
            Gear5Integrator.initializeOscillatorDerivatives(p, k, gamma);
        }

        StateWriter sw = new StateWriter(out);
        EnergyWriter ew = new EnergyWriter(eout, "E_kin,E_pot,E_tot");

        double t = 0.0;
        double t_write = 0.0;

        while (t <= tf + 1e-12) {
            if (t - t_write >= dt2 - 1e-12) {
                sw.write(t, arr);
                double ek = Energy.kinetic(arr);
                double ep = Energy.potentialOscillator(p, k);
                ew.write(t, ek, ep, ek + ep);
                t_write = t;
            }
            integrator.step(arr, dt, fc);
            t += dt;
        }

        sw.close();
        ew.close();
        System.out.println("Finished oscillator with " + integrator.name() + " -> " + out + ", " + eout);
    }

    static void runGravity(String integratorName, double dt, double tf, int N, boolean multipleRuns) throws IOException {
        String paramLabel = String.format("dt%.0eN%d",dt,N);
        String folder = "outputs/gravity/sim_results/"+integratorName+"/"+(multipleRuns? paramLabel:"");
        String outFolder = folder+"/out/";
        String eoutFolder = folder+"/energy/";
        new File(outFolder).mkdirs();
        new File(eoutFolder).mkdirs();
        Random rnd = new Random();
        String out = outFolder + "out_" + ( multipleRuns? rnd.nextInt():paramLabel) + ".csv";
        String eout = eoutFolder + "energy_"+ paramLabel +".csv";

        Particle[] arr = new Particle[N];

        for (int i = 0; i < N; i++) {
            arr[i] = new Particle(i);
            arr[i].m = 1.0;
            arr[i].r.set(rnd.nextGaussian(), rnd.nextGaussian(), rnd.nextGaussian());
            double theta = 2 * Math.PI * rnd.nextDouble();
            double phi = Math.acos(2 * rnd.nextDouble() - 1);
            arr[i].v.set(
                    0.1 * Math.cos(theta) * Math.sin(phi),
                    0.1 * Math.sin(theta) * Math.sin(phi),
                    0.1 * Math.cos(phi)
            );
        }

        final double G = 1.0, h = 0.05;
        ForceCalculator fc = new GravityForce(G, h);
        Integrator integrator = buildIntegrator(integratorName);

        StateWriter sw = new StateWriter(out);
        EnergyWriter ew = new EnergyWriter(eout, "E_kin,E_pot,E_tot");

        double t = 0.0, t_write = 0.0;
        tf += 1e-12;
        dt2 -= 1e-12;
        long startTime = System.currentTimeMillis();

        while (t <= tf) {
            if(t - t_write >= dt2) {
                sw.write(t, arr);
                double ek = Energy.kinetic(arr);
                double ep = Energy.potentialGravity(arr, G, h);
                ew.write(t, ek, ep, ek + ep);
                t_write = t;
            }
            integrator.step(arr, dt, fc);
            t += dt;
        }

        long endTime = System.currentTimeMillis();
        sw.close();
        ew.close();
        System.out.println("Finished gravity with " + integrator.name() + " -> " + out + ", " + eout);
        System.out.println("Execution time: " + (endTime - startTime));
    }
}



