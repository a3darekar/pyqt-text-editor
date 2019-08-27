import sys
import unittest

from editor import MainWindow, QApplication


class MyTestCase(unittest.TestCase):
	app = QApplication(sys.argv)
	window = MainWindow()

	def test_something(self):
		self.assertEqual(True, False)

	def test_path(self):
		index = self.window.tabs.currentIndex()
		if index != -1:
			self.assertEqual(self.window.paths[index], self.window.path)
		else:
			assert True


if __name__ == '__main__':
	unittest.main()
