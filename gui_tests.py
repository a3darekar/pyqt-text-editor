import sys
from unittest import TestCase
from PyQt5.QtGui import QTextCursor

from editor import MainWindow, QApplication


class EditorOperationTests(TestCase):
	app = QApplication(sys.argv)
	window = MainWindow()

	def test_path(self):
		index = self.window.tabs.currentIndex()
		if index != -1:
			self.assertEqual(self.window.paths[index], self.window.path)
		else:
			assert True

	def test_copy(self):
		self.window.add_new_tab()
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText("Hello")
		self.window.current_editor.selectAll()
		self.window.copy_document()
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "Hello")
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "HelloHello")

	def test_cut(self):
		self.window.add_new_tab()
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText("Hello")
		self.window.current_editor.selectAll()
		self.window.cut_document()
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "Hello")
		self.window.paste_document()
		self.assertEqual(self.window.current_editor.toPlainText(), "HelloHello")


class FileOperationTests(TestCase):
	app = QApplication(sys.argv)
	window = MainWindow()

	def test_file_open(self):
		self.window._open_file_tab('/home/amey/test')

		file = open('/home/amey/test', 'r')
		text = file.read()
		file.close()

		self.assertEqual(self.window.current_editor.toPlainText(), text)

	def test_file_save(self):
		text = "Lorem Ipsum dolor sit amet."
		cursor = QTextCursor(self.window.current_editor.document())
		cursor.insertText(text)

		self.window._save_to_path('/home/amey/test_new')

		file = open('/home/amey/test_new', 'r')
		file_text = file.read()
		file.close()

		self.assertEqual(self.window.current_editor.toPlainText(), file_text)


if __name__ == '__main__':
	unittest.main()
