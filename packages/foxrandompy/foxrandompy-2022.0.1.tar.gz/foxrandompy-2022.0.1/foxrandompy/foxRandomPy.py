from random import choice, randint


version = "2022.0.1"


def foxRandomVersion():
	return version

def foxRandomInt(xInt = None, yInt = None):
	if xInt == None and yInt == None:
		return print('Аргументы не введены в функции foxRandomInt, xInt и Int!')
	elif xInt == None:
		return print('Аргумент не введён в функции foxRandomInt, xInt!')
	elif yInt == None:
		yInt = xInt
		xInt = 0
	try:
		return randint(xInt, yInt)
	except ValueError:
		print('Произошла ошибка: Похоже X(икс) или Y(игрик) (foxRandomInt) не являются числом или вы используете десятичные числа и т.п.! Данная функция принимает только обычные цифры например "-1", "5"!')
		return '-----------------------------------------------------------'
	except:
		print('Произошла неизвестная ошибка с функцией foxRandomInt! Если вы хотите, можете скинуть ошибку(или скрин ошибки) мне на почту bfire1999@gmail.com!')
		return '-----------------------------------------------------------'

def foxRandomChoice(list = None):
	if list == None:
		return print('Отсутствует список в функции foxRandomChoice!')
	try:
		return choice(list)
	except:
		print('Произошла неизвестная ошибка с функцией foxRandomChoice! Если вы хотите, можете скинуть ошибку(или скрин ошибки) мне на почту bfire1999@gmail.com!')
		return '-----------------------------------------------------------'

def foxRandomTime(style = None, token = None):
	if token == None:
		if style == None: token = ':'
		if style == 'one': token = '-'
		if style == 'two': token = '∙'

	if style == None:
		minutes = randint(1, 59)
		hours = randint(1, 12)
		if minutes < 10:
			minutes = f'0{minutes}'
		if hours < 10:
			hours = f'0{hours}'
		return f"{hours}{token}{minutes}"
	if style == 'one':
		minutes = randint(1, 59)
		hours = randint(1, 12)
		if minutes < 10:
			minutes = f'0{minutes}'
		if hours < 10:
			hours = f'0{hours}'
		return f"{hours}{token}{minutes}"
	if style == 'two':
		minutes = randint(1, 59)
		hours = randint(1, 12)
		if minutes < 10:
			minutes = f'0{minutes}'
		if hours < 10:
			hours = f'0{hours}'
		return f"{hours}{token}{minutes}"