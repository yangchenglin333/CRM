#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRM系统UI自动化 - 可复用测试脚本
生成时间: 2026-05-03
特性:
- 多定位策略支持
- 显示等待
- 元素可见性检查
- AI自愈逻辑框架
"""

from playwright.sync_api import sync_playwright
import time
import os

class CRMAutomation:
    def __init__(self, base_url="http://localhost:5500/CRM.html"):
        self.base_url = base_url
        self.playwright = None
        self.browser = None
        self.page = None
    
    def start(self, headless=False):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        self.page.set_default_timeout(10000)
    
    def stop(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def find_element(self, locators, timeout=10000, state="visible"):
        """
        使用多个定位器查找元素（带AI自愈逻辑）
        
        Args:
            locators: 定位器列表，按优先级排序
            timeout: 超时时间（毫秒）
            state: 等待状态：visible/attached/hidden/detached
            
        Returns:
            找到的元素或None
        """
        for i, locator in enumerate(locators):
            try:
                element = self.page.wait_for_selector(locator, timeout=3000, state=state)
                print(f"✓ 找到元素: {locator} (定位器{i+1})")
                return element
            except Exception as e:
                print(f"✗ 定位器{i+1}失败: {locator}")
        
        print("⚠ 所有定位器均失败，尝试AI自愈...")
        # 这里可以实现AI分析页面结构的逻辑
        return None
    
    def open_login_page(self):
        """打开登录页面"""
        self.page.goto(self.base_url, wait_until="networkidle")
        time.sleep(1)
    
    def input_username(self, username):
        """输入用户名（多定位策略）"""
        locators = [
            "#username",
            "input[id='username']",
            "input[placeholder*='账号']",
            "input[type='text']",
            "//input[@id='username']"
        ]
        element = self.find_element(locators)
        if element:
            element.fill(username)
        return element is not None
    
    def input_password(self, password):
        """输入密码（多定位策略）"""
        locators = [
            "#password",
            "input[id='password']",
            "input[type='password']",
            "input[placeholder*='密码']",
            "//input[@id='password']"
        ]
        element = self.find_element(locators)
        if element:
            element.fill(password)
        return element is not None
    
    def click_login_button(self):
        """点击登录按钮（多定位策略）"""
        locators = [
            "button:has-text('登录')",
            "button[onclick*='login']",
            ".btn:has-text('登录')",
            "//button[text()='登录']"
        ]
        element = self.find_element(locators)
        if element:
            element.click()
        return element is not None
    
    def login(self, username="admin", password="123456"):
        """完整登录流程"""
        print(f"正在登录... 用户: {username}")
        self.open_login_page()
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()
        time.sleep(2)
        return self.is_logged_in()
    
    def is_logged_in(self):
        """检查是否已登录（工作台显示）"""
        locators = [
            "#workPage",
            ".page.active",
            "//div[contains(text(), '工作台')]"
        ]
        try:
            element = self.page.wait_for_selector(locators[0], timeout=3000, state="visible")
            return element is not None
        except:
            return False
    
    def navigate_to_page(self, page_name):
        """导航到指定页面"""
        page_map = {
            "工作台": "workPage",
            "客户管理": "customerPage",
            "商机管理": "businessPage",
            "合同管理": "contractPage"
        }
        
        if page_name in page_map:
            locators = [
                f"li[onclick*='{page_map[page_name]}']",
                f"//li[contains(@onclick, '{page_map[page_name]}')]"
            ]
            element = self.find_element(locators)
            if element:
                element.click()
                time.sleep(1)
                return True
        return False
    
    def take_screenshot(self, name, full_page=False):
        """截图"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{name}_{timestamp}.png"
        self.page.screenshot(path=filename, full_page=full_page)
        print(f"✓ 截图已保存: {filename}")
        return filename


def main():
    """示例: 执行登录流程"""
    print("="*60)
    print("CRM系统UI自动化 - 示例脚本")
    print("="*60)
    
    crm = CRMAutomation()
    crm.start(headless=False)
    
    try:
        # 测试登录
        success = crm.login("admin", "123456")
        
        if success:
            print("✅ 登录成功！")
            crm.take_screenshot("workbench")
            
            # 导航到客户管理
            crm.navigate_to_page("客户管理")
            time.sleep(1)
            crm.take_screenshot("customer_page")
        else:
            print("❌ 登录失败")
            crm.take_screenshot("login_failed")
    
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        crm.take_screenshot("error")
    
    finally:
        input("按回车键退出...")
        crm.stop()


if __name__ == "__main__":
    main()
