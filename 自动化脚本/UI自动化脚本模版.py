# -*- coding: utf-8 -*-
"""
Playwright 自动化测试脚本模板

使用说明：
1. 复制此模板创建新的测试脚本
2. 修改配置区域的参数
3. 在业务逻辑区域添加具体的操作步骤
4. 运行脚本执行自动化测试

模板版本：v1.0
"""
import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ==================== 配置类 ====================
class Config:
    """测试配置类 - 在此修改测试参数"""

    # ---------- 浏览器配置 ----------
    HEADLESS = False  # 是否无头模式运行
    SLOW_MO = 200  # 操作间隔时间(毫秒)，便于观察
    VIEWPORT_WIDTH = 1920  # 浏览器窗口宽度
    VIEWPORT_HEIGHT = 1080  # 浏览器窗口高度

    # ---------- 超时配置 ----------
    DEFAULT_TIMEOUT = 30000  # 默认操作超时时间(毫秒)
    NAVIGATION_TIMEOUT = 30000  # 页面导航超时时间(毫秒)

    # ---------- 登录配置 ----------
    LOGIN_URL = ""  # 登录页面URL
    USERNAME = ""  # 用户名
    PASSWORD = ""  # 密码

    # ---------- 业务配置 ----------
    # 在此添加业务相关的配置参数
    # 例如：
    # ORDER_ID = "ORD202501010001"
    # CUSTOMER_NAME = "测试客户"


# ==================== 工具函数 ====================
def safe_click(page, locator, description="元素", max_retries=3, timeout=5000):
    """
    安全点击元素，带重试机制

    Args:
        page: Playwright 页面对象
        locator: 元素定位器
        description: 元素描述（用于日志）
        max_retries: 最大重试次数
        timeout: 单次尝试超时时间

    Returns:
        bool: 是否点击成功
    """
    for attempt in range(max_retries):
        try:
            element = page.locator(locator) if isinstance(locator, str) else locator
            element.wait_for(state="visible", timeout=timeout)
            element.click()
            return True
        except PlaywrightTimeoutError:
            if attempt < max_retries - 1:
                print(f"  ⚠️ 点击{description}失败，重试 {attempt + 1}/{max_retries}")
            else:
                print(f"  ❌ 点击{description}失败，已重试{max_retries}次")
                return False
    return False


def safe_fill(page, locator, value, description="输入框", clear_first=True, timeout=5000):
    """
    安全填写输入框

    Args:
        page: Playwright 页面对象
        locator: 元素定位器
        value: 要填写的值
        description: 元素描述（用于日志）
        clear_first: 是否先清空
        timeout: 超时时间

    Returns:
        bool: 是否填写成功
    """
    try:
        element = page.locator(locator) if isinstance(locator, str) else locator
        element.wait_for(state="visible", timeout=timeout)
        if clear_first:
            element.clear()
        element.fill(value)
        return True
    except PlaywrightTimeoutError:
        print(f"  ❌ 填写{description}失败")
        return False


def wait_for_loading_complete(page, timeout=10000):
    """
    等待页面加载完成（等待加载动画消失）

    Args:
        page: Playwright 页面对象
        timeout: 超时时间
    """
    loading_selectors = [
        ".ant-spin-spinning",
        ".ant-spin-dot-spin",
        ".ant-table-loading",
        ".ant-spin-container.ant-spin-blur",
        ".loading",
        ".el-loading-mask"
    ]

    page.wait_for_load_state("networkidle")

    for selector in loading_selectors:
        try:
            loading = page.locator(selector)
            if loading.count() > 0:
                loading.first.wait_for(state="hidden", timeout=timeout)
        except:
            pass


def handle_popup_page(page, click_action, timeout=10000):
    """
    处理点击后打开新标签页的情况

    Args:
        page: 当前页面对象
        click_action: 点击操作的 lambda 函数
        timeout: 等待新页面超时时间

    Returns:
        new_page: 新打开的页面对象
    """
    with page.expect_popup(timeout=timeout) as popup_info:
        click_action()
    new_page = popup_info.value
    new_page.set_default_timeout(Config.DEFAULT_TIMEOUT)
    new_page.wait_for_load_state("domcontentloaded")
    return new_page


def check_element_visible(page, locator, timeout=3000):
    """
    检查元素是否可见

    Args:
        page: Playwright 页面对象
        locator: 元素定位器
        timeout: 超时时间

    Returns:
        bool: 元素是否可见
    """
    try:
        element = page.locator(locator) if isinstance(locator, str) else locator
        return element.is_visible(timeout=timeout)
    except:
        return False


def query_with_retry(page, query_value, max_retries=3, wait_between=2000):
    """
    带重试的查询操作

    Args:
        page: Playwright 页面对象
        query_value: 查询值
        max_retries: 最大重试次数
        wait_between: 重试间隔时间(毫秒)

    Returns:
        bool: 是否查询到数据
    """
    for retry in range(max_retries):
        # 输入查询条件
        page.get_by_role("textbox").first.click()
        page.get_by_role("textbox").first.fill("")
        page.get_by_role("textbox").first.fill(query_value)
        page.get_by_role("button", name="查 询").click()

        # 等待查询结果
        page.wait_for_load_state("networkidle")

        # 等待加载动画消失
        try:
            page.locator(".ant-spin-spinning, .ant-table-loading").first.wait_for(
                state="hidden", timeout=10000
            )
        except:
            pass

        # 额外等待
        page.wait_for_timeout(1500)

        # 检查是否有数据
        data_rows = page.locator(".ant-table-tbody tr.ant-table-row")
        if data_rows.count() > 0:
            print(f"  ✅ 第 {retry + 1} 次查询成功，找到 {data_rows.count()} 条数据")
            return True
        else:
            print(f"  ⚠️ 第 {retry + 1} 次查询无数据，将重试...")
            if retry < max_retries - 1:
                page.wait_for_timeout(wait_between)

    print(f"  ❌ 经过 {max_retries} 次查询仍未找到数据")
    return False


