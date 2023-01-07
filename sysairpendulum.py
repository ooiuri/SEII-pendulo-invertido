from numpy import pi, sin, sqrt, arange, floor, array, append
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Variaveis auxiliares
rad2deg = 180/pi
deg2rad = pi/180

b = 0.006856
m = 0.3182
g = 9.81
I = 0.0264
kh = 2.12829e-5
LH = 0.32

class AirPendulum():
    # Definindo dinamica da planta
    # Parametros da planta

    def __init__(self, theta_b=30, ta=1e-3):
        super(AirPendulum, self).__init__()

        self.theta_register = array([])
        self.theta = 0

        self.theta_p_register = array([])
        self.theta_p = 0

        self.theta_p_b = 0*deg2rad
        self.theta_b = theta_b*deg2rad
        self.ta = ta

        self.omega_register = array([])
        self.omega = 0
        self.omega_b = sqrt(m*g*sin(self.theta_b)/kh)

    def dynamic(self, omega):
        # Evoluindo a din. da planta
        x0 = [self.theta + self.theta_b,
              self.theta_p]   # condicao inicial
        sol = odeint(self.model, x0, [0.0, self.ta],
                     args=(omega + self.omega_b,))

        self.omega = omega
        self.theta = sol[:, 0][-1] - self.theta_b
        self.theta_p = sol[:, 1][-1]

        self.omega_register= append(self.omega_register, self.omega)
        self.theta_register= append(self.theta_register, self.theta)
        self.theta_p_register= append(self.theta_p_register, self.theta_p)

        return [self.theta, self.theta_p]

    def model(self, y, _, omega):
        # Definindo estados
        x1, x2 = y
        # Dinamica do pendulo
        x1p = x2
        x2p = (LH*kh/I)*omega**2 - (LH*m*g/I)*sin(x1) - (b/I)*x2
        return [x1p, x2p]

    def control_simulation(self):
        for _ in range(30000):
            # Entrada da planta
            if _*self.ta > 1:
                self.omega = 20

            self.dynamic(self.omega)
        
        self.plot_air_pendulum_result()

    def plot_air_pendulum_result(self):

        # Plotando resultados
        plt.figure()
        plt.plot(arange(0, self.theta_register.size)*self.ta, (self.theta_register + self.theta_b) *
                 rad2deg, lw=2, label=r'$\theta$ (deg)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.grid(True)
        plt.savefig("airpendulum_theta_tempo.png")

        plt.figure()
        plt.plot(arange(0, self.theta_p_register.size)*self.ta, (self.theta_p_register) *
                 rad2deg, lw=2, label=r'$\theta_d$ (deg)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.grid(True)
        plt.savefig("airpendulum_theta_p_tempo.png")

        plt.figure()
        plt.plot(arange(0,self.omega_register.size)*self.ta,
                 self.omega_register[-1] + self.omega_register, 'r--', lw=2, label=r'$\omega$ (rad/s)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.grid(True)

        plt.show()
        plt.savefig("airpendulum_omega_tempo.png")

pendulo = AirPendulum()
pendulo.control_simulation()