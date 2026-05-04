from locust import HttpUser, task, between, SequentialTaskSet
import json

class CRMTasks(SequentialTaskSet):
    """CRM系统压测任务"""
    
    @task
    def login(self):
        """测试登录接口"""
        response = self.client.post("/api/users/login", json={
            "username": "admin",
            "password": "123456"
        })
        if response.status_code == 200:
            self.user.token = response.json().get("token", "")
    
    @task(3)
    def get_customers(self):
        """测试获取客户列表接口"""
        headers = {}
        if hasattr(self.user, "token") and self.user.token:
            headers["Authorization"] = f"Bearer {self.user.token}"
        self.client.get("/api/customers", headers=headers)
    
    @task(2)
    def add_customer(self):
        """测试添加客户接口"""
        headers = {}
        if hasattr(self.user, "token") and self.user.token:
            headers["Authorization"] = f"Bearer {self.user.token}"
        self.client.post("/api/customers", headers=headers, json={
            "name": "测试客户",
            "phone": "13812345678",
            "industry": "互联网",
            "tag": ["新客户"],
            "remark": "测试客户"
        })
    
    @task(2)
    def get_business(self):
        """测试获取商机列表接口"""
        headers = {}
        if hasattr(self.user, "token") and self.user.token:
            headers["Authorization"] = f"Bearer {self.user.token}"
        self.client.get("/api/business", headers=headers)
    
    @task(1)
    def add_business(self):
        """测试添加商机接口"""
        headers = {}
        if hasattr(self.user, "token") and self.user.token:
            headers["Authorization"] = f"Bearer {self.user.token}"
        self.client.post("/api/business", headers=headers, json={
            "name": "测试商机",
            "customer_id": 1,
            "amount": 100000.00,
            "status": "待跟进",
            "expected_date": "2026-12-31",
            "follow_person": "管理员"
        })

class WebsiteUser(HttpUser):
    """网站用户"""
    tasks = [CRMTasks]
    wait_time = between(1, 5)  # 每次请求后等待 1-5 秒
    host = "http://localhost:3000"  # CRM 系统地址