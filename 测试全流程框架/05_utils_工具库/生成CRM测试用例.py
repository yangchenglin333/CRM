# -*- coding: utf-8 -*-
import csv
import os

def generate_test_case_csv(output_path, test_cases_data):
    header = ['用例ID', '关联需求', '测试场景', '前置条件', '步骤描述', '输入', '期望输出', '优先级']
    rows = [header]

    for tc in test_cases_data:
        steps = tc.get('steps', [])
        if steps:
            step_descs = []
            inputs = []
            expected_outputs = []
            for i, step in enumerate(steps):
                step_descs.append(f'{i+1}.{step.get("step_desc", "")}')
                inp = step.get('input', '')
                if inp:
                    inputs.append(f'{i+1}.{inp}')
                out = step.get('expected_output', '')
                if out:
                    expected_outputs.append(f'{i+1}.{out}')

            rows.append([
                tc['test_case_id'],
                tc.get('related_req', ''),
                tc['name'],
                tc['precondition'],
                '\n'.join(step_descs),
                '\n'.join(inputs) if inputs else '',
                '\n'.join(expected_outputs),
                tc['priority']
            ])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)

    print(f'CSV文件已生成：{output_path}')
    print(f'总行数：{len(rows)}')
    return output_path

def create_login_test_cases():
    return [
        {
            'test_case_id': 'TC-001',
            'name': '登录-正常登录成功',
            'priority': 'P0',
            'precondition': '系统已启动；存在测试用户账号：admin（用户名4字符），密码：admin（6字符）',
            'related_req': 'R001,R002,R004',
            'steps': [
                {'step_desc': '在登录页面，输入正确的用户名和密码', 'input': '用户名：admin，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '登录成功，跳转到工作台页面'}
            ]
        },
        {
            'test_case_id': 'TC-002',
            'name': '登录-用户名为空',
            'priority': 'P0',
            'precondition': '系统已启动',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，用户名留空，输入任意密码', 'input': '用户名：（空），密码：anypassword', 'expected_output': '密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"用户名不能为空"，停留在登录页面'}
            ]
        },
        {
            'test_case_id': 'TC-003',
            'name': '登录-密码为空',
            'priority': 'P0',
            'precondition': '系统已启动；存在测试用户账号',
            'related_req': 'R002',
            'steps': [
                {'step_desc': '在登录页面，输入用户名，密码留空', 'input': '用户名：admin，密码：（空）', 'expected_output': '用户名输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"密码不能为空"，停留在登录页面'}
            ]
        },
        {
            'test_case_id': 'TC-004',
            'name': '登录-用户名3字符（边界值）',
            'priority': 'P1',
            'precondition': '系统已启动',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入3字符用户名', 'input': '用户名：abc，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"用户名长度需4-50字符"'}
            ]
        },
        {
            'test_case_id': 'TC-005',
            'name': '登录-用户名4字符（边界值）',
            'priority': 'P1',
            'precondition': '系统已启动；存在4字符用户名的测试账号',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入4字符用户名和正确密码', 'input': '用户名：test，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-006',
            'name': '登录-用户名50字符（边界值）',
            'priority': 'P1',
            'precondition': '系统已启动；存在50字符用户名的测试账号',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入50字符用户名和正确密码', 'input': '用户名：aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-007',
            'name': '登录-用户名51字符（边界值）',
            'priority': 'P1',
            'precondition': '系统已启动',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入51字符用户名', 'input': '用户名：aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"用户名长度需4-50字符"'}
            ]
        },
        {
            'test_case_id': 'TC-008',
            'name': '登录-用户名支持中文',
            'priority': 'P1',
            'precondition': '系统已启动；存在中文用户名的测试账号：张三',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入中文用户名和正确密码', 'input': '用户名：张三，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-009',
            'name': '登录-用户名支持英文',
            'priority': 'P1',
            'precondition': '系统已启动；存在英文用户名的测试账号：testuser',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入英文用户名和正确密码', 'input': '用户名：testuser，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-010',
            'name': '登录-用户名支持数字',
            'priority': 'P1',
            'precondition': '系统已启动；存在纯数字用户名的测试账号：user123',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入纯数字用户名和正确密码', 'input': '用户名：user123，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-011',
            'name': '登录-用户名支持下划线',
            'priority': 'P1',
            'precondition': '系统已启动；存在带下划线用户名的测试账号：user_name',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入带下划线的用户名和正确密码', 'input': '用户名：user_name，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-012',
            'name': '登录-用户名支持混合字符',
            'priority': 'P1',
            'precondition': '系统已启动；存在混合字符用户名的测试账号：张三_test_001',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入混合字符用户名和正确密码', 'input': '用户名：张三_test_001，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-013',
            'name': '登录-用户名不支持特殊字符',
            'priority': 'P1',
            'precondition': '系统已启动',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入包含特殊字符的用户名', 'input': '用户名：test@user#123，密码：admin', 'expected_output': '提示"用户名格式不正确，仅支持中文、英文、数字、下划线"'}
            ]
        },
        {
            'test_case_id': 'TC-014',
            'name': '登录-用户名不存在',
            'priority': 'P0',
            'precondition': '系统已启动',
            'related_req': 'R001',
            'steps': [
                {'step_desc': '在登录页面，输入不存在的用户名', 'input': '用户名：notexist，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"用户名或密码错误"，停留在登录页面'}
            ]
        },
        {
            'test_case_id': 'TC-015',
            'name': '登录-密码5字符（边界值）',
            'priority': 'P1',
            'precondition': '系统已启动',
            'related_req': 'R002',
            'steps': [
                {'step_desc': '在登录页面，输入任意用户名和5字符密码', 'input': '用户名：test，密码：12345', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"密码长度需6-32字符"'}
            ]
        },
        {
            'test_case_id': 'TC-016',
            'name': '登录-密码6字符（边界值）',
            'priority': 'P1',
            'precondition': '系统已启动；存在6字符密码的测试账号',
            'related_req': 'R002',
            'steps': [
                {'step_desc': '在登录页面，输入正确用户名和6字符密码', 'input': '用户名：admin，密码：123456', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-017',
            'name': '登录-密码32字符（边界值）',
            'priority': 'P1',
            'precondition': '系统已启动；存在32字符密码的测试账号',
            'related_req': 'R002',
            'steps': [
                {'step_desc': '在登录页面，输入正确用户名和32字符密码', 'input': '用户名：admin，密码：aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '正常进行登录验证'}
            ]
        },
        {
            'test_case_id': 'TC-018',
            'name': '登录-密码33字符（边界值）',
            'priority': 'P1',
            'precondition': '系统已启动',
            'related_req': 'R002',
            'steps': [
                {'step_desc': '在登录页面，输入任意用户名和33字符密码', 'input': '用户名：test，密码：aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"密码长度需6-32字符"'}
            ]
        },
        {
            'test_case_id': 'TC-019',
            'name': '登录-密码错误',
            'priority': 'P0',
            'precondition': '系统已启动；存在测试用户账号：admin',
            'related_req': 'R002',
            'steps': [
                {'step_desc': '在登录页面，输入正确用户名、错误密码', 'input': '用户名：admin，密码：wrongpwd', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"用户名或密码错误"，停留在登录页面'}
            ]
        },
        {
            'test_case_id': 'TC-020',
            'name': '登录-连续失败4次不锁定',
            'priority': 'P1',
            'precondition': '系统已启动；存在测试用户账号',
            'related_req': 'R003',
            'steps': [
                {'step_desc': '在登录页面，输入正确用户名、错误密码，点击"登录"（第1次）', 'input': '用户名：admin，密码：wrong1', 'expected_output': '提示"用户名或密码错误"'},
                {'step_desc': '输入正确用户名、错误密码，点击"登录"（第2次）', 'input': '用户名：admin，密码：wrong2', 'expected_output': '提示"用户名或密码错误"'},
                {'step_desc': '输入正确用户名、错误密码，点击"登录"（第3次）', 'input': '用户名：admin，密码：wrong3', 'expected_output': '提示"用户名或密码错误"'},
                {'step_desc': '输入正确用户名、错误密码，点击"登录"（第4次）', 'input': '用户名：admin，密码：wrong4', 'expected_output': '提示"用户名或密码错误"'},
                {'step_desc': '输入正确用户名和密码，点击"登录"', 'input': '用户名：admin，密码：admin', 'expected_output': '登录成功，跳转到工作台'}
            ]
        },
        {
            'test_case_id': 'TC-021',
            'name': '登录-连续失败5次锁定账号',
            'priority': 'P0',
            'precondition': '系统已启动；存在测试用户账号',
            'related_req': 'R003',
            'steps': [
                {'step_desc': '在登录页面，输入正确用户名、错误密码，点击"登录"（第1次）', 'input': '用户名：admin，密码：wrong1', 'expected_output': '提示"用户名或密码错误"'},
                {'step_desc': '输入正确用户名、错误密码，点击"登录"（第2次）', 'input': '用户名：admin，密码：wrong2', 'expected_output': '提示"用户名或密码错误"'},
                {'step_desc': '输入正确用户名、错误密码，点击"登录"（第3次）', 'input': '用户名：admin，密码：wrong3', 'expected_output': '提示"用户名或密码错误"'},
                {'step_desc': '输入正确用户名、错误密码，点击"登录"（第4次）', 'input': '用户名：admin，密码：wrong4', 'expected_output': '提示"用户名或密码错误"'},
                {'step_desc': '输入正确用户名、错误密码，点击"登录"（第5次）', 'input': '用户名：admin，密码：wrong5', 'expected_output': '提示"账号已锁定，请10分钟后再试"'}
            ]
        },
        {
            'test_case_id': 'TC-022',
            'name': '登录-锁定期间无法登录',
            'priority': 'P0',
            'precondition': '系统已启动；测试账号已被锁定',
            'related_req': 'R003',
            'steps': [
                {'step_desc': '在登录页面，输入已锁定账号的正确用户名和密码', 'input': '用户名：admin，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"账号已锁定，请10分钟后再试"，停留在登录页面'}
            ]
        },
        {
            'test_case_id': 'TC-023',
            'name': '登录-10分钟后自动解锁',
            'priority': 'P1',
            'precondition': '系统已启动；测试账号已被锁定超过10分钟',
            'related_req': 'R003',
            'steps': [
                {'step_desc': '在登录页面，输入已解锁账号的正确用户名和密码', 'input': '用户名：admin，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '登录成功，跳转到工作台'}
            ]
        },
        {
            'test_case_id': 'TC-024',
            'name': '登录-会话创建成功',
            'priority': 'P0',
            'precondition': '系统已启动；存在测试用户账号：admin，密码：admin',
            'related_req': 'R004',
            'steps': [
                {'step_desc': '在登录页面，输入正确的用户名和密码', 'input': '用户名：admin，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '登录成功，跳转到工作台，会话已创建'}
            ]
        },
        {
            'test_case_id': 'TC-025',
            'name': '登录-会话有效期内正常访问',
            'priority': 'P1',
            'precondition': '系统已启动；用户已登录且会话创建时间小于2小时',
            'related_req': 'R004',
            'steps': [
                {'step_desc': '用户已登录系统，等待1小时59分钟', 'input': '', 'expected_output': '系统保持登录状态'},
                {'step_desc': '点击任意菜单或刷新页面', 'input': '', 'expected_output': '页面正常加载，用户保持登录状态'}
            ]
        },
        {
            'test_case_id': 'TC-026',
            'name': '登录-会话超时自动退出',
            'priority': 'P0',
            'precondition': '系统已启动；用户已登录且会话创建时间超过2小时',
            'related_req': 'R004',
            'steps': [
                {'step_desc': '用户已登录系统，等待2小时1分钟', 'input': '', 'expected_output': '系统检测到会话超时'},
                {'step_desc': '点击任意菜单或刷新页面', 'input': '', 'expected_output': '自动跳转到登录页面，提示"会话已过期，请重新登录"'}
            ]
        },
        {
            'test_case_id': 'TC-027',
            'name': '登录-主动退出登录',
            'priority': 'P1',
            'precondition': '系统已启动；存在测试用户账号：admin，密码：admin',
            'related_req': 'R004',
            'steps': [
                {'step_desc': '在登录页面，输入用户名和密码，点击"登录"', 'input': '用户名：admin，密码：admin', 'expected_output': '登录成功，跳转到工作台'},
                {'step_desc': '点击页面右上角的"退出"按钮', 'input': '', 'expected_output': '弹出"确认退出"提示'},
                {'step_desc': '点击"确认"', 'input': '', 'expected_output': '退出成功，返回到登录页面，会话已销毁'}
            ]
        },
        {
            'test_case_id': 'TC-028',
            'name': '登录-SQL注入攻击测试',
            'priority': 'P2',
            'precondition': '系统已启动',
            'related_req': '',
            'steps': [
                {'step_desc': '在登录页面，输入包含SQL注入语句的用户名', 'input': '用户名：\' OR \'1\'=\'1，密码：anypassword', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"用户名或密码错误"，系统不被SQL注入'}
            ]
        },
        {
            'test_case_id': 'TC-029',
            'name': '登录-XSS攻击测试',
            'priority': 'P2',
            'precondition': '系统已启动',
            'related_req': '',
            'steps': [
                {'step_desc': '在登录页面，输入包含XSS脚本的用户名', 'input': '用户名：<script>alert(1)</script>，密码：anypassword', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮', 'input': '', 'expected_output': '提示"用户名或密码错误"，不执行XSS脚本'}
            ]
        },
        {
            'test_case_id': 'TC-030',
            'name': '登录-登录页面加载时间',
            'priority': 'P2',
            'precondition': '系统已启动',
            'related_req': '',
            'steps': [
                {'step_desc': '打开登录页面，记录加载时间', 'input': '', 'expected_output': '登录页面正常显示，加载时间≤2秒'}
            ]
        },
        {
            'test_case_id': 'TC-031',
            'name': '登录-登录操作响应时间',
            'priority': 'P2',
            'precondition': '系统已启动；存在测试用户账号：admin，密码：admin',
            'related_req': '',
            'steps': [
                {'step_desc': '在登录页面，输入正确的用户名和密码', 'input': '用户名：admin，密码：admin', 'expected_output': '用户名和密码输入成功'},
                {'step_desc': '点击"登录"按钮，记录响应时间', 'input': '', 'expected_output': '登录成功，响应时间≤2秒'}
            ]
        }
    ]

def create_workspace_test_cases():
    return [
        {
            'test_case_id': 'TC-032',
            'name': '工作台-数据卡片区展示',
            'priority': 'P1',
            'precondition': '用户已登录系统（admin/admin）',
            'related_req': '',
            'steps': [
                {'step_desc': '用户登录成功后进入工作台', 'input': '', 'expected_output': '工作台页面正常显示，包含关键业务数据概览卡片'}
            ]
        },
        {
            'test_case_id': 'TC-033',
            'name': '工作台-待跟进客户列表展示',
            'priority': 'P1',
            'precondition': '用户已登录系统，存在待跟进客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在工作台页面，查看待跟进客户列表', 'input': '', 'expected_output': '列表展示客户名称、下次跟进时间、负责人信息'}
            ]
        },
        {
            'test_case_id': 'TC-034',
            'name': '工作台-添加跟进记录入口',
            'priority': 'P0',
            'precondition': '用户已登录系统，存在待跟进客户',
            'related_req': '',
            'steps': [
                {'step_desc': '在工作台-待跟进客户列表中，点击「添加跟进」按钮', 'input': '', 'expected_output': '弹出"添加跟进记录"弹窗'}
            ]
        },
        {
            'test_case_id': 'TC-035',
            'name': '工作台-添加跟进-跟进方式选择',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出添加跟进记录弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在添加跟进记录弹窗中，点击跟进方式下拉框', 'input': '', 'expected_output': '下拉框展开，可选择：电话/拜访/微信/邮件/短信'},
                {'step_desc': '选择"电话"跟进方式', 'input': '跟进方式：电话', 'expected_output': '已选中"电话"'}
            ]
        },
        {
            'test_case_id': 'TC-036',
            'name': '工作台-添加跟进-跟进内容输入',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出添加跟进记录弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在跟进内容文本域中，输入跟进详情', 'input': '跟进内容：与客户沟通了项目需求，确认下周安排演示', 'expected_output': '跟进内容输入成功'},
                {'step_desc': '输入500字符（最大限制）', 'input': '跟进内容：aaa...（500字符）', 'expected_output': '输入成功，最多支持500字符'}
            ]
        },
        {
            'test_case_id': 'TC-037',
            'name': '工作台-添加跟进-下次跟进时间选择',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出添加跟进记录弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在下次跟进时间选择器中，选择未来日期', 'input': '下次跟进时间：2025-12-31', 'expected_output': '日期选择成功'}
            ]
        },
        {
            'test_case_id': 'TC-038',
            'name': '工作台-添加跟进-提交成功',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出添加跟进记录弹窗，填写完整信息',
            'related_req': '',
            'steps': [
                {'step_desc': '在弹窗中选择跟进方式为"电话"', 'input': '跟进方式：电话', 'expected_output': '已选中"电话"'},
                {'step_desc': '输入跟进内容', 'input': '跟进内容：与客户沟通了项目需求', 'expected_output': '跟进内容输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '弹窗关闭，跟进记录保存成功，下次跟进时间列更新'}
            ]
        },
        {
            'test_case_id': 'TC-039',
            'name': '工作台-待审批事项卡片展示',
            'priority': 'P1',
            'precondition': '用户已登录系统，存在待审批事项',
            'related_req': '',
            'steps': [
                {'step_desc': '在工作台页面，查看待审批事项卡片', 'input': '', 'expected_output': '每个审批项为独立卡片，包含审批类型、内容摘要、操作按钮'}
            ]
        },
        {
            'test_case_id': 'TC-040',
            'name': '工作台-待审批事项-审批通过',
            'priority': 'P0',
            'precondition': '用户已登录系统，存在待审批合同',
            'related_req': '',
            'steps': [
                {'step_desc': '在待审批事项卡片中，点击"同意"按钮', 'input': '', 'expected_output': '弹出确认提示'},
                {'step_desc': '点击确认', 'input': '', 'expected_output': '审批通过，事项从待审批列表中移除'}
            ]
        },
        {
            'test_case_id': 'TC-041',
            'name': '工作台-待审批事项-审批拒绝',
            'priority': 'P1',
            'precondition': '用户已登录系统，存在待审批合同',
            'related_req': '',
            'steps': [
                {'step_desc': '在待审批事项卡片中，点击"拒绝"按钮', 'input': '', 'expected_output': '弹出确认提示'},
                {'step_desc': '点击确认', 'input': '', 'expected_output': '审批拒绝，事项从待审批列表中移除'}
            ]
        },
        {
            'test_case_id': 'TC-042',
            'name': '工作台-无待跟进客户提示',
            'priority': 'P2',
            'precondition': '用户已登录系统，不存在待跟进客户',
            'related_req': '',
            'steps': [
                {'step_desc': '在工作台页面，查看待跟进客户列表区域', 'input': '', 'expected_output': '显示"暂无待跟进客户，去新增客户"提示'}
            ]
        },
        {
            'test_case_id': 'TC-043',
            'name': '工作台-无待审批事项提示',
            'priority': 'P2',
            'precondition': '用户已登录系统，不存在待审批事项',
            'related_req': '',
            'steps': [
                {'step_desc': '在工作台页面，查看待审批事项卡片区域', 'input': '', 'expected_output': '显示"暂无待审批事项"提示'}
            ]
        }
    ]

def create_customer_test_cases():
    return [
        {
            'test_case_id': 'TC-044',
            'name': '客户管理-列表页面展示',
            'priority': 'P1',
            'precondition': '用户已登录系统（admin/admin）',
            'related_req': '',
            'steps': [
                {'step_desc': '在顶部导航菜单中，点击"客户管理"模块', 'input': '', 'expected_output': '进入客户管理列表页面，展示客户列表及操作入口'}
            ]
        },
        {
            'test_case_id': 'TC-045',
            'name': '客户管理-工具栏按钮',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入客户管理列表页',
            'related_req': '',
            'steps': [
                {'step_desc': '在客户管理列表页面，查看工具栏', 'input': '', 'expected_output': '工具栏包含：新增客户按钮、导入按钮、导出按钮、筛选按钮'}
            ]
        },
        {
            'test_case_id': 'TC-046',
            'name': '客户管理-新增客户入口',
            'priority': 'P0',
            'precondition': '用户已登录系统，进入客户管理列表页',
            'related_req': '',
            'steps': [
                {'step_desc': '在工具栏中，点击「新增客户」按钮', 'input': '', 'expected_output': '弹出新增/编辑客户弹窗'}
            ]
        },
        {
            'test_case_id': 'TC-047',
            'name': '客户管理-新增客户-客户名称必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': 'R009',
            'steps': [
                {'step_desc': '在新增客户弹窗中，客户名称留空，填写其他必填字段', 'input': '客户名称：（空）', 'expected_output': '客户名称字段高亮提示"客户名称不能为空"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"客户名称不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-048',
            'name': '客户管理-新增客户-客户名称1字符（边界值）',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': 'R009',
            'steps': [
                {'step_desc': '在客户名称输入框中，输入1个字符', 'input': '客户名称：a', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"客户名称长度需2-100字符"'}
            ]
        },
        {
            'test_case_id': 'TC-049',
            'name': '客户管理-新增客户-客户名称2字符（边界值）',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': 'R009',
            'steps': [
                {'step_desc': '在客户名称输入框中，输入2个字符', 'input': '客户名称：张三', 'expected_output': '输入成功'},
                {'step_desc': '填写其他必填字段，点击"保存"按钮', 'input': '', 'expected_output': '保存成功'}
            ]
        },
        {
            'test_case_id': 'TC-050',
            'name': '客户管理-新增客户-客户名称100字符（边界值）',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': 'R009',
            'steps': [
                {'step_desc': '在客户名称输入框中，输入100个字符', 'input': '客户名称：aaa...（100字符）', 'expected_output': '输入成功'},
                {'step_desc': '填写其他必填字段，点击"保存"按钮', 'input': '', 'expected_output': '保存成功'}
            ]
        },
        {
            'test_case_id': 'TC-051',
            'name': '客户管理-新增客户-客户名称101字符（边界值）',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': 'R009',
            'steps': [
                {'step_desc': '在客户名称输入框中，输入101个字符', 'input': '客户名称：aaa...（101字符）', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"客户名称长度需2-100字符"'}
            ]
        },
        {
            'test_case_id': 'TC-052',
            'name': '客户管理-新增客户-联系电话格式验证',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': 'R010',
            'steps': [
                {'step_desc': '在联系电话输入框中，输入非11位手机号', 'input': '联系电话：12345', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"联系电话需为11位手机号格式"'}
            ]
        },
        {
            'test_case_id': 'TC-053',
            'name': '客户管理-新增客户-联系电话正确格式',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': 'R010',
            'steps': [
                {'step_desc': '在联系电话输入框中，输入11位手机号', 'input': '联系电话：17612345678', 'expected_output': '输入成功'},
                {'step_desc': '填写其他必填字段，点击"保存"按钮', 'input': '', 'expected_output': '保存成功'}
            ]
        },
        {
            'test_case_id': 'TC-054',
            'name': '客户管理-新增客户-客户标签多选',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': 'R011',
            'steps': [
                {'step_desc': '在客户标签下拉中，选择3个标签', 'input': '客户标签：意向客户、老客户、潜在客户', 'expected_output': '已选中3个标签'},
                {'step_desc': '再选择第4个标签', 'input': '客户标签：新增第4个标签', 'expected_output': '提示"最多只能选择3个标签"'}
            ]
        },
        {
            'test_case_id': 'TC-055',
            'name': '客户管理-新增客户-负责人必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在新增客户弹窗中，负责人下拉留空，填写其他必填字段', 'input': '负责人：（空）', 'expected_output': '负责人字段高亮提示"负责人不能为空"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"负责人不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-056',
            'name': '客户管理-新增客户-保存成功',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在弹窗中填写客户名称', 'input': '客户名称：测试客户A', 'expected_output': '输入成功'},
                {'step_desc': '选择行业', 'input': '行业：互联网', 'expected_output': '已选择"互联网"'},
                {'step_desc': '输入联系电话', 'input': '联系电话：17612345678', 'expected_output': '输入成功'},
                {'step_desc': '选择负责人', 'input': '负责人：管理员', 'expected_output': '已选择"管理员"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功，弹窗关闭，客户列表新增一条记录'}
            ]
        },
        {
            'test_case_id': 'TC-057',
            'name': '客户管理-新增客户-取消操作',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增客户弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在弹窗中填写部分信息', 'input': '客户名称：测试客户B', 'expected_output': '输入成功'},
                {'step_desc': '点击"取消"按钮', 'input': '', 'expected_output': '弹窗关闭，不保存数据'}
            ]
        },
        {
            'test_case_id': 'TC-058',
            'name': '客户管理-查看客户详情',
            'priority': 'P0',
            'precondition': '用户已登录系统，客户管理列表页存在客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在客户列表中，点击某客户的「查看」按钮', 'input': '', 'expected_output': '弹出客户详情弹窗，展示客户完整信息（基本信息、跟进记录摘要）'}
            ]
        },
        {
            'test_case_id': 'TC-059',
            'name': '客户管理-编辑客户信息',
            'priority': 'P0',
            'precondition': '用户已登录系统，客户管理列表页存在客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在客户列表中，点击某客户的「编辑」按钮', 'input': '', 'expected_output': '弹出编辑客户弹窗'},
                {'step_desc': '修改客户名称', 'input': '客户名称：修改后的客户名称', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功，弹窗关闭，客户列表中客户名称已更新'}
            ]
        },
        {
            'test_case_id': 'TC-060',
            'name': '客户管理-删除客户需二次确认',
            'priority': 'P0',
            'precondition': '用户已登录系统，客户管理列表页存在客户数据',
            'related_req': 'R008',
            'steps': [
                {'step_desc': '在客户列表中，点击某客户的「删除」按钮', 'input': '', 'expected_output': '弹出确认提示"确定要删除该客户吗？"'},
                {'step_desc': '点击"取消"', 'input': '', 'expected_output': '删除取消，客户数据保留'},
                {'step_desc': '再次点击「删除」按钮，点击"确认"', 'input': '', 'expected_output': '删除成功，客户从列表中移除'}
            ]
        },
        {
            'test_case_id': 'TC-061',
            'name': '客户管理-关键词搜索',
            'priority': 'P1',
            'precondition': '用户已登录系统，客户管理列表页存在多条客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在搜索框中，输入客户姓名关键词', 'input': '关键词：测试', 'expected_output': '搜索结果实时更新'},
                {'step_desc': '按回车或点击搜索按钮', 'input': '', 'expected_output': '列表显示匹配"测试"的客户记录'}
            ]
        },
        {
            'test_case_id': 'TC-062',
            'name': '客户管理-高级筛选-行业',
            'priority': 'P1',
            'precondition': '用户已登录系统，客户管理列表页存在多条客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"筛选"按钮，展开高级筛选', 'input': '', 'expected_output': '高级筛选区域展开'},
                {'step_desc': '在行业下拉中选择"互联网"', 'input': '行业：互联网', 'expected_output': '已选择"互联网"'},
                {'step_desc': '点击"应用"按钮', 'input': '', 'expected_output': '列表显示行业为"互联网"的客户记录'}
            ]
        },
        {
            'test_case_id': 'TC-063',
            'name': '客户管理-高级筛选-负责人',
            'priority': 'P1',
            'precondition': '用户已登录系统，客户管理列表页存在多条客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"筛选"按钮，展开高级筛选', 'input': '', 'expected_output': '高级筛选区域展开'},
                {'step_desc': '在负责人下拉中选择"管理员"', 'input': '负责人：管理员', 'expected_output': '已选择"管理员"'},
                {'step_desc': '点击"应用"按钮', 'input': '', 'expected_output': '列表显示负责人为"管理员"的客户记录'}
            ]
        },
        {
            'test_case_id': 'TC-064',
            'name': '客户管理-高级筛选-创建时间',
            'priority': 'P1',
            'precondition': '用户已登录系统，客户管理列表页存在多条客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"筛选"按钮，展开高级筛选', 'input': '', 'expected_output': '高级筛选区域展开'},
                {'step_desc': '在创建时间选择器中选择日期范围', 'input': '创建时间：2025-01-01 至 2025-12-31', 'expected_output': '日期范围选择成功'},
                {'step_desc': '点击"应用"按钮', 'input': '', 'expected_output': '列表显示创建时间在范围内的客户记录'}
            ]
        },
        {
            'test_case_id': 'TC-065',
            'name': '客户管理-联系方式脱敏显示',
            'priority': 'P0',
            'precondition': '用户已登录系统，客户管理列表页存在客户数据',
            'related_req': 'R005',
            'steps': [
                {'step_desc': '在客户列表中，查看客户联系电话列', 'input': '', 'expected_output': '联系电话显示为脱敏格式：如 176****3123'}
            ]
        },
        {
            'test_case_id': 'TC-066',
            'name': '客户管理-普通用户只能查看自己负责的客户',
            'priority': 'P0',
            'precondition': '系统存在普通用户（非管理员），该用户负责客户A，不负责客户B',
            'related_req': 'R006',
            'steps': [
                {'step_desc': '使用普通用户账号登录系统', 'input': '用户名：user1，密码：user123', 'expected_output': '登录成功'},
                {'step_desc': '进入客户管理模块', 'input': '', 'expected_output': '只能看到自己负责的客户A，看不到客户B'}
            ]
        },
        {
            'test_case_id': 'TC-067',
            'name': '客户管理-管理员可以查看所有客户',
            'priority': 'P0',
            'precondition': '系统存在管理员账号和多个客户数据',
            'related_req': 'R007',
            'steps': [
                {'step_desc': '使用管理员账号登录系统', 'input': '用户名：admin，密码：admin', 'expected_output': '登录成功'},
                {'step_desc': '进入客户管理模块', 'input': '', 'expected_output': '可以查看所有客户数据，包括其他负责人创建的客户'}
            ]
        }
    ]

