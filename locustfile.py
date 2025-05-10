from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    user_counter = 0  # class-level counter

    def on_start(self):
        """Executed when a simulated user starts"""
        WebsiteUser.user_counter += 1
        self.user_id = WebsiteUser.user_counter
        self.username = f"user{self.user_id}"
        self.password = "test123"
        self.session = self.client

        # Register the user
        self.session.post("/register", data={
            "username": self.username,
            "password": self.password
        })

        # Login
        self.session.post("/login", data={
            "username": self.username,
            "password": self.password
        })

    @task
    def visit_home_and_add_info(self):
        # GET /home
        self.session.get("/home")

        # POST /add-info
        self.session.post("/add-info", data={
            "fname": "Mark Angelo",
            "mname": "G.",
            "lname": "Yakit",
            "age": str(random.randint(18, 60)),
            "address": "Butuan City",
            "birthday": "1990-01-01"
        })

        print(f"user {self.user_id}: Done queue")
