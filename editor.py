import os
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFontDatabase, QIcon, QPixmap
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QStatusBar, QVBoxLayout, QPlainTextEdit, \
	QAction, QFileDialog, QMessageBox, QTextEdit, QFontComboBox, QComboBox, QWidgetAction, QDialog, QLabel, \
	QDialogButtonBox


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


# noinspection PyPep8Naming
class MainWindow(QMainWindow):
	
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.showMaximized()
		self.setWindowTitle('Text Editor')
		self.setWindowIcon(QIcon('favicon.png'))

		self.current_editor = self.create_editor(text='')
		self.editors = []
		self.paths = []

		self.path = None

		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.tabs.currentChanged.connect(self.change_text_editor)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.add_new_tab()

		self.configure_menuBar()
		self.configure_statusBar()
		self.configure_toolbar()

		self.setCentralWidget(self.tabs)

		navtb = QToolBar("Navigation")
		navtb.setIconSize(QSize(16, 16))
		self.addToolBar(navtb)

		self.show()

	def configure_menuBar(self):
		menubar = self.menuBar()

		menubar_items = {
			'&File': [
				("&New", "Ctrl+N", self.add_new_tab),
				("&Open", "Ctrl+O", self.file_open),
				("&Save", "Ctrl+S", self.save_document),
				("&Save", "Ctrl+Shift+S", self.save_as),
				("&Print", "Ctrl+P", self.print_document),
				None,
				("&Quit", "Ctrl+Q", self.quit),
			],
			'&Edit': [
				("&Cut", "Ctrl+X", self.cut_document),
				("&Copy", "Ctrl+C", self.copy_document),
				("&Paste", "Ctrl+V", self.paste_document),
				None,
				("&Undo", "Ctrl+Z", self.undo_document),
				("&Redo", "Ctrl+Y", self.redo_document)
			],
			'&View': [
				("&Fullscreen", "F11", self.fullscreen),
				None,
				("&Align Left", "", self.align_left),
				("&Align Right", "", self.align_right),
				("&Align Center", "", self.align_center),
				("&Align Justify", "", self.align_justify)
			],
			'&About': [
				("&About Us", "", self.about),
				None,
				("&Help", "", self.help)
			]
		}

		for menuitem, actions in menubar_items.items():
			menu = menubar.addMenu(menuitem)
			for act in actions:
				if act:
					text, shortcut, callback = act
					action = QAction(text, self)
					action.setShortcut(shortcut)
					action.triggered.connect(callback)
					menu.addAction(action)
				else:
					menu.addSeparator()

		# Font Family Input
		fontBox = QFontComboBox(self)
		fontBox.currentFontChanged.connect(self.fontfamily)

		fontSize = QComboBox(self)
		fontSize.setEditable(True)
		fontSize.setMinimumContentsLength(3)

		fontSize.activated.connect(self.fontsize)

		# Font Sizes
		fontSizes = [
			'6', '7', '8', '9', '10', '11', '12', '13', '14',
			'15', '16', '18', '20', '22', '24', '26', '28',
			'32', '36', '40', '44', '48', '54', '60', '66',
			'72', '80', '88', '96'
		]

		fontSize.addItems(fontSizes)
		font_family = QWidgetAction(self)
		font_family.setDefaultWidget(fontBox)
		# Settings Menubar
		settings = menubar.addMenu('&Settings')
		menu_font = settings.addMenu("&Font")
		menu_font.addAction(font_family)

		font_size = QWidgetAction(self)
		font_size.setDefaultWidget(fontSize)
		menu_size = settings.addMenu("&Font Size")
		menu_size.addAction(font_size)

	def about(self):
		dlg = AboutDialog()
		dlg.exec_()

	def configure_toolbar(self):
		items = (
			('icons/new.png', 'New', self.add_new_tab),
			('icons/open.png', 'Open', self.file_open),
			('icons/save.png', 'Save', self.save_document),
			('icons/save_as.png', 'Save As', self.save_as),
			None,
			('icons/cut.png', 'Cut', self.cut_document),
			('icons/copy.png', 'Copy', self.copy_document),
			('icons/paste.png', 'Paste', self.paste_document),
			None,
			('icons/undo.png', 'Undo', self.undo_document),
			('icons/redo.png', 'Redo', self.redo_document),
			None,
			('icons/print.png', 'Print', self.print_document),
			None,
			('icons/quit.png', 'Quit', self.quit),
			None,
			('icons/question.png', 'Help', self.help),
		)
		self.toolbar = self.addToolBar("Toolbar")

		for item in items:
			if item:
				icon, text, callback = item
				action = QAction(QIcon(icon), text, self)
				action.triggered.connect(callback)
				self.toolbar.addAction(action)
			else:
				self.toolbar.addSeparator()

	def configure_statusBar(self):
		self.status = QStatusBar()
		self.setStatusBar(self.status)

	def dialog_critical(self, s):
		dlg = QMessageBox(self)
		dlg.setText(s)
		dlg.setIcon(QMessageBox.Critical)
		dlg.show()

	def change_text_editor(self, index):
		if index < len(self.editors) and index != -1:
			self.current_editor = self.editors[index]

	def file_open(self):
		path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")
		if path:
			try:
				with open(path, 'r') as f:
					text = f.read()
					self.add_new_tab(path, text)
					self.update_title()

			except Exception as e:
				self.dialog_critical(str(e))

	def create_editor(self, text):
		editor = QTextEdit(text)
		fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
		fixedfont.setPointSize(12)
		editor.setFont(fixedfont)
		return editor

	def remove_editor(self, index):
		self.tabs.removeTab(index)
		if index < len(self.editors):
			del self.editors[index]

	def save_document(self):
		if not self.path:
			new_path, _ = QFileDialog.getSaveFileName(self, 'Save File')
		else:
			new_path = self.path
		try:
			file = open(new_path, 'w')
			if file:
				text = self.current_editor.toPlainText()
				file.write(text)
				file.close()
			index = self.tabs.currentIndex()
			self.paths[index] = new_path

		except Exception as e:
			self.dialog_critical(str(e))

	def save_as(self):
		new_path, _ = QFileDialog.getSaveFileName(self, 'Save File')
		try:
			file = open(new_path, 'w')
			if file:
				text = self.current_editor.toPlainText()
				file.write(text)
				file.close()
			index = self.tabs.currentIndex()
			self.paths[index] = new_path
		except Exception as e:
			self.dialog_critical(str(e))

	def print_document(self):
		print_dialog = QPrintDialog()
		if print_dialog.exec_() == QDialog.Accepted:
			self.current_editor.document().print_(print_dialog.printer())

	def add_new_tab(self, label='Untitled', text=''):
		self.current_editor = self.create_editor(text)
		index = self.tabs.currentIndex()
		if index != -1:
			if self.paths[index]:
				label = self.paths[index]
		self.tabs.addTab(self.current_editor, label)
		self.update_title()
		self.paths.append(label)

	def file_save(self):
		if self.path is None:
			# If we do not have a path, we need to use Save As.
			return self.file_saveas()

		self._save_to_path(self.path)

	def tab_open_doubleclick(self, i):
		if i == -1:
			self.add_new_tab()

	def current_tab_changed(self, i):
		self.path = self.paths[i]
		self.update_title()

	def update_title(self):
		self.setWindowTitle("%s - Text Editor" % (self.path if self.path else "Untitled"))

	def close_current_tab(self, i):
		if self.tabs.count() < 2:
			self.quit()
		else:
			self.update_title()
		self.tabs.removeTab(i)

	def quit(self):
		self.close()

	def undo_document(self):
		self.current_editor.undo()

	def redo_document(self):
		self.current_editor.redo()

	def cut_document(self):
		self.current_editor.cut()

	def copy_document(self):
		self.current_editor.copy()

	def paste_document(self):
		self.current_editor.paste()

	def align_left(self):
		self.current_editor.setAlignment(Qt.AlignLeft)

	def align_right(self):
		self.current_editor.setAlignment(Qt.AlignRight)

	def align_center(self):
		self.current_editor.setAlignment(Qt.AlignCenter)

	def align_justify(self):
		self.current_editor.setAlignment(Qt.AlignJustify)

	def fullscreen(self):
		if not self.isFullScreen():
			self.showFullScreen()
		else:
			self.showMaximized()

	def fontfamily(self, font):
		self.current_editor.setCurrentFont(font)

	def fontsize(self, fontsize):
		self.current_editor.setFontPointSize(int(fontsize))

	def help(self):
		## TODO: Write Help Text
		pass


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setApplicationName('Text Editor')

	window = MainWindow()
	app.exec_()
