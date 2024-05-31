import math

current_amount = 18
current_volume = 130

for i in range(0,38):
    print(f"volume:{current_volume+3*i}, amount:{current_amount}")
    current_amount += 84 - current_amount/(current_volume+3*i)*3