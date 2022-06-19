import threading
import time
from random import randint

from regex import P
from simulated_players import simulate_session
threads = []
wait_times_all = []

num_sessions = 25

for i in range(num_sessions):
    wait_times = [{'max': 0, 'avg': 0}, {'max': 0, 'avg': 0}]
    wait_times_all.append(wait_times)
    threads.append(threading.Thread(target=simulate_session, args=([wait_times])))

for thread in threads:
    time.sleep(randint(1, 10))
    thread.start()

for thread in threads:
    thread.join()

print(len(wait_times_all))
max_wait_all = 0
avg_wait_all = 0
for wait_times in wait_times_all:
    for wait in wait_times:
        max_wait_all += wait['max']
        avg_wait_all += wait['avg']

avg_max_wait = max_wait_all/(num_sessions*2)
avg_avg_wait = avg_wait_all/(num_sessions*2)

print(wait_times_all)
print(avg_max_wait, avg_avg_wait)