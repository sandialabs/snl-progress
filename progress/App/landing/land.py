import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import QTimer, Qt, QRectF, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from progress.paths import get_path
import os
base = get_path()

class Leaf(QGraphicsPixmapItem):
    def __init__(self, pixmap, view_width, view_height):
        super().__init__(pixmap)

        self.setPos(random.randint(0, view_width), -200)
        self.scale_factor = random.uniform(0.1, 0.3)
        self.setScale(self.scale_factor)  # Set the scale
        self.rotation_angle = random.uniform(0, 360)

        # Calculate rotation speed based on size (smaller leaves rotate faster)
        self.rotation_speed = 0.5 * (1 - self.scale_factor)

    def advance(self):
        # Move the leaf downwards and slightly to the right
        self.moveBy(0.4, 1)

        # Update rotation angle based on rotation speed
        self.rotation_angle += self.rotation_speed
        if self.rotation_angle >= 360:
            self.rotation_angle -= 360

        self.setRotation(self.rotation_angle)  # Set the new rotation

        # Mark for removal if it goes out of the view
        if self.y() > self.scene().height() + 50:  # Allow the leaf to fall completely off the screen
            self.marked_for_removal = True

class LeafAnimation(QGraphicsView):
    MAX_LEAVES = 27
    page_changer = Signal()
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
       # self.setMinimumSize(800, 600)  # Set minimum size for the view

        # Hide scroll bars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set background color
        self.scene().setBackgroundBrush(QColor(31, 31, 31))

        # Load leaf image
        leaf_png = os.path.join(base, "Images", "icons", "leaf_transparent.png")
        self.leaf_pixmap = QPixmap(leaf_png)
        if self.leaf_pixmap.isNull():
            print("Error: Leaf image not found. Please check the path.")
            # Use a simple fallback image if the leaf image is not found
            self.leaf_pixmap = QPixmap(20, 20)  # Create a 20x20 pixel image
            self.leaf_pixmap.fill(QColor(255, 0, 0))  # Fill it with red color for testing

        # Create leaves list
        self.leaves = []

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_leaves)
        self.timer.start(10)
        # Timer for adding leaves
        self.add_leaf_timer = QTimer()  # Initialize the timer here
        self.add_leaf_timer.timeout.connect(self.add_random_leaves)
        self.add_leaf_timer.start(random.randint(3000, 9000))  # Start with a random interval between 1 and 3 seconds

        # Add initial leaves
        self.add_random_leaves()

        # Create overlay widget for labels and button
        self.overlay_widget = QWidget(self)
       # self.overlay_widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # Create layout for labels and button
        main_layout = QVBoxLayout(self.overlay_widget)
        main_layout.setAlignment(Qt.AlignTop)  # Align the main content to the top
        main_layout.setContentsMargins(20, 20, 20, 20)  # Set margins to avoid cutting off

        # Add a spacer to push the main content down
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create the first label
        title_label = QLabel("Probabilistic Grid Reliability Analysis with Energy Storage Systems")
        title_label.setFont(QFont("Arial", 48))
        title_label.setStyleSheet("color: white;")  # Set text color to white
        title_label.setWordWrap(True)  # Enable word wrap
        title_label.setAlignment(Qt.AlignCenter)  # Center the text
        main_layout.addWidget(title_label)

        # Add a spacer to create 30px space between the title and subtitle
        main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Create the second label
        subtitle_label = QLabel("A Python-based open-source tool for assessing the resource adequacy of the evolving electric power grid integrated with energy storage systems.")
        subtitle_label.setFont(QFont("Arial", 16))  # Set font size to 16
        subtitle_label.setStyleSheet("color: white;")  # Set text color to white
        subtitle_label.setWordWrap(True)  # Enable word wrap
        subtitle_label.setAlignment(Qt.AlignCenter)  # Center the text
        main_layout.addWidget(subtitle_label)

        # Add a spacer to create space between the subtitle and the button
        main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Create the button
        get_started_button = QPushButton("Get Started")
        get_started_button.setFont(QFont("Arial", 16))
        get_started_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: transparent;
                border: 2px solid white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)  # Style the button
        get_started_button.clicked.connect(self.on_get_started_clicked)  # Connect the button to the method
        main_layout.addWidget(get_started_button, alignment=Qt.AlignCenter)  # Center the button in the layout

        # Add a spacer to push the images and acknowledgement to the bottom
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create layout for images and acknowledgement text
        bottom_layout = QVBoxLayout()
        bottom_layout.setAlignment(Qt.AlignBottom)

        # Create layout for images
        images_layout = QHBoxLayout()
        images_layout.setAlignment(Qt.AlignCenter)

        # Load and add images
        quest_png = os.path.join(base, "Images", "logos", "Quest_Logo_RGB.png")
        snl_png = os.path.join(base, "Images", "logos", "Sandia_National_Laboratories_logo.svg")
        doe_png = os.path.join(base, "Images", "logos", "DOE_transparent.png")
        image_paths = [
            quest_png,
            snl_png,
            doe_png
        ]
        for path in image_paths:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                print(f"Error: Image not found at {path}. Please check the path.")
                pixmap = QPixmap(50, 50)  # Create a placeholder image
                pixmap.fill(QColor(255, 0, 0))  # Fill it with red color for testing
            else:
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Scale the image
            label = QLabel()
            label.setPixmap(pixmap)
            images_layout.addWidget(label)

        # Add images layout to bottom layout
        bottom_layout.addLayout(images_layout)

        # Create and add acknowledgement text
        acknowledgement_label = QLabel("Acknowledgement\nThis material is based upon work supported by the U.S. Department of Energy, Office of Electricity (OE), Energy Storage Division.")
        acknowledgement_label.setFont(QFont("Arial", 12))  # Set font size to 12
        acknowledgement_label.setStyleSheet("color: white;")  # Set text color to white
        acknowledgement_label.setWordWrap(True)  # Enable word wrap
        acknowledgement_label.setAlignment(Qt.AlignCenter)  # Center the text
        bottom_layout.addWidget(acknowledgement_label)

        # Add bottom layout to main layout
        main_layout.addLayout(bottom_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay_widget.setGeometry(self.rect())  # Adjust overlay widget size
        self.scene().setSceneRect(QRectF(self.rect()))  # Adjust scene rect

    def update_leaves(self):
        for leaf in self.leaves:
            leaf.advance()
        self.scene().update()

    def add_random_leaves(self):
        num_leaves_to_add = random.randint(1, 5)
        for _ in range(num_leaves_to_add):
            if len(self.leaves) >= self.MAX_LEAVES:

                oldest_leaf = self.leaves.pop(0)
                self.scene().removeItem(oldest_leaf)
            new_leaf = Leaf(self.leaf_pixmap, self.width(), self.height())
            self.leaves.append(new_leaf)
            self.scene().addItem(new_leaf)
            #print(f"Added leaf at position: {new_leaf.pos()}")  # Debugging position

        # Reset the timer with a new random interval
        self.add_leaf_timer.start(random.randint(3000, 7000))
    def on_get_started_clicked(self):
        self.page_changer.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LeafAnimation()
    window.setWindowTitle("Falling Leaves Animation")
    window.show()
    sys.exit(app.exec())
