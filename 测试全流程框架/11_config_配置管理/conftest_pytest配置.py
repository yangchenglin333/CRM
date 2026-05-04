import pytest
from pathlib import Path
from utils.config import Config


def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption("--env", action="store", default="default", help="测试环境: default, dev, test, prod")


@pytest.fixture(scope="session")
def config(request):
    """配置文件fixture"""
    env = request.config.getoption("--env")
    config = Config()
    config._config['test']['environment'] = env
    return config


@pytest.fixture(scope="function")
def page_context(browser_context, config):
    """页面上下文fixture"""
    context = browser_context
    return context


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束钩子"""
    print("\n" + "="*50)
    print("测试执行完成!")
    print(f"退出状态码: {exitstatus}")
    print("="*50)
