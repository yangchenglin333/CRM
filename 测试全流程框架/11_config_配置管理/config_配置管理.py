import yaml
import os
from pathlib import Path


class Config:
    """配置管理工具类"""

    def __init__(self, config_path: str = None):
        """初始化配置"""
        if config_path is None:
            config_path = str(Path(__file__).parent.parent / "10_config_配置管理" / "config_主配置.yaml")
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_environment_config(self):
        """获取环境配置"""
        env = self.config.get('environment', {}).get('default', 'test')
        return self.config.get('environment', {}).get(env, {})

    def get_browser_config(self):
        """获取浏览器配置"""
        return self.config.get('browser', {})

    def get_test_config(self):
        """获取测试配置"""
        return self.config.get('test', {})

    def get_report_config(self):
        """获取报告配置"""
        return self.config.get('report', {})

    def get_base_url(self):
        """获取基础URL"""
        return self.get_environment_config().get('base_url', '')

    def get_username(self):
        """获取用户名"""
        return self.get_environment_config().get('username', '')

    def get_password(self):
        """获取密码"""
        return self.get_environment_config().get('password', '')
