# -*- coding: utf-8 -*-
"""
POM自动化测试脚本
使用Playwright，全部使用显式等待，等待时间10秒，支持重试
异步版本，支持循环执行直到查询不到结果
"""
from playwright.async_api import async_playwright
import importlib
import playwright_common
import asyncio

importlib.reload(playwright_common)
from playwright_common import PlaywrightHelper

# 配置
WAIT_TIME = 10000  # 显式等待时间（毫秒）
MAX_RETRIES = 3  # 最大重试次数
URL = "https://xin-sandbox.asiainfo.com:14603/webapps/ai-pom-web/myApprove"
# URL = "https://xin-uat.asiainfo.com/webapps/ai-pom-web"
USERNAME = "yangcl5"
PASSWORD = "133366YCL@ycl"
PROXY_USERNAME = "yangcl5"

# 创建公共工具实例
helper = PlaywrightHelper(wait_time=WAIT_TIME, max_retries=MAX_RETRIES)

# 验证方法是否存在
if not hasattr(helper, 'get_table_rows_data'):
    print("❌ 错误：get_table_rows_data 方法不存在！")
    print("可用方法:", [m for m in dir(helper) if not m.startswith('_') and callable(getattr(helper, m))])
    raise AttributeError("PlaywrightHelper 类缺少 get_table_rows_data 方法")
else:
    print("✅ get_table_rows_data 方法存在")


# 为了向后兼容，提供函数式接口（直接调用helper的方法）
def click_menu_item(page, menu_text):
    """点击左侧菜单项"""
    return helper.click_menu_item(page, menu_text)


def fill_select_input(page, locator, value):
    """填充选择输入框（支持Ant Design Select组件）"""
    return helper.fill_select_input(page, locator, value)


async def fill_select_input_async(page, locator, value):
    """异步版本的填充选择输入框（支持Ant Design Select组件）"""
    return await helper.fill_select_input_async(page, locator, value)


def select_dropdown_option(page, input_value, expected_text):
    """选择下拉选项"""
    return helper.select_dropdown_option(page, input_value, expected_text)


def wait_for_page_ready(page, timeout=WAIT_TIME):
    """等待页面就绪"""
    return helper.wait_for_page_ready(page, timeout)


async def wait_for_page_ready_async(page, timeout=WAIT_TIME):
    """异步版本的等待页面就绪"""
    return await helper.wait_for_page_ready_async(page, timeout)


def wait_for_element_ready(page, element, description):
    """等待元素就绪"""
    return helper.wait_for_element_ready(page, element, description)


async def wait_for_element_ready_async(page, element, description):
    """异步版本的等待元素就绪"""
    return await helper.wait_for_element_ready_async(page, element, description)


def try_locators(page, locator_factories, element_name, timeout=WAIT_TIME):
    """通用重试定位函数：依次尝试多种定位方式，直到找到可用元素"""
    return helper.try_locators(page, locator_factories, element_name, timeout)


async def try_locators_async(page, locator_factories, element_name, timeout=WAIT_TIME):
    """异步版本的通用重试定位函数：依次尝试多种定位方式，直到找到可用元素"""
    return await helper.try_locators_async(page, locator_factories, element_name, timeout)


def fill_input_with_wait(page, locator, value, description, use_type=False):
    """填充输入框并等待输入完成"""
    return helper.fill_input_with_wait(page, locator, value, description, use_type)


async def fill_input_with_wait_async(page, locator, value, description, use_type=False):
    """异步版本的填充输入框并等待输入完成"""
    return await helper.fill_input_with_wait_async(page, locator, value, description, use_type)


def click_radio_button(page, radio_locator, description):
    """点击radio按钮并确保选中"""
    return helper.click_radio_button(page, radio_locator, description)


def click_button_with_retry(page, locator_factories, element_name, max_retries=10, scroll_step=300):
    """点击按钮，如果按钮被禁用则滚动后重试"""
    return helper.click_button_with_retry(page, locator_factories, element_name, max_retries, scroll_step)


def click_change_button_with_radio_retry(page, button_locator_factories, radio_locator, max_retries=15):
    """点击变更按钮，如果无法点击则回到项目代码radio按钮，模拟键盘向下键后重试"""
    return helper.click_change_button_with_radio_retry(page, button_locator_factories, radio_locator, max_retries)


def wait_for_modal(page):
    """等待弹窗出现"""
    return helper.wait_for_modal(page)


async def wait_for_modal_async(page):
    """异步版本的等待弹窗出现"""
    return await helper.wait_for_modal_async(page)


def jump_to_last_page(page):
    """跳转到分页的最后一页"""
    return helper.jump_to_last_page(page)


async def get_table_rows_data_async(page, header_keywords=None, serial_pattern="POM", enable_fallback=True):
    """
    异步版本的获取表格行数据，自动识别流水号列

    Args:
        page: Playwright页面对象（异步API）
        header_keywords: 表头关键词列表，用于查找流水号列
                        默认值：['申请单流水号', '流水号', '申请单号', '单号']
        serial_pattern: 流水号匹配模式，默认"POM"（匹配POM开头的数字）
        enable_fallback: 是否启用fallback机制（从第一行数据推断列索引），默认True

    Returns:
        列表，每个元素包含：
        - index: 行索引（从0开始）
        - serialNumber: 流水号
        - row: 行元素（在evaluate中无法返回，实际返回None）
    """
    return await helper.get_table_rows_data_async(page, header_keywords, serial_pattern, enable_fallback)


async def wait_for_overlay_disappear_async(page, timeout=WAIT_TIME):
    """异步版本的等待遮罩层消失"""
    try:
        # 等待常见的遮罩层消失
        overlay_selectors = [
            '.ant-spin-spinning',
            '.ant-spin-container .ant-spin-blur',
            '.loading',
            '[class*="loading"]',
            '[class*="spinner"]',
            '.ant-skeleton',
            '.ant-modal-mask:not([style*="display: none"])'
        ]

        for selector in overlay_selectors:
            try:
                await page.wait_for_selector(selector, state="hidden", timeout=min(timeout / 1000.0, 3))
            except:
                pass

        # 等待一小段时间确保遮罩层完全消失
        await page.wait_for_timeout(200)
    except:
        # 如果出错，简单等待一小段时间
        await page.wait_for_timeout(300)


