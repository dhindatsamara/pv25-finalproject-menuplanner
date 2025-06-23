import sys
from PyQt5 import QtWidgets
from ui_manager import MenuPlannerApp
 
if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MenuPlannerApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: Application failed to start: {str(e)}")
        sys.exit(1)