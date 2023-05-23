from datetime import datetime

# As format: '0500', in 24 hour format, then subtract lunch from final value if indicated
# name = input("whose hours are being calculated?")
first = input("enter first time value:")
second = input("enter second time value:")
# lunch = 0
lunch = input("any time for lunch break?:")


time_1 = datetime.strptime(first, "%H%M")
time_2 = datetime.strptime(second, "%H%M")

try:
    lunch_time = datetime.strptime(lunch, "%H%M")
    time_interval = time_2 - time_1 - lunch_time
except AttributeError:
    time_interval = time_2 - time_1

time_interval = time_2 - time_1 - lunch_time
# print(f"For {name.capitalize()}, this much time was worked: {time_interval}")

print(f"For that person, this much time was worked: {time_interval}")
