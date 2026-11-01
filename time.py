import time

for seconds in range(60, 0, -1):
    print(f"Time remaining: {seconds} seconds")
    time.sleep(1)

print("Time is up!")