#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import requests
import json
import allure
import os

BASE_URL = "http://localhost:3000"
session = requests.Session()

def login_first():
    """登录获取session"""
    try:
        response = session.post(f"{BASE_URL}/api/users/login",
                            json={"username": "admin", "password": "123456"})
        if response.status_code == 200:
            print("登录成功")
    except Exception as e:
        print(f"登录失败: {e}")

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """测试环境初始化"""
    with allure.step("【前置操作】初始化测试环境"):
        login_first()
        allure.attach("登录用户: admin", name="登录信息", attachment_type=allure.attachment_type.TEXT)
    yield
    with allure.step("【后置操作】清理测试环境"):
        pass

def send_request(method, url, headers=None, params=None, body=None):
    """统一请求发送方法，自动记录请求和响应信息到Allure报告"""
    allure.attach(url, name="请求URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(method, name="请求方法", attachment_type=allure.attachment_type.TEXT)

    if headers:
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=2),
                     name="请求头", attachment_type=allure.attachment_type.JSON)

    if params:
        allure.attach(json.dumps(params, ensure_ascii=False, indent=2),
                     name="URL参数", attachment_type=allure.attachment_type.JSON)

    if body:
        allure.attach(json.dumps(body, ensure_ascii=False, indent=2),
                     name="请求体", attachment_type=allure.attachment_type.JSON)

    with allure.step(f"执行请求: {method} {url}"):
        if method.upper() == "GET":
            response = session.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = session.post(url, headers=headers, json=body, params=params)
        elif method.upper() == "PUT":
            response = session.put(url, headers=headers, json=body, params=params)
        elif method.upper() == "DELETE":
            response = session.delete(url, headers=headers, json=body, params=params)
        else:
            raise ValueError(f"不支持的请求方法: {method}")

    allure.attach(str(response.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)

    try:
        response_data = response.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2),
                     name="响应数据", attachment_type=allure.attachment_type.JSON)
    except:
        allure.attach(response.text, name="响应文本", attachment_type=allure.attachment_type.TEXT)

    return response

def load_test_cases():
    """从JSON文件加载测试用例"""
    json_path = os.path.join(os.path.dirname(__file__), '../02_api_testcases/json/20260502_CRM_API测试用例_v1.1.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

test_cases = load_test_cases()

def pytest_generate_tests(metafunc):
    """动态生成测试用例"""
    if 'test_case' in metafunc.fixturenames:
        metafunc.parametrize('test_case', test_cases)

@pytest.fixture
def test_case(request):
    """返回当前测试用例数据"""
    return request.param

def test_api(test_case, test_runner):
    """动态API测试函数"""
    case_id = test_case['id']
    case_name = test_case['name']
    path = test_case['path']
    method = test_case['method']
    headers = test_case.get('headers', {})
    params = test_case.get('params', {})
    body = test_case.get('body')
    expected_status = test_case['expected_status']
    module = test_case.get('module', '默认模块')
    description = test_case.get('description', '')
    test_type = test_case.get('test_type', '单接口')
    priority = test_case.get('priority', 'P1')

    url = f"{BASE_URL}{path}"

    test_runner.attach(description, name="用例描述", attachment_type=allure.attachment_type.TEXT)

    response = send_request(method, url, headers=headers, params=params, body=body)

    with allure.step(f"验证状态码: 预期={expected_status}, 实际={response.status_code}"):
        assert response.status_code == expected_status, \
            f"用例[{case_id}]{case_name}失败: 期望状态码 {expected_status}, 实际 {response.status_code}"

@pytest.fixture
def test_runner(request):
    """Allure测试运行器"""
    class AllureTestRunner:
        def attach(self, body, name, attachment_type):
            allure.attach(body, name=name, attachment_type=attachment_type)

    return AllureTestRunner()
