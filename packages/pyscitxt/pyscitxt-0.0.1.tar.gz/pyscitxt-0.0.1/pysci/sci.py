class Py:
	'''
	Example:

	my = Py('')
	my.a()
	my.b()


	'''
	def __init__(self,name):
		self.name = name


	def a(self):
		print("a")

	def b(self):
		print("b")


if __name__ == '__main__':
	my = Py('')
	my.a()
	my.b()