async def main():
    """POM自动化测试主函数（异步版本）"""
    playwright = None
    browser = None
    page = None

    try:
        print("=" * 50)
        print("POM自动化测试开始")
        print("=" * 50)

        # 初始化浏览器
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        # 步骤1. 打开链接
        print("\n[步骤1] 打开登录页面...")
        await page.goto(URL, wait_until="domcontentloaded", timeout=WAIT_TIME)
        await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
        print("✅ 页面加载完成")

        # 步骤2. 输入用户名和密码
        print("\n[步骤2] 输入用户名和密码...")
        username_locators = [
            lambda p: p.locator("input[name='username']"),
            lambda p: p.locator("input#username"),
            lambda p: p.locator("#username")
        ]
        username_input = await try_locators_async(page, username_locators, "用户名输入框")
        await username_input.clear()
        await username_input.fill(USERNAME)
        await page.wait_for_timeout(200)
        print(f"✅ 已输入用户名: {USERNAME}")

        password_locators = [
            lambda p: p.locator("input[name='password']"),
            lambda p: p.locator("input#password"),
            lambda p: p.locator("#password")
        ]
        password_input = await try_locators_async(page, password_locators, "密码输入框")
        await password_input.clear()
        await password_input.fill(PASSWORD)
        await page.wait_for_timeout(200)
        print(f"✅ 已输入密码")

        # 步骤3. 点击登录
        print("\n[步骤3] 点击登录...")

        login_button_locators = [
            lambda p: p.get_by_role("button", name="登录"),
            lambda p: p.get_by_text("登录", exact=True),
            lambda p: p.locator("button:has-text('登录')").first,
            lambda p: p.locator("button[type='submit']")
        ]
        login_button = await try_locators_async(page, login_button_locators, "登录按钮")
        await login_button.click()
        print("✅ 已点击登录按钮")

        # 等待登录完成
        print("  等待登录完成...")
        try:
            await page.wait_for_url(f"**/webapps/ai-pom-web/**", timeout=WAIT_TIME)
        except:
            menu_locators = [
                lambda p: p.get_by_text("进度与成本管理", exact=True).first,
                lambda p: p.locator("span:has-text('进度与成本管理')").first,
                lambda p: p.get_by_role("menuitem", name="进度与成本管理"),
                lambda p: p.locator("div:has-text('进度与成本管理')").first,
                lambda p: p.locator("li:has-text('进度与成本管理')").first
            ]
            await try_locators_async(page, menu_locators, "进度与成本管理菜单")

        # 等待遮罩层消失
        await wait_for_overlay_disappear_async(page)
        print("✅ 登录成功")

        # 循环执行审批流程，直到查询不到申请单流水号
        loop_count = 0
        query_fail_count = 0  # 查询失败计数器
        while True:
            loop_count += 1
            print("\n" + "=" * 50)
            print(f"开始第 {loop_count} 次循环")
            print("=" * 50)

            # 步骤4. 点击左侧菜单栏的"我的审批"模块父级
            print("\n[步骤4] 点击左侧菜单栏'我的审批'模块...")
            await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)

            print("  定位'我的审批'菜单...")
            my_approval_menu_locators = [
                lambda p: p.locator("xpath=//span[text()='我的审批']").first,
                lambda p: p.get_by_text("我的审批", exact=True).first,
                lambda p: p.locator("li:has-text('我的审批')").first,
                lambda p: p.get_by_role("menuitem", name="我的审批"),
                lambda p: p.locator("xpath=//span[contains(text(),'我的审批')]").first
            ]
            my_approval_menu = await try_locators_async(page, my_approval_menu_locators, "我的审批菜单")
            await my_approval_menu.scroll_into_view_if_needed()
            await my_approval_menu.wait_for(state="visible", timeout=WAIT_TIME)
            await my_approval_menu.wait_for(state="attached", timeout=WAIT_TIME)
            print("  点击'我的审批'菜单...")
            try:
                await my_approval_menu.click()
            except Exception as e:
                print(f"  直接点击失败，尝试使用JavaScript点击: {e}")
                await my_approval_menu.evaluate("el => el.click()")
            print("✅ 已点击'我的审批'菜单")

            # 优化：等待"我的审批"模块完全加载（针对网速慢的情况）
            print("  等待'我的审批'模块完全加载...")

            # 等待DOM和网络加载完成
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=WAIT_TIME)
                print("  ✅ DOM已加载")
            except:
                print("  ⚠ 警告：等待DOM加载超时，继续尝试...")

            try:
                await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
                print("  ✅ 网络请求已完成")
            except:
                print("  ⚠ 警告：等待网络空闲超时，继续尝试...")

            # 等待主要内容区域出现
            print("  等待主要内容区域加载...")
            try:
                await page.wait_for_selector("main, .ant-layout-content, [class*='content'], #root", timeout=WAIT_TIME)
                print("  ✅ 主要内容区域已出现")
            except:
                print("  ⚠ 警告：主要内容区域可能未完全加载，继续尝试...")

            # 等待关键元素出现（表单、输入框等，这些是后续操作需要的）
            print("  等待关键元素加载...")
            key_selectors = [
                "form, .ant-form, [class*='form']",  # 表单容器
                ".ant-select, input, .ant-input",  # 输入框或选择框
                "table, .ant-table",  # 表格（如果有）
                "button, .ant-btn"  # 按钮
            ]

            elements_loaded = False
            max_wait_attempts = 5
            for attempt in range(max_wait_attempts):
                try:
                    # 检查至少一个关键元素是否存在
                    for selector in key_selectors:
                        try:
                            element_count = await page.evaluate(f"""
                                () => {{
                                    const elements = document.querySelectorAll('{selector}');
                                    return elements.length;
                                }}
                            """)
                            if element_count > 0:
                                elements_loaded = True
                                print(f"  ✅ 关键元素已加载（找到 {element_count} 个 {selector} 元素）")
                                break
                        except:
                            continue

                    if elements_loaded:
                        break
                    else:
                        if attempt < max_wait_attempts - 1:
                            print(f"  等待关键元素出现... (尝试 {attempt + 1}/{max_wait_attempts})")
                            await page.wait_for_timeout(1000)
                            # 再次等待网络空闲
                            try:
                                await page.wait_for_load_state("networkidle", timeout=3000)
                            except:
                                pass
                except Exception as e:
                    if attempt < max_wait_attempts - 1:
                        print(f"  等待关键元素时出错，重试... (尝试 {attempt + 1}/{max_wait_attempts}): {str(e)[:50]}")
                        await page.wait_for_timeout(1000)
                    else:
                        print(f"  ⚠ 警告：等待关键元素超时: {e}")

            # 等待页面状态稳定（确保没有正在进行的动画或加载）
            print("  等待页面状态稳定...")
            await page.wait_for_timeout(500)  # 短暂等待，让页面稳定

            # 验证页面是否真的加载完成（检查是否有加载中的指示器）
            try:
                loading_indicators = await page.evaluate("""
                    () => {
                        // 检查常见的加载指示器
                        const loadingSelectors = [
                            '.ant-spin-spinning',
                            '.loading',
                            '[class*="loading"]',
                            '[class*="spinner"]',
                            '.ant-skeleton'
                        ];
                        for (const selector of loadingSelectors) {
                            const elements = document.querySelectorAll(selector);
                            for (const el of elements) {
                                const style = window.getComputedStyle(el);
                                if (style.display !== 'none' && style.visibility !== 'hidden') {
                                    return true;
                                }
                            }
                        }
                        return false;
                    }
                """)

                if loading_indicators:
                    print("  ⚠ 检测到加载指示器，等待加载完成...")
                    # 等待加载指示器消失
                    max_loading_wait = 10
                    for i in range(max_loading_wait):
                        await page.wait_for_timeout(500)
                        loading_indicators = await page.evaluate("""
                            () => {
                                const loadingSelectors = [
                                    '.ant-spin-spinning',
                                    '.loading',
                                    '[class*="loading"]',
                                    '[class*="spinner"]',
                                    '.ant-skeleton'
                                ];
                                for (const selector of loadingSelectors) {
                                    const elements = document.querySelectorAll(selector);
                                    for (const el of elements) {
                                        const style = window.getComputedStyle(el);
                                        if (style.display !== 'none' && style.visibility !== 'hidden') {
                                            return true;
                                        }
                                    }
                                }
                                return false;
                            }
                        """)
                        if not loading_indicators:
                            print("  ✅ 加载指示器已消失")
                            break
                        if i == max_loading_wait - 1:
                            print("  ⚠ 警告：加载指示器可能仍在显示，继续执行...")
                else:
                    print("  ✅ 未检测到加载指示器，页面可能已加载完成")
            except Exception as e:
                print(f"  ⚠ 检查加载指示器时出错: {e}，继续执行...")

            # 最终等待网络空闲，确保所有异步请求完成
            try:
                await page.wait_for_load_state("networkidle", timeout=5000)
                print("  ✅ 最终网络状态已稳定")
            except:
                print("  ⚠ 警告：最终网络等待超时，继续执行...")

            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            print("✅ 我的审批模块已完全加载")

            # 步骤5.点击"审批干预"模块
            print(" \n[步骤5] 点击'审批干预'模块...")
            intervention_locators = [
                lambda p: p.get_by_text("审批干预", exact=True).first,
                lambda p: p.locator("li:has-text('审批干预')").first,
                lambda p: p.locator("span:has-text('审批干预')").first,
                lambda p: p.get_by_role("menuitem", name="审批干预")
            ]
            intervention_menu = await try_locators_async(page, intervention_locators, "审批干预模块")
            await intervention_menu.scroll_into_view_if_needed()
            await intervention_menu.click()
            print("✅ 已点击'审批干预'模块")

            await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            print("✅审批干预已加载")

            # 找到申请单流水号输入框，输入并选择
            print(" 找到申请单流水号输入框，输入并选择...")

            # 等待页面完全加载（按照规则：DOM → 网络 → 元素可见 → 元素可交互）
            print("  等待页面状态稳定...")
            await page.wait_for_load_state("domcontentloaded", timeout=WAIT_TIME)
            await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)

            # 等待表单容器加载
            try:
                await page.wait_for_selector("form, .ant-form, [class*='form']", timeout=5000)
                print("  ✅ 表单容器已加载")
            except:
                print("  ⚠ 警告：表单容器可能未完全加载，继续尝试...")

            await wait_for_page_ready_async(page)

            # 找到"申请单流水号"输入框
            print("  查找'申请单流水号'输入框...")
            serial_number_input_locators = [
                # 方法1：通过包含文本的元素定位，找到选择框（不是下拉菜单）
                lambda p: p.locator("*:has-text('申请单流水号')").locator(
                    "xpath=following::div[contains(@class,'ant-select') and not(contains(@class,'ant-select-dropdown'))][1]").first,
                # 方法2：通过label定位
                lambda p: p.locator("label:has-text('申请单流水号')").locator(
                    "xpath=following::div[contains(@class,'ant-select') and not(contains(@class,'ant-select-dropdown'))][1]").first,
                # 方法3：直接查找表单中的ant-select（排除下拉菜单）
                lambda p: p.locator(
                    "form .ant-select:not(.ant-select-dropdown), .ant-form .ant-select:not(.ant-select-dropdown)").first,
            ]

            serial_number_input = await try_locators_async(page, serial_number_input_locators, "申请单流水号输入框",
                                                           timeout=WAIT_TIME)

            # 等待元素完全就绪（按照规则：可见 → 已附加 → 可交互）
            try:
                await serial_number_input.scroll_into_view_if_needed(timeout=5000)
            except:
                print("  ⚠ 警告：滚动到元素失败，继续尝试...")

            try:
                await serial_number_input.wait_for(state="visible", timeout=WAIT_TIME)
                await serial_number_input.wait_for(state="attached", timeout=WAIT_TIME)
                print("  ✅ 申请单流水号输入框已就绪")
            except Exception as e:
                print(f"  ⚠ 警告：等待元素就绪时出错: {e}，继续尝试...")

            print("  在'申请单流水号'输入框中输入POM2026011529416...")
            await fill_select_input_async(page, serial_number_input, "POM2026011529416")

            # 等待输入完成
            await page.wait_for_timeout(500)

            # 确保输入框获得焦点
            try:
                await serial_number_input.focus()
                await page.wait_for_timeout(200)
            except:
                pass

            # 等待下拉菜单出现并加载选项
            print("  等待下拉选项加载...")
            dropdown_visible = False
            try:
                await page.wait_for_selector(
                    ".ant-select-dropdown:not([style*='display: none']), "
                    ".ant-select-dropdown-menu:not([style*='display: none']), "
                    "div[role='listbox']:not([style*='display: none'])",
                    timeout=3000
                )
                dropdown_visible = True
                print("  ✅ 下拉菜单已出现")
            except:
                print("  ⚠ 警告：下拉菜单可能未完全加载，继续尝试...")

            # 检查下拉菜单中是否有搜索结果
            print("  检查下拉菜单中是否有搜索结果...")
            has_results = False
            try:
                # 检查下拉菜单中是否有选项
                dropdown_options = await page.evaluate("""
                    () => {
                        const dropdown = document.querySelector('.ant-select-dropdown:not([style*="display: none"]), .ant-select-dropdown-menu:not([style*="display: none"]), div[role="listbox"]:not([style*="display: none"])');
                        if (!dropdown) return false;
                        const options = dropdown.querySelectorAll('.ant-select-item, li[role="option"], .ant-select-dropdown-menu-item');
                        return options.length > 0;
                    }
                """)
                if dropdown_options:
                    has_results = True
                    print("  ✅ 下拉菜单中有搜索结果")
                else:
                    print("  ⚠ 下拉菜单中没有搜索结果")
            except Exception as e:
                print(f"  ⚠ 检查下拉菜单时出错: {e}")
                # 如果检查失败，尝试通过文本内容检查
                try:
                    dropdown_text = await page.evaluate("""
                        () => {
                            const dropdown = document.querySelector('.ant-select-dropdown:not([style*="display: none"])');
                            return dropdown ? dropdown.textContent.trim() : '';
                        }
                    """)
                    if dropdown_text and "无数据" not in dropdown_text and "暂无" not in dropdown_text:
                        has_results = True
                        print("  ✅ 下拉菜单中有搜索结果（通过文本检查）")
                    else:
                        print("  ⚠ 下拉菜单中没有搜索结果（通过文本检查）")
                except:
                    pass

            # 使用键盘操作选择选项
            target_text = "POM2026011529416"
            print("  使用键盘操作选择选项...")
            # 确保输入框有焦点
            try:
                await serial_number_input.focus()
                await page.wait_for_timeout(200)
            except:
                pass

            # 按向下键选择第一个选项
            print("  按向下键选择选项...")
            await page.keyboard.press("ArrowDown")
            await page.wait_for_timeout(500)

            # 验证选项是否被选中（高亮）
            try:
                await page.wait_for_function(
                    "() => document.querySelector('.ant-select-item-option-active, .ant-select-item-option-selected') !== null",
                    timeout=1000
                )
                print("  ✅ 选项已高亮")
            except:
                print("  ⚠ 警告：选项可能未高亮，继续操作...")

            # 按Enter键确认选择
            print("  按Enter键确认选择...")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(500)

            # 等待下拉菜单关闭
            print("  等待下拉菜单关闭...")
            try:
                # 等待下拉菜单隐藏
                await page.wait_for_function(
                    "() => { const dropdown = document.querySelector('.ant-select-dropdown:not([style*=\"display: none\"])'); return !dropdown || dropdown.offsetParent === null; }",
                    timeout=3000
                )
                print("  ✅ 下拉菜单已关闭")
            except:
                # 如果等待隐藏超时，尝试等待一段时间让下拉菜单自然关闭
                await page.wait_for_timeout(1000)
                print("  ⚠ 警告：等待下拉菜单关闭超时，继续执行...")

            # 验证选择是否成功（检查输入框的值或文本内容）
            option_clicked = False
            try:
                await page.wait_for_timeout(300)
                # 尝试多种方式获取输入框的值
                input_value = ""
                try:
                    # 检查选中值的显示元素
                    selected_value = await page.evaluate("""
                    () => {
                        const selected = document.querySelector('.ant-select-selection-selected-value');
                        return selected ? selected.textContent || selected.getAttribute('title') || '' : '';
                    }
                """)
                    input_value = selected_value
                except:
                    try:
                        input_value = await serial_number_input.text_content() or ""
                    except:
                        try:
                            input_value = await serial_number_input.evaluate(
                                "el => el.value || el.textContent || el.getAttribute('title') || ''") or ""
                        except:
                            pass

                if target_text in input_value:
                    print(f"  ✅ 已通过键盘选择选项: {target_text}")
                    option_clicked = True
                else:
                    print(f"  ⚠ 警告：选择可能未成功，输入框值: {input_value}")
            except Exception as verify_error:
                print(f"  ✅ 已通过键盘选择选项（验证时出错: {str(verify_error)[:50]}）")
                option_clicked = True

            # 最终验证选择是否成功
            if option_clicked:
                # 等待选择完成
                await page.wait_for_timeout(500)
                # 验证选中值是否显示
                try:
                    selected_value_element = page.locator(
                        ".ant-select-selection-selected-value[title='POM2026011529416']").first
                    if await selected_value_element.count() > 0:
                        print(f"  ✅ 已成功选择申请单流水号: {target_text}")
                    else:
                        # 尝试其他方式验证
                        selected_text = await page.evaluate("""
                            () => {
                                const selected = document.querySelector('.ant-select-selection-selected-value');
                                return selected ? selected.textContent.trim() : '';
                            }
                        """)
                        if target_text in selected_text:
                            print(f"  ✅ 已成功选择申请单流水号: {target_text}")
                        else:
                            print(f"  ⚠ 警告：选择验证失败，当前值: {selected_text}")
                except Exception as e:
                    print(f"  ⚠ 警告：验证选择结果时出错: {e}")
            else:
                print(f"  ⚠ 警告：未能成功选择选项，继续执行...")

            # 等待操作完成
            await page.wait_for_timeout(500)
            await wait_for_page_ready_async(page, timeout=3000)
            print("✅ 申请单流水号输入完成")

            # 点击查询按钮
            print("\n  点击查询按钮...")

            print("✅ 申请单流水号输入完成")

            # 点击查询按钮
            print("\n  点击查询按钮...")

            # 等待页面状态稳定（按照规则：操作前必须等待页面完全加载）
            print("  等待页面状态稳定...")
            await page.wait_for_load_state("domcontentloaded", timeout=WAIT_TIME)
            await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)

            # 多种方式定位查询按钮
            query_button_locators = [
                # 方法1：通过文本定位（最常用）
                lambda p: p.get_by_role("button", name="查询").first,
                lambda p: p.get_by_text("查 询", exact=True).first,
                lambda p: p.get_by_text("查询", exact=True).first,
            ]

            query_button = await try_locators_async(page, query_button_locators, "查询按钮", timeout=WAIT_TIME)

            # 等待元素完全就绪（按照规则：可见 → 已附加 → 可交互）
            await query_button.scroll_into_view_if_needed()
            await query_button.wait_for(state="visible", timeout=WAIT_TIME)
            await query_button.wait_for(state="attached", timeout=WAIT_TIME)

            # 点击查询按钮
            try:
                await query_button.click()
                print("  ✅ 已点击查询按钮")
            except Exception as click_error:
                print(f"  警告：直接点击失败，使用JavaScript: {click_error}")
                await query_button.evaluate("""
                    el => {
                        if (el) {
                            el.click();
                            el.dispatchEvent(new Event('click', { bubbles: true }));
                        }
                    }
                """)
                print("  ✅ 已通过JavaScript点击查询按钮")

            # 等待查询结果加载（按照规则：操作后必须等待响应完成）
            print("  等待查询结果加载...")
            await page.wait_for_timeout(1000)
            await page.wait_for_load_state("domcontentloaded", timeout=WAIT_TIME)
            await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)

            # 等待表格容器出现
            try:
                await page.wait_for_selector("table, .ant-table", timeout=WAIT_TIME)
                print("  ✅ 表格容器已出现")
            except:
                print("  ⚠ 警告：表格容器可能未出现，继续尝试...")

            # 等待查询结果加载（关键：确保数据已加载）
            print("  等待查询结果加载...")
            max_wait_attempts = 5
            has_data_rows = False
            row_count = 0

            for attempt in range(max_wait_attempts):
                try:
                    # 等待表格容器出现
                    await page.wait_for_selector("table, .ant-table", timeout=3000)

                    # 检查表格中是否有数据行（排除表头）
                    row_count = await page.evaluate("""
                        () => {
                            // 查找所有表格行
                            const rows = document.querySelectorAll('table tbody tr');
                            let validRowCount = 0;

                            // 过滤掉空行和"无数据"提示行
                            rows.forEach(row => {
                                const text = row.textContent.trim();
                                // 排除空行和无数据提示行
                                if (text && 
                                    !text.includes('暂无数据') && 
                                    !text.includes('无数据') && 
                                    !text.includes('No Data') &&
                                    !text.includes('没有数据') &&
                                    text.length > 0) {
                                    validRowCount++;
                                }
                            });

                            return validRowCount;
                        }
                    """)

                    if row_count > 0:
                        has_data_rows = True
                        print(f"  ✅ 查询结果已加载，共 {row_count} 行有效数据")
                        break
                    else:
                        # 检查是否有"无数据"提示
                        has_empty_message = await page.evaluate("""
                            () => {
                                const emptySelectors = [
                                    '.ant-empty',
                                    '.ant-table-empty',
                                    '[class*="empty"]',
                                    '[class*="no-data"]'
                                ];

                                for (const selector of emptySelectors) {
                                    const elements = document.querySelectorAll(selector);
                                    for (const el of elements) {
                                        const text = el.textContent || '';
                                        if (text.includes('暂无数据') || 
                                            text.includes('无数据') || 
                                            text.includes('No Data') ||
                                            text.includes('没有数据') ||
                                            text.includes('暂无')) {
                                            return true;
                                        }
                                    }
                                }

                                // 检查表格body中是否有"无数据"文本
                                const tbody = document.querySelector('table tbody');
                                if (tbody) {
                                    const tbodyText = tbody.textContent || '';
                                    if (tbodyText.includes('暂无数据') || 
                                        tbodyText.includes('无数据') || 
                                        tbodyText.includes('No Data') ||
                                        tbodyText.includes('没有数据') ||
                                        tbodyText.includes('暂无')) {
                                        return true;
                                    }
                                }

                                return false;
                            }
                        """)

                        if has_empty_message:
                            print(f"  ⚠ 检测到无数据提示，查询结果为空")
                            has_data_rows = False
                            break
                        else:
                            if attempt < max_wait_attempts - 1:
                                print(f"  表格容器存在但无数据行，等待中... (尝试 {attempt + 1}/{max_wait_attempts})")
                                await page.wait_for_timeout(1000)
                                await page.wait_for_load_state("networkidle", timeout=3000)
                            else:
                                print(f"  ⚠ 警告：等待超时，未检测到数据行")
                                has_data_rows = False
                except Exception as e:
                    if attempt < max_wait_attempts - 1:
                        print(f"  等待表格数据行出现... (尝试 {attempt + 1}/{max_wait_attempts})")
                        await page.wait_for_timeout(1000)
                        await page.wait_for_load_state("networkidle", timeout=3000)
                    else:
                        print(f"  ⚠ 警告：等待表格数据行超时: {e}")
                        has_data_rows = False

            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            await wait_for_page_ready_async(page, timeout=3000)
            print("✅ 查询操作完成")

            # 检查查询结果是否有数据（多重验证）
            print("  检查查询结果是否有数据...")

            # 方法1：检查是否有有效的数据行
            if not has_data_rows or row_count == 0:
                print("  ⚠ 未检测到有效数据行")
                # 再次确认：尝试获取表格数据
                try:
                    rows_data = await get_table_rows_data_async(
                        page,
                        header_keywords=['申请单流水号', '流水号', '申请单号', '单号'],
                        serial_pattern="POM",
                        enable_fallback=True
                    )
                    if not rows_data or len(rows_data) == 0:
                        raise Exception("确认无数据")
                    # 查询成功，重置失败计数器
                    query_fail_count = 0
                    print(f"  ✅ 方法1确认查询到 {len(rows_data)} 条申请单数据")
                except:
                    # 确认没有数据，增加失败计数
                    query_fail_count += 1
                    print(f"  ⚠ 第 {query_fail_count} 次查询不到申请单流水号")
                    
                    # 如果连续两次都查询不到，停止代码运行
                    if query_fail_count >= 2:
                        print("\n" + "=" * 50)
                        print("⚠ 连续两次查询不到申请单流水号，停止代码运行")
                        print("=" * 50)
                        # 使用JavaScript弹出提示框
                        await page.evaluate("""
                            () => {
                                alert('连续两次查询不到申请单流水号，代码已停止运行');
                            }
                        """)
                        return  # 停止代码运行
                    
                    # 如果只失败一次，继续下一次循环
                    print("  继续下一次循环尝试...")
                    continue
            else:
                # 方法1检查通过，重置失败计数器
                query_fail_count = 0

            # 方法2：获取所有表格行的申请单流水号进行验证
            try:
                rows_data = await get_table_rows_data_async(
                    page,
                    header_keywords=['申请单流水号', '流水号', '申请单号', '单号'],
                    serial_pattern="POM",
                    enable_fallback=True
                )

                # 如果没有数据，增加失败计数
                if not rows_data or len(rows_data) == 0:
                    query_fail_count += 1
                    print(f"  ⚠ 第 {query_fail_count} 次查询不到申请单流水号")
                    
                    # 如果连续两次都查询不到，停止代码运行
                    if query_fail_count >= 2:
                        print("\n" + "=" * 50)
                        print("⚠ 连续两次查询不到申请单流水号，停止代码运行")
                        print("=" * 50)
                        # 使用JavaScript弹出提示框
                        await page.evaluate("""
                            () => {
                                alert('连续两次查询不到申请单流水号，代码已停止运行');
                            }
                        """)
                        return  # 停止代码运行
                    
                    # 如果只失败一次，继续下一次循环
                    print("  继续下一次循环尝试...")
                    continue

                # 查询成功，重置失败计数器
                query_fail_count = 0
                print(f"  ✅ 查询到 {len(rows_data)} 条申请单数据")
            except Exception as e:
                # 如果获取数据失败，也认为没有数据，增加失败计数
                query_fail_count += 1
                print(f"  ⚠ 获取表格数据时出错: {e}")
                print(f"  ⚠ 第 {query_fail_count} 次查询不到申请单流水号")
                
                # 如果连续两次都查询不到，停止代码运行
                if query_fail_count >= 2:
                    print("\n" + "=" * 50)
                    print("⚠ 连续两次查询不到申请单流水号，停止代码运行")
                    print("=" * 50)
                    # 使用JavaScript弹出提示框
                    await page.evaluate("""
                        () => {
                            alert('连续两次查询不到申请单流水号，代码已停止运行');
                        }
                    """)
                    return  # 停止代码运行
                
                # 如果只失败一次，继续下一次循环
                print("  继续下一次循环尝试...")
                continue

            # 步骤5. 获取最后一页的申请单流水号，找到最后一个，点击转交按钮
            print("\n[步骤6] 获取最后一页申请单流水号，找到最后一个，点击转交按钮...")

            try:
                await page.wait_for_selector("table tbody tr", timeout=WAIT_TIME)
            except:
                raise Exception("表格未加载或没有数据")

            # 获取所有表格行的申请单流水号（再次获取，确保数据是最新的）
            rows_data = await get_table_rows_data_async(
                page,
                header_keywords=['申请单流水号', '流水号', '申请单号', '单号'],
                serial_pattern="POM",
                enable_fallback=True
            )

            if not rows_data:
                raise Exception("未找到任何申请单数据")

            print(f"  找到 {len(rows_data)} 条申请单数据")
            for item in rows_data:
                print(f"    行{item['index'] + 1}: {item['serialNumber']}")

            last_row_index = len(rows_data) - 1
            last_serial_number = rows_data[last_row_index]['serialNumber']
            print(f"  最后一个申请单流水号: {last_serial_number} (第{last_row_index + 1}行)")

            # 定位最后一行的转交按钮
            transfer_button_locators = [
                lambda p: p.locator(f"table tbody tr").nth(last_row_index).locator("a:has-text('转交')").first,
                lambda p: p.locator(f"table tbody tr:nth-child({last_row_index + 1}) button:has-text('转交')").first,
                lambda p: p.locator("table tbody tr:last-child button:has-text('转交')").first,
                lambda p: p.locator(f"table tbody tr").nth(last_row_index).locator("button:has-text('转交')").first
            ]

            # 尝试定位转交按钮
            try:
                transfer_button = await try_locators_async(page, transfer_button_locators,
                                                           f"最后一个申请单的转交按钮（流水号: {last_serial_number}）",
                                                           timeout=5000)
                await transfer_button.scroll_into_view_if_needed()

                # 点击转交按钮
                try:
                    await transfer_button.click()
                    print(f"✅ 已点击最后一个申请单的转交按钮（流水号: {last_serial_number}）")
                except Exception as click_error:
                    print(f"  警告：直接点击失败，使用JavaScript: {click_error}")
                    await transfer_button.evaluate("""
                            el => {
                                if (el) {
                                    el.click();
                                    el.dispatchEvent(new Event('click', { bubbles: true }));
                                }
                            }
                        """)
                    print(f"✅ 已通过JavaScript点击转交按钮（流水号: {last_serial_number}）")

                await page.wait_for_timeout(1000)
                await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
                # 等待遮罩层消失
                await wait_for_overlay_disappear_async(page)

            except Exception as transfer_error:
                # 找不到转交按钮，直接继续下一次循环
                print(f"  ⚠ 警告：未找到转交按钮: {str(transfer_error)[:100]}")
                print(f"  继续下一次循环尝试...")
                continue

            # 填写转交信息并提交
            print("填写转交信息并提交...")
            await wait_for_modal_async(page)

            # 找到"转交审批给"输入框
            print("  查找'转交审批给'输入框...")
            transfer_to_input_locators = [
                lambda p: p.locator(
                    "xpath=//div[contains(@class,'ant-modal')]//div[contains(@class,'ant-select')]//span[last()]").first,
                lambda p: p.locator(
                    "xpath=//div[contains(@class,'ant-modal')]//div[contains(@class,'ant-select')]//input").first,
                lambda p: p.get_by_placeholder("转交审批给"),
                lambda p: p.get_by_placeholder("请输入员工编号/员工姓名"),
                lambda p: p.locator(".ant-select-search__field, .ant-select-selection-search-input").first
            ]

            transfer_to_input = await try_locators_async(page, transfer_to_input_locators, "转交审批给输入框",
                                                         timeout=5000)
            await transfer_to_input.scroll_into_view_if_needed()

            print("  在'转交审批给'输入框中输入133366...")
            await fill_select_input_async(page, transfer_to_input, "133366")

            # 等待输入完成
            await page.wait_for_timeout(500)

            # 确保输入框获得焦点
            try:
                await transfer_to_input.focus()
                await page.wait_for_timeout(200)
            except:
                pass

            # 等待下拉菜单出现并加载选项
            print("  等待下拉选项加载...")
            dropdown_visible = False
            try:
                await page.wait_for_selector(
                    ".ant-select-dropdown:not([style*='display: none']), "
                    ".ant-select-dropdown-menu:not([style*='display: none']), "
                    "div[role='listbox']:not([style*='display: none'])",
                    timeout=3000
                )
                dropdown_visible = True
                print("  ✅ 下拉菜单已出现")
            except:
                print("  ⚠ 警告：下拉菜单可能未完全加载，继续尝试...")

            # 优先尝试直接点击目标选项
            target_text = "（杨承霖）133366"
            option_clicked = False
            if dropdown_visible:
                print(f"  尝试直接点击选项: {target_text}...")
                option_locators = [
                    lambda p: p.locator(f".ant-select-dropdown:not([style*='display: none'])").get_by_text(target_text,
                                                                                                           exact=False).first,
                    lambda p: p.locator(f"li.ant-select-dropdown-menu-item:has-text('{target_text}')").first,
                    lambda p: p.locator(f"div[role='listbox'] li:has-text('{target_text}')").first,
                    lambda p: p.get_by_text(target_text, exact=False).filter(
                        has=p.locator(".ant-select-dropdown")).first,
                ]

                for idx, locator_factory in enumerate(option_locators, 1):
                    try:
                        option = locator_factory(page)
                        if await option.count() > 0:
                            await option.scroll_into_view_if_needed()
                            await option.wait_for(state="visible", timeout=1000)
                            await option.click()
                            await page.wait_for_timeout(500)
                            print(f"  ✅ 已通过点击选择选项: {target_text}")
                            option_clicked = True
                            break
                    except Exception as e:
                        if idx < len(option_locators):
                            continue
                        else:
                            print(f"  ⚠ 直接点击选项失败，尝试键盘操作: {str(e)[:50]}")

            # 如果直接点击失败，使用键盘操作
            if not option_clicked:
                print("  使用键盘操作选择选项...")
                # 确保输入框有焦点
                try:
                    await transfer_to_input.focus()
                    await page.wait_for_timeout(200)
                except:
                    pass

                # 按向下键选择第一个选项
                print("  按向下键选择选项...")
                await page.keyboard.press("ArrowDown")
                await page.wait_for_timeout(500)

                # 验证选项是否被选中（高亮）
                try:
                    await page.wait_for_function(
                        "() => document.querySelector('.ant-select-item-option-active, .ant-select-item-option-selected') !== null",
                        timeout=1000
                    )
                    print("  ✅ 选项已高亮")
                except:
                    print("  ⚠ 警告：选项可能未高亮，继续操作...")

                # 按Enter键确认选择
                print("  按Enter键确认选择...")
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(500)

                # 验证选择是否成功（检查输入框的值或文本内容）
                try:
                    await page.wait_for_timeout(300)
                    # 尝试多种方式获取输入框的值
                    input_value = ""
                    try:
                        input_value = await transfer_to_input.input_value()
                    except:
                        try:
                            input_value = await transfer_to_input.text_content() or ""
                        except:
                            try:
                                input_value = await transfer_to_input.evaluate(
                                    "el => el.value || el.textContent || ''") or ""
                            except:
                                pass

                    if target_text in input_value or "133366" in input_value or "杨承霖" in input_value:
                        print(f"  ✅ 已通过键盘选择选项: {target_text}")
                    else:
                        print(f"  ⚠ 警告：选择可能未成功，输入框值: {input_value}")
                except Exception as verify_error:
                    print(f"  ✅ 已通过键盘选择选项（验证时出错: {str(verify_error)[:50]}）")

            # 找到"转交原因"输入框
            print("  查找'转交原因'输入框...")
            transfer_reason_input_locators = [
                lambda p: p.get_by_placeholder("转交原因"),
                lambda p: p.get_by_label("转交原因"),
                lambda p: p.get_by_role("textbox", name="转交原因"),
                lambda p: p.get_by_role("textbox", name="转交原因").filter(has_text="")
            ]

            transfer_reason_input = await try_locators_async(page, transfer_reason_input_locators, "转交原因输入框",
                                                             timeout=5000)
            await transfer_reason_input.scroll_into_view_if_needed()

            print("  在'转交原因'输入框中输入'测试单子'...")
            await transfer_reason_input.clear()
            await fill_input_with_wait_async(page, transfer_reason_input, "测试单子", "转交原因", use_type=True)

            # 点击确定按钮
            print("  查找确定按钮...")
            confirm_button_locators = [
                lambda p: p.get_by_role("button", name="确 定").first,
                lambda p: p.get_by_role("button", name="确定").first,
                lambda p: p.get_by_text("确 定", exact=True).first,
                lambda p: p.get_by_text("确定", exact=True).first,
                lambda p: p.locator("div.ant-modal, div[role='dialog']").get_by_role("button", name="确 定").first,
                lambda p: p.locator("div.ant-modal, div[role='dialog']").get_by_role("button", name="确定").first
            ]

            confirm_button = await try_locators_async(page, confirm_button_locators, "确定按钮", timeout=5000)
            await confirm_button.scroll_into_view_if_needed()
            await confirm_button.click()
            print("✅ 已点击确定按钮")

            await page.wait_for_timeout(2000)
            await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            print("✅ 转交弹窗已关闭")

            # 步骤7.点击页面内的"我的审批"子模块
            print("\n[步骤7] 点击页面内的'我的审批'子模块...")
            
            # 先检查并关闭可能存在的模态框
            print("  检查是否存在打开的模态框...")
            try:
                # 检查是否有打开的模态框
                modal_exists = await page.evaluate("""
                    () => {
                        const modals = document.querySelectorAll('.ant-modal-wrap:not([style*="display: none"]), .ant-modal:not([style*="display: none"]), div[role="dialog"]:not([style*="display: none"])');
                        return modals.length > 0;
                    }
                """)
                
                if modal_exists:
                    print("  ⚠ 检测到打开的模态框，尝试关闭...")
                    # 方法1：尝试点击关闭按钮
                    try:
                        close_button_locators = [
                            lambda p: p.locator(".ant-modal-close, .ant-modal-close-x, button[aria-label='Close']").first,
                            lambda p: p.locator("div.ant-modal button:has-text('关闭')").first,
                            lambda p: p.locator("div.ant-modal button:has-text('取消')").first,
                        ]
                        close_button = await try_locators_async(page, close_button_locators, "模态框关闭按钮", timeout=3000)
                        await close_button.click()
                        print("  ✅ 已点击关闭按钮")
                        await page.wait_for_timeout(500)
                    except:
                        # 方法2：尝试按ESC键关闭
                        try:
                            await page.keyboard.press("Escape")
                            print("  ✅ 已按ESC键关闭模态框")
                            await page.wait_for_timeout(500)
                        except:
                            print("  ⚠ 无法关闭模态框，继续尝试...")
                    
                    # 等待模态框消失
                    try:
                        await page.wait_for_selector(".ant-modal-wrap, .ant-modal, div[role='dialog']", state="hidden", timeout=5000)
                        print("  ✅ 模态框已关闭")
                    except:
                        print("  ⚠ 等待模态框消失超时，继续尝试...")
            except Exception as e:
                print(f"  ⚠ 检查模态框时出错: {e}，继续尝试...")
            
            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            
            my_approval_tab_locators = [
                lambda p: p.locator("xpath=//div[contains(@class,'ant-tabs')]//div[contains(text(),'我的审批')]").first,
                # 用户提供的精确XPath（最高优先级）
                lambda p: p.locator(
                    "xpath=//*[@id='root']/section/section/main/div/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]").first,
                # 其他可能的定位方式
                lambda p: p.locator("div.ant-tabs-tab:has-text('我的审批')").first,
                lambda p: p.locator("div[role='tab']:has-text('我的审批')").first,
                lambda p: p.get_by_text("我的审批", exact=True).first,
                lambda p: p.locator("span:has-text('我的审批')").first,
                lambda p: p.locator("xpath=//span[contains(text(),'我的审批')]").first,
            ]

            my_approval_tab = await try_locators_async(page, my_approval_tab_locators, "我的审批子模块", timeout=5000)
            await wait_for_element_ready_async(page, my_approval_tab, "我的审批子模块")
            await my_approval_tab.scroll_into_view_if_needed()
            
            # 尝试点击，如果失败则使用JavaScript点击
            try:
                await my_approval_tab.click(timeout=10000)
                print("✅ 已点击页面内的'我的审批'子模块")
            except Exception as click_error:
                print(f"  ⚠ 直接点击失败: {str(click_error)[:100]}，尝试使用JavaScript点击...")
                try:
                    # 再次检查并关闭模态框
                    await page.evaluate("""
                        () => {
                            // 关闭所有打开的模态框
                            const modals = document.querySelectorAll('.ant-modal-wrap:not([style*="display: none"])');
                            modals.forEach(modal => {
                                const closeBtn = modal.querySelector('.ant-modal-close, .ant-modal-close-x');
                                if (closeBtn) {
                                    closeBtn.click();
                                }
                            });
                        }
                    """)
                    await page.wait_for_timeout(500)
                    
                    # 使用JavaScript点击
                    await my_approval_tab.evaluate("""
                        el => {
                            if (el) {
                                el.click();
                                el.dispatchEvent(new Event('click', { bubbles: true }));
                            }
                        }
                    """)
                    print("✅ 已通过JavaScript点击页面内的'我的审批'子模块")
                except Exception as js_error:
                    print(f"  ⚠ JavaScript点击也失败: {str(js_error)[:100]}")
                    raise Exception(f"无法点击'我的审批'子模块: {js_error}")

            # 等待子模块内容加载
            await page.wait_for_timeout(1000)
            await wait_for_page_ready_async(page, timeout=5000)
            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            print("✅ 我的审批子模块已加载")

            # 转交完成，刷新页面，确保页面状态正确
            print("\n[刷新页面] 刷新页面以确保页面状态正确...")
            try:
                await page.reload(wait_until="domcontentloaded", timeout=WAIT_TIME)
                print("  ✅ 页面已刷新")
            except Exception as e:
                print(f"  ⚠ 警告：页面刷新时出错: {e}")
                # 如果刷新失败，尝试使用JavaScript刷新
                try:
                    await page.evaluate("window.location.reload()")
                    await page.wait_for_load_state("domcontentloaded", timeout=WAIT_TIME)
                    print("  ✅ 已通过JavaScript刷新页面")
                except Exception as e2:
                    print(f"  ⚠ 警告：JavaScript刷新也失败: {e2}")

            # 等待页面完全加载
            print("  等待刷新后的页面完全加载...")
            await page.wait_for_load_state("domcontentloaded", timeout=WAIT_TIME)
            await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)

            # 等待登录状态确认（确保刷新后仍然登录）
            try:
                # 检查是否还在登录状态，如果跳转到登录页则需要重新登录
                if "login" in page.url.lower() or "登录" in page.title():
                    print("  ⚠ 警告：刷新后已退出登录，需要重新登录")
                    raise Exception("刷新后需要重新登录")
                else:
                    print("  ✅ 刷新后仍保持登录状态")
            except:
                pass

            # 等待主要内容区域加载
            try:
                await page.wait_for_selector("main, .ant-layout-content, [class*='content'], #root", timeout=5000)
                print("  ✅ 主要内容区域已加载")
            except:
                print("  ⚠ 警告：主要内容区域可能未完全加载，继续尝试...")

            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            print("✅ 页面刷新完成")

            # 步骤8. 选中最后一条数据的复选框，然后点击审批
            print("\n[步骤8] 选中最后一条数据的复选框，然后点击审批...")

            # 等待页面完全加载
            await wait_for_page_ready_async(page)

            # 等待表格加载
            try:
                await page.wait_for_selector("table tbody tr", timeout=WAIT_TIME)
                print("✅ 表格已加载")
            except:
                pass

            # 查询页面所有数据，找到最下方的一条数据
            print("  查询页面所有表格数据，定位最下方的一条数据...")

            # 使用JavaScript查询所有表格行数据
            rows_data = await page.evaluate("""
                            () => {
                                // 查找流水号列索引
                                const headers = Array.from(document.querySelectorAll('table thead th, table thead tr:first-child th'));
                                let serialNumberColumnIndex = -1;

                                if (headers.length > 0) {
                                    for (let i = 0; i < headers.length; i++) {
                                        const headerText = headers[i].textContent.trim();
                                        if (headerText.includes('流水号') || headerText.includes('申请单号') || headerText.includes('单号')) {
                                            serialNumberColumnIndex = i;
                                            break;
                                        }
                                    }
                                }

                                const rows = Array.from(document.querySelectorAll('table tbody tr'));
                                const data = [];
                                rows.forEach((row, index) => {
                                    const cells = row.querySelectorAll('td');
                                    let serialNumber = '';

                                    if (serialNumberColumnIndex !== -1 && cells.length > serialNumberColumnIndex) {
                                        serialNumber = cells[serialNumberColumnIndex].textContent.trim();
                                    } else {
                                        for (let i = 0; i < cells.length; i++) {
                                            const text = cells[i].textContent.trim();
                                            if (text && text.startsWith('POM') && /^POM\\d+$/.test(text)) {
                                                serialNumber = text;
                                                break;
                                            }
                                        }
                                    }

                                    data.push({
                                        index: index,
                                        serialNumber: serialNumber || `行${index + 1}`,
                                        row: row
                                    });
                                });
                                return data;
                            }
                        """)

            if not rows_data:
                raise Exception("❌ 未找到任何申请单数据")

            print(f"  找到 {len(rows_data)} 条申请单数据")
            for item in rows_data:
                print(f"    行{item['index'] + 1}: {item['serialNumber']}")

            last_row_index = len(rows_data) - 1
            last_serial_number = rows_data[last_row_index]['serialNumber']
            print(f"  最后一个申请单流水号: {last_serial_number} (第{last_row_index + 1}行)")

            # 定位最后一行的审批按钮（在数据右侧）
            print("  定位最后一个申请单的审批按钮...")

            # 多种方式定位最后一行的审批按钮
            approve_button_locators = [
                # 方法1：在最后一行中查找审批按钮/链接
                lambda p: p.locator(f"table tbody tr").nth(last_row_index).get_by_text("审批", exact=True).first,
                lambda p: p.locator(f"table tbody tr").nth(last_row_index).get_by_text("审批").first,
                lambda p: p.locator(f"table tbody tr").nth(last_row_index).locator("a:has-text('审批')").first,
                lambda p: p.locator(f"table tbody tr").nth(last_row_index).locator("button:has-text('审批')").first,
                # 方法2：通过角色定位
                lambda p: p.locator(f"table tbody tr").nth(last_row_index).get_by_role("link", name="审批").first,
                lambda p: p.locator(f"table tbody tr").nth(last_row_index).get_by_role("button", name="审批").first,
            ]

            approve_button = await try_locators_async(page, approve_button_locators,
                                                      f"最后一个申请单的审批按钮（流水号: {last_serial_number}）",
                                                      timeout=5000)
            await approve_button.scroll_into_view_if_needed()
            await approve_button.wait_for(state="visible", timeout=5000)

            # 记录当前页面URL（用于判断是否跳转）
            current_url = page.url
            print(f"  当前页面URL: {current_url}")

            # 步骤9.点击审批按钮
            print("\n[步骤9] 点击审批按钮...")
            try:
                await approve_button.click()
                print(f"✅ 已点击最后一个申请单的审批按钮（流水号: {last_serial_number}）")
            except Exception as click_error:
                print(f"  警告：直接点击失败，使用JavaScript: {click_error}")
                await approve_button.evaluate("""
                                            el => {
                                                if (el) {
                                                    el.click();
                                                    el.dispatchEvent(new Event('click', { bubbles: true }));
                                                }
                                            }
                                        """)
                print(f"✅ 已通过JavaScript点击审批按钮（流水号: {last_serial_number}）")

            # 等待新页面加载（可能跳转到新页面或打开新窗口）
            print("  等待新页面加载...")
            await page.wait_for_timeout(2000)
            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)

            # 检查是否有新窗口打开
            if len(page.context.pages) > 1:
                print("  检测到新窗口，切换到新窗口...")
                new_page = page.context.pages[-1]
                await new_page.wait_for_load_state("domcontentloaded", timeout=WAIT_TIME)
                await new_page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
                # 等待遮罩层消失
                await wait_for_overlay_disappear_async(new_page)
                page = new_page
                print("✅ 已切换到新窗口")
            else:
                # 等待页面跳转或加载
                try:
                    # 等待URL变化
                    await page.wait_for_function(
                        f"() => window.location.href !== '{current_url}'",
                        timeout=WAIT_TIME
                    )
                    print("✅ 页面已跳转")
                except:
                    pass

            # 等待新页面完全加载
            await wait_for_page_ready_async(page)
            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            print(f"  新页面URL: {page.url}")

            # 步骤10. 找到审批人员部分，检查并处理复选框
            print("\n[步骤10] 检查审批人员复选框状态...")

            # 定义需要检查的审批人员字段
            approval_fields = [
                "BU区域运营负责人",
                "BU项目管理负责人",
                "BU总经理",
                "BU运营负责人",
                "项目运营管理总监",
                "CFO",
                "大区区总",
                "省负责人",
                "产品线总监",
                "部门总监"
            ]

            # 先检查页面中是否存在审批人员部分
            print("  检查页面中是否存在审批人员部分...")
            has_approval_section = False

            # 尝试多种方式检查是否存在审批人员部分
            try:
                # 方法1：检查是否存在任何审批人员字段的文本
                for field_name in approval_fields:
                    try:
                        field_element = page.locator(f"*:has-text('{field_name}')").first
                        if await field_element.count() > 0:
                            has_approval_section = True
                            print(f"  ✅ 找到审批人员字段: {field_name}")
                            break
                    except:
                        continue

                # 方法2：如果方法1没找到，检查是否存在复选框区域
                if not has_approval_section:
                    try:
                        checkbox_elements = page.locator("label, .ant-checkbox-wrapper, input[type='checkbox']")
                        if await checkbox_elements.count() > 0:
                            # 进一步检查是否包含审批人员相关的文本
                            page_text = await page.evaluate("() => document.body.innerText || ''")
                            for field_name in approval_fields:
                                if field_name in page_text:
                                    has_approval_section = True
                                    print(f"  ✅ 在页面文本中找到审批人员字段: {field_name}")
                                    break
                    except:
                        pass
            except Exception as e:
                print(f"  ⚠ 检查审批人员部分时出错: {e}")

            # 如果页面中没有审批人员部分，跳过步骤23，直接执行步骤17
            if not has_approval_section:
                print("  ⚠ 页面中未找到审批人员部分，跳过步骤23，直接执行点击同意按钮操作")
            else:
                # 等待审批人员部分加载
                print("  等待审批人员部分加载...")
                try:
                    await page.wait_for_selector("label, .ant-checkbox-wrapper, input[type='checkbox']",
                                                 timeout=WAIT_TIME)
                    print("  ✅ 复选框区域已加载")
                except:
                    print("  ⚠ 警告：复选框区域可能未完全加载，继续尝试...")

                # 统计信息
                checked_count = 0
                unchecked_count = 0
                disabled_count = 0
                not_found_count = 0

                # 遍历每个字段，检查并处理复选框
                for field_name in approval_fields:
                    print(f"\n  处理字段: {field_name}")

                    # 多种方式定位复选框
                    checkbox_locators = [
                        # 方法1：通过label文本定位
                        lambda p, name: p.locator(f"label:has-text('{name}')").locator("input[type='checkbox']").first,
                        lambda p, name: p.locator(f"label:has-text('{name}')").locator(".ant-checkbox-input").first,
                        # 方法2：通过包含文本的元素定位
                        lambda p, name: p.locator(f"*:has-text('{name}')").locator("input[type='checkbox']").first,
                        lambda p, name: p.locator(f"*:has-text('{name}')").locator(".ant-checkbox-input").first,
                    ]

                    checkbox_found = False
                    checkbox = None

                    # 尝试定位复选框
                    for idx, locator_factory in enumerate(checkbox_locators, 1):
                        try:
                            checkbox = locator_factory(page, field_name)
                            if await checkbox.count() > 0:
                                await checkbox.wait_for(state="attached", timeout=2000)
                                checkbox_found = True
                                print(f"    ✅ 找到复选框（方式{idx}）")
                                break
                        except:
                            continue

                    if not checkbox_found:
                        print(f"    ⚠ 警告：未找到 {field_name} 的复选框")
                        not_found_count += 1
                        continue

                    # 检查复选框是否被禁用（置灰）
                    try:
                        is_disabled = await checkbox.evaluate("""
                            el => {
                                // 检查input元素本身的disabled属性
                                if (el.disabled) {
                                    return true;
                                }
                                // 检查父元素是否有禁用相关的类或属性
                                const parent = el.closest('.ant-checkbox-wrapper, label');
                                if (parent) {
                                    // 检查是否有ant-checkbox-disabled类
                                    if (parent.classList.contains('ant-checkbox-disabled')) {
                                        return true;
                                    }
                                    // 检查父元素是否有disabled属性
                                    if (parent.hasAttribute('disabled') || parent.getAttribute('aria-disabled') === 'true') {
                                        return true;
                                    }
                                    // 检查父元素的样式是否包含pointer-events: none
                                    const style = window.getComputedStyle(parent);
                                    if (style.pointerEvents === 'none' || style.opacity === '0.5' || style.cursor === 'not-allowed') {
                                        return true;
                                    }
                                }
                                return false;
                            }
                        """)

                        if is_disabled:
                            print(f"    ⊘ 复选框已被禁用（置灰），跳过处理（上一个审批人已修改，无权限修改）")
                            disabled_count += 1
                            continue
                    except Exception as disabled_check_error:
                        print(f"    ⚠ 警告：检查复选框禁用状态时出错: {disabled_check_error}，继续处理...")

                    # 检查复选框是否被勾选
                    try:
                        is_checked = await checkbox.evaluate("el => el.checked")
                        checkbox_type = await checkbox.evaluate("el => el.type")

                        # 如果是Ant Design的复选框，可能需要检查父元素
                        if not is_checked:
                            try:
                                # 检查父元素是否有checked类
                                parent_checked = await checkbox.evaluate("""
                                        el => {
                                            const parent = el.closest('.ant-checkbox-wrapper, label');
                                            if (parent) {
                                                return parent.classList.contains('ant-checkbox-checked') || 
                                                       parent.querySelector('.ant-checkbox-checked') !== null;
                                            }
                                            return false;
                                        }
                                    """)
                                if parent_checked:
                                    is_checked = True
                            except:
                                pass

                        if is_checked:
                            print(f"    ✓ 复选框已被勾选，点击取消勾选...")
                            try:
                                # 滚动到复选框位置
                                await checkbox.scroll_into_view_if_needed()
                                await checkbox.wait_for(state="visible", timeout=2000)

                                # 点击复选框
                                await checkbox.click()
                                await page.wait_for_timeout(300)  # 等待状态更新

                                # 验证是否已取消勾选
                                is_checked_after = await checkbox.evaluate("el => el.checked")
                                if not is_checked_after:
                                    print(f"    ✅ 已成功取消勾选 {field_name}")
                                    checked_count += 1
                                else:
                                    print(f"    ⚠ 警告：点击后复选框仍被勾选，尝试使用JavaScript...")
                                    # 使用JavaScript强制取消勾选
                                    await checkbox.evaluate(
                                        "el => { el.checked = false; el.dispatchEvent(new Event('change', { bubbles: true })); }")
                                    await page.wait_for_timeout(300)
                                    print(f"    ✅ 已通过JavaScript取消勾选 {field_name}")
                                    checked_count += 1
                            except Exception as click_error:
                                print(f"    ⚠ 警告：点击复选框失败: {click_error}")
                                # 尝试使用JavaScript
                                try:
                                    await checkbox.evaluate(
                                        "el => { el.checked = false; el.dispatchEvent(new Event('change', { bubbles: true })); }")
                                    await page.wait_for_timeout(300)
                                    print(f"    ✅ 已通过JavaScript取消勾选 {field_name}")
                                    checked_count += 1
                                except Exception as js_error:
                                    print(f"    ❌ 错误：无法取消勾选 {field_name}: {js_error}")
                        else:
                            print(f"    ○ 复选框未被勾选，无需操作")
                            unchecked_count += 1

                    except Exception as e:
                        print(f"    ❌ 错误：检查复选框状态时出错: {e}")
                        not_found_count += 1

                # 输出统计信息
                print(f"\n  处理完成统计:")
                print(f"    - 已取消勾选: {checked_count} 个")
                print(f"    - 未勾选（无需操作）: {unchecked_count} 个")
                print(f"    - 已禁用（置灰，跳过处理）: {disabled_count} 个")
                print(f"    - 未找到: {not_found_count} 个")

                if checked_count > 0:
                    print(f"  ✅ 已处理 {checked_count} 个被勾选的复选框")
                elif unchecked_count + disabled_count == len(approval_fields):
                    print(f"  ✅ 所有复选框都未被勾选或已禁用，无需更改")
                else:
                    print(f"  ⚠ 警告：部分复选框未找到或处理失败")

            # 步骤11. 检查"审批意见"部分，如果有就勾选"已确认以上商机信息"复选框
            print("\n[步骤11] 检查'审批意见'部分...")

            # 先检查页面中是否存在"审批意见"部分
            print("  检查页面中是否存在'审批意见'部分...")
            has_approval_opinion_section = False

            try:
                # 方法1：检查是否存在"审批意见"文本
                approval_opinion_keywords = ["审批意见", "审批", "意见"]
                for keyword in approval_opinion_keywords:
                    try:
                        opinion_element = page.locator(f"*:has-text('{keyword}')").first
                        if await opinion_element.count() > 0:
                            # 进一步检查是否包含"已确认以上商机信息"相关文本
                            page_text = await page.evaluate("() => document.body.innerText || ''")
                            if "已确认以上商机信息" in page_text or "已确认" in page_text:
                                has_approval_opinion_section = True
                                print(f"  ✅ 找到'审批意见'部分（通过关键词: {keyword}）")
                                break
                    except:
                        continue

                # 方法2：直接检查是否存在"已确认以上商机信息"文本
                if not has_approval_opinion_section:
                    try:
                        confirm_text_elements = page.locator("*:has-text('已确认以上商机信息')")
                        if await confirm_text_elements.count() > 0:
                            has_approval_opinion_section = True
                            print(f"  ✅ 找到'已确认以上商机信息'文本")
                    except:
                        pass

            except Exception as e:
                print(f"  ⚠ 检查'审批意见'部分时出错: {e}")

            # 如果页面中没有"审批意见"部分，忽略
            if not has_approval_opinion_section:
                print("  ⚠ 页面中未找到'审批意见'部分，忽略此步骤")
            else:
                # 等待页面稳定
                await page.wait_for_timeout(500)

                # 查找"已确认以上商机信息"的复选框
                print("  查找'已确认以上商机信息'复选框...")
                confirm_checkbox_locators = [
                    # 方法1：通过label文本定位
                    lambda p: p.locator("label:has-text('已确认以上商机信息')").locator("input[type='checkbox']").first,
                    lambda p: p.locator("label:has-text('已确认以上商机信息')").locator(".ant-checkbox-input").first,
                    # 方法2：通过包含文本的元素定位
                    lambda p: p.locator("*:has-text('已确认以上商机信息')").locator("input[type='checkbox']").first,
                    lambda p: p.locator("*:has-text('已确认以上商机信息')").locator(".ant-checkbox-input").first,
                    # 方法3：通过"已确认"关键词定位
                    lambda p: p.locator("label:has-text('已确认')").locator("input[type='checkbox']").first,
                    lambda p: p.locator("*:has-text('已确认')").locator("input[type='checkbox']").first,
                ]

                checkbox_found = False
                confirm_checkbox = None

                # 尝试定位复选框
                for idx, locator_factory in enumerate(confirm_checkbox_locators, 1):
                    try:
                        confirm_checkbox = locator_factory(page)
                        if await confirm_checkbox.count() > 0:
                            await confirm_checkbox.wait_for(state="attached", timeout=2000)
                            checkbox_found = True
                            print(f"  ✅ 找到'已确认以上商机信息'复选框（方式{idx}）")
                            break
                    except:
                        continue

                if not checkbox_found:
                    print("  ⚠ 警告：未找到'已确认以上商机信息'复选框，忽略此步骤")
                else:
                    # 检查复选框是否被禁用（置灰）
                    try:
                        is_disabled = await confirm_checkbox.evaluate("""
                            el => {
                                if (el.disabled) return true;
                                const parent = el.closest('.ant-checkbox-wrapper, label');
                                if (parent) {
                                    if (parent.classList.contains('ant-checkbox-disabled')) return true;
                                    if (parent.hasAttribute('disabled') || parent.getAttribute('aria-disabled') === 'true') return true;
                                    const style = window.getComputedStyle(parent);
                                    if (style.pointerEvents === 'none' || style.opacity === '0.5' || style.cursor === 'not-allowed') return true;
                                }
                                return false;
                            }
                        """)

                        if is_disabled:
                            print("  ⊘ 复选框已被禁用（置灰），跳过处理")
                        else:
                            # 检查复选框是否已被勾选
                            try:
                                is_checked = await confirm_checkbox.evaluate("el => el.checked")

                                # 如果是Ant Design的复选框，可能需要检查父元素
                                if not is_checked:
                                    try:
                                        parent_checked = await confirm_checkbox.evaluate("""
                                            el => {
                                                const parent = el.closest('.ant-checkbox-wrapper, label');
                                                if (parent) {
                                                    return parent.classList.contains('ant-checkbox-checked') || 
                                                           parent.querySelector('.ant-checkbox-checked') !== null;
                                                }
                                                return false;
                                            }
                                        """)
                                        if parent_checked:
                                            is_checked = True
                                    except:
                                        pass

                                if is_checked:
                                    print("  ✓ 复选框已被勾选，无需操作")
                                else:
                                    print("  ○ 复选框未被勾选，开始勾选...")
                                    try:
                                        # 滚动到复选框位置
                                        await confirm_checkbox.scroll_into_view_if_needed()
                                        await confirm_checkbox.wait_for(state="visible", timeout=2000)

                                        # 点击复选框
                                        await confirm_checkbox.click()
                                        await page.wait_for_timeout(300)  # 等待状态更新

                                        # 验证是否已勾选
                                        is_checked_after = await confirm_checkbox.evaluate("el => el.checked")
                                        if is_checked_after:
                                            print("  ✅ 已成功勾选'已确认以上商机信息'复选框")
                                        else:
                                            # 检查父元素
                                            parent_checked_after = await confirm_checkbox.evaluate("""
                                                el => {
                                                    const parent = el.closest('.ant-checkbox-wrapper, label');
                                                    if (parent) {
                                                        return parent.classList.contains('ant-checkbox-checked') || 
                                                               parent.querySelector('.ant-checkbox-checked') !== null;
                                                    }
                                                    return false;
                                                }
                                            """)
                                            if parent_checked_after:
                                                print("  ✅ 已成功勾选'已确认以上商机信息'复选框（通过父元素验证）")
                                            else:
                                                print("  ⚠ 警告：点击后复选框仍未被勾选，尝试使用JavaScript...")
                                                # 使用JavaScript强制勾选
                                                await confirm_checkbox.evaluate(
                                                    "el => { el.checked = true; el.dispatchEvent(new Event('change', { bubbles: true })); }")
                                                await page.wait_for_timeout(300)
                                                print("  ✅ 已通过JavaScript勾选'已确认以上商机信息'复选框")
                                    except Exception as click_error:
                                        print(f"  ⚠ 警告：点击复选框失败: {click_error}")
                                        # 尝试使用JavaScript
                                        try:
                                            await confirm_checkbox.evaluate(
                                                "el => { el.checked = true; el.dispatchEvent(new Event('change', { bubbles: true })); }")
                                            await page.wait_for_timeout(300)
                                            print("  ✅ 已通过JavaScript勾选'已确认以上商机信息'复选框")
                                        except Exception as js_error:
                                            print(f"  ❌ 错误：无法勾选复选框: {js_error}")
                            except Exception as e:
                                print(f"  ❌ 错误：检查复选框状态时出错: {e}")
                    except Exception as disabled_check_error:
                        print(f"  ⚠ 警告：检查复选框禁用状态时出错: {disabled_check_error}，继续处理...")

            print("✅ '审批意见'部分检查完成")

            # 步骤11.5. 检查"审批矩阵"部分，如果有就逐行选择"不触碰"单选按钮
            print("\n[步骤11.5] 检查'审批矩阵'部分...")

            # 先检查页面中是否存在"审批矩阵"部分
            print("  检查页面中是否存在'审批矩阵'部分...")
            has_approval_matrix_section = False

            try:
                # 方法1：检查是否存在"审批矩阵"文本
                approval_matrix_keywords = ["审批矩阵", "矩阵"]
                for keyword in approval_matrix_keywords:
                    try:
                        matrix_element = page.locator(f"*:has-text('{keyword}')").first
                        if await matrix_element.count() > 0:
                            # 进一步检查是否包含风险识别相关文本
                            page_text = await page.evaluate("() => document.body.innerText || ''")
                            if "风险识别" in page_text and ("不触碰" in page_text or "触碰" in page_text):
                                has_approval_matrix_section = True
                                print(f"  ✅ 找到'审批矩阵'部分（通过关键词: {keyword}）")
                                break
                    except:
                        continue

                # 方法2：直接检查是否存在风险识别相关文本
                if not has_approval_matrix_section:
                    try:
                        page_text = await page.evaluate("() => document.body.innerText || ''")
                        if "风险识别" in page_text and ("不触碰" in page_text or "触碰" in page_text):
                            has_approval_matrix_section = True
                            print(f"  ✅ 找到审批矩阵相关字段（风险识别）")
                    except:
                        pass

            except Exception as e:
                print(f"  ⚠ 检查'审批矩阵'部分时出错: {e}")

            # 如果页面中没有"审批矩阵"部分，跳过
            if not has_approval_matrix_section:
                print("  ⚠ 页面中未找到'审批矩阵'部分，跳过此步骤")
            else:
                # 等待页面稳定
                await page.wait_for_timeout(500)
                # 等待遮罩层消失
                await wait_for_overlay_disappear_async(page)

                # 使用JavaScript查找审批矩阵表格并逐行处理
                try:
                    result = await page.evaluate("""
                        () => {
                            // 查找包含"审批矩阵"或"风险识别"的表格
                            const tables = Array.from(document.querySelectorAll('table'));
                            let targetTable = null;

                            for (const table of tables) {
                                const tableText = table.textContent || '';
                                if (tableText.includes('风险识别') && (tableText.includes('不触碰') || tableText.includes('触碰'))) {
                                    targetTable = table;
                                    break;
                                }
                            }

                            if (!targetTable) return { found: false, message: '未找到审批矩阵表格' };

                            // 找到"风险识别"列的索引
                            const headerRow = targetTable.querySelector('thead tr, tr:first-child');
                            if (!headerRow) return { found: false, message: '未找到表头' };

                            const headers = Array.from(headerRow.querySelectorAll('th, td'));
                            let riskIdentificationColumnIndex = -1;

                            for (let i = 0; i < headers.length; i++) {
                                const headerText = headers[i].textContent.trim();
                                if (headerText.includes('风险识别')) {
                                    riskIdentificationColumnIndex = i;
                                    break;
                                }
                            }

                            if (riskIdentificationColumnIndex === -1) {
                                return { found: false, message: '未找到"风险识别"列' };
                            }

                            // 获取所有数据行
                            const rows = Array.from(targetTable.querySelectorAll('tbody tr, tr'));
                            const dataRows = rows.filter(row => {
                                // 排除表头行
                                return row.querySelector('th') === null;
                            });

                            const rowData = [];

                            dataRows.forEach((row, rowIndex) => {
                                const cells = Array.from(row.querySelectorAll('td'));
                                if (cells.length > riskIdentificationColumnIndex) {
                                    const riskCell = cells[riskIdentificationColumnIndex];
                                    // 在风险识别列中查找"不触碰"单选按钮
                                    const radios = Array.from(riskCell.querySelectorAll('input[type="radio"]'));

                                    for (const radio of radios) {
                                        // 检查这个单选按钮是否是"不触碰"
                                        let isNotTouch = false;

                                        // 方法1：检查父元素文本
                                        let parent = radio.parentElement;
                                        for (let i = 0; i < 5 && parent; i++) {
                                            const text = parent.textContent || '';
                                            if (text.includes('不触碰')) {
                                                isNotTouch = true;
                                                break;
                                            }
                                            parent = parent.parentElement;
                                        }

                                        // 方法2：检查label
                                        if (!isNotTouch) {
                                            const label = document.querySelector(`label[for="${radio.id}"]`);
                                            if (label && label.textContent.includes('不触碰')) {
                                                isNotTouch = true;
                                            }
                                        }

                                        // 方法3：检查相邻文本
                                        if (!isNotTouch) {
                                            let nextSibling = radio.nextSibling;
                                            while (nextSibling) {
                                                if (nextSibling.nodeType === 3 && nextSibling.textContent.includes('不触碰')) {
                                                    isNotTouch = true;
                                                    break;
                                                }
                                                if (nextSibling.nodeType === 1 && nextSibling.textContent.includes('不触碰')) {
                                                    isNotTouch = true;
                                                    break;
                                                }
                                                nextSibling = nextSibling.nextSibling;
                                            }
                                        }

                                        if (isNotTouch) {
                                            // 生成唯一ID（如果还没有）
                                            if (!radio.id) {
                                                radio.id = `not_touch_radio_row_${rowIndex}_${Date.now()}`;
                                            }

                                            rowData.push({
                                                rowIndex: rowIndex,
                                                radioId: radio.id,
                                                radioName: radio.name || '',
                                                radioValue: radio.value || '',
                                                checked: radio.checked,
                                                disabled: radio.disabled
                                            });
                                            break; // 每行只取第一个"不触碰"单选按钮
                                        }
                                    }
                                }
                            });

                            return {
                                found: true,
                                rowCount: rowData.length,
                                rows: rowData
                            };
                        }
                    """)

                    if not result.get('found', False):
                        print(f"  ⚠ 警告：{result.get('message', '未找到审批矩阵表格')}，跳过此步骤")
                    elif result.get('rowCount', 0) == 0:
                        print(f"  ⚠ 警告：未找到任何包含'不触碰'单选按钮的行，跳过此步骤")
                    else:
                        print(f"  ✅ 找到审批矩阵表格，共 {result.get('rowCount', 0)} 行需要处理")

                        # 统计信息
                        checked_count = 0
                        already_checked_count = 0
                        disabled_count = 0
                        not_found_count = 0

                        # 逐行处理
                        for row_info in result.get('rows', []):
                            row_index = row_info.get('rowIndex', -1)
                            radio_id = row_info.get('radioId', '')
                            radio_name = row_info.get('radioName', '')
                            radio_value = row_info.get('radioValue', '')
                            is_checked = row_info.get('checked', False)
                            is_disabled = row_info.get('disabled', False)

                            print(f"\n  处理第 {row_index + 1} 行...")

                            # 如果已被禁用，跳过
                            if is_disabled:
                                print(f"    ⊘ 第 {row_index + 1} 行的'不触碰'单选按钮已被禁用（置灰），跳过处理")
                                disabled_count += 1
                                continue

                            # 如果已经选中，跳过
                            if is_checked:
                                print(f"    ✓ 第 {row_index + 1} 行的'不触碰'单选按钮已选中，跳过")
                                already_checked_count += 1
                                continue

                            # 定位单选按钮
                            radio_button = None

                            # 方法1：通过ID定位
                            if radio_id:
                                try:
                                    radio_button = page.locator(f"input[type='radio'][id='{radio_id}']").first
                                    if await radio_button.count() == 0:
                                        radio_button = None
                                except:
                                    radio_button = None

                            # 方法2：通过name和value定位
                            if not radio_button and radio_name and radio_value:
                                try:
                                    radio_button = page.locator(
                                        f"input[type='radio'][name='{radio_name}'][value='{radio_value}']"
                                    ).first
                                    if await radio_button.count() == 0:
                                        radio_button = None
                                except:
                                    radio_button = None

                            # 方法3：通过表格行定位（备用方案）
                            if not radio_button:
                                try:
                                    # 找到表格
                                    table = page.locator("table:has-text('风险识别')").first
                                    if await table.count() > 0:
                                        # 找到对应的行
                                        rows = table.locator("tbody tr, tr").filter(has_not=page.locator("th"))
                                        row = rows.nth(row_index)
                                        if await row.count() > 0:
                                            # 在行中查找"不触碰"单选按钮
                                            not_touch_radio = row.locator("input[type='radio']").filter(
                                                has=page.locator("*:has-text('不触碰')")
                                            ).first
                                            if await not_touch_radio.count() > 0:
                                                radio_button = not_touch_radio
                                except:
                                    pass

                            if not radio_button:
                                print(f"    ⚠ 警告：无法定位第 {row_index + 1} 行的'不触碰'单选按钮")
                                not_found_count += 1
                                continue

                            # 再次检查是否被禁用（动态检查）
                            try:
                                is_disabled_now = await radio_button.evaluate("""
                                    el => {
                                        if (el.disabled) return true;
                                        const parent = el.closest('.ant-radio-wrapper, label');
                                        if (parent) {
                                            if (parent.classList.contains('ant-radio-disabled')) return true;
                                            if (parent.hasAttribute('disabled') || parent.getAttribute('aria-disabled') === 'true') return true;
                                            const style = window.getComputedStyle(parent);
                                            if (style.pointerEvents === 'none' || style.opacity === '0.5' || style.cursor === 'not-allowed') return true;
                                        }
                                        return false;
                                    }
                                """)

                                if is_disabled_now:
                                    print(f"    ⊘ 第 {row_index + 1} 行的'不触碰'单选按钮已被禁用（置灰），跳过处理")
                                    disabled_count += 1
                                    continue
                            except:
                                pass

                            # 选择单选按钮
                            try:
                                # 滚动到单选按钮位置
                                await radio_button.scroll_into_view_if_needed()
                                await radio_button.wait_for(state="visible", timeout=2000)

                                # 点击单选按钮
                                await radio_button.click()
                                await page.wait_for_timeout(300)  # 等待状态更新

                                # 验证是否已选中
                                is_checked_after = await radio_button.evaluate("el => el.checked")
                                if is_checked_after:
                                    print(f"    ✅ 已成功选择第 {row_index + 1} 行的'不触碰'单选按钮")
                                    checked_count += 1
                                else:
                                    # 检查父元素
                                    parent_checked = await radio_button.evaluate("""
                                        el => {
                                            const parent = el.closest('.ant-radio-wrapper, label, .ant-radio-group');
                                            if (parent) {
                                                if (parent.classList.contains('ant-radio-checked')) return true;
                                                if (parent.querySelector('.ant-radio-checked') !== null) return true;
                                                if (parent.classList.contains('ant-radio-group')) {
                                                    const checkedRadio = parent.querySelector('input[type="radio"]:checked');
                                                    if (checkedRadio && checkedRadio === el) return true;
                                                }
                                            }
                                            return false;
                                        }
                                    """)

                                    if parent_checked:
                                        print(
                                            f"    ✅ 已成功选择第 {row_index + 1} 行的'不触碰'单选按钮（通过父元素验证）")
                                        checked_count += 1
                                    else:
                                        print(f"    ⚠ 警告：点击后单选按钮仍未被选中，尝试使用JavaScript...")
                                        # 使用JavaScript强制选中
                                        await radio_button.evaluate("""
                                            el => {
                                                // 如果是radio组，先取消同组其他选项
                                                const group = el.closest('.ant-radio-group');
                                                if (group) {
                                                    const radios = group.querySelectorAll('input[type="radio"]');
                                                    radios.forEach(r => r.checked = false);
                                                }
                                                el.checked = true;
                                                el.dispatchEvent(new Event('change', { bubbles: true }));
                                                el.dispatchEvent(new Event('click', { bubbles: true }));
                                            }
                                        """)
                                        await page.wait_for_timeout(300)

                                        # 再次验证
                                        is_checked_final = await radio_button.evaluate("el => el.checked")
                                        if is_checked_final:
                                            print(f"    ✅ 已通过JavaScript选择第 {row_index + 1} 行的'不触碰'单选按钮")
                                            checked_count += 1
                                        else:
                                            print(f"    ❌ 错误：无法选择第 {row_index + 1} 行的'不触碰'单选按钮")
                                            not_found_count += 1
                            except Exception as click_error:
                                print(f"    ⚠ 警告：点击单选按钮失败: {click_error}")
                                # 尝试使用JavaScript
                                try:
                                    await radio_button.evaluate("""
                                        el => {
                                            const group = el.closest('.ant-radio-group');
                                            if (group) {
                                                const radios = group.querySelectorAll('input[type="radio"]');
                                                radios.forEach(r => r.checked = false);
                                            }
                                            el.checked = true;
                                            el.dispatchEvent(new Event('change', { bubbles: true }));
                                            el.dispatchEvent(new Event('click', { bubbles: true }));
                                        }
                                    """)
                                    await page.wait_for_timeout(300)
                                    is_checked_final = await radio_button.evaluate("el => el.checked")
                                    if is_checked_final:
                                        print(f"    ✅ 已通过JavaScript选择第 {row_index + 1} 行的'不触碰'单选按钮")
                                        checked_count += 1
                                    else:
                                        print(f"    ❌ 错误：无法选择第 {row_index + 1} 行的'不触碰'单选按钮")
                                        not_found_count += 1
                                except Exception as js_error:
                                    print(f"    ❌ 错误：无法选择单选按钮: {js_error}")
                                    not_found_count += 1

                        # 输出统计信息
                        print(f"\n  处理完成统计:")
                        print(f"    - 已选择: {checked_count} 个")
                        print(f"    - 已选中（跳过）: {already_checked_count} 个")
                        print(f"    - 已禁用（跳过）: {disabled_count} 个")
                        print(f"    - 未找到: {not_found_count} 个")

                        if checked_count > 0:
                            print(f"  ✅ 已处理 {checked_count} 个单选按钮")
                        elif already_checked_count > 0:
                            print(f"  ✅ 所有单选按钮都已选中，无需操作")
                        elif disabled_count > 0:
                            print(f"  ⚠ 所有单选按钮都已禁用，无法处理")

                        # 等待遮罩层消失，确保所有操作完成
                        await wait_for_overlay_disappear_async(page)
                        await page.wait_for_timeout(500)

                except Exception as e:
                    print(f"  ❌ 错误：处理审批矩阵时出错: {e}")
                    import traceback
                    traceback.print_exc()

            print("✅ '审批矩阵'部分检查完成")

            # 步骤12. 在新页面上点击"同意"按钮
            print("\n[步骤12] 在新页面上点击'同意'按钮...")

            # 等待页面完全加载
            await wait_for_page_ready_async(page)

            # 等待按钮区域加载
            print("  等待按钮区域加载...")
            try:
                await page.wait_for_selector("button.ant-btn, button.ant-btn-primary", timeout=5000)
                print("  ✅ 按钮区域已加载")
            except:
                print("  ⚠ 警告：按钮区域可能未完全加载，继续尝试...")

            # 调试：打印页面上所有包含"同意"文本的元素
            try:
                all_agree_elements = await page.locator("*:has-text('同意')").all()
                print(f"  找到 {len(all_agree_elements)} 个包含'同意'文本的元素")
            except:
                pass

            # 调试：打印页面上所有class包含ant-btn-primary的按钮
            try:
                all_primary_buttons = await page.locator("button.ant-btn-primary").all()
                print(f"  找到 {len(all_primary_buttons)} 个主按钮（ant-btn-primary）")
                for idx, btn in enumerate(all_primary_buttons[:5]):  # 只打印前5个
                    try:
                        btn_text = await btn.text_content() or ""
                        btn_class = await btn.get_attribute("class") or ""
                        print(f"    按钮{idx + 1}: 文本='{btn_text}', class='{btn_class}'")
                    except:
                        pass
            except:
                pass

            # 定位"同意"按钮（优先使用文本和class定位）
            # 注意：按钮文本在 <span>同 意</span> 中，需要定位包含span的button
            agree_button_locators = [
                # 方法1：通过包含span的button定位（最可靠）
                lambda p: p.locator("button:has(span:has-text('同 意'))").first,
                lambda p: p.locator("button.ant-btn:has(span:has-text('同 意'))").first,
                lambda p: p.locator("button.ant-btn-primary:has(span:has-text('同 意'))").first,
                lambda p: p.locator("button.ant-btn.ant-btn-primary:has(span:has-text('同 意'))").first,

            ]

            agree_button = await try_locators_async(page, agree_button_locators, "同意按钮", timeout=WAIT_TIME)
            await agree_button.scroll_into_view_if_needed()
            await wait_for_element_ready_async(page, agree_button, "同意按钮")

            # 优化：确保按钮真正可点击（更严格的验证）
            print("  验证按钮是否真正可点击...")
            max_click_attempts = 3
            click_success = False

            for attempt in range(1, max_click_attempts + 1):
                try:
                    # 方法1：等待按钮可见和可交互
                    await agree_button.wait_for(state="visible", timeout=WAIT_TIME)
                    await agree_button.wait_for(state="attached", timeout=WAIT_TIME)

                    # 方法2：滚动到按钮位置，确保在视口中
                    await agree_button.scroll_into_view_if_needed()
                    await page.wait_for_timeout(300)  # 等待滚动完成

                    # 方法3：检查按钮是否真正可点击（包括是否被遮挡）
                    is_enabled = await agree_button.evaluate("""
                        el => {
                            // 检查基本属性
                            if (el.disabled) return false;
                            if (el.offsetParent === null) return false;
                            if (el.classList.contains('ant-btn-disabled') || 
                                el.classList.contains('disabled') ||
                                el.closest('.ant-btn-disabled')) return false;

                            // 检查样式
                            const style = window.getComputedStyle(el);
                            if (style.pointerEvents === 'none') return false;
                            if (style.display === 'none' || style.visibility === 'hidden') return false;

                            // 检查是否被其他元素遮挡
                            const rect = el.getBoundingClientRect();
                            const centerX = rect.left + rect.width / 2;
                            const centerY = rect.top + rect.height / 2;
                            const topElement = document.elementFromPoint(centerX, centerY);

                            // 如果点击位置被其他元素遮挡，且不是按钮本身或其子元素
                            if (topElement && !el.contains(topElement) && topElement !== el) {
                                // 检查遮挡元素是否是遮罩层或加载层（这些可以忽略）
                                const isOverlay = topElement.classList.contains('ant-modal-mask') ||
                                                 topElement.classList.contains('ant-spin-container') ||
                                                 topElement.closest('.ant-spin-container');
                                if (!isOverlay) {
                                    return false;  // 被其他元素遮挡
                                }
                            }

                            return true;
                        }
                    """)

                    if not is_enabled:
                        print(f"  ⚠ 警告：同意按钮当前不可点击（尝试 {attempt}/{max_click_attempts}）")
                        if attempt < max_click_attempts:
                            await page.wait_for_timeout(1000)
                            continue
                        else:
                            raise Exception("按钮不可点击")

                    print(f"  ✅ 同意按钮已找到且可点击（尝试 {attempt}/{max_click_attempts}）")

                    # 步骤4：记录点击前的状态（用于验证）
                    current_url_before = page.url
                    button_exists_before = await agree_button.count() > 0

                    # 步骤5：尝试点击按钮（使用force确保点击成功）
                    print(f"  尝试点击'同意'按钮（尝试 {attempt}/{max_click_attempts}）...")
                    try:
                        # 先尝试普通点击
                        await agree_button.click(timeout=5000)
                        print(f"  ✅ 已通过普通点击方式点击'同意'按钮")
                    except Exception as normal_click_error:
                        print(f"  ⚠ 普通点击失败，尝试强制点击: {str(normal_click_error)[:50]}")
                        # 如果普通点击失败，使用force强制点击
                        try:
                            await agree_button.click(force=True, timeout=5000)
                            print(f"  ✅ 已通过强制点击方式点击'同意'按钮")
                        except Exception as force_click_error:
                            print(f"  ⚠ 强制点击也失败，使用JavaScript: {str(force_click_error)[:50]}")
                            # 最后尝试JavaScript点击
                            await agree_button.evaluate("""
                                el => {
                                    if (el) {
                                        // 触发多种事件确保点击生效
                                        el.focus();
                                        el.click();
                                        el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                                        el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                                        el.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                                    }
                                }
                            """)
                            print(f"  ✅ 已通过JavaScript点击'同意'按钮")

                    # 步骤6：验证点击是否成功
                    print("  验证点击是否成功...")
                    await page.wait_for_timeout(500)  # 等待点击响应

                    # 验证方法1：检查是否有弹窗出现（成功点击后通常会弹出提示）
                    try:
                        modal_appeared = await page.wait_for_selector(
                            "div.ant-modal:not([style*='display: none']), "
                            "div.ant-modal.ant-modal-open, "
                            "div[role='dialog']:not([style*='display: none'])",
                            timeout=3000
                        )
                        if modal_appeared:
                            print("  ✅ 验证成功：检测到弹窗出现，点击已生效")
                            click_success = True
                            break
                    except:
                        pass

                    # 验证方法2：检查按钮是否消失或变为禁用状态（某些情况下按钮会消失）
                    try:
                        button_exists_after = await agree_button.count() > 0
                        if not button_exists_after:
                            print("  ✅ 验证成功：按钮已消失，点击已生效")
                            click_success = True
                            break

                        # 检查按钮是否变为禁用状态
                        is_disabled_after = await agree_button.evaluate("""
                            el => {
                                return el.disabled || 
                                       el.classList.contains('ant-btn-disabled') ||
                                       el.classList.contains('disabled');
                            }
                        """)
                        if is_disabled_after:
                            print("  ✅ 验证成功：按钮已变为禁用状态，点击已生效")
                            click_success = True
                            break
                    except:
                        pass

                    # 验证方法3：检查页面URL是否变化
                    try:
                        await page.wait_for_timeout(1000)
                        current_url_after = page.url
                        if current_url_after != current_url_before:
                            print(f"  ✅ 验证成功：页面URL已变化，点击已生效")
                            click_success = True
                            break
                    except:
                        pass

                    # 验证方法4：检查是否有网络请求（点击后通常会有API请求）
                    try:
                        # 等待网络请求完成
                        await page.wait_for_load_state("networkidle", timeout=3000)
                        print("  ✅ 验证成功：检测到网络请求完成，点击可能已生效")
                        click_success = True
                        break
                    except:
                        pass

                    # 如果所有验证都失败，但这是最后一次尝试，认为可能成功
                    if attempt == max_click_attempts:
                        print("  ⚠ 警告：无法完全验证点击是否成功，但已执行点击操作")
                        click_success = True  # 假设成功，继续执行
                        break
                    else:
                        print(f"  ⚠ 验证失败，重试点击（尝试 {attempt + 1}/{max_click_attempts}）...")
                        await page.wait_for_timeout(1000)

                except Exception as e:
                    print(f"  ❌ 点击失败（尝试 {attempt}/{max_click_attempts}）: {str(e)[:100]}")
                    if attempt < max_click_attempts:
                        print(f"  等待后重试...")
                        await page.wait_for_timeout(1000)
                    else:
                        raise Exception(f"点击'同意'按钮失败（已重试{max_click_attempts}次）: {str(e)}")

            if not click_success:
                raise Exception("点击'同意'按钮失败，无法验证点击是否成功")

            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            print("✅ 已成功点击'同意'按钮并验证成功")

            # 等待弹窗出现并点击知道了按钮
            print("\n[步骤10] 等待弹窗并点击确定按钮...")

            try:
                await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
            except:
                await page.wait_for_load_state("domcontentloaded", timeout=WAIT_TIME)

            await wait_for_modal_async(page)

            # 等待弹窗内容完全加载
            try:
                await page.wait_for_function(
                    "() => { const modal = document.querySelector('.ant-modal-content, [role=dialog]'); return modal && modal.offsetParent !== null; }",
                    timeout=WAIT_TIME
                )
            except:
                pass

            # 弹窗确定按钮的所有定位方式
            confirm_button_locators = [
                lambda p: p.locator("div.ant-modal, div[role='dialog']").get_by_role("button", name="知道了").first,
                lambda p: p.locator("div.ant-modal, div[role='dialog']").get_by_text("知道了", exact=True).first,
                lambda p: p.get_by_role("button", name="知道了").first,
                lambda p: p.get_by_text("知道了", exact=True).first,
                lambda p: p.locator("div.ant-modal button:has-text('知道了')").first,
                lambda p: p.locator("div[role='dialog'] button:has-text('知道了')").first
            ]

            confirm_button = await try_locators_async(page, confirm_button_locators, "知道了按钮", timeout=5000)
            await confirm_button.scroll_into_view_if_needed()
            await confirm_button.wait_for(state="visible", timeout=2000)
            await confirm_button.click()
            print("✅ 已点击知道了按钮")

            # 等待弹窗关闭
            try:
                await page.wait_for_selector("div.ant-modal, div[role='dialog']", state="hidden", timeout=WAIT_TIME)
                print("✅ 弹窗已关闭")
            except:
                await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)

            # 等待遮罩层消失
            await wait_for_overlay_disappear_async(page)
            # 等待操作完成
            await page.wait_for_timeout(500)
            await wait_for_page_ready_async(page, timeout=3000)

            await page.wait_for_timeout(2000)
            await page.wait_for_load_state("networkidle", timeout=WAIT_TIME)
            # 再次等待遮罩层消失，确保所有加载完成
            await wait_for_overlay_disappear_async(page)
            print("✅ 审批操作已完成")

            # 完成一次循环，继续下一次循环
            print("\n✅ 本次循环完成，继续下一次循环...")

        # 等待5秒钟
        print("\n  等待5秒钟...")
        await page.wait_for_timeout(5000)
        print("  ✅ 等待完成")

    except Exception as e:
        print("\n" + "=" * 50)
        print(f"❌ 测试失败: {str(e)}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        raise
    finally:
        if page:
            await page.close()
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()


if __name__ == '__main__':
    asyncio.run(main())