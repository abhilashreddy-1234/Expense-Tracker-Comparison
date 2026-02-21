
import sys
from PyQt5.QtWidgets import QApplication
from ui_main import ExpenseTrackerUI

app = QApplication(sys.argv)
window = ExpenseTrackerUI()
window.show()
sys.exit(app.exec_())
