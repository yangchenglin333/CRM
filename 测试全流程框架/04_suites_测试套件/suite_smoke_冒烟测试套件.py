"""冒烟测试套件 - 快速验证核心功能"""
import pytest


class TestSmokeSuite:
    """冒烟测试套件"""
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_functionality(self, page):
        """测试登录功能"""
        from pages.login_page import LoginPage
        from pages.dashboard_page import DashboardPage
        from utils.config import Config
        
        config = Config()
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        login_page.go_to_login_page(config.get_base_url())
        login_page.login(config.get_username(), config.get_password())
        
        assert dashboard_page.is_dashboard_page(), "登录后应该在工作台页面"
    
    @pytest.mark.smoke
    def test_dashboard_display(self, page):
        """测试工作台显示"""
        from pages.login_page import LoginPage
        from pages.dashboard_page import DashboardPage
        from utils.config import Config
        
        config = Config()
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        login_page.go_to_login_page(config.get_base_url())
        login_page.login(config.get_username(), config.get_password())
        
        assert dashboard_page.verify_workbench_data(), "工作台数据应该正常显示"
