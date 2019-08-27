import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QDialog, QVBoxLayout


class AboutDialog(QDialog):
	def __init__(self, *args, **kwargs):
		super(AboutDialog, self).__init__(*args, **kwargs)

		quitButton = QDialogButtonBox.Ok  # No cancel
		self.buttonBox = QDialogButtonBox(quitButton)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		layout = QVBoxLayout()

		title = QLabel("Text Editor")
		font = title.font()
		font.setPointSize(20)
		title.setFont(font)

		layout.addWidget(title)

		logo = QLabel()
		logo.setPixmap(QPixmap(os.path.join('icons', 'ma-icon-128.png')))
		layout.addWidget(logo)

		layout.addWidget(QLabel("Developed by Knowhere1998 (Amey Darekar)"))

		for i in range(0, layout.count()):
			layout.itemAt(i).setAlignment(Qt.AlignHCenter)

		layout.addWidget(self.buttonBox)

		self.setLayout(layout)
