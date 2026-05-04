import importlib.util
import sys
from pathlib import Path

# 动态导入基础页面模块
base_page_path = Path(__file__).parent / "base_page_基础页面.py"
spec = importlib.util.spec_from_file_location("base_page", str(base_page_path))
base_page = importlib.util.module_from_spec(spec)
sys.modules["base_page"] = base_page
spec.loader.exec_module(base_page)
BasePage = base_page.BasePage


class LoginPage(BasePage):
    """登录页面"""

    def __init__(self, page):
        """初始化登录页面"""
        super().__init__(page)
        self.page_name = "login"

    def go_to_login_page(self, url: str):
        """跳转到登录页面"""
        self.go_to(url)
        self.wait_for_page_load()

    def login(self, username: str, password: str):
        """登录操作"""
        # 填写用户名
        self.fill_element("用户名输入框", username)
        # 填写密码
        self.fill_element("密码输入框", password)
        # 点击登录按钮
        self.click_element("登录按钮")
        # 等待页面跳转
        self.wait_for_page_load()

    def is_login_page(self) -> bool:
        """判断是否在登录页面"""
        try:
            return self.is_element_visible("登录按钮")
        except Exception:
            return False
