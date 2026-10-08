# To run the program, only run this file 
# Entry point for CareerPilot AI (main.py) initializes the application and displays the main window.

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
import fonts
from GUI.main_window import MainWindow

if __name__ == "__main__":
    # Create the Qt application instance.
    app = QApplication(sys.argv)
    # Load custom fonts into the application.
    fonts.load_fonts()
    # Set the default font for the entire application (Persian by default).
    app.setFont(QFont(fonts.get_family("fa"), 18))
    # Create and display the main application window.
    window = MainWindow()
    window.show()
    # Execute the application event loop and exit cleanly when closed.
    sys.exit(app.exec())