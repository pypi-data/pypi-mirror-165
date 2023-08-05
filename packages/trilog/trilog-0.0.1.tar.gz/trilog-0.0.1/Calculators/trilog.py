import math as m

def anglerefiner(angle):
  print('Is your angle in degree?')
  resp = input('Type "y" for yes and "n" for no: ')
  if resp == 'y':
    angle = angle * m.pi / 180
  return angle
  
def sin(x):
  a = anglerefiner(x)
  value = m.sin(a)
  return value

def cos(x):
  value = (1 - (sin(x) ** 2)) ** 0.5
  return value

def tan(x):
  try:
    s = sin(x)
    value = s / (1 - (s ** 2)) ** 0.5
    return value
  except ZeroDivisionError:
    return '∞'

def sec(x):
  try:
    value = 1 / (1 - (sin(x) ** 2)) ** 0.5
    return value
  except ZeroDivisionError:
    return '∞'

def cosec(x):
  try:
    value = 1 / sin(x)
    return value
  except ZeroDivisionError:
    return '∞'

def cot(x):
  try:
    value = 1 / tan(x)
    return value
  except ZeroDivisionError:
    return '∞'

def ln(no , n):
  l = n * ((no ** (1/n)) - 1)
  return l

def log(no , base , acc):
  acc = acc * 100000
  no1 = ln(no , acc)
  base1 = ln(base , acc)
  z = no1 / base1
  print(z)
  print('This no is usually inaccurate after 7 decimal digits')