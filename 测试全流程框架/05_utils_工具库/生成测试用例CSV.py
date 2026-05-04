# -*- coding: utf-8 -*-
"""
测试用例CSV文件生成工具
使用Python的csv模块确保引号正确转义，避免列错位问题

使用方法：
1. 直接调用函数：
   from 生成测试用例CSV import generate_test_case_csv
   generate_test_case_csv('testcases/CSV/文件名.csv', test_cases_data)

2. 修改此脚本中的create_test_case_data()函数，添加测试用例数据，然后运行：
   python 生成测试用例CSV.py

3. 命令行调用（指定输出文件）：
   python 生成测试用例CSV.py testcases/CSV/文件名.csv
"""
import atexit
import csv
import os
import sys
from datetime import datetime

# 脚本结束时自动清理 __pycache__
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
if os.path.join(_root, "其他", "系统维护") not in sys.path:
    sys.path.insert(0, os.path.join(_root, "其他", "系统维护"))
try:
    from 清理缓存 import clean_pycache
    atexit.register(lambda: clean_pycache(verbose=False))
except ImportError:
    pass


def generate_test_case_csv(output_path, test_cases_data):
    """
    生成测试用例CSV文件
    
    参数:
        output_path: 输出文件路径
        test_cases_data: 测试用例数据列表，格式为：
        [
            {
                'test_case_id': 'TC-001',
                'precondition': '前置条件',
                'name': '测试场景名称',
                'owner': 'yangcl5',  # 用例责任人
                'steps': [
                    {
                        'step_name': '步骤1',
                        'step_desc': '步骤描述',
                        'input': '输入数据',
                        'expected_output': '期望输出'
                    },
                    ...
                ]
            },
            ...
        ]
    """
    # CSV表头（14列：1-12业务列+M/N列，O列已删除）
    header = [
        '用例责任人',
        '计划完成时间',
        '用例关键字',
        '用例标识',
        '前置条件',
        '名称',
        '关联业务',
        '步骤名称',
        '步骤描述',
        '输入',
        '期望输出',
        '备注',
        '5cee1b5ae0ee7741889a51f8',
        '5c403daae0ee7730f883fcac',
    ]
    
    # 准备数据行
    rows = [header]
    
    for test_case in test_cases_data:
        # 全面版支持：用例标识优先用 priority（重要/正常），否则用 test_case_id
        test_case_id = test_case.get('test_case_id', '')
        priority = test_case.get('priority', '')
        case_identifier = priority if priority else test_case_id
        keyword = test_case.get('keyword', '')  # 用例关键字，如 功能正确性
        business = test_case.get('business', '')  # 关联业务，如 GAC_US_6805
        precondition = test_case.get('precondition', '')
        name = test_case.get('name', '')
        owner = test_case.get('owner', 'yangcl5')
        steps = test_case.get('steps', [])
        section_only = test_case.get('section_only', False)  # 仅分组行：只输出名称列
        if section_only or (not steps and name):
            rows.append([
                '', '', '', '', '', name, '', '', '', '', '', '', '', ''
            ])
            continue
        # 第一条数据：包含前置条件和名称
        if steps:
            first_step = steps[0]
            rows.append([
                owner,  # 用例责任人
                '',  # 计划完成时间
                keyword,  # 用例关键字
                case_identifier,  # 用例标识（全面版为重要/正常）
                precondition,  # 前置条件
                name,  # 名称
                business,  # 关联业务
                first_step.get('step_name', ''),  # 步骤名称
                first_step.get('step_desc', ''),  # 步骤描述
                first_step.get('input', ''),  # 输入
                first_step.get('expected_output', ''),  # 期望输出
                '',  # 备注
                '',  # 5cee1b5ae0ee7741889a51f8（留空显示）
                '',  # 5c403daae0ee7730f883fcac（留空显示）
            ])
            # 其他步骤：前置条件和名称为空
            for step in steps[1:]:
                rows.append([
                    '',  # 用例责任人（空）
                    '',  # 计划完成时间
                    '',  # 用例关键字（后续步骤留空）
                    case_identifier,  # 用例标识
                    '',  # 前置条件（空）
                    '',  # 名称（空）
                    '',  # 关联业务（后续步骤留空）
                    step.get('step_name', ''),  # 步骤名称
                    step.get('step_desc', ''),  # 步骤描述
                    step.get('input', ''),  # 输入
                    step.get('expected_output', ''),  # 期望输出
                    '',  # 备注
                    '',  # 5cee1b5ae0ee7741889a51f8（留空显示）
                    '',  # 5c403daae0ee7730f883fcac（留空显示）
                ])
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 使用csv模块写入文件，确保引号正确转义
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)
    
    print(f'CSV文件已生成: {output_path}')
    print(f'总行数: {len(rows)} (包含表头)')
    print(f'数据行数: {len(rows) - 1}')
    
    # 验证文件格式
    verify_csv_format(output_path)
    
    return output_path


