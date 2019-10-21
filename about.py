import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QDialog, QVBoxLayout


class AboutDialog(QDialog):
	title = "Text Editor"
	dev_info = "Developed by Knowhere1998 (Amey Darekar)"

	def __init__(self, *args, **kwargs):
		super(AboutDialog, self).__init__(*args, **kwargs)
		self.setWindowTitle("About %s" % self.title)
		quitButton = QDialogButtonBox.Ok
		self.buttonBox = QDialogButtonBox(quitButton)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		layout = QVBoxLayout()

		title = QLabel(self.title)
		font = title.font()
		font.setPointSize(20)
		title.setFont(font)

		layout.addWidget(title)

		logo = QLabel()
		logo.setPixmap(QPixmap(os.path.join('icons', 'ma-icon-128.png')))
		layout.addWidget(logo)

		layout.addWidget(QLabel(self.dev_info))

		for i in range(0, layout.count()):
			layout.itemAt(i).setAlignment(Qt.AlignHCenter)

		layout.addWidget(self.buttonBox)

		self.setLayout(layout)
		self.setVisible(True)
