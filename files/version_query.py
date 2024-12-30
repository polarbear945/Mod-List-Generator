import sys
import csv
import requests
import webbrowser
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout, QLabel, QScrollArea

def fetch_minecraft_versions():
    url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        versions = [{"id": version["id"], "type": version["type"]} for version in data["versions"]]
        return versions
    return []

def read_mods_data():
    mods = []
    try:
        with open("mods_details.csv", mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                mods.append({"name": row["Name"], "link": row["Link"], "supported_versions": row["Supported Versions"].split()})
    except UnicodeDecodeError:
        print("Error: The CSV file contains characters that cannot be decoded with UTF-8 encoding.")
    return mods

def normalize_version(version):
    return ".".join(version.split(".")[:2])

def check_version_compatibility(mod, selected_version):
    normalized_selected_version = normalize_version(selected_version)
    return normalized_selected_version in [normalize_version(v) for v in mod["supported_versions"]]

class ModVersionChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Mod Compatibility Checker")
        self.setGeometry(300, 200, 600, 400)
        self.show_snapshots = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.version_label = QLabel("Select Minecraft Version:")
        layout.addWidget(self.version_label)
        self.version_dropdown = QComboBox()
        self.all_versions = fetch_minecraft_versions()
        self.update_version_dropdown()
        layout.addWidget(self.version_dropdown)
        self.snapshot_button = QPushButton("Show Snapshots")
        self.snapshot_button.clicked.connect(self.toggle_snapshots)
        layout.addWidget(self.snapshot_button)
        self.check_button = QPushButton("Check Mods")
        self.check_button.clicked.connect(self.display_mods)
        layout.addWidget(self.check_button)
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def update_version_dropdown(self):
        self.version_dropdown.clear()
        if self.show_snapshots:
            self.version_dropdown.addItems([v["id"] for v in self.all_versions])
        else:
            self.version_dropdown.addItems([v["id"] for v in self.all_versions if v["type"] == "release"])

    def toggle_snapshots(self):
        self.show_snapshots = not self.show_snapshots
        self.update_version_dropdown()
        if self.show_snapshots:
            self.snapshot_button.setText("Hide Snapshots")
        else:
            self.snapshot_button.setText("Show Snapshots")

    def display_mods(self):
        selected_version = self.version_dropdown.currentText()
        available_mods = []
        unavailable_mods = []
        mods = read_mods_data()
        for mod in mods:
            if check_version_compatibility(mod, selected_version):
                available_mods.append(mod)
            else:
                unavailable_mods.append(mod)
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.add_mods_to_layout(available_mods, f"Available Mods for Version {selected_version}", "green")
        self.add_mods_to_layout(unavailable_mods, f"Unavailable Mods for Version {selected_version}", "red")

    def add_mods_to_layout(self, mods, label_text, color):
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignLeft)
        self.scroll_layout.addWidget(label)
        if mods:
            for mod in mods:
                mod_label = QLabel(f"<a href=\"{mod['link']}\">{mod['name']}</a>")
                mod_label.setOpenExternalLinks(True)
                mod_label.setStyleSheet(f"color: {color}; font-size: 14px;")
                self.scroll_layout.addWidget(mod_label)
            open_all_button = QPushButton(f"Open All {label_text}")
            open_all_button.clicked.connect(lambda _, mods=mods: self.open_all_links(mods))
            self.scroll_layout.addWidget(open_all_button)
        else:
            no_mod_label = QLabel("No mods found for this version.")
            no_mod_label.setStyleSheet("color: gray; font-size: 14px;")
            self.scroll_layout.addWidget(no_mod_label)

    def open_all_links(self, mods):
        for mod in mods:
            if mod["link"]:
                webbrowser.open(mod["link"])

app = QApplication(sys.argv)
window = ModVersionChecker()
window.show()
sys.exit(app.exec_())