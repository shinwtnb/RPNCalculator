# coding:utf-8
class RPN():
	'''The class implements Reverse Polish Notation.

	'''
	__stack__ = []
	funcEq = ['op()',
					'op(RPN.__stack__[-1])',
					'op(RPN.__stack__[-2], RPN.__stack__[-1])']
			
	def enter(val):
		RPN.__stack__.append(val)
	
	def denter():
		try:
			RPN.__stack__.pop()
		except IndexError:
			pass
	
	def swap():
		if len(RPN.__stack__) >= 2:
			a = RPN.__stack__[-2:]
			del  RPN.__stack__[-2:]
			a.reverse()
			RPN.__stack__ += a
	
	def x():
		return RPN.__stack__[-2]
	
	def y():
		return RPN.__stack__[-1]
	
	def operation(op):
		n = op.__code__.co_argcount
		if len(RPN.__stack__) >= n:
			z = eval(RPN.funcEq[n])
			if type(z) is complex:
				raise ValueError
			del RPN.__stack__[-n:]
			RPN.__stack__.append(z)
			
	def add():
		RPN.operation(lambda x, y: x + y)

	def subtract():
		RPN.operation(lambda x, y: x - y)
		
	def multiply():
		RPN.operation(lambda x, y: x * y)
		
	def divide():
		RPN.operation(lambda x, y: x / y)


