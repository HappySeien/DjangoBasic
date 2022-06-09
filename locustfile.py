from locust import HttpUser, task

SERVER_IP_ADDR = '89.108.102.54'

class LoadTestingBraniacLMS(HttpUser):
    @task
    def test_some_pages_open(self):
        # Mainapp
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/courses/1')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/courses/1/detail/1')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/news/1')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/news/1/detail/18')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/contacts/')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/docsite/')

        # Authapp
        self.client.get(f'http://{SERVER_IP_ADDR}/authapp/register/')
        self.client.get(f'http://{SERVER_IP_ADDR}/authapp/login/')
        self.client.get(f'http://{SERVER_IP_ADDR}/authapp/edit/')
