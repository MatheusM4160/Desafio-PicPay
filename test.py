import time

day = time.localtime().tm_mday
mon = time.localtime().tm_mon
year = time.localtime().tm_year
date = f'{day}/{mon}/{year}'

print(date)