def create_followup_test_cases():
    return [
        {
            'test_case_id': 'TC-068',
            'name': '跟进记录-列表页面展示',
            'priority': 'P1',
            'precondition': '用户已登录系统（admin/admin）',
            'related_req': '',
            'steps': [
                {'step_desc': '在顶部导航菜单中，点击"跟进记录"模块', 'input': '', 'expected_output': '进入跟进记录列表页面，展示跟进记录列表'}
            ]
        },
        {
            'test_case_id': 'TC-069',
            'name': '跟进记录-关键词搜索',
            'priority': 'P1',
            'precondition': '用户已登录系统，跟进记录列表页存在多条数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在搜索框中，输入客户姓名或跟进内容关键词', 'input': '关键词：项目需求', 'expected_output': '搜索结果实时更新'},
                {'step_desc': '按回车或点击搜索按钮', 'input': '', 'expected_output': '列表显示匹配的跟进记录'}
            ]
        },
        {
            'test_case_id': 'TC-070',
            'name': '跟进记录-新增跟进记录入口',
            'priority': 'P0',
            'precondition': '用户已登录系统，存在客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在跟进记录列表页面，点击「新增跟进」按钮', 'input': '', 'expected_output': '弹出新增跟进记录弹窗'}
            ]
        },
        {
            'test_case_id': 'TC-071',
            'name': '跟进记录-新增-关联客户必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在弹窗中，关联客户下拉留空', 'input': '关联客户：（空）', 'expected_output': '关联客户字段高亮提示"请选择关联客户"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"关联客户不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-072',
            'name': '跟进记录-新增-跟进方式必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在弹窗中选择关联客户', 'input': '关联客户：测试客户A', 'expected_output': '已选择"测试客户A"'},
                {'step_desc': '跟进方式下拉留空', 'input': '跟进方式：（空）', 'expected_output': '跟进方式字段高亮提示"请选择跟进方式"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"跟进方式不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-073',
            'name': '跟进记录-新增-跟进内容必填且长度校验',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': 'R013',
            'steps': [
                {'step_desc': '在弹窗中选择关联客户和跟进方式', 'input': '关联客户：测试客户A，跟进方式：电话', 'expected_output': '选择成功'},
                {'step_desc': '跟进内容输入框留空', 'input': '跟进内容：（空）', 'expected_output': '跟进内容字段高亮提示"跟进内容不能为空"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"跟进内容不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-074',
            'name': '跟进记录-新增-跟进内容9字符（边界值）',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': 'R013',
            'steps': [
                {'step_desc': '在弹窗中填写关联客户和跟进方式', 'input': '关联客户：测试客户A，跟进方式：电话', 'expected_output': '选择成功'},
                {'step_desc': '在跟进内容输入框中输入9个字符', 'input': '跟进内容：沟通需求', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"跟进内容长度需10-2000字符"'}
            ]
        },
        {
            'test_case_id': 'TC-075',
            'name': '跟进记录-新增-跟进内容10字符（边界值）',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': 'R013',
            'steps': [
                {'step_desc': '在弹窗中填写关联客户、跟进方式、跟进内容10字符', 'input': '跟进内容：与客户沟通了项目需求确认', 'expected_output': '输入成功'},
                {'step_desc': '填写跟进时间', 'input': '跟进时间：2025-06-20 10:00', 'expected_output': '时间选择成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功'}
            ]
        },
        {
            'test_case_id': 'TC-076',
            'name': '跟进记录-新增-跟进内容2000字符（边界值）',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': 'R013',
            'steps': [
                {'step_desc': '在弹窗中填写关联客户、跟进方式、跟进内容2000字符', 'input': '跟进内容：aaa...（2000字符）', 'expected_output': '输入成功'},
                {'step_desc': '填写跟进时间，点击"保存"按钮', 'input': '', 'expected_output': '保存成功'}
            ]
        },
        {
            'test_case_id': 'TC-077',
            'name': '跟进记录-新增-跟进内容2001字符（边界值）',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': 'R013',
            'steps': [
                {'step_desc': '在弹窗中填写关联客户、跟进方式', 'input': '', 'expected_output': '选择成功'},
                {'step_desc': '在跟进内容输入框中输入2001个字符', 'input': '跟进内容：aaa...（2001字符）', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"跟进内容长度需10-2000字符"'}
            ]
        },
        {
            'test_case_id': 'TC-078',
            'name': '跟进记录-新增-下次跟进时间不能早于当前时间',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': 'R014',
            'steps': [
                {'step_desc': '在弹窗中填写关联客户、跟进方式、跟进内容', 'input': '', 'expected_output': '填写成功'},
                {'step_desc': '在下下次跟进时间选择器中，选择过去的时间', 'input': '下次跟进时间：2020-01-01', 'expected_output': '日期选择成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"下次跟进时间不能早于当前时间"'}
            ]
        },
        {
            'test_case_id': 'TC-079',
            'name': '跟进记录-新增-保存成功',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在弹窗中选择关联客户', 'input': '关联客户：测试客户A', 'expected_output': '已选择"测试客户A"'},
                {'step_desc': '选择跟进方式', 'input': '跟进方式：电话', 'expected_output': '已选择"电话"'},
                {'step_desc': '输入跟进内容', 'input': '跟进内容：与客户沟通了项目需求，确认下周安排演示', 'expected_output': '输入成功'},
                {'step_desc': '选择跟进时间', 'input': '跟进时间：2025-06-20 10:00', 'expected_output': '时间选择成功'},
                {'step_desc': '选择下次跟进时间（可选）', 'input': '下次跟进时间：2025-06-25', 'expected_output': '日期选择成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功，弹窗关闭，跟进记录列表新增一条记录'}
            ]
        },
        {
            'test_case_id': 'TC-080',
            'name': '跟进记录-新增-取消操作',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增跟进记录弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在弹窗中填写部分信息', 'input': '跟进内容：这是测试内容', 'expected_output': '输入成功'},
                {'step_desc': '点击"取消"按钮', 'input': '', 'expected_output': '弹窗关闭，不保存数据'}
            ]
        },
        {
            'test_case_id': 'TC-081',
            'name': '跟进记录-编辑跟进记录',
            'priority': 'P0',
            'precondition': '用户已登录系统，跟进记录列表页存在跟进记录',
            'related_req': 'R012',
            'steps': [
                {'step_desc': '在跟进记录列表中，点击某记录的「编辑」按钮', 'input': '', 'expected_output': '弹出编辑跟进记录弹窗'},
                {'step_desc': '修改跟进内容', 'input': '跟进内容：修改后的跟进内容', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功，弹窗关闭，记录已更新'}
            ]
        },
        {
            'test_case_id': 'TC-082',
            'name': '跟进记录-删除后不可见（不可删除）',
            'priority': 'P0',
            'precondition': '用户已登录系统，跟进记录列表页存在跟进记录',
            'related_req': 'R012',
            'steps': [
                {'step_desc': '在跟进记录列表中，查看操作列', 'input': '', 'expected_output': '只有「编辑」按钮，没有「删除」按钮'},
                {'step_desc': '尝试右键删除或删除按钮', 'input': '', 'expected_output': '系统不支持删除跟进记录'}
            ]
        }
    ]

def create_business_opportunity_test_cases():
    return [
        {
            'test_case_id': 'TC-083',
            'name': '商机管理-列表页面展示',
            'priority': 'P1',
            'precondition': '用户已登录系统（admin/admin）',
            'related_req': '',
            'steps': [
                {'step_desc': '在顶部导航菜单中，点击"商机管理"模块', 'input': '', 'expected_output': '进入商机管理列表页面，展示商机列表及操作入口'}
            ]
        },
        {
            'test_case_id': 'TC-084',
            'name': '商机管理-工具栏按钮',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入商机管理列表页',
            'related_req': '',
            'steps': [
                {'step_desc': '在商机管理列表页面，查看工具栏', 'input': '', 'expected_output': '工具栏包含：新增商机按钮、导入按钮、导出按钮、筛选按钮'}
            ]
        },
        {
            'test_case_id': 'TC-085',
            'name': '商机管理-新增商机入口',
            'priority': 'P0',
            'precondition': '用户已登录系统，进入商机管理列表页',
            'related_req': '',
            'steps': [
                {'step_desc': '在工具栏中，点击「新增商机」按钮', 'input': '', 'expected_output': '弹出新增/编辑商机弹窗'}
            ]
        },
        {
            'test_case_id': 'TC-086',
            'name': '商机管理-新增商机-商机名称必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增商机弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在新增商机弹窗中，商机构名称留空，填写其他必填字段', 'input': '商机名称：（空）', 'expected_output': '商机名称字段高亮提示"商机名称不能为空"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"商机名称不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-087',
            'name': '商机管理-新增商机-关联客户必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增商机弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在新增商机弹窗中，关联客户下拉留空', 'input': '关联客户：（空）', 'expected_output': '关联客户字段高亮提示"请选择关联客户"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"关联客户不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-088',
            'name': '商机管理-新增商机-预估金额格式验证',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增商机弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在预估金额输入框中，输入非数字内容', 'input': '预估金额：abc', 'expected_output': '输入被拒绝或提示"请输入有效金额"'},
                {'step_desc': '在预估金额输入框中，输入负数', 'input': '预估金额：-1000', 'expected_output': '提示"预估金额不能为负数"'},
                {'step_desc': '在预估金额输入框中，输入正确金额', 'input': '预估金额：50000', 'expected_output': '输入成功'}
            ]
        },
        {
            'test_case_id': 'TC-089',
            'name': '商机管理-新增商机-商机阶段必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增商机弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在新增商机弹窗中，商机组阶段下拉留空', 'input': '商机阶段：（空）', 'expected_output': '商机阶段字段高亮提示"请选择商机阶段"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"商机阶段不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-090',
            'name': '商机管理-新增商机-预计成交日期格式验证',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增商机弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在预计成交日期选择器中，选择过去日期', 'input': '预计成交日期：2020-01-01', 'expected_output': '日期选择成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"预计成交日期不能早于当前日期"'}
            ]
        },
        {
            'test_case_id': 'TC-091',
            'name': '商机管理-新增商机-保存成功',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增商机弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '填写商机名称', 'input': '商机名称：测试商机A', 'expected_output': '输入成功'},
                {'step_desc': '选择关联客户', 'input': '关联客户：测试客户A', 'expected_output': '已选择"测试客户A"'},
                {'step_desc': '输入预估金额', 'input': '预估金额：100000', 'expected_output': '输入成功'},
                {'step_desc': '选择商机阶段', 'input': '商机阶段：需求调研', 'expected_output': '已选择"需求调研"'},
                {'step_desc': '选择预计成交日期', 'input': '预计成交日期：2025-12-31', 'expected_output': '日期选择成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功，弹窗关闭，商机组列表新增一条记录'}
            ]
        },
        {
            'test_case_id': 'TC-092',
            'name': '商机管理-编辑商机信息',
            'priority': 'P0',
            'precondition': '用户已登录系统，商机管理列表页存在商机数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在商机列表中，点击某商机的「编辑」按钮', 'input': '', 'expected_output': '弹出编辑商机弹窗'},
                {'step_desc': '修改预估金额', 'input': '预估金额：200000', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功，弹窗关闭，商机列表中预估金额已更新'}
            ]
        },
        {
            'test_case_id': 'TC-093',
            'name': '商机管理-商机阶段推进（只能向前）',
            'priority': 'P0',
            'precondition': '用户已登录系统，存在商机阶段为"需求调研"的商机',
            'related_req': '',
            'steps': [
                {'step_desc': '在商机列表中，点击某商机的「编辑」按钮', 'input': '', 'expected_output': '弹出编辑商机弹窗'},
                {'step_desc': '将商机阶段从"需求调研"修改为"方案制定"', 'input': '商机阶段：方案制定', 'expected_output': '已选择"方案制定"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功'}
            ]
        },
        {
            'test_case_id': 'TC-094',
            'name': '商机管理-商机阶段不能回退',
            'priority': 'P0',
            'precondition': '用户已登录系统，存在商机阶段为"方案制定"的商机',
            'related_req': '',
            'steps': [
                {'step_desc': '在商机列表中，点击某商机的「编辑」按钮', 'input': '', 'expected_output': '弹出编辑商机弹窗'},
                {'step_desc': '尝试将商机阶段从"方案制定"修改为"需求调研"（回退）', 'input': '商机阶段：需求调研', 'expected_output': '提示"商机阶段不能回退，只能向前推进"或阶段下拉禁用已选阶段之前的选项'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存失败或商机阶段保持为"方案制定"'}
            ]
        },
        {
            'test_case_id': 'TC-095',
            'name': '商机管理-删除商机需二次确认',
            'priority': 'P0',
            'precondition': '用户已登录系统，商机管理列表页存在商机数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在商机列表中，点击某商机的「删除」按钮', 'input': '', 'expected_output': '弹出确认提示"确定要删除该商机吗？"'},
                {'step_desc': '点击"取消"', 'input': '', 'expected_output': '删除取消，商机数据保留'},
                {'step_desc': '再次点击「删除」按钮，点击"确认"', 'input': '', 'expected_output': '删除成功，商机从列表中移除'}
            ]
        },
        {
            'test_case_id': 'TC-096',
            'name': '商机管理-商机转化率统计展示',
            'priority': 'P1',
            'precondition': '用户已登录系统，存在多个不同阶段的商机',
            'related_req': '',
            'steps': [
                {'step_desc': '在商机管理页面，查看商机转化率统计区域', 'input': '', 'expected_output': '展示各阶段商机数量及转化率漏斗图'}
            ]
        },
        {
            'test_case_id': 'TC-097',
            'name': '商机管理-关键词搜索',
            'priority': 'P1',
            'precondition': '用户已登录系统，商机管理列表页存在多条商机数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在搜索框中，输入商机名称关键词', 'input': '关键词：测试', 'expected_output': '搜索结果实时更新'},
                {'step_desc': '按回车或点击搜索按钮', 'input': '', 'expected_output': '列表显示匹配"测试"的商机记录'}
            ]
        },
        {
            'test_case_id': 'TC-098',
            'name': '商机管理-高级筛选-商机阶段',
            'priority': 'P1',
            'precondition': '用户已登录系统，商机管理列表页存在多条商机数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"筛选"按钮，展开高级筛选', 'input': '', 'expected_output': '高级筛选区域展开'},
                {'step_desc': '在商机阶段下拉中选择"需求调研"', 'input': '商机阶段：需求调研', 'expected_output': '已选择"需求调研"'},
                {'step_desc': '点击"应用"按钮', 'input': '', 'expected_output': '列表显示商机阶段为"需求调研"的商机记录'}
            ]
        }
    ]

