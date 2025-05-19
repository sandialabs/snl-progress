import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

class RAPlotTools:
    """
    Provides plotting tools for visualizing simulation results, including wind and solar generation, 
    state-of-charge (SOC) of ESS, load curtailment, and outage heat maps.

    :param main_folder: The primary directory where plot outputs will be saved.
    :type main_folder: str
    """
    def __init__(self, main_folder):
        """
        Initializes the RAPlotTools class and prepares the directory for storing results.

        :param main_folder: The primary directory where plot outputs will be saved.
        :type main_folder: str
        """
        self.main_folder = main_folder
        pass

    def PlotWindGen(self, wind_rec, bus_name):
        """
        Plots wind power generation over time.

        :param wind_rec: A 2D NumPy array (shape: ``(number_of_zones, hours)``) 
                         of wind power generation values over time.
        :type wind_rec: numpy.ndarray
        :param bus_name: A list of bus names corresponding to each row (zone) in ``wind_rec``.
        :type bus_name: list[str]

        :return: None
        :rtype: None
        """

        plt.title("Wind Power Generation")
        plt.xlabel("Hours")
        plt.ylabel("Output (MW)")
        plt.plot(wind_rec.T, label = bus_name)
        plt.legend()
        plt.savefig(f'{self.main_folder}/Results/wind_generation.pdf')
        plt.close()

    def PlotSolarGen(self, solar_rec, bus_name):
        """
        Plots solar power generation over time.

        :param solar_rec: A 2D NumPy array (shape: ``(number_of_zones, hours)``) 
                          of solar power generation values over time.
        :type solar_rec: numpy.ndarray
        :param bus_name: A list of bus names corresponding to each row (zone) in ``solar_rec``.
        :type bus_name: list[str]

        :return: None
        :rtype: None
        """

        plt.title("Solar Power Generation")
        plt.xlabel("Hours")
        plt.ylabel("Output (MW)")
        plt.plot(solar_rec.T, label = bus_name)
        plt.legend()
        plt.savefig(f'{self.main_folder}/Results/solar_generation.pdf')
        plt.close()

    def PlotSOC(self, SOC_rec, essname):
        """
        Plots state of charge (SOC) of energy storage systems (ESS) over time.

        :param SOC_rec: A 2D NumPy array (shape: ``(number_of_ESS, hours)``) representing 
                        the state of charge of each ESS over time.
        :type SOC_rec: numpy.ndarray
        :param essname: A list of ESS names corresponding to each row in ``SOC_rec``.
        :type essname: list[str]

        :return: None
        :rtype: None
        """

        plt.title("ESS SOC")
        plt.xlabel("Hours")
        plt.ylabel("SOC (MWh)")
        plt.plot(SOC_rec.T, label = essname)
        plt.legend(loc = 'upper right')
        plt.savefig(f'{self.main_folder}/Results/SOC.pdf')
        plt.close()

    def PlotLoadCurt(self, curt_rec):
        """
        Plots load curtailment over time.

        :param curt_rec: A 1D NumPy array (length = hours) of load curtailment values (in MW).
        :type curt_rec: numpy.ndarray

        :return: None
        :rtype: None
        """

        plt.title("Load Curtailment")
        plt.xlabel("Hours")
        plt.ylabel("MW")
        plt.plot(curt_rec)
        # plt.legend(loc = 'upper right')
        plt.savefig(f'{self.main_folder}/Results/loadcurt.pdf')
        plt.close()

    def OutageMap(self, outage_data):

        """
        Plots a heatmap of outage data, typically representing the percentage of 
        load loss across months and hours.

        :param outage_data: Path to a CSV file containing outage percentages, 
                            with rows corresponding to months and columns corresponding to hours.
        :type outage_data: str

        :return: None
        :rtype: None

        :raises FileNotFoundError: If the specified CSV file does not exist.
        """

        outage_data = pd.read_csv(outage_data, header=0, index_col=0).values
        y_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        x_label = np.arange(1, 25, 1)

        heatmap = plt.imshow(outage_data, cmap='Reds', interpolation='nearest')
        plt.xticks(range(len(x_label)), x_label, fontsize = 5)
        plt.yticks(range(len(y_label)), y_label, fontsize = 6)
        plt.xlabel('Hour', fontsize = 8)
        plt.title('Outage Heat Map')

        for i in range(outage_data.shape[0]):
            for j in range(outage_data.shape[1]):
                value = outage_data[i, j]
                if value > 0.1:
                    plt.text(j, i, f'{value:.2f}', ha = 'center', va = 'center', color = 'black', fontsize = 3)

        cbar = plt.colorbar(heatmap, shrink=0.6)
        cbar.set_label('Outage %', rotation=270, labelpad=15, fontsize = 8)
        cbar.ax.tick_params(labelsize=5)
        
        plt.savefig(f"{self.main_folder}/Results/heatmap.pdf", bbox_inches='tight')
        plt.close()

    def PlotLOLP(self, mLOLP_rec, samples, size):
        """
        Plots the running average of the Loss of Load Probability (LOLP) across samples.

        :param mLOLP_rec: A 1D NumPy array (length = samples) of running mean LOLP values.
        :type mLOLP_rec: numpy.ndarray
        :param samples: Number of Monte Carlo samples.
        :type samples: int
        :param size: The total number of MPI processes (or 1 if serial execution).
        :type size: int

        :return: None
        :rtype: None
        """

        plt.plot(np.arange(1, samples+1), mLOLP_rec)
        plt.xticks(np.arange(1, samples+1, 1), size*np.arange(1, samples+1, 1))
        plt.xlabel('Samples')
        plt.ylabel('LOLP')
        plt.savefig(f'{self.main_folder}/Results/LOLP_track.pdf')
        plt.close()

    def PlotCOV(self, COV_rec, samples, size):
        """
        Plots the Coefficient of Variation (COV) of LOLP across samples.

        :param COV_rec: A 1D NumPy array (length = samples) of COV values computed at each sample.
        :type COV_rec: numpy.ndarray
        :param samples: Number of Monte Carlo samples.
        :type samples: int
        :param size: The total number of MPI processes (or 1 if serial execution).
        :type size: int

        :return: None
        :rtype: None
        """

        plt.plot(np.arange(1, samples+1), COV_rec)
        plt.xticks(np.arange(1, samples+1, 1), size*np.arange(1, samples+1, 1))
        plt.xlabel('Samples')
        plt.ylabel('Coefficient of Variation')
        plt.savefig(f'{self.main_folder}/Results/COV_track.pdf')
        plt.close()

############ EXTRA VISUALIZATION CODE ######################

    # outage_day = var_s["outage_day"]
    # month_names = [calendar.month_abbr[i] for i in range(1, 13)]
    # tick_positions = np.arange(15, 365, 30)

    # plt.bar(np.arange(365), outage_day)
    # plt.xticks(tick_positions, month_names, rotation = 45)
    # plt.ylabel('Outage Duration (Hours)')
    # plt.savefig('outages.pdf')


    # N = len(out_durations)
    # colors = np.random.rand(N)
    # plt.scatter(np.arange(N), out_durations, c = colors, alpha = 0.5)
    # plt.savefig('outages.pdf')

    # print(out_durations)