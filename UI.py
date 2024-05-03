import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

if __name__ == "__main__" : 
    app = QApplication(sys.argv)
    main_icon = sys.argv[1] if len(sys.argv)>1 else "./icons/logo.ico"
    main_window = QMainWindow()
    main_window.show()
    sys.exit(app.exec())