def create_contract_test_cases():
    return [
        {
            'test_case_id': 'TC-099',
            'name': '合同管理-列表页面展示',
            'priority': 'P1',
            'precondition': '用户已登录系统（admin/admin）',
            'related_req': '',
            'steps': [
                {'step_desc': '在顶部导航菜单中，点击"合同管理"模块', 'input': '', 'expected_output': '进入合同管理列表页面，展示合同列表及操作入口'}
            ]
        },
        {
            'test_case_id': 'TC-100',
            'name': '合同管理-工具栏按钮',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入合同管理列表页',
            'related_req': '',
            'steps': [
                {'step_desc': '在合同管理列表页面，查看工具栏', 'input': '', 'expected_output': '工具栏包含：新增合同按钮、导入按钮、导出按钮、筛选按钮'}
            ]
        },
        {
            'test_case_id': 'TC-101',
            'name': '合同管理-新增合同入口',
            'priority': 'P0',
            'precondition': '用户已登录系统，进入合同管理列表页',
            'related_req': '',
            'steps': [
                {'step_desc': '在工具栏中，点击「新增合同」按钮', 'input': '', 'expected_output': '弹出新增/编辑合同弹窗'}
            ]
        },
        {
            'test_case_id': 'TC-102',
            'name': '合同管理-新增合同-合同名称必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增合同弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在新增合同弹窗中，合同名称留空，填写其他必填字段', 'input': '合同名称：（空）', 'expected_output': '合同名称字段高亮提示"合同名称不能为空"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"合同名称不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-103',
            'name': '合同管理-新增合同-关联商机必填',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增合同弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在新增合同弹窗中，关联商机下拉留空', 'input': '关联商机：（空）', 'expected_output': '关联商机字段高亮提示"请选择关联商机"'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '提示"关联商机不能为空"，保存失败'}
            ]
        },
        {
            'test_case_id': 'TC-104',
            'name': '合同管理-新增合同-合同金额格式验证',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增合同弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在合同金额输入框中，输入非数字内容', 'input': '合同金额：abc', 'expected_output': '输入被拒绝或提示"请输入有效金额"'},
                {'step_desc': '在合同金额输入框中，输入负数', 'input': '合同金额：-50000', 'expected_output': '提示"合同金额不能为负数"'},
                {'step_desc': '在合同金额输入框中，输入正确金额', 'input': '合同金额：100000', 'expected_output': '输入成功'}
            ]
        },
        {
            'test_case_id': 'TC-105',
            'name': '合同管理-新增合同-合同期限验证',
            'priority': 'P1',
            'precondition': '用户已登录系统，弹出新增合同弹窗',
            'related_req': '',
            'steps': [
                {'step_desc': '在合同期限选择器中，选择结束日期早于开始日期', 'input': '开始日期：2025-12-31，结束日期：2025-01-01', 'expected_output': '提示"结束日期不能早于开始日期"'}
            ]
        },
        {
            'test_case_id': 'TC-106',
            'name': '合同管理-新增合同-保存成功',
            'priority': 'P0',
            'precondition': '用户已登录系统，弹出新增合同弹窗，存在已成交商机',
            'related_req': '',
            'steps': [
                {'step_desc': '填写合同名称', 'input': '合同名称：测试合同A', 'expected_output': '输入成功'},
                {'step_desc': '选择关联商机', 'input': '关联商机：测试商机A', 'expected_output': '已选择"测试商机A"（该商机已成交）'},
                {'step_desc': '输入合同金额', 'input': '合同金额：150000', 'expected_output': '输入成功'},
                {'step_desc': '选择合同开始日期', 'input': '开始日期：2025-06-01', 'expected_output': '日期选择成功'},
                {'step_desc': '选择合同结束日期', 'input': '结束日期：2026-05-31', 'expected_output': '日期选择成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功，弹窗关闭，合同列表新增一条记录'}
            ]
        },
        {
            'test_case_id': 'TC-107',
            'name': '合同管理-编辑合同信息',
            'priority': 'P0',
            'precondition': '用户已登录系统，合同管理列表页存在合同数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在合同列表中，点击某合同的「编辑」按钮', 'input': '', 'expected_output': '弹出编辑合同弹窗'},
                {'step_desc': '修改合同金额', 'input': '合同金额：200000', 'expected_output': '输入成功'},
                {'step_desc': '点击"保存"按钮', 'input': '', 'expected_output': '保存成功，弹窗关闭，合同列表中合同金额已更新'}
            ]
        },
        {
            'test_case_id': 'TC-108',
            'name': '合同管理-删除合同需二次确认',
            'priority': 'P0',
            'precondition': '用户已登录系统，合同管理列表页存在合同数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在合同列表中，点击某合同的「删除」按钮', 'input': '', 'expected_output': '弹出确认提示"确定要删除该合同吗？"'},
                {'step_desc': '点击"取消"', 'input': '', 'expected_output': '删除取消，合同数据保留'},
                {'step_desc': '再次点击「删除」按钮，点击"确认"', 'input': '', 'expected_output': '删除成功，合同从列表中移除'}
            ]
        },
        {
            'test_case_id': 'TC-109',
            'name': '合同管理-关键词搜索',
            'priority': 'P1',
            'precondition': '用户已登录系统，合同管理列表页存在多条合同数据',
            'related_req': '',
            'steps': [
                {'step_desc': '在搜索框中，输入合同名称关键词', 'input': '关键词：测试', 'expected_output': '搜索结果实时更新'},
                {'step_desc': '按回车或点击搜索按钮', 'input': '', 'expected_output': '列表显示匹配"测试"的合同记录'}
            ]
        },
        {
            'test_case_id': 'TC-110',
            'name': '合同管理-高级筛选-合同状态',
            'priority': 'P1',
            'precondition': '用户已登录系统，合同管理列表页存在多条合同数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"筛选"按钮，展开高级筛选', 'input': '', 'expected_output': '高级筛选区域展开'},
                {'step_desc': '在合同状态下拉中选择"执行中"', 'input': '合同状态：执行中', 'expected_output': '已选择"执行中"'},
                {'step_desc': '点击"应用"按钮', 'input': '', 'expected_output': '列表显示合同状态为"执行中"的合同记录'}
            ]
        },
        {
            'test_case_id': 'TC-111',
            'name': '合同管理-商机成交后自动创建合同',
            'priority': 'P0',
            'precondition': '用户已登录系统，存在商机阶段为"合同签订"的商机',
            'related_req': '',
            'steps': [
                {'step_desc': '将某商机的阶段推进至"合同签订"', 'input': '商机阶段：合同签订', 'expected_output': '阶段推进成功'},
                {'step_desc': '系统自动弹出"创建合同"提示或自动跳转到合同创建页面', 'input': '', 'expected_output': '关联商机字段自动填充为该商机'}
            ]
        }
    ]

