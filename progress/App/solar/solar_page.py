from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QLabel, QSizePolicy
from progress.App.solar.ui.ui_solar_gui import Ui_solar_widget
from PySide6.QtCore import Signal, Qt
from progress.mod_solar import Solar
from progress.App.gui_tools.tools import WorkerThread, StdoutBuffer
from progress.mod_kmeans import KMeans_Pipeline
from progress.paths import get_path
base_dir = get_path()
import os
from PySide6.QtGui import QPixmap

class solar_form(QWidget, Ui_solar_widget):
    """Landing page widget."""

    page_changer_next = Signal()
    page_changer_previous = Signal()

    def __init__(self, data_handler, parent=None):
        """Sets up the UI file to show in the application"""
        super(solar_form, self).__init__(parent)
        self.setupUi(self)

        self.data_handler = data_handler
        self.pushButton_DI_previous_2.clicked.connect(lambda: self.page_changer_previous.emit())
        self.pushButton_DI_next_2.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))
        self.pushButton_DI_next_5.clicked.connect(lambda: self.page_changer_next.emit())
        self.pushButton_DI_previous_5.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(0))
        self.pushButton.clicked.connect(lambda: self.page_changer_next.emit())


        self.widget_5.setVisible(False)
        self.textBrowser_4.setVisible(False)
        self.pushButton_solar_dl.setVisible(False)
        self.pushButton_DI_next_2.setVisible(False)
        self.pushButton_DI_next_5.setVisible(False)
        self.pushButton_solar_upload.setVisible(False)
        self.comboBox_2.currentIndexChanged.connect(self.solar_cb_changed)
        self.pushButton_solar_upload.clicked.connect(self.upload_solar_data)
        self.pushButton_help_solar.clicked.connect(self.show_help_solar)
        self.textBrowser_6.setVisible(False)
        self.textBrowser_5.setVisible(False)
        self.pushButton_solar_dl.clicked.connect(self.solar_data_process)
        self.pushButton_2.clicked.connect(self.kmeans_eval)
        self.pushButton_3.clicked.connect(self.kmeans_gen)
        self.pushButton.clicked.connect(self.save_solar_data)
        self.pushButton_api_8.clicked.connect(self.show_help_clusters)
        self.cluster_results = os.path.join(base_dir, "Data", "Solar", "clustering_results.txt")
        self.pdf_path = os.path.join(base_dir, "Data", "Solar", "SSE_Curve.png")
        self.solar_directory = os.path.join(base_dir, "Data", "Solar")
        self.data_handler.set_solar_directory(self.solar_directory)
        self.tester=0
        self.png_count =0
        self.counter = 0

    def show_help_clusters(self):
        QMessageBox.information(self, "Clusters Help", "This step finds the optimum number of clusters to evaluate.")

    def show_help_solar(self):
        QMessageBox.information(self, "Solar Help", "You can skip this step if your solar power generation data has previously been clustered.")

    def solar_cb_changed(self, index):
        if index == 1:
            self.textBrowser_4.setVisible(True)
            self.widget_5.setVisible(True)
            self.pushButton_solar_dl.setVisible(True)
            self.pushButton_solar_upload.setVisible(False)
        elif index == 2:
            self.pushButton_solar_upload.setVisible(True)
            self.textBrowser_4.setVisible(False)
            self.widget_5.setVisible(False)
            self.pushButton_solar_dl.setVisible(False)
            # self.pushButton_DI_next_2.setVisible(True)
        elif index == 3:
            self.data_handler.set_solar_directory(False)
            self.pushButton_DI_next_2.setVisible(True)

    def upload_solar_data(self):

        self.solar_directory = QFileDialog.getExistingDirectory(self, "Select Directory", base_dir)
        self.data_handler.set_solar_directory(self.solar_directory)
        QMessageBox.information(self, "Solar Upload", "Solar data uploaded and saved!")


        self.pushButton_DI_next_2.setVisible(True)

    # download weather data and convert to solar generation data for all sites
    def solar_data_process(self):
        self.textBrowser_4.append("Downloading solar data...")
        self.input_starty = int(self.lineEdit_starty.text())
        self.input_endy = int(self.lineEdit_endy.text())
        self.solar_site_data = self.solar_directory+"/solar_sites.csv"
        self.solar_prob_data = self.solar_directory+"/solar_probs.csv"
        self.solar = Solar(self.solar_site_data, self.solar_directory)

        # Create worker threads for download and gather processes
        self.download_thread = WorkerThread(self.solar.SolarGen, self.data_handler.input_api, self.data_handler.input_name, \
                                            self.data_handler.input_aff, self.data_handler.input_email, self.input_starty, self.input_endy)
        self.gather_thread = WorkerThread(self.solar.SolarGenGather, self.input_starty, self.input_endy)

        self.start_download_thread()

        # Connect the output_updated signal to update the GUI
        self.download_thread.output_updated.connect(lambda text: self.handle_output(self.textBrowser_4, text))

        # Connect the finished signal of download_thread to start the gather_thread
        self.download_thread.finished.connect(self.start_gather_thread)

        # Connect the output_updated signal to update the GUI
        self.gather_thread.output_updated.connect(lambda text: self.handle_output(self.textBrowser_4, text))

        # Connect the finished signal of gather_thread to handle thread completion
        self.gather_thread.finished.connect(self.end_gather_thread)

        self.pushButton_DI_next_2.setVisible(True)

    def start_download_thread(self):
        # start download thread
        self.download_thread.start()
        #self.textBrowser_4.append("Downloading solar data please wait until the process has finished.")
        #self.output_window.show()

    def start_gather_thread(self):
        # Start the gather_thread
        self.gather_thread.start()

    def end_gather_thread(self):
        pass

    def kmeans_eval(self):

        if hasattr(self, 'label_sse'):
            self.label_sse.setVisible(False)
            self.horizontalLayout_23.removeWidget(self.label_sse)
        self.textBrowser_6.setVisible(True)
        self.textBrowser_5.setVisible(True)
        self.solar_site_data = self.solar_directory + "/solar_sites.csv"
        self.solar_prob_data = self.solar_directory + "/solar_probs.csv"
        self.solar = Solar(self.solar_site_data, self.solar_directory)

        QMessageBox.information(self, "Clustering Metrics", "Press OK to continue. This may take a few minutes.")

        self.clust_eval = self.lineEdit.text()

        # Create a worker thread for the instantiation of KMeans_Pipeline
        self.worker_pipeline = WorkerThread(self.create_pipeline)
        self.worker_pipeline.output_updated.connect(lambda text: self.handle_output(self.textBrowser_6, text))
        #self.worker_pipeline.finished.connect(self.start_test_metrics)
        self.worker_pipeline.finished.connect(self.checker)
        # Start the worker thread for pipeline instantiation
        self.worker_pipeline.start()

    def checker(self):
        if self.counter==0:
            # print(self.counter)
            self.counter = 1
            # print(self.counter)
        else:
            self.start_test_metrics()
            self.counter = 0

    def create_pipeline(self):
        self.pipeline = KMeans_Pipeline(self.solar_directory, self.solar_site_data)

    # creating dummy method for Worker 1 to bypass threading issue for M-chip macbooks
    def dummy_func(self):
        pass

    def start_test_metrics(self):
        # Check if worker_pipeline has completed
        if hasattr(self, 'worker_pipeline') and self.worker_pipeline.isFinished():
            
            # directly calling test_metrics instead of using worker thread to bypass threading issue for M-chip macbooks
            self.pipeline.test_metrics(int(self.clust_eval)) 
            # Create worker threads for the pipeline methods
            # self.worker1 = WorkerThread(self.pipeline.test_metrics, int(self.clust_eval)) # this is causing Bus 10 error for M-chip macbooks (threading issue)
            self.worker1 = WorkerThread(self.dummy_func)        
            self.worker2 = WorkerThread(self.display_text_file, self.cluster_results)

            # Connect signals
            self.worker1.output_updated.connect(lambda text: self.handle_output(self.textBrowser_6, text))
            self.worker1.finished.connect(self.start_worker2)
            self.worker2.output_updated.connect(lambda text: self.handle_output(self.textBrowser_5, text))
            self.worker2.finished.connect(self.on_workers_finished)

            # Start the first worker
            self.worker1.start()
        else:
            print("worker_pipeline has not finished yet.")

    def start_worker2(self):
        if self.tester==0:
            self.tester=1
        else:
            self.worker2.start()
            self.tester=0

    def display_text_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.textBrowser_5.append(content)  # Append the content to the QTextBrowser
        except Exception as e:
            self.textBrowser_5.append(f"Error loading file: {e}")


    def display_png(self, file_path):
        if os.path.isfile(file_path):  # Check if the file exists
            pixmap = QPixmap(file_path)

            if not pixmap.isNull():
                # Hide the QTextBrowser
                if self.png_count == 0:
                    self.png_count = 1
                elif self.png_count ==1 :
                    self.textBrowser_6.hide()

                    # Create a QLabel to display the image
                    self.label_sse = QLabel()
                    self.label_sse.setPixmap(pixmap)
                    self.label_sse.setPixmap(pixmap.scaled(self.textBrowser_6.width(), self.textBrowser_6.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    self.label_sse.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                    self.horizontalLayout_23.insertWidget(0, self.label_sse)
                    self.png_count = 0

                    # label.setAlignment(Qt.AlignCenter)
                    # label.setGeometry(self.textBrowser_6.geometry())
                    # label.show()

                #print('Image displayed successfully.')
            else:
                self.textBrowser_6.setText("Failed to load image.")
                self.textBrowser_6.show()
                print("Failed to load image.")
        else:
            self.textBrowser_6.setText("File does not exist.")
            self.textBrowser_6.show()
            print("File does not exist.")

    # def display_png(self, file_path):
    #     if os.path.isfile(file_path):  # Check if the file exists
    #         url = QUrl.fromLocalFile(file_path)  # Convert the file path to a URL
    #         html_content = f'<img src="{url.toString()}" />'
    #         self.textBrowser_6.setHtml(html_content)  # Load the image in the QTextBrowser
    #         print('Image displayed successfully.')
    #     else:
    #         self.textBrowser_6.setText("File does not exist.")
    #         print("File does not exist.")

    def on_workers_finished(self):
        # QMessageBox.information(self, "Clustering Metrics", "Please look at SSE curve and silhouette score results to make an informed choice on the number of clusters.")
        self.display_png(self.pdf_path)
        # self.display_text_file(self.cluster_results)

    def kmeans_gen(self):
        # self.textBrowser_5.setVisible(False)
        self.clust_gen = self.lineEdit_2.text()
        self.pipeline.run(n_clusters = int(self.clust_gen))
        self.pipeline.calculate_cluster_probability()
        self.pipeline.split_and_cluster_data()

        self.s_sites, self.s_zone_no, self.s_max, self.s_profiles, self.solar_prob = self.solar.GetSolarProfiles(self.solar_prob_data)


        # Set solar data in DataHandler
        self.data_handler.set_s_sites(self.s_sites)
        self.data_handler.set_s_zone_no(self.s_zone_no)
        self.data_handler.set_s_max(self.s_max)
        self.data_handler.set_s_profiles(self.s_profiles)
        self.data_handler.set_solar_prob(self.solar_prob)

        QMessageBox.information(self, "Clustering Complete", "Clustering of solar data complete!")

        self.pushButton_DI_next_5.setVisible(True)

    def save_solar_data(self):

        if self.data_handler.solar_directory:

            solar_site_data = self.solar_directory+"/solar_sites.csv"
            solar_prob_data = self.solar_directory+"/solar_probs.csv"

            solar = Solar(solar_site_data, self.solar_directory)

            self.s_sites, self.s_zone_no, self.s_max, self.s_profiles, self.solar_prob = \
                solar.GetSolarProfiles(solar_prob_data)

            # Set solar data in DataHandler
            self.data_handler.set_s_sites(self.s_sites)
            self.data_handler.set_s_zone_no(self.s_zone_no)
            self.data_handler.set_s_max(self.s_max)
            self.data_handler.set_s_profiles(self.s_profiles)
            self.data_handler.set_solar_prob(self.solar_prob)

    def handle_output(self, text_browser, text):
        # Update the GUI with the output text
        text_browser.append(text)

