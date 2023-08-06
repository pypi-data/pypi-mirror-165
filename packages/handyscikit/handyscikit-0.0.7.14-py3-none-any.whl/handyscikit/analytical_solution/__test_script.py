from handyscikit import cprint
import handyscikit.analytical_solution as AS
import numpy as np


class AnalyticalSolutions:
    @staticmethod
    def theis():
        theis = AS.Theis(t=None, q=-0.01, h=2000, s=1e-6)
        theis.set_conductivity_by_permeability(4e-13, 1000, 9.8, 1.01e-3, 1)

        error = 1e-6
        assert theis.calc(np.array([36.8176, 52.5568, 0]), 3600) == 2431.2246307060827
        assert theis.calc(np.array([36.8176, 52.5568, 0]), 7200) == 2565.994836182302

        cprint("[AnalyticalSolutions Test] Theis test passed.", color="green")

    @staticmethod
    def gaussian_hill():
        gauss = AS.GaussianHill(0.05, np.array([[0.001, 0], [0, 0.001]]))

        assert gauss.calc(np.array([0.1, 0.1]), 0) == 0.018315638888734175
        assert gauss.calc(np.array([0.1, 0.1]), 100) == 0.011750824499050483
        assert gauss.calc(np.array([0.1, 0.1]), 500) == 0.0024690137745113686
        assert gauss.calc(np.array([0.1, 0.1]), 999) == 0.0012434562892379337

        assert gauss.calc_initial_condition(np.array([0, 0, 0])) == 1.0
        assert gauss.calc_initial_condition(np.array([0.05, 0.05, 0])) == 0.3678794411714422

        cprint("[AnalyticalSolutions Test] Gaussian hill test passed.", color="green")

    @staticmethod
    def convection_diffusion_in_channel():
        solution = AS.ConvectionDiffusionInChannel(1, 1, np.array([0.001, 0.001]), 0.02)

        assert solution.calc(np.array([0.2, 0.5])) == -0.01053842453305654

        cprint("[AnalyticalSolutions Test] Convection diffusion in channel test passed.", color="green")


if __name__ == "__main__":
    AnalyticalSolutions.theis()
    AnalyticalSolutions.gaussian_hill()
    AnalyticalSolutions.convection_diffusion_in_channel()