def create_report_test_cases():
    return [
        {
            'test_case_id': 'TC-112',
            'name': '报表中心-列表页面展示',
            'priority': 'P1',
            'precondition': '用户已登录系统（admin/admin）',
            'related_req': '',
            'steps': [
                {'step_desc': '在顶部导航菜单中，点击"报表中心"模块', 'input': '', 'expected_output': '进入报表中心列表页面，展示报表类型及入口'}
            ]
        },
        {
            'test_case_id': 'TC-113',
            'name': '报表中心-报表类型展示',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入报表中心',
            'related_req': '',
            'steps': [
                {'step_desc': '在报表中心页面，查看报表类型列表', 'input': '', 'expected_output': '展示客户分析、商机分析、合同分析、销售漏斗等报表类型'}
            ]
        },
        {
            'test_case_id': 'TC-114',
            'name': '报表中心-客户分析报表',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入报表中心，存在客户数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"客户分析"报表类型', 'input': '', 'expected_output': '进入客户分析详情页，展示客户数量、来源分布、等级分布等图表'}
            ]
        },
        {
            'test_case_id': 'TC-115',
            'name': '报表中心-客户分析-时间范围筛选',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入客户分析报表',
            'related_req': '',
            'steps': [
                {'step_desc': '在时间范围选择器中选择日期范围', 'input': '时间范围：2025-01-01 至 2025-06-30', 'expected_output': '日期范围选择成功'},
                {'step_desc': '点击"查询"按钮', 'input': '', 'expected_output': '报表数据按所选时间范围重新计算展示'}
            ]
        },
        {
            'test_case_id': 'TC-116',
            'name': '报表中心-商机分析报表',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入报表中心，存在商机数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"商机分析"报表类型', 'input': '', 'expected_output': '进入商机分析详情页，展示商机数量、阶段分布、转化率等图表'}
            ]
        },
        {
            'test_case_id': 'TC-117',
            'name': '报表中心-商机分析-转化率漏斗',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入商机分析报表，存在多阶段商机',
            'related_req': '',
            'steps': [
                {'step_desc': '在商机分析页面，查看转化率漏斗图', 'input': '', 'expected_output': '展示从初步接触到最终成交各阶段的转化率'}
            ]
        },
        {
            'test_case_id': 'TC-118',
            'name': '报表中心-合同分析报表',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入报表中心，存在合同数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"合同分析"报表类型', 'input': '', 'expected_output': '进入合同分析详情页，展示合同数量、金额、状态分布等图表'}
            ]
        },
        {
            'test_case_id': 'TC-119',
            'name': '报表中心-合同分析-金额统计',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入合同分析报表',
            'related_req': '',
            'steps': [
                {'step_desc': '在合同分析页面，查看合同金额统计', 'input': '', 'expected_output': '展示合同总金额、当月合同金额、当季合同金额等数据'}
            ]
        },
        {
            'test_case_id': 'TC-120',
            'name': '报表中心-销售漏斗报表',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入报表中心，存在销售数据',
            'related_req': '',
            'steps': [
                {'step_desc': '点击"销售漏斗"报表类型', 'input': '', 'expected_output': '进入销售漏斗详情页，展示从线索到成交的完整漏斗图'}
            ]
        },
        {
            'test_case_id': 'TC-121',
            'name': '报表中心-销售漏斗-各阶段数据',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入销售漏斗报表',
            'related_req': '',
            'steps': [
                {'step_desc': '在销售漏斗页面，查看各阶段数据', 'input': '', 'expected_output': '展示各阶段客户数量、金额、转化率数据'}
            ]
        },
        {
            'test_case_id': 'TC-122',
            'name': '报表中心-导出报表',
            'priority': 'P1',
            'precondition': '用户已登录系统，进入某报表详情页',
            'related_req': '',
            'steps': [
                {'step_desc': '在报表详情页，点击「导出」按钮', 'input': '', 'expected_output': '弹出导出设置（如导出格式、范围等）'},
                {'step_desc': '选择导出格式为Excel，点击"导出"', 'input': '导出格式：Excel', 'expected_output': '导出成功，下载Excel文件'}
            ]
        },
        {
            'test_case_id': 'TC-123',
            'name': '报表中心-无数据提示',
            'priority': 'P2',
            'precondition': '用户已登录系统，进入报表中心，不存在相关数据',
            'related_req': '',
            'steps': [
                {'step_desc': '进入某报表详情页', 'input': '', 'expected_output': '显示"暂无数据"提示'}
            ]
        },
        {
            'test_case_id': 'TC-124',
            'name': '报表中心-普通用户权限验证',
            'priority': 'P0',
            'precondition': '系统存在普通用户（非管理员）',
            'related_req': '',
            'steps': [
                {'step_desc': '使用普通用户账号登录系统', 'input': '用户名：user1，密码：user123', 'expected_output': '登录成功'},
                {'step_desc': '尝试进入报表中心', 'input': '', 'expected_output': '根据权限设置，或可查看报表或提示"无权限访问"'}
            ]
        }
    ]

if __name__ == '__main__':
    output_file = '/Users/admin/Desktop/test-management-platform 2/测试全流程框架/07_testcases_测试用例/csv_表格用/20260502_CRM系统完整测试用例.csv'
    all_test_cases = []
    all_test_cases.extend(create_login_test_cases())
    all_test_cases.extend(create_workspace_test_cases())
    all_test_cases.extend(create_customer_test_cases())
    all_test_cases.extend(create_followup_test_cases())
    all_test_cases.extend(create_business_opportunity_test_cases())
    all_test_cases.extend(create_contract_test_cases())
    all_test_cases.extend(create_report_test_cases())
    generate_test_case_csv(output_file, all_test_cases)
    print(f'测试用例已生成：{output_file}')
    print(f'共生成 {len(all_test_cases)} 条测试用例')