def handle_modal_confirm(page, timeout=3000):
    """
    处理模态框确认

    Args:
        page: Playwright 页面对象
        timeout: 超时时间

    Returns:
        bool: 是否处理了弹窗
    """
    try:
        page.locator(".ant-modal, .ant-modal-wrap").first.wait_for(
            state="visible", timeout=timeout
        )

        # 尝试多种确认按钮选择器
        confirm_selectors = [
            ".ant-modal-confirm-btns .ant-btn-primary",
            ".ant-modal-footer .ant-btn-primary",
            ".ant-modal .ant-btn-primary",
        ]

        for selector in confirm_selectors:
            try:
                confirm_btn = page.locator(selector).first
                if confirm_btn.is_visible(timeout=1000):
                    confirm_btn.click()
                    print("  ✅ 已点击确认按钮")
                    return True
            except:
                continue

        # 尝试使用 get_by_role
        for btn_name in ["确 定", "确定", "确 认", "确认"]:
            try:
                confirm_button = page.get_by_role("button", name=btn_name)
                if confirm_button.is_visible(timeout=1000):
                    confirm_button.click()
                    print(f"  ✅ 已点击确认按钮 ({btn_name})")
                    return True
            except:
                continue

        return False
    except:
        return False


# ==================== 业务操作函数 ====================
def do_login(page):
    """
    执行登录操作

    Args:
        page: Playwright 页面对象

    Returns:
        bool: 是否登录成功
    """
    print("\n[步骤] 执行登录...")

    try:
        # 1. 打开登录页面
        page.goto(Config.LOGIN_URL)
        page.wait_for_load_state("domcontentloaded")
        print("  ✅ 页面加载完成")

        # 2. 输入用户名
        page.get_by_role("textbox", name="用户名").fill(Config.USERNAME)
        print("  ✅ 用户名输入完成")

        # 3. 输入密码
        page.get_by_role("textbox", name="密码").fill(Config.PASSWORD)
        print("  ✅ 密码输入完成")

        # 4. 点击登录按钮
        page.get_by_role("button", name="登录").click()
        page.wait_for_load_state("domcontentloaded")
        print("  ✅ 登录成功")

        return True

    except Exception as e:
        print(f"  ❌ 登录失败: {e}")
        return False


# ==================== 主函数 ====================
def run_auto():
    """自动化测试主函数"""

    with sync_playwright() as p:
        # ---------- 初始化浏览器 ----------
        browser = p.chromium.launch(
            headless=Config.HEADLESS,
            slow_mo=Config.SLOW_MO
        )
        context = browser.new_context(
            viewport={
                'width': Config.VIEWPORT_WIDTH,
                'height': Config.VIEWPORT_HEIGHT
            }
        )
        page = context.new_page()

        # 预定义可能用到的页面变量
        page1 = None
        page2 = None

        # 设置全局超时
        page.set_default_timeout(Config.DEFAULT_TIMEOUT)
        page.set_default_navigation_timeout(Config.NAVIGATION_TIMEOUT)

        try:
            # ==================== 1. 登录 ====================
            if not do_login(page):
                raise Exception("登录失败，终止测试")

            # ==================== 2. 业务操作 ====================
            # 在此添加具体的业务操作步骤
            # 示例：
            # print("\n[步骤X] 操作描述...")
            # page.get_by_role("button", name="按钮名称").click()
            # print("  ✅ 操作完成")

            # ==================== 3. 处理新标签页示例 ====================
            # print("\n[步骤X] 打开新标签页...")
            # with page.expect_popup() as popup_info:
            #     page.get_by_role("link", name="链接名称").click()
            # page1 = popup_info.value
            # page1.set_default_timeout(Config.DEFAULT_TIMEOUT)
            # print("  ✅ 已打开新页面")

            # ==================== 4. 循环处理示例 ====================
            # max_loops = 10
            # for loop_count in range(1, max_loops + 1):
            #     print(f"\n{'=' * 50}")
            #     print(f"🔄 开始第 {loop_count} 轮循环")
            #     print(f"{'=' * 50}")
            #
            #     # 循环内的操作
            #     # ...
            #
            #     # 检查是否需要退出循环
            #     if some_condition:
            #         print("✅ 循环条件满足，退出循环")
            #         break

            # ==================== 完成 ====================
            print("\n" + "=" * 50)
            print("✅ 自动化测试执行完成")
            print("=" * 50)

        except Exception as e:
            print(f"\n❌ 执行出错: {e}")

        finally:
            # 清理资源
            if page1:
                page1.close()
            if page2:
                page2.close()
            # 可选：等待用户确认后关闭
            # input("\n按回车键关闭浏览器...")
            context.close()
            browser.close()


if __name__ == "__main__":
    run_auto()
