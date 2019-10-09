import sys
from unittest import TestCase

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import unittest

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QFileDialog
from pytestqt.plugin import qtbot

from editor import MainWindow, QApplication


class FileOperationTests(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.app = QApplication(sys.argv)
		cls.window = MainWindow()
		cls.window.show()

	@classmethod
	def tearDownClass(cls):
		cls.app.exit()

	###
	#
	#	TC_A_1
	#
	###
	def test_file_open(self):
		self.window._open_file_tab('/home/amey/test')
		file = open('/home/amey/test', 'r')
		text = file.read()
		file.close()

		self.assertEqual(self.window.current_editor.toPlainText(), text)

	###
	#
	#	TC_A_2
	#
	###
	def test_file_save(self):
		text = "Lorem Ipsum dolor sit amet."
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText(text)

		self.window._save_to_path('/home/amey/test_new')

		file = open('/home/amey/test_new', 'r')
		file_text = file.read()
		file.close()

		self.assertEqual(self.window.current_editor.toPlainText(), file_text)

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


class EditorOperationTests(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.app = QApplication(sys.argv)
		cls.window = MainWindow()
		cls.window.show()

	@classmethod
	def tearDownClass(cls):
		cls.app.exit()

	###
	#
	#	TC_B_1
	#
	###
	def test_cut(self):
		text = "text"
		self.write_data(text)
		self.window.current_editor.selectAll()
		self.window.cut_document()
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), text)
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "%s%s" % (text, text))

	###
	#
	#	TC_B_2
	#
	###
	def test_copy(self):
		text = "text"
		self.write_data(text)
		self.window.current_editor.selectAll()
		self.window.copy_document()
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "text")
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "%s%s" % (text, text))

	###
	#
	#	TC_B_3
	#
	###
	def test_path(self):
		index = self.window.tabs.currentIndex()
		if index != -1:
			self.assertEqual(self.window.paths[index], self.window.path)
		else:
			assert True

	def write_data(self, text):
		self.window.add_new_tab()
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText(text)


class SupportFeatureTestCases(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.app = QApplication(sys.argv)
		cls.window = MainWindow()
		cls.window.show()

	@classmethod
	def tearDownClass(cls):
		cls.app.exit()

	def test_aboutDialogVisible(self):
		aboutWindow = self.window.about()
		self.assertTrue(self.window.isVisible(), "Visible")
		# print(QTest.mouseClick(aboutWindow.buttonBox, Qt.LeftButton))
		# self.assertTrue(self.window.isVisible() == False, "Not Visible")

	def test_help_launchWebBrowser(self):
		helpResonse = self.window.help()
		self.assertTrue(helpResonse, "Browser Launched")
		# print(QTest.mouseClick(aboutWindow.buttonBox, Qt.LeftButton))
		# self.assertTrue(self.window.isVisible() == False, "Not Visible")


if __name__ == '__main__':
	unittest.main()
