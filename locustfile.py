from locust import HttpUser, task

class DeliveriesUser(HttpUser):
    @task
    def deliveries(self):
        self.client.get("/deliveries")
    
    @task
    def create_delivery(self):
        self.client.post("/deliveries", json={"status":"выполняется"})
