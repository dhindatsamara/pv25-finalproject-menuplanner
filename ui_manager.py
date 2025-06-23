import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
from menu_generator import MenuGenerator
from export_manager import ExportManager
from utils import validate_inputs, get_selected_meal_time, get_selected_goal

class MenuPlannerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            loadUi('menu_planner.ui', self)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", "Gagal memuat file UI! Pastikan menu_planner.ui ada.")
            sys.exit(1)
        self.load_stylesheet()
        try:
            if not hasattr(self, 'statusbar') or self.statusbar is None:
                self.statusbar = QtWidgets.QStatusBar()
                self.setStatusBar(self.statusbar)
            self.statusbar.setVisible(True)
            self.statusbar.setMinimumHeight(24)
            # self.statusbar.setStyleSheet("QStatusBar { background-color: #f5f5f5; color: #222; font-size: 12px; padding: 4px; border-top: 1px solid #ccc; }")
            self.statusbar.showMessage("Dhinda Tsamara Shalsabilla | F1D022005")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Gagal menginisialisasi status bar: {str(e)}")
        self.setup_radio_buttons()
        self.setup_comboboxes()
        self.menu_generator = MenuGenerator(self)
        self.export_manager = ExportManager(self)
        self.setup_menu_bar()
        self.connect_signals()
        try:
            self.stackedWidget.setCurrentIndex(0)
            self.tabWidget.setCurrentIndex(0)
        except AttributeError:
            pass

    def setup_radio_buttons(self):
        try:
            if all(hasattr(self, attr) for attr in ['timeBreakfast', 'timeLunch', 'timeDinner', 'timeSnack']):
                self.meal_group = QtWidgets.QButtonGroup(self)
                self.meal_group.addButton(self.timeBreakfast, 1)
                self.meal_group.addButton(self.timeLunch, 2)
                self.meal_group.addButton(self.timeDinner, 3)
                self.meal_group.addButton(self.timeSnack, 4)
        except Exception as e:
            pass
        try:
            if all(hasattr(self, attr) for attr in ['goalBudget', 'goalFancy', 'goalHealthy']):
                self.goal_group = QtWidgets.QButtonGroup(self)
                self.goal_group.addButton(self.goalBudget, 1)
                self.goal_group.addButton(self.goalFancy, 2)
                self.goal_group.addButton(self.goalHealthy, 3)
        except Exception as e:
            pass

    def setup_comboboxes(self):
        try:
            if hasattr(self, 'prepTimeCombo'):
                self.prepTimeCombo.setCurrentIndex(-1)
                self.prepTimeCombo.currentTextChanged.connect(self.update_prep_time)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Input waktu persiapan tidak ditemukan.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", "Gagal menginisialisasi input waktu persiapan!")
        try:
            if hasattr(self, 'tasteCombo'):
                self.tasteCombo.setCurrentIndex(-1)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Input selera rasa tidak ditemukan.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", "Gagal menginisialisasi input selera rasa!")

    def update_prep_time(self, text):
        try:
            self.prep_time = text if text else None
        except Exception as e:
            self.prep_time = None

    def load_stylesheet(self):
        try:
            with open('styles.qss', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, "Warning", "File styles.qss tidak ditemukan!")
        except Exception as e:
            pass

    def setup_menu_bar(self):
        try:
            if not hasattr(self, 'menubar'):
                QtWidgets.QMessageBox.critical(self, "Error", "Menu bar tidak ditemukan di UI!")
                return
            if hasattr(self, 'actionExportCsv'):
                self.actionExportCsv.triggered.connect(self.export_manager.export_to_csv)
            if hasattr(self, 'actionExportPdf'):
                self.actionExportPdf.triggered.connect(self.export_manager.export_to_pdf)
            if hasattr(self, 'actionExit'):
                self.actionExit.triggered.connect(self.close)
            if hasattr(self, 'actionClearHistory'):
                self.actionClearHistory.triggered.connect(self.export_manager.clear_history)
            if hasattr(self, 'actionClearForm'):
                self.actionClearForm.triggered.connect(self.reset_fields)
            if hasattr(self, 'actionAbout'):
                self.actionAbout.triggered.connect(self.show_about_dialog)
            if hasattr(self, 'actionUserGuide'):
                self.actionUserGuide.triggered.connect(self.show_user_guide)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal mengatur menu bar: {str(e)}")

    def show_user_guide(self):
        try:
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("User Guide")
            dialog.setFixedSize(500, 400)
            layout = QtWidgets.QVBoxLayout()
            text_browser = QtWidgets.QTextBrowser()
            text_browser.setOpenExternalLinks(True)
            guide_content = """
            <h2>MenuPlanner+ User Guide</h2>
            <p>Selamat datang di <b>MenuPlanner+</b>, aplikasi untuk merencanakan menu makanan!</p>
            <h3>Cara Penggunaan:</h3>
            <ul>
                <li><b>Landing Page:</b> Klik tombol <b>START</b> untuk masuk ke halaman utama.</li>
                <li><b>Plan Your Meal:</b>
                    <ul>
                        <li>Masukkan nama di kolom <b>Nama</b>.</li>
                        <li>Pilih waktu makan (Sarapan, Makan Siang, dll.).</li>
                        <li>Pilih rasa (Manis, Pedas, dll.) dari dropdown.</li>
                        <li>Pilih tujuan konsumsi (Hemat, Mewah, Diet).</li>
                        <li>Pilih waktu persiapan (Cepat, Sedang, Lama).</li>
                        <li>Klik <b>Generate Menu</b> untuk rekomendasi atau <b>Surprise Me!</b> untuk menu acak untuk makan seharian.</li>
                        <li>Klik <b>Reset</b> untuk mengosongkan input.</li>
                    </ul>
                </li>
                <li><b>Meal History:</b>
                    <ul>
                        <li>Lihat riwayat rekomendasi di tabel.</li>
                        <li>Klik <b>Export to CSV</b> atau <b>Export to PDF</b> untuk menyimpan riwayat.</li>
                        <li>Klik <b>Clear History</b> untuk menghapus riwayat.</li>
                    </ul>
                </li>
                <li><b>Menu Bar:</b>
                    <ul>
                        <li><b>File > Export to CSV/PDF:</b> Ekspor riwayat.</li>
                        <li><b>File > Exit:</b> Keluar dari aplikasi (konfirmasi akan muncul).</li>
                        <li><b>Edit > Clear History:</b> Hapus riwayat.</li>
                        <li><b>Edit > Reset Form:</b> Kosongkan formulir input.</li>
                        <li><b>Help > About:</b> Info aplikasi.</li>
                        <li><b>Help > User Guide:</b> Baca panduan ini.</li>
                    </ul>
                </li>
            </ul>
            <p><b>Catatan:</b> Pastikan database <i>menu.db</i> terisi dan <i>styles.qss</i> ada di direktori aplikasi.</p>
            """
            text_browser.setHtml(guide_content)
            layout.addWidget(text_browser)
            close_button = QtWidgets.QPushButton("Close")
            close_button.clicked.connect(dialog.accept)
            layout.addWidget(close_button)
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menampilkan panduan pengguna: {str(e)}")

    def show_about_dialog(self):
        try:
            QtWidgets.QMessageBox.information(
                self, "About MenuPlanner+",
                "MenuPlanner+ v2.0\nAplikasi rekomendasi menu makanan untuk masak sendiri.\nDibuat oleh Dhinda Tsamara Shalsabilla (F1D022005)"
            )
        except Exception as e:
            pass

    def connect_signals(self):
        try:
            required_widgets = [
                'startButton', 'generateButton', 'surpriseButton', 'resetButton',
                'exportCsvButton', 'exportPdfButton', 'clearHistoryButton',
                'nameInput', 'tasteCombo'
            ]
            missing = [w for w in required_widgets if not hasattr(self, w)]
            if missing:
                QtWidgets.QMessageBox.critical(self, "Error", f"Widget tidak ditemukan: {', '.join(missing)}")
                sys.exit(1)
            self.startButton.clicked.connect(self.show_main_page)
            self.generateButton.clicked.connect(self.menu_generator.generate_menu)
            self.surpriseButton.clicked.connect(self.menu_generator.surprise_menu)
            self.resetButton.clicked.connect(self.reset_fields)
            self.exportCsvButton.clicked.connect(self.export_manager.export_to_csv)
            self.exportPdfButton.clicked.connect(self.export_manager.export_to_pdf)
            self.clearHistoryButton.clicked.connect(self.export_manager.clear_history)
            self.nameInput.textChanged.connect(self.update_button_states)
            self.tasteCombo.currentTextChanged.connect(self.update_button_states)
            if hasattr(self, 'meal_group'):
                self.meal_group.buttonClicked.connect(self.update_button_states)
            if hasattr(self, 'goal_group'):
                self.goal_group.buttonClicked.connect(self.update_button_states)
            if hasattr(self, 'prepTimeCombo'):
                self.prepTimeCombo.currentTextChanged.connect(self.update_button_states)
            self.generateButton.setEnabled(False)
            self.surpriseButton.setEnabled(True)
            self.update_button_states()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menghubungkan sinyal: {str(e)}")

    def update_button_states(self):
        try:
            name = self.nameInput.text().strip() if hasattr(self, 'nameInput') else ""
            flavor = self.tasteCombo.currentText() if hasattr(self, 'tasteCombo') else ""
            meal_time = get_selected_meal_time(self)
            goal = get_selected_goal(self)
            prep_time = self.prepTimeCombo.currentText() if hasattr(self, 'prepTimeCombo') else ""
            all_filled = bool(name and flavor and meal_time and goal and prep_time)
            only_name_filled = bool(name and not flavor and not meal_time and not goal and not prep_time)
            no_meal_time = not meal_time
            if hasattr(self, 'generateButton') and hasattr(self, 'surpriseButton'):
                self.generateButton.setEnabled(all_filled)
                self.surpriseButton.setEnabled(no_meal_time or only_name_filled)
        except Exception as e:
            pass

    def show_main_page(self):
        try:
            if hasattr(self, 'stackedWidget') and hasattr(self, 'main_page'):
                self.stackedWidget.setCurrentWidget(self.main_page)
        except Exception as e:
            pass

    def reset_fields(self):
        try:
            confirm = QtWidgets.QMessageBox.question(
                self, "Konfirmasi Reset",
                "Yakin ingin menghapus semua input dan hasil?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.No:
                return
            self.nameInput.clear()
            self.tasteCombo.setCurrentIndex(-1)
            if hasattr(self, 'meal_group'):
                self.meal_group.setExclusive(False)
                for btn in self.meal_group.buttons():
                    btn.setChecked(False)
                self.meal_group.setExclusive(True)
            if hasattr(self, 'goal_group'):
                self.goal_group.setExclusive(False)
                for btn in self.goal_group.buttons():
                    btn.setChecked(False)
                self.goal_group.setExclusive(True)
            if hasattr(self, 'prepTimeCombo'):
                self.prepTimeCombo.setCurrentIndex(-1)
                self.prep_time = None
            self.resultTextEdit.clear()
            self.generateButton.setEnabled(False)
            self.surpriseButton.setEnabled(True)
        except Exception as e:
            pass

    def closeEvent(self, event):
        try:
            confirm = QtWidgets.QMessageBox.question(
                self, "Konfirmasi Keluar",
                "Yakin ingin keluar dari MenuPlanner+?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                if hasattr(self, 'conn'):
                    self.conn.close()
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            event.accept()