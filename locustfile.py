from locust import HttpUser, task,between
from locust.env import Environment

class QuickstartUser(HttpUser): 
   wait_time = between(1,5) 
   
   @task
   def hello_world(self):
      self.client.post("/ingest_video",json={"video_id":"y1PZ06qVchc"})
      self.client.get("/docs")

      