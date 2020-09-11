import time
import random
from locust import HttpUser, task, between,events
import logging

class QuickstartUser(HttpUser):
    wait_time = between(0, 1)

    @task
    def on_start(self):
        points = random.randint(1,20)
        fake_data = [[random.random() for _ in range(13)] for _ in range(points)]
        self.client.post("/predict", json={"data":fake_data})

@events.quitting.add_listener  
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 2000:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    # elif environment.stats.total.get_response_time_percentile(0.95) > 800:
    #     logging.error("Test failed due to 95th percentile response time > 800 ms")
    #     environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0