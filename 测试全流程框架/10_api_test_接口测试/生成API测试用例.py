#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import csv
import json
import os
from datetime import datetime

def generate_api_test_cases(swagger_file):
    """根据swagger.yaml生成API测试用例"""
    with open(swagger_file, 'r', encoding='utf-8') as f:
        swagger_data = yaml.safe_load(f)
    
    cases = []
    case_id = 1
    
    for path, methods in swagger_data.get('paths', {}).items():
        for method, spec in methods.items():
            summary = spec.get('summary', '')
            description = spec.get('description', '')
            
            # 获取请求参数示例
            request_example = {}
            parameters = spec.get('parameters', [])
            for param in parameters:
                if param.get('in') == 'body' and 'schema' in param:
                    schema = param['schema']
                    if 'properties' in schema:
                        for prop_name, prop_def in schema['properties'].items():
                            if 'example' in prop_def:
                                request_example[prop_name] = prop_def['example']
                            else:
                                request_example[prop_name] = 'test'
            
            # 获取响应示例
            response_example = {}
            responses = spec.get('responses', {})
            if '200' in responses:
                resp_200 = responses['200']
                if 'examples' in resp_200:
                    response_example = resp_200['examples'].get('application/json', {})
                elif 'schema' in resp_200:
                    # 如果没有示例，从schema生成
                    schema = resp_200['schema']
                    if 'properties' in schema:
                        for prop_name, prop_def in schema['properties'].items():
                            if prop_def.get('type') == 'string':
                                response_example[prop_name] = 'string'
                            elif prop_def.get('type') == 'integer':
                                response_example[prop_name] = 0
            
            # 生成正向测试用例
            cases.append({
                'ID': case_id,
                '模块': summary or path,
                '用例名称': f'{summary}-正常请求成功',
                '优先级': 'P0',
                '接口名称': path,
                '前置条件': '无',
                '请求URL': f"{swagger_data.get('basePath', '')}{path}",
                '请求类型': method.upper(),
                '请求头': 'Content-Type: application/json',
                '请求参数类型': 'JSON',
                '请求参数': json.dumps(request_example, ensure_ascii=False),
                '预期响应状态码': 200,
                '预期返回数据': json.dumps(response_example, ensure_ascii=False) if response_example else '{}'
            })
            case_id += 1
            
            # 生成参数缺失测试用例
            if request_example:
                cases.append({
                    'ID': case_id,
                    '模块': summary or path,
                    '用例名称': f'{summary}-参数缺失',
                    '优先级': 'P1',
                    '接口名称': path,
                    '前置条件': '无',
                    '请求URL': f"{swagger_data.get('basePath', '')}{path}",
                    '请求类型': method.upper(),
                    '请求头': 'Content-Type: application/json',
                    '请求参数类型': 'JSON',
                    '请求参数': '{}',
                    '预期响应状态码': 400,
                    '预期返回数据': '{"error": "参数错误"}'
                })
                case_id += 1
            
            # 生成401未授权测试用例（登录接口除外）
            if path != '/users/login':
                cases.append({
                    'ID': case_id,
                    '模块': summary or path,
                    '用例名称': f'{summary}-未授权访问',
                    '优先级': 'P1',
                    '接口名称': path,
                    '前置条件': '未登录',
                    '请求URL': f"{swagger_data.get('basePath', '')}{path}",
                    '请求类型': method.upper(),
                    '请求头': 'Content-Type: application/json',
                    '请求参数类型': 'JSON',
                    '请求参数': json.dumps(request_example, ensure_ascii=False),
                    '预期响应状态码': 401,
                    '预期返回数据': '{"error": "未登录或会话已过期"}'
                })
                case_id += 1
    
    return cases

def write_csv_cases(cases, output_file):
    """写入CSV测试用例"""
    headers = ['ID', '模块', '用例名称', '优先级', '接口名称', '前置条件', 
               '请求URL', '请求类型', '请求头', '请求参数类型', '请求参数', 
               '预期响应状态码', '预期返回数据']
    
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(cases)

