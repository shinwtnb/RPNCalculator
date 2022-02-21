# coding: utf-8

import ui
from console import hud_alert
import math
import re

from RPN import RPN
from mode import Mode


# definition global variables and class
# definition global variables and classes
controlls = {}
inputBuffer = ''
numericalKeys = {'key' + str(i) for i in range(10)}
calcKeyMap = {'keyAdd':RPN.add,
			  'keySubtract':RPN.subtract,
			  'keyMultiply':RPN.multiply,
			  'keyDivide':RPN.divide}
tableMenu = [{'title':'1/y', 'op':lambda x:1/x},
			 {'title':'x^y', 'op':lambda x, y: x**y},
			 {'title':'√','op':lambda x:x**0.5},
			 {'title':'Log_y(x)', 'op':lambda x, y:math.log(x, y)},
			 {'title':'sin(x)', 'op':lambda x: math.sin(x)},
			 {'title':'cos(x)', 'op':lambda x: math.cos(x)},
			 {'title':'tan(x)', 'op':lambda x: math.tan(x)}
			 ]

class Conv():
	reg = re.compile(r'\.*0+$')

	def num(s):
		return float(s)
				
	def str(n):
		return Conv.reg.sub('','{:,f}'.format(n))


def edit_key_tapped(sender):
	global inputBuffer

	# Clearキーの処理
	if sender.name == 'keyClear':
		if Mode.isEditting():
			if inputBuffer != '':
				inputBuffer = ''
			else:
				try:
					inputBuffer = Conv.str(RPN.y())
					RPN.denter()
				except IndexError:
					inputBuffer = ''
		elif Mode.isFixed():
			RPN.denter()
	
	# BSキーの処理
	if sender.name == 'keyBS':
		if Mode.isEditting():
			inputBuffer = inputBuffer[:-1]
			if inputBuffer == '-':
				inputBuffer = ''	
		elif Mode.isFixed():
			inputBuffer = Conv.str(RPN.y())
			RPN.denter()
			Mode.setEditting()					

	# Enterキーの処理
	if sender.name == 'keyEnter':
		if Mode.isEditting():
			try:
				fix_inputBuffer()
			except ValueError:
				pass

	update_displays()


def swap_key_tapped(sender):
	if Mode.isEditting():
		try:
			fix_inputBuffer()
			RPN.swap()
		except ValueError:
			pass
	elif Mode.isFixed():
		RPN.swap()

	update_displays()


def calc_key_tapped(sender):
	try:
		if Mode.isEditting():
			fix_inputBuffer()
		calcKeyMap[sender.name]()
	except ValueError:
		pass
	except ZeroDivisionError:
		hud_alert('ZeroDivision')
	
	update_displays()


def figure_key_tapped(sender):
	global inputBuffer

	# 数字キーの処理
	if sender.name in numericalKeys:
		inputBuffer += sender.title
	
	# 小数点キーの処理
	if sender.name == 'keyDecimal':
		inputBuffer += '.' if not '.' in inputBuffer else ''

	# 符号キーの処理
	if sender.name == 'keySign':
		if '-' in inputBuffer:
			inputBuffer = inputBuffer[1:]
		else:
			inputBuffer = '-' + inputBuffer

	Mode.setEditting()
	update_displays()
	

def table_selected(sender):
	sender.reload()
	if Mode.isEditting():
		try:
			fix_inputBuffer()
		except ValueError:
			return 
	item = sender.items[sender.selected_row]
	if item.get('op', False):
		try:
			RPN.operation(item['op'])
		except ValueError:
			hud_alert('Complex is not supported')
		except ZeroDivisionError:
			hud_alert('Zero division')
	
	update_displays()


def update_displays():
	global inputBuffer

	if Mode.isEditting():
		try:
			controlls['stackX'].text = Conv.str(RPN.y())
		except IndexError:
			controlls['stackX'].text = ''
			
		controlls['stackY'].text_color = 'blue'
		
		controlls['stackY'].text = re.sub(r'(\d)(?=(\d{3})+$)','\\1,',inputBuffer) if not '.' in inputBuffer else re.sub(r'(\d)(?=(\d{3})+\.)','\\1,',inputBuffer)
	
	elif Mode.isFixed():
		try:
			controlls['stackX'].text = Conv.str(RPN.x())
		except IndexError:
			controlls['stackX'].text = ''
			
		controlls['stackY'].text_color = 'black'		
		try:
			controlls['stackY'].text = Conv.str(RPN.y())
		except IndexError:
			controlls['stackY'].text = ''
			
			
def fix_inputBuffer():
	global inputBuffer
	
	try:
		val = Conv.num(inputBuffer)
		RPN.enter(val)
		Mode.setFixed()
		inputBuffer = ''
	except ValueError:
		raise ValueError

# main routine
v = ui.load_view('RPNCalculator')

if min(ui.get_screen_size()) >= 768:
	# iPad
	v.frame = (0, 0, 320, 480)
	v.present('sheet')
else:
	# iPhone
	v.present(orientations=['portrait'])

controlls = {i.name:i for i in v.subviews}

controlls['tableFunction'].data_source.items = tableMenu
update_displays()

