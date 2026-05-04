from typing import Dict, List, Any
from datetime import datetime
import sys
import os
import importlib.util

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 动态导入模块
def import_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 导入模块
login_page = import_module_from_path('login_page', '06_pages_页面对象/login_page_登录页面.py')
LoginPage = login_page.LoginPage

dashboard_page = import_module_from_path('dashboard_page', '06_pages_页面对象/dashboard_page_工作台页面.py')
DashboardPage = dashboard_page.DashboardPage

self_healing_locator = import_module_from_path('self_healing_locator', '05_utils_工具库/self_healing_locator_智能定位器.py')
SelfHealingLocator = self_healing_locator.SelfHealingLocator

# 导入AI Agent控制器
from .ai_agent_controller import AIAgentController

class MCPController:
    """MCP模式控制器"""
    
    def __init__(self, page):
        """初始化MCP控制器"""
        self.page = page
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.self_healing = SelfHealingLocator()
        self.ai_agent = AIAgentController(page)
    
    async def execute_test_case(self, case: Dict) -> Dict:
        """执行测试用例"""
        case_id = case['case_id']
        test_name = case['case_name']
        
        print(f"\n🚀 MCP模式执行: {case_id} - {test_name}")
        print(f"🤖 AI Agent 分析测试用例...")
        
        # 使用AI Agent分析测试用例
        test_suggestions = await self.ai_agent.generate_test_suggestions(case)
        if test_suggestions:
            print("💡 AI建议:")
            for suggestion in test_suggestions:
                print(f"   - {suggestion}")
        
        result = {
            'case_id': case_id,
            'test_name': test_name,
            'status': 'passed',
            'steps': [],
            'error': None,
            'screenshot': None,
            'ai_suggestions': test_suggestions
        }
        
        try:
            # 检查是否需要登录
            if self._needs_login(case):
                await self._perform_login()
            
            # 执行测试步骤
            for step in case['steps']:
                # 使用AI Agent调整测试步骤
                context = {'current_step': step['step_number']}
                adapted_step = await self.ai_agent.adapt_test_step(step, context)
                
                if adapted_step != step:
                    print(f"🔄 AI调整步骤 {step['step_number']}")
                
                step_result = await self._execute_step(adapted_step)
                result['steps'].append(step_result)
                
                if step_result['status'] == 'failed':
                    # 使用AI Agent处理错误
                    error_context = {
                        'error': step_result['error'],
                        'step': step
                    }
                    decision = await self.ai_agent.make_decision(error_context)
                    print(f"🤖 AI决策: {decision['action']} - {decision['reasoning']}")
                    
                    result['status'] = 'failed'
                    result['error'] = step_result.get('error', 'Step failed')
                    break
            
            # 学习执行结果
            execution_data = {
                'case_id': case_id,
                'status': result['status'],
                'error': result.get('error'),
                'timestamp': datetime.now().isoformat()
            }
            await self.ai_agent.learn_from_execution(execution_data)
            
            if result['status'] == 'passed':
                print(f"✅ {test_name} - 通过")
            else:
                print(f"❌ {test_name} - 失败: {result['error']}")
                
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            print(f"❌ {test_name} - 失败: {e}")
            
            # 学习错误
            execution_data = {
                'case_id': case_id,
                'status': 'failed',
                'error': str(e),
                'error_type': type(e).__name__,
                'timestamp': datetime.now().isoformat()
            }
            await self.ai_agent.learn_from_execution(execution_data)
        
        # 获取优化建议
        optimization_suggestions = await self.ai_agent.get_optimization_suggestions()
        if optimization_suggestions:
            print("📈 优化建议:")
            for suggestion in optimization_suggestions:
                print(f"   - {suggestion}")
            result['optimization_suggestions'] = optimization_suggestions
        
        return result
    
    def _needs_login(self, case: Dict) -> bool:
        """判断是否需要登录"""
        if '登录' in case['case_name']:
            return True
        
        for step in case['steps']:
            if '登录' in step['action']:
                return True
        
        return False
    
    async def _perform_login(self):
        """执行登录操作"""
        # 动态导入配置模块
        config_module = import_module_from_path('config', '10_config_配置管理/config_配置管理.py')
        Config = config_module.Config
        config = Config()
        base_url = config.get_base_url()
        username = config.get_username()
        password = config.get_password()
        
        print(f"🔐 执行登录操作: {base_url}")
        await self.login_page.go_to_login_page(base_url)
        await self.login_page.login(username, password)
        
        assert await self.dashboard_page.is_dashboard_page(), "登录后应该在工作台页面"
        print("✅ 登录成功")
    
    async def _execute_step(self, step: Dict) -> Dict:
        """执行单个测试步骤"""
        step_num = step['step_number']
        action = step['action']
        selector = step['selector']
        data = step['data']
        expected = step['expected']
        
        step_result = {
            'step_number': step_num,
            'action': action,
            'selector': selector,
            'data': data,
            'expected': expected,
            'status': 'passed',
            'error': None
        }
        
        print(f"  步骤 {step_num}: {action}")
        
        try:
            # 使用自愈能力执行操作
            if action == '登录系统':
                # 已经在前面处理了登录
                pass
            elif action == '验证工作台标题':
                assert await self.dashboard_page.is_dashboard_page(), expected
            elif action == '验证今日数据区域':
                assert await self.dashboard_page.verify_workbench_data(), expected
            elif action == '验证本月数据区域':
                assert await self.dashboard_page.verify_workbench_data(), expected
            elif action == '验证待跟进客户列表':
                assert await self.dashboard_page.verify_customer_list(), expected
            elif action == '验证待审批事项列表':
                assert await self.dashboard_page.verify_approval_list(), expected
            elif action == '查看今日新增客户':
                assert await self.dashboard_page.verify_today_customers(), expected
            elif action == '点击工作台菜单':
                await self.dashboard_page.click_workbench_menu()
            elif action == '点击客户管理菜单':
                await self.dashboard_page.click_customer_menu()
            elif action == '查看待跟进客户列表':
                assert await self.dashboard_page.verify_customer_list(), expected
            elif action == '点击添加跟进按钮':
                await self.dashboard_page.click_add_follow_button()
            
        except Exception as e:
            step_result['status'] = 'failed'
            step_result['error'] = str(e)
            print(f"    ❌ 失败: {e}")
        
        return step_result