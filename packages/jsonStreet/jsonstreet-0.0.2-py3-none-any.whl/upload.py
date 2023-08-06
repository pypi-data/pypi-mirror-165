from re import I
import pyautogui as pg
from time import sleep


sleep(3)

pg.write('py -m twine upload dist/*')
pg.press('enter')
sleep(1)
pg.write('__token__')
pg.press('enter')
sleep(1)
pg.write('pypi-AgEIcHlwaS5vcmcCJGU5NDNiN2Q5LTU3MDYtNDA5Yy1iMTA4LThjZWI5OGE1NmIwZAACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgmJ71X8xybxnYOyumGC4kGH1i7Cy6H6vKLApuXtQbAm8')
pg.press('enter')
