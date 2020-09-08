import time
import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(0, 1)

    @task
    def on_start(self):
        points = random.randint(1,20)
        fake_data = [[random.random() for _ in range(13)] for _ in range(points)]
        self.client.post("/predict", json={"data":fake_data})