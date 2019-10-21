import sys
from unittest import TestCase

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import unittest

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QFileDialog
from pytestqt.plugin import qtbot

from editor import MainWindow, QApplication

"""
	Test Suite for Testing File operations
"""


class FileOperationTests(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.app = QApplication(sys.argv)
		cls.window = MainWindow()
		cls.window.show()

	@classmethod
	def tearDownClass(cls):
		cls.app.exit()

	"""
		Test to verify text content from opened file matches the contents in the file
	"""

	def test_file_open(self):
		self.window._open_file_tab('/home/amey/test')
		file = open('/home/amey/test', 'r')
		text = file.read()
		file.close()

		self.assertEqual(self.window.current_editor.toPlainText(), text)

	"""
		Test to verify save method stores editor text to the file specified  
	"""
	def test_file_save(self):
		text = "Lorem Ipsum dolor sit amet."
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText(text)

		self.window._save_to_path('/home/amey/test_new')

		file = open('/home/amey/test_new', 'r')
		file_text = file.read()
		file.close()

		self.assertEqual(self.window.current_editor.toPlainText(), file_text)

	"""
		Test to verify save method stores editor text to the file specified at given location  
	"""

	def test_file_save_as(self):
		text = "Lorem Ipsum dolor sit amet."
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText(text)

		new_path, _ = QFileDialog.getSaveFileName(self.window, 'Save File As')
		if new_path:
			self.window._save_to_path(new_path)

			file = open(new_path, 'r')
			file_text = file.read()
			file.close()
			self.assertEqual(self.window.current_editor.toPlainText(), file_text)
		else:
			self.assertTrue(True, "File path not selected")

	"""
		Test to verify reopening the file loads content properly   
	"""

	def test_verify_path(self):
		text = "Lorem Ipsum dolor sit amet."
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText(text)

		new_path, _ = QFileDialog.getSaveFileName(self.window, 'Save File As')
		if new_path:
			self.window._save_to_path(new_path)
			current_path = self.window.path
			self.assertEqual(current_path, new_path)
			file = open(new_path, 'r')
			file_text = file.read()
			file.close()
			self.assertEqual(self.window.current_editor.toPlainText(), file_text)
		else:
			self.assertTrue(True, "File path not selected")


"""
	Test to verify text editor operations  
"""
class EditorOperationTests(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.app = QApplication(sys.argv)
		cls.window = MainWindow()
		cls.window.show()

	@classmethod
	def tearDownClass(cls):
		cls.app.exit()

	"""
		Test to verify text editor operation:- cut paste  
	"""
	def test_cut(self):
		text = "text"
		self.write_data(text)
		self.window.current_editor.selectAll()
		self.window.cut_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "")
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), text)
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "%s%s" % (text, text))

	"""
		Test to verify text editor operation:- copy -> paste -> paste  
	"""
	def test_copy(self):
		text = "text"
		self.write_data(text)
		self.window.current_editor.selectAll()
		self.window.copy_document()
		self.assertEqual(self.window.current_editor.toPlainText(), text)
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "text")
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "%s%s" % (text, text))

	"""
		Testing File path matches from paths list for current tab
	"""
	def test_path(self):
		index = self.window.tabs.currentIndex()
		if index != -1:
			self.assertEqual(self.window.paths[index], self.window.path)
		else:
			assert True

	"""
		Helper function to write data to insert text to an editor tab 
	"""
	def write_data(self, text):
		self.window.add_new_tab()
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText(text)


"""
	Test suite for testing non-functional features such as About and Help
"""
class SupportFeatureTestCases(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.app = QApplication(sys.argv)
		cls.window = MainWindow()
		cls.window.show()

	@classmethod
	def tearDownClass(cls):
		cls.app.exit()

	"""
		Test to verify visibility of About dialog
	"""
	def test_aboutDialogVisible(self):
		aboutWindow = self.window.about()
		print(aboutWindow.isVisible())
		self.assertTrue(aboutWindow.isVisible(), "Visible")

	"""
		Test to verify help option triggers the browser window to open the documentation page site
	"""
	def test_help_launchWebBrowser(self):
		helpResponse = self.window.help()
		self.assertTrue(helpResponse, "Browser Launched")


if __name__ == '__main__':
	unittest.main()
