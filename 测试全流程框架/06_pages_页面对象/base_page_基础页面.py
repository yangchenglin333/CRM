import time
from pathlib import Path
from typing import Optional, Tuple
import importlib.util
import sys

# 动态导入智能定位器模块
self_healing_locator_path = Path(__file__).parent.parent / "05_utils_工具库" / "self_healing_locator_智能定位器.py"
spec = importlib.util.spec_from_file_location("self_healing_locator", str(self_healing_locator_path))
self_healing_locator = importlib.util.module_from_spec(spec)
sys.modules["self_healing_locator"] = self_healing_locator
spec.loader.exec_module(self_healing_locator)
SelfHealingLocator = self_healing_locator.SelfHealingLocator


class BasePage:
    """基础页面类 - 提供通用的页面操作方法"""

    def __init__(self, page):
        """初始化基础页面"""
        self.page = page
        self.page_name = "base"
        self.locator = SelfHealingLocator()
        self._current_selector = None

    async def go_to(self, url: str):
        """跳转到指定URL"""
        await self.page.goto(url)

    async def wait_for_page_load(self, timeout: int = 30000):
        """等待页面加载完成"""
        await self.page.wait_for_load_state("networkidle", timeout=timeout)

    async def find_element(self, element_name: str) -> Tuple[Optional[any], Optional[str]]:
        """智能查找元素（使用Self-Healing定位器）"""
        selectors = self.locator.get_selectors(self.page_name, element_name)
        
        for selector in selectors:
            try:
                element = await self.page.wait_for_selector(selector, timeout=5000, state="visible")
                if element:
                    self.locator.record_success(self.page_name, element_name, selector)
                    self._current_selector = selector
                    return element, selector
            except Exception:
                continue
        
        return None, None

    async def fill_element(self, element_name: str, value: str):
        """填写元素"""
        element, selector = await self.find_element(element_name)
        if element:
            await element.fill(value)
        else:
            raise Exception(f"无法找到元素: {element_name}")

    async def click_element(self, element_name: str):
        """点击元素"""
        element, selector = await self.find_element(element_name)
        if element:
            await element.click()
        else:
            raise Exception(f"无法找到元素: {element_name}")

    async def get_element_text(self, element_name: str) -> Optional[str]:
        """获取元素文本"""
        element, selector = await self.find_element(element_name)
        if element:
            return await element.inner_text()
        return None

    async def is_element_visible(self, element_name: str) -> bool:
        """检查元素是否可见"""
        element, selector = await self.find_element(element_name)
        return element is not None

    async def wait_for_element(self, element_name: str, timeout: int = 10000) -> bool:
        """等待元素出现"""
        selectors = self.locator.get_selectors(self.page_name, element_name)
        
        for selector in selectors:
            try:
                await self.page.wait_for_selector(selector, timeout=timeout, state="visible")
                self.locator.record_success(self.page_name, element_name, selector)
                return True
            except Exception:
                continue
        
        return False

    async def take_screenshot(self, screenshot_path: str):
        """截图"""
        Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
        await self.page.screenshot(path=screenshot_path)

    def sleep(self, seconds: float):
        """等待指定时间"""
        time.sleep(seconds)
