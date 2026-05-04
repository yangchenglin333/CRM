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


class DashboardPage(BasePage):
    """仪表盘页面（工作台页面）"""

    def __init__(self, page):
        """初始化仪表盘页面"""
        super().__init__(page)
        self.page_name = "dashboard"

    async def is_dashboard_page(self) -> bool:
        """判断是否在工作台页面"""
        try:
            return await self.is_element_visible("工作台标题")
        except Exception:
            return False

    async def get_today_new_customers(self) -> str:
        """获取今日新增客户数"""
        return await self.get_element_text("今日新增客户") or ""

    async def get_today_followups(self) -> str:
        """获取今日待跟进数"""
        return await self.get_element_text("今日待跟进") or ""

    async def click_customer_menu(self):
        """点击客户管理菜单"""
        await self.click_element("客户管理菜单")
        await self.wait_for_page_load()

    async def verify_workbench_data(self) -> bool:
        """验证工作台数据显示"""
        has_today_customers = await self.is_element_visible("今日新增客户")
        has_today_followups = await self.is_element_visible("今日待跟进")
        return has_today_customers and has_today_followups

    async def verify_customer_list(self) -> bool:
        """验证待跟进客户列表"""
        try:
            return await self.is_element_visible("待跟进客户")
        except Exception:
            return False

    async def verify_approval_list(self) -> bool:
        """验证待审批事项列表"""
        try:
            return await self.is_element_visible("待审批事项")
        except Exception:
            return False

    async def verify_today_customers(self) -> bool:
        """验证今日新增客户"""
        try:
            return await self.is_element_visible("今日新增客户")
        except Exception:
            return False

    async def click_workbench_menu(self):
        """点击工作台菜单"""
        await self.click_element("工作台菜单")
        await self.wait_for_page_load()

    async def click_add_follow_button(self):
        """点击添加跟进按钮"""
        await self.click_element("添加跟进按钮")
        await self.wait_for_page_load()