def write_json_cases(cases, output_file):
    """写入JSON测试用例"""
    json_cases = []
    for case in cases:
        json_cases.append({
            'name': case['用例名称'],
            'path': case['请求URL'],
            'method': case['请求类型'],
            'params': {},
            'body': json.loads(case['请求参数']) if case['请求参数'] else {},
            'expected_status': case['预期响应状态码'],
            'expected_response': json.loads(case['预期返回数据']) if case['预期返回数据'] else {},
            'test_type': '单接口',
            'priority': case['优先级'],
            'module': case['模块'],
            'case_name': case['用例名称'],
            'precondition': case['前置条件']
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_cases, f, ensure_ascii=False, indent=2)

def generate_test_script(cases, output_file):
    """生成Python测试脚本"""
    script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import requests
import json
import allure

# 基础URL
BASE_URL = "http://localhost:3000"

# 全局会话
session = requests.Session()

def get_token():
    """获取登录token"""
    try:
        response = session.post(f"{BASE_URL}/api/users/login", 
                               json={"username": "admin_zhangsan", "password": "Pass1234!"})
        if response.status_code == 200:
            data = response.json()
            return data.get("token", "")
    except Exception as e:
        print(f"获取token失败: {e}")
    return ""

@pytest.fixture(scope="session")
def auth_token():
    """登录并返回token"""
    token = get_token()
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})
    return token

'''
    
    for case in cases:
        case_name = case['用例名称'].replace('"', '\\"').replace("'", "\\'")
        case_docstring = f'''@allure.feature("{case['模块']}")
@allure.story("{case['用例名称']}")
def test_{case['ID']}_{case['用例名称'].replace(' ', '_').replace('-', '_')}(auth_token):
    """{case['用例名称']}"""
    url = f"{{BASE_URL}}{case['请求URL']}"
    method = "{case['请求类型']}"
    headers = {{"Content-Type": "application/json"}}
    
    try:
        body = {case['请求参数']}
    except:
        body = {{}}
    
    expected_status = {case['预期响应状态码']}
    
    with allure.step(f"请求: {{{{method}}}} {{{{url}}}}"):
        if method == "GET":
            response = session.get(url, params=body, headers=headers)
        elif method == "POST":
            response = session.post(url, json=body, headers=headers)
        elif method == "PUT":
            response = session.put(url, json=body, headers=headers)
        elif method == "DELETE":
            response = session.delete(url, json=body, headers=headers)
        else:
            pytest.skip(f"不支持的方法: {{{{method}}}}")
    
    with allure.step(f"验证状态码: {{{{expected_status}}}}"):
        assert response.status_code == expected_status, f"期望状态码 {{{{expected_status}}}}, 实际 {{{{response.status_code}}}}"
    
    if response.status_code == 200:
        with allure.step("验证响应数据"):
            try:
                resp_data = response.json()
                expected_data = {case['预期返回数据']}
                for key, value in expected_data.items():
                    assert key in resp_data, f"响应中缺少字段: {{{{key}}}}"
            except:
                pass

'''
        script += case_docstring
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script)

if __name__ == '__main__':
    swagger_file = '/Users/admin/Desktop/test-management-platform 2/测试全流程框架/10_api_test_接口测试/01_api_docs/swagger.yaml'
    
    # 生成测试用例
    cases = generate_api_test_cases(swagger_file)
    print(f"生成了 {len(cases)} 条测试用例")
    
    # 写入CSV
    today = datetime.now().strftime('%Y%m%d')
    csv_file = f'/Users/admin/Desktop/test-management-platform 2/测试全流程框架/10_api_test_接口测试/02_api_testcases/csv/{today}_CRM_API测试用例_v1.0.csv'
    write_csv_cases(cases, csv_file)
    print(f"CSV测试用例已保存: {csv_file}")
    
    # 写入JSON
    json_file = f'/Users/admin/Desktop/test-management-platform 2/测试全流程框架/10_api_test_接口测试/02_api_testcases/json/{today}_CRM_API测试用例_v1.0.json'
    write_json_cases(cases, json_file)
    print(f"JSON测试用例已保存: {json_file}")
    
    # 生成测试脚本
    test_script = '/Users/admin/Desktop/test-management-platform 2/测试全流程框架/10_api_test_接口测试/03_api_tests/test_crm_api.py'
    generate_test_script(cases, test_script)
    print(f"测试脚本已保存: {test_script}")