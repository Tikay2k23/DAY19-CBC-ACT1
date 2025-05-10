from locust import HttpUser, task, between
import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Executed when a simulated user starts"""
        self.username = f"user_{random_string()}"
        self.password = "test123"
        self.session = self.client

        #Register the user
        self.session.post("/register", data={
            "username": self.username,
            "password": self.password
        })

        #Login
        self.session.post("/login", data={
            "username": self.username,
            "password": self.password
        })

    @task
    def visit_home_and_add_info(self):
        #GET /home
        self.session.get("/home")

        #POST /add-info
        self.session.post("/add-info", data={
            "fname": "John",
            "mname": "A.",
            "lname": "Doe",
            "age": str(random.randint(18, 60)),
            "address": "123 Test Street",
            "birthday": "1990-01-01"
        })