def verify_csv_format(file_path):
    """
    验证CSV文件格式是否正确
    """
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if not rows:
            print('[错误] 文件为空')
            return False
        
        expected_columns = 14  # 14列：1-12业务列+M/N列，O列已删除
        header = rows[0]
        
        if len(header) != expected_columns:
            print(f'[错误] 表头列数错误: {len(header)} (期望{expected_columns})')
            return False
        
        errors = []
        for i, row in enumerate(rows[1:], start=2):
            if len(row) != expected_columns:
                errors.append((i, len(row)))
        
        if errors:
            print(f'[错误] 发现 {len(errors)} 行列数不正确:')
            for line_num, col_count in errors[:5]:  # 只显示前5个错误
                print(f'  第{line_num}行: {col_count}列 (期望{expected_columns}列)')
            return False
        else:
            print(f'[成功] 所有行都是{expected_columns}列，格式正确')
            return True
            
    except Exception as e:
        print(f'[错误] 验证过程中出错: {e}')
        return False


def create_test_case_data():
    """
    创建测试用例数据
    此函数可以根据需求文档生成测试用例数据
    返回格式：test_cases_data列表
    """
    # 组织调整税务审批测试用例数据
    # 注意：由于用例数量较多，这里先包含前10个测试用例
    # 完整的测试用例数据需要根据需求文档继续补充（预计95个左右）
    test_cases = [
        {
            'test_case_id': 'TC-001',
            'precondition': '已登录系统；用户角色：HRBP；系统存在组织调整申请单；申请单中组织的职能标签原来没有"BU级研发"，现在有"BU级研发"',
            'name': '验证职能标签原来没有现在有BU级研发时触发税务审批',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整模块，创建一个新的组织调整申请单', 'input': '', 'expected_output': '成功进入组织调整模块，新建申请单页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '选择一个组织，该组织的职能标签原来没有"BU级研发"', 'input': '', 'expected_output': '组织选择成功，组织信息正常显示，职能标签中不包含"BU级研发"'},
                {'step_name': '步骤4', 'step_desc': '修改该组织的职能标签，添加"BU级研发"标签', 'input': 'BU级研发', 'expected_output': '职能标签修改成功，"BU级研发"标签已添加'},
                {'step_name': '步骤5', 'step_desc': '提交组织调整申请单', 'input': '', 'expected_output': '申请单提交成功，进入审批流程'},
                {'step_name': '步骤6', 'step_desc': '查看审批流程节点', 'input': '', 'expected_output': '审批流程正常显示，包含税务部专员审批节点'}
            ]
        },
        {
            'test_case_id': 'TC-002',
            'precondition': '已登录系统；用户角色：HRBP；系统存在组织调整申请单；申请单中组织的职能标签原来有"BU级研发"，现在没有"BU级研发"',
            'name': '验证职能标签原来有现在没有BU级研发时触发税务审批',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整模块，创建一个新的组织调整申请单', 'input': '', 'expected_output': '成功进入组织调整模块，新建申请单页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '选择一个组织，该组织的职能标签原来有"BU级研发"', 'input': '', 'expected_output': '组织选择成功，组织信息正常显示，职能标签中包含"BU级研发"'},
                {'step_name': '步骤4', 'step_desc': '修改该组织的职能标签，移除"BU级研发"标签', 'input': '', 'expected_output': '职能标签修改成功，"BU级研发"标签已移除'},
                {'step_name': '步骤5', 'step_desc': '提交组织调整申请单', 'input': '', 'expected_output': '申请单提交成功，进入审批流程'},
                {'step_name': '步骤6', 'step_desc': '查看审批流程节点', 'input': '', 'expected_output': '审批流程正常显示，包含税务部专员审批节点'}
            ]
        },
        {
            'test_case_id': 'TC-003',
            'precondition': '已登录系统；用户角色：HRBP；系统存在组织调整申请单；申请单中组织的职能标签原来有"BU级研发"，现在也有"BU级研发"',
            'name': '验证职能标签原来有现在也有BU级研发时触发税务审批',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整模块，创建一个新的组织调整申请单', 'input': '', 'expected_output': '成功进入组织调整模块，新建申请单页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '选择一个组织，该组织的职能标签原来有"BU级研发"', 'input': '', 'expected_output': '组织选择成功，组织信息正常显示，职能标签中包含"BU级研发"'},
                {'step_name': '步骤4', 'step_desc': '修改该组织的其他信息（如组织名称），但保持"BU级研发"标签不变', 'input': '新组织名称', 'expected_output': '组织信息修改成功，"BU级研发"标签仍然存在'},
                {'step_name': '步骤5', 'step_desc': '提交组织调整申请单', 'input': '', 'expected_output': '申请单提交成功，进入审批流程'},
                {'step_name': '步骤6', 'step_desc': '查看审批流程节点', 'input': '', 'expected_output': '审批流程正常显示，包含税务部专员审批节点'}
            ]
        },
        {
            'test_case_id': 'TC-004',
            'precondition': '已登录系统；用户角色：HRBP；系统存在组织调整申请单；申请单中组织的职能标签变更，但不涉及"BU级研发"标签',
            'name': '验证职能标签变更但不涉及BU级研发时不触发税务审批',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整模块，创建一个新的组织调整申请单', 'input': '', 'expected_output': '成功进入组织调整模块，新建申请单页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '选择一个组织，修改该组织的职能标签（如添加"职能&其他"标签），但不涉及"BU级研发"标签', 'input': '职能&其他', 'expected_output': '职能标签修改成功，新标签已添加'},
                {'step_name': '步骤4', 'step_desc': '提交组织调整申请单', 'input': '', 'expected_output': '申请单提交成功，进入审批流程'},
                {'step_name': '步骤5', 'step_desc': '查看审批流程节点', 'input': '', 'expected_output': '审批流程正常显示，不包含税务部专员审批节点'}
            ]
        },
        {
            'test_case_id': 'TC-005',
            'precondition': '已登录系统；用户角色：HRBP；系统存在外包组织调整申请单',
            'name': '验证外包组织调整申请单不触发税务审批',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整模块，创建一个外包组织调整申请单', 'input': '', 'expected_output': '成功进入组织调整模块，新建申请单页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '选择外包组织，修改职能标签为包含"BU级研发"', 'input': 'BU级研发', 'expected_output': '职能标签修改成功，"BU级研发"标签已添加'},
                {'step_name': '步骤4', 'step_desc': '提交外包组织调整申请单', 'input': '', 'expected_output': '申请单提交成功，进入审批流程'},
                {'step_name': '步骤5', 'step_desc': '查看审批流程节点', 'input': '', 'expected_output': '审批流程正常显示，不包含税务部专员审批节点'}
            ]
        },
        {
            'test_case_id': 'TC-006',
            'precondition': '已登录系统；用户角色：HRBP；系统存在成本中心调整申请单',
            'name': '验证成本中心调整申请单不触发税务审批',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整模块，创建一个成本中心调整申请单', 'input': '', 'expected_output': '成功进入组织调整模块，新建申请单页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '选择成本中心，进行相关调整', 'input': '', 'expected_output': '成本中心调整信息设置成功'},
                {'step_name': '步骤4', 'step_desc': '提交成本中心调整申请单', 'input': '', 'expected_output': '申请单提交成功，进入审批流程'},
                {'step_name': '步骤5', 'step_desc': '查看审批流程节点', 'input': '', 'expected_output': '审批流程正常显示，不包含税务部专员审批节点'}
            ]
        },
        {
            'test_case_id': 'TC-007',
            'precondition': '已登录系统；用户角色：税务部专员；系统存在一级组织调整申请单，已触发税务审批；审批流程已流转到税务部专员节点',
            'name': '验证一级组织调整申请单中税务部专员审批节点位置',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整申请单详情页面', 'input': '', 'expected_output': '成功进入申请单详情页面，页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '查看审批流程节点', 'input': '', 'expected_output': '审批流程正常显示，包含所有审批节点'},
                {'step_name': '步骤4', 'step_desc': '查看税务部专员审批节点在审批流程中的位置', 'input': '', 'expected_output': '税务部专员审批节点位于预算部负责人审批之后、HRBP Head审批之前'}
            ]
        },
        {
            'test_case_id': 'TC-008',
            'precondition': '已登录系统；用户角色：税务部专员；系统存在二级及以下组织调整申请单，已触发税务审批；审批流程已流转到税务部专员节点',
            'name': '验证二级及以下组织调整申请单中税务部专员审批节点位置',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整申请单详情页面', 'input': '', 'expected_output': '成功进入申请单详情页面，页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '查看审批流程节点', 'input': '', 'expected_output': '审批流程正常显示，包含所有审批节点'},
                {'step_name': '步骤4', 'step_desc': '查看税务部专员审批节点在审批流程中的位置', 'input': '', 'expected_output': '税务部专员审批节点位于预算部专员审批之后、HRBP Head审批之前'}
            ]
        },
        {
            'test_case_id': 'TC-009',
            'precondition': '已登录系统；用户角色：税务部专员；系统存在组织调整申请单，已触发税务审批；审批流程已流转到税务部专员节点',
            'name': '验证税务审批节点申请单信息展示',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整申请单详情页面', 'input': '', 'expected_output': '成功进入申请单详情页面，页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '查看申请单信息区域', 'input': '', 'expected_output': '申请单信息区域正常显示，包含申请单号、申请人、申请时间等字段'},
                {'step_name': '步骤4', 'step_desc': '验证申请单信息字段的展示内容', 'input': '', 'expected_output': '申请单信息字段展示内容与其他审批节点的展示一致，字段完整且准确'}
            ]
        },
        {
            'test_case_id': 'TC-010',
            'precondition': '已登录系统；用户角色：税务部专员；系统存在组织调整申请单，已触发税务审批；审批流程已流转到税务部专员节点',
            'name': '验证税务审批节点调整信息Tab页展示',
            'owner': 'yangcl5',
            'steps': [
                {'step_name': '步骤1', 'step_desc': '登录系统', 'input': '', 'expected_output': '成功登录系统，进入首页'},
                {'step_name': '步骤2', 'step_desc': '进入组织调整申请单详情页面', 'input': '', 'expected_output': '成功进入申请单详情页面，页面正常显示'},
                {'step_name': '步骤3', 'step_desc': '查看调整信息区域', 'input': '', 'expected_output': '调整信息区域正常显示'},
                {'step_name': '步骤4', 'step_desc': '查看调整信息Tab页', 'input': '', 'expected_output': 'Tab页仅展示"调整预览"和"调整明细"两个Tab，不展示"干部任命"和"异常检查"Tab'},
                {'step_name': '步骤5', 'step_desc': '验证调整概述和附件是否展示', 'input': '', 'expected_output': '调整概述和附件在税务审批节点不展示'}
            ]
        }
    ]
    return test_cases


if __name__ == '__main__':
    import sys
    
    # 如果提供了命令行参数，使用参数作为输出文件路径
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        # 默认输出文件路径
        output_file = 'testcases/CSV/组织调整税务审批_2026-01-13_001.csv'
    
    # 获取测试用例数据（可以从需求文档解析或手动创建）
    test_cases = create_test_case_data()
    
    # 生成CSV文件
    generate_test_case_csv(output_file, test_cases)
