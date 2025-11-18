import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

class RAPlotTools:
    '''Provides plotting tools for visualizing simulation results.'''
    def __init__(self, results_subdir):
        """
        Initializes the RAPlotTools class and creates a directory for storing results.
        """
        self.results_subdir = results_subdir
        pass

    def PlotSolarGen(self, solar_rec, bus_name, s):
        """
        Plots solar power generation over time.

        Parameters:
            solar_rec (numpy.ndarray): Solar power generation records.
            bus_name (list): List of bus names.
        """
        plt.title("Solar Power Generation")
        plt.xlabel("Hours")
        plt.ylabel("Output (MW)")
        plt.plot(solar_rec.T, label = bus_name)
        plt.legend()

        pdf_path = os.path.join(self.results_subdir, f'solar_generation_sample_{s+1}.pdf')

        plt.savefig(pdf_path)
        plt.close()

    def PlotWindGen(self, wind_rec, bus_name, s):
        """
        Plots wind power generation over time.

        Parameters:
            wind_rec (numpy.ndarray): Wind power generation records.
            bus_name (list): List of bus names.
        """
        plt.title("Wind Power Generation")
        plt.xlabel("Hours")
        plt.ylabel("Output (MW)")
        plt.plot(wind_rec.T, label = bus_name)
        plt.legend()

        pdf_path = os.path.join(self.results_subdir, f'wind_generation_sample_{s+1}.pdf')

        plt.savefig(pdf_path)
        plt.close()

    def PlotSOC(self, SOC_rec, essname, s):
        """
        Plots state of charge (SOC) of energy storage systems (ESS) over time.

        Parameters:
            SOC_rec (numpy.ndarray): SOC records.
            essname (list): List of ESS names.
        """

        plt.title("ESS SOC")
        plt.xlabel("Hours")
        plt.ylabel("SOC (MWh)")
        plt.plot(SOC_rec.T, label = essname)
        plt.legend(loc = 'upper right')

        pdf_path = os.path.join(self.results_subdir, f'SOC_sample_{s+1}.pdf')

        plt.savefig(pdf_path)
        plt.close()

    def PlotESCap(self, ess_cap_rec, essname, s):
        """
        Plots state of charge (SOC) of energy storage systems (ESS) over time.

        Parameters:
            SOC_rec (numpy.ndarray): SOC records.
            essname (list): List of ESS names.
        """

        plt.title("ESS Capacity")
        plt.xlabel("Hours")
        plt.ylabel("Capacity (MWh)")
        plt.plot(ess_cap_rec.T, label = essname)
        plt.legend(loc = 'upper right')

        pdf_path = os.path.join(self.results_subdir, f'ESS_Cap_sample_{s+1}.pdf')

        plt.savefig(pdf_path)
        plt.close()

    def PlotLoadCurt(self, curt_rec, s):
        """
        Plots load curtailment over time.

        Parameters:
            curt_rec (numpy.ndarray): Load curtailment records.
        """

        plt.title("Load Curtailment")
        plt.xlabel("Hours")
        plt.ylabel("MW")
        plt.plot(curt_rec)

        pdf_path = os.path.join(self.results_subdir, f'loadcurt_sample_{s+1}.pdf')

        plt.savefig(pdf_path)
        plt.close()

    def OutageMap(self, outage_data):

        """
        Plots a heatmap of outage data.

        Parameters:
            outage_data (str): Path to the Excel file containing outage data.
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
        
        pdf_path = os.path.join(self.results_subdir, 'heatmap.pdf')

        plt.savefig(pdf_path)
        plt.close()

    def PlotLOLP(self, mLOLP_rec, samples, size):

        plt.plot(np.arange(1, samples+1), mLOLP_rec)
        plt.xticks(np.arange(1, samples+1, 1), size*np.arange(1, samples+1, 1))
        plt.xlabel('Samples')
        plt.ylabel('LOLP')

        pdf_path = os.path.join(self.results_subdir, 'LOLP_track.pdf')

        plt.savefig(pdf_path)
        plt.close()

    def PlotCOV(self, COV_rec, samples, size):

        plt.plot(np.arange(1, samples+1), COV_rec)
        plt.xticks(np.arange(1, samples+1, 1), size*np.arange(1, samples+1, 1))
        plt.xlabel('Samples')
        plt.ylabel('Coefficient of Variation')

        pdf_path = os.path.join(self.results_subdir, 'COV_track.pdf')

        plt.savefig(pdf_path)
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