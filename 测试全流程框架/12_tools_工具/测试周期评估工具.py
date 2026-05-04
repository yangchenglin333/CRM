#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试周期评估工具
用于评估测试团队成员对每个需求文档所需的测试周期（天数）
"""
import atexit
import os
import sys

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
import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class TeamMember:
    """团队成员信息类"""
    
    def __init__(self, name: str, rank: str, years: str):
        self.name = name
        self.rank = rank
        self.years = years
        self.rank_coefficient = self._get_rank_coefficient()
        self.years_coefficient = self._get_years_coefficient()
    
    def _get_rank_coefficient(self) -> float:
        """获取职级系数"""
        rank_map = {
            "初级": 1.2,
            "中级2": 1.0,
            "中级3": 0.8
        }
        return rank_map.get(self.rank, 1.0)
    
    def _get_years_coefficient(self) -> float:
        """获取工作年限系数"""
        years_map = {
            "2~3年": 1.1,
            "3~4年": 1.0,
            "5年以上": 0.9
        }
        return years_map.get(self.years, 1.0)
    
    def get_comprehensive_coefficient(self, familiarity: str) -> float:
        """计算综合系数，并限制在0.7~2.0范围内"""
        familiarity_map = {
            "不熟悉": 1.5,
            "一般": 1.2,
            "熟悉": 1.0,
            "非常熟悉": 0.8
        }
        familiarity_coefficient = familiarity_map.get(familiarity, 1.0)
        coefficient = self.rank_coefficient * self.years_coefficient * familiarity_coefficient
        # 限制综合系数在0.7~2.0范围内
        return max(0.7, min(2.0, coefficient))


class RequirementAnalyzer:
    """需求文档分析器"""
    
    def __init__(self, requirement_file_path: str):
        self.file_path = requirement_file_path
        self.content = self._read_file()
        self.complexity = self._analyze_complexity()
    
    def _read_file(self) -> str:
        """读取需求文档内容"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"读取需求文档失败: {e}")
    
    def _analyze_complexity(self) -> Dict:
        """分析需求复杂度"""
        content = self.content
        
        # 统计功能模块数量（通过功能说明章节识别，更精准）
        # 查找"新增【"、"更新【"等实际功能模块
        new_modules = len(re.findall(r'新增【[^】]+】', content))
        update_modules = len(re.findall(r'更新【[^】]+】', content))
        module_count = new_modules + update_modules
        if module_count == 0:
            # 如果没有找到，尝试查找"3.4.1"等一级功能模块编号
            module_sections = len(re.findall(r'3\.4\.\d+\s+[^0-9]', content))
            module_count = max(module_sections, 2)  # 默认至少2个
        
        # 统计业务流程数量（只统计实际业务流程章节，更精准）
        # 查找章节标题中的"流程"
        process_patterns = [
            r'^\d+\.\d+.*业务流程',  # 2.1 业务流程
            r'^\d+\.\d+\.\d+\.\d+\.\d+\s+流程',  # 3.4.1.1.3 流程
        ]
        process_matches = set()
        for pattern in process_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                # 检查上下文，排除"不涉及审批流"、"示例："等
                idx = content.find(match)
                context = content[max(0, idx-100):min(len(content), idx+100)]
                if '不涉及' not in context and '示例' not in context:
                    process_matches.add(match)
        process_count = len(process_matches) if process_matches else 3  # 默认3个
        
        # 统计数据表数量（只统计实际数据表，更精准）
        # 查找"数据要素"章节
        data_section_match = re.search(r'数据要素|字段\s*\|', content)
        if data_section_match:
            start_idx = max(0, data_section_match.start() - 200)
            end_idx = min(len(content), data_section_match.end() + 1000)
            section_content = content[start_idx:end_idx]
            # 统计实际数据表（配置表、关联表等）
            table_mentions = len(re.findall(r'配置表|关联表|行业表|规则表|数据表[^名路径]', section_content))
            table_count = max(1, min(table_mentions, 6))  # 限制在1-6个之间
        else:
            table_count = 4  # 默认4个
        
        # 统计页面数量（只统计实际功能页面，更精准）
        # 1. 统计报表和视图（在"关联功能说明"章节查找）
        report_section = re.search(r'报表名称\s*\||以下报表|关联功能说明', content)
        if report_section:
            start_idx = max(0, report_section.start() - 100)
            end_idx = min(len(content), report_section.end() + 800)
            section_content = content[start_idx:end_idx]
            # 统计报表名称（去重）
            report_names = [
                'AR统一视图', 'AR项目视图', '逾期风险款报表', '回款预测明细',
                '大版本报表', '回款明细表', '预测明细列表（组织维度）', '大版本报表（组织维度）'
            ]
            report_count = sum(1 for name in report_names if name in section_content)
            if report_count == 0:
                # 如果没找到，尝试更宽泛的匹配
                report_count = len(re.findall(r'AR统一视图|AR项目视图|逾期风险款报表|回款预测明细|大版本报表|回款明细表|预测明细列表|组织维度', section_content))
                report_count = min(report_count, 9)  # 最多9个
        else:
            report_count = 9  # 默认9个报表
        
        # 2. 配置页面：域内外标签配置页面、风险等级配置页面
        config_pages = 2
        
        # 3. 原型图交互页面：查询界面、新建弹窗、编辑弹窗等
        # 查找"查询界面"、"新建弹窗"、"编辑弹窗"等
        prototype_keywords = ['查询界面', '新建弹窗', '编辑弹窗', '弹窗界面']
        prototype_pages = sum(1 for keyword in prototype_keywords if keyword in content)
        if prototype_pages == 0:
            prototype_pages = 4  # 默认4个
        
        # 总页面数
        page_count = report_count + config_pages + prototype_pages
        
        # 统计业务逻辑复杂度权重
        business_complexity_weight = 0.0
        # 跨系统交互
        if len(re.findall(r'跨系统|系统集成|外部系统|第三方系统', content)) > 0:
            business_complexity_weight += 2.0
        # 复杂权限控制
        if len(re.findall(r'权限控制|多角色|多层级|权限管理', content)) > 3:
            business_complexity_weight += 1.5
        # 高并发场景
        if len(re.findall(r'高并发|性能测试|压力测试|并发', content)) > 0:
            business_complexity_weight += 1.5
        # 复杂业务规则
        if len(re.findall(r'复杂计算|状态机|业务规则|规则引擎', content)) > 2:
            business_complexity_weight += 1.0
        # 数据一致性要求高
        if len(re.findall(r'分布式事务|数据一致性|事务管理', content)) > 0:
            business_complexity_weight += 1.0
        # 单需求最高不超过5分
        business_complexity_weight = min(5.0, business_complexity_weight)
        
        # 计算功能点总数（不考虑接口测试，因此不统计接口数量）
        function_points = (
            module_count + 
            process_count + 
            table_count * 0.3 + 
            page_count * 0.5 +
            business_complexity_weight
        )
        
        # 确定复杂度等级
        if function_points <= 5:
            complexity_level = "简单需求"
            base_complexity = "simple"
        elif function_points <= 15:
            complexity_level = "中等需求"
            base_complexity = "medium"
        elif function_points <= 30:
            complexity_level = "复杂需求"
            base_complexity = "complex"
        else:
            complexity_level = "非常复杂需求"
            base_complexity = "very_complex"
        
        return {
            "module_count": module_count,
            "process_count": process_count,
            "table_count": table_count,
            "page_count": page_count,
            "business_complexity_weight": round(business_complexity_weight, 1),
            "function_points": round(function_points, 1),
            "complexity_level": complexity_level,
            "base_complexity": base_complexity
        }


class TestCaseAnalyzer:
    """测试用例分析器"""
    
    def __init__(self, csv_file_path: Optional[str] = None):
        self.csv_file_path = csv_file_path
        self.case_count = self._count_cases() if csv_file_path else None
    
    def _count_cases(self) -> int:
        """统计CSV文件中的用例数量"""
        if not self.csv_file_path or not os.path.exists(self.csv_file_path):
            return 0
        
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                cases = set()
                for row in reader:
                    case_id = row.get('用例标识', '').strip()
                    if case_id:
                        cases.add(case_id)
                return len(cases)
        except Exception as e:
            print(f"警告：读取测试用例文件失败: {e}")
            return 0
    
    def get_case_count(self) -> Optional[int]:
        """获取用例数量"""
        return self.case_count


class TestCycleEvaluator:
    """测试周期评估器"""
    
    # 团队成员基础信息
    TEAM_MEMBERS = {
        "周亚鹏": TeamMember("周亚鹏", "初级", "2~3年"),
        "马凯": TeamMember("马凯", "初级", "2~3年"),
        "林晓明": TeamMember("林晓明", "初级", "2~3年"),
        "成鑫怡": TeamMember("成鑫怡", "中级2", "3~4年"),
        "亢晓松": TeamMember("亢晓松", "初级", "2~3年"),
        "于岩斌": TeamMember("于岩斌", "初级", "2~3年"),
        "宋智鹏": TeamMember("宋智鹏", "初级", "2~3年"),
        "赵忠浩": TeamMember("赵忠浩", "中级3", "5年以上"),
        "赵中浩": TeamMember("赵忠浩", "中级3", "5年以上"),  # 别名
        "张旭": TeamMember("张旭", "中级3", "5年以上"),
        "夏丹": TeamMember("夏丹", "初级", "2~3年")
    }
    
    def __init__(self, requirement_file_path: str, member_name: str, familiarity: str = "熟悉",
                 automation_rate: float = 0.0, requirement_change_risk: str = "低",
                 execution_strategy: str = "串行", bug_severity_ratio: float = 0.1,
                 ai_case_ratio: float = 0.0, ai_case_time: float = 0.75,
                 ai_quality_rate: float = 0.8,
                 test_case_file_path: Optional[str] = None, environment_complexity: str = "中等"):
        self.requirement_file_path = requirement_file_path
        self.member_name = member_name
        self.familiarity = familiarity
        self.automation_rate = automation_rate  # 自动化率，0.0-1.0
        self.requirement_change_risk = requirement_change_risk  # 需求变更风险：低、中、高
        self.execution_strategy = execution_strategy  # 执行策略：并行、串行
        self.bug_severity_ratio = bug_severity_ratio  # 严重BUG占比，0.0-1.0
        self.ai_case_ratio = ai_case_ratio  # AI已生成用例比例，0.0-1.0
        self.ai_case_time = ai_case_time  # AI生成用例时间，0.5-1.0天
        self.ai_quality_rate = ai_quality_rate  # AI用例合格率，0.0-1.0，默认0.8（80%）
        self.environment_complexity = environment_complexity  # 环境复杂度：简单、中等、复杂
        self.analyzer = RequirementAnalyzer(requirement_file_path)
        self.case_analyzer = TestCaseAnalyzer(test_case_file_path) if test_case_file_path else None
        self.member = self._get_member()
        self.comprehensive_coefficient = self.member.get_comprehensive_coefficient(familiarity)
    
    def _get_member(self) -> TeamMember:
        """获取团队成员信息"""
        member = self.TEAM_MEMBERS.get(self.member_name)
        if not member:
            raise Exception(f"未找到团队成员: {self.member_name}")
        return member
    
    def _get_automation_coefficient(self) -> float:
        """获取自动化率系数"""
        if self.automation_rate == 0:
            return 1.0
        elif self.automation_rate <= 0.3:
            return 0.9
        elif self.automation_rate <= 0.6:
            return 0.7
        elif self.automation_rate <= 0.8:
            return 0.5
        else:
            return 0.4
    
    def _get_change_risk_coefficient(self) -> float:
        """获取需求变更风险系数"""
        risk_map = {
            "低": 1.0,
            "中": 1.1,
            "高": 1.2
        }
        return risk_map.get(self.requirement_change_risk, 1.0)
    
    def _get_execution_strategy_coefficient(self) -> float:
        """获取执行策略系数"""
        if self.execution_strategy == "并行":
            return 0.8
        else:
            return 1.0
    
    def _get_bug_severity_coefficient_regression(self) -> float:
        """获取BUG回归验证时间的严重程度系数"""
        if self.bug_severity_ratio >= 0.3:
            return 1.2  # 严重BUG多，需要覆盖更多关联场景，时间更长
        elif self.bug_severity_ratio >= 0.1:
            return 1.0
        else:
            return 0.8
    
    def _get_ai_case_time(self) -> float:
        """获取AI生成用例时间（保留用于输出展示，实际计算已改用40%规则）"""
        if self.ai_case_ratio == 0:
            return 0.0
        if self.ai_case_ratio <= 0.5:
            return 0.5
        elif self.ai_case_ratio <= 0.8:
            return 0.75
        else:
            return 1.0

    def _get_ai_quality_coefficient(self) -> float:
        """获取AI用例合格率系数（保留用于输出展示）"""
        if self.ai_case_ratio == 0:
            return 1.0
        if self.ai_quality_rate > 0.8:
            return 1.0
        elif self.ai_quality_rate >= 0.6:
            return 1.2
        else:
            return 1.5

    # AI辅助系数：有AI参与时，用例设计与编写时间按传统的40%
    AI_ASSISTED_COEFFICIENT = 0.4

    def _calculate_case_design_and_writing_time(self, base_time: float) -> float:
        """计算用例设计与编写时间（40%规则：有AI参与时按传统时间的40%）"""
        traditional_time = base_time * self.comprehensive_coefficient
        if self.ai_case_ratio == 0:
            return traditional_time
        # 有AI辅助：按传统时间的40%评估，例如传统5天→2天
        return traditional_time * self.AI_ASSISTED_COEFFICIENT
    
    def _get_case_execution_base_time(self) -> float:
        """根据实际用例数量获取用例执行基础时间（方式3：需求+用例）"""
        if not self.case_analyzer or self.case_analyzer.case_count is None:
            return None  # 未提供用例文件，返回None，使用需求复杂度估算
        
        case_count = self.case_analyzer.case_count
        env = self.environment_complexity
        
        # 根据用例数量和环境复杂度确定基础时间（规则3.1.5）
        if case_count <= 20:
            if env == "简单":
                return 1.5
            elif env == "中等":
                return 2.0
            else:  # 复杂
                return 2.5
        elif case_count <= 50:
            if env == "简单":
                return 2.5
            elif env == "中等":
                return 3.0
            else:  # 复杂
                return 3.5
        elif case_count <= 100:
            if env == "简单":
                return 3.5
            elif env == "中等":
                return 4.0
            else:  # 复杂
                return 4.5
        else:  # >100
            if env == "简单":
                return 4.5
            elif env == "中等":
                return 5.0
            else:  # 复杂
                return 5.5
    
    def _get_base_time(self, stage: str, complexity: str) -> float:
        """获取各阶段基础时间"""
        complexity_map = {
            "simple": {
                "requirement_understanding": 0.5,
                "data_preparation": 0.3,
                "case_design_and_writing": 1.0,  # 合并：设计0.5 + 编写0.5
                "case_review": 0.3,  # 动态：简单需求0.3天
                "case_execution": 1.5,  # 合并：执行1.0 + 环境测试0.5（简单环境）
                "bug_regression": 0.5
            },
            "medium": {
                "requirement_understanding": 1.0,
                "data_preparation": 0.5,
                "case_design_and_writing": 2.0,  # 合并：设计1.5 + 编写0.75（已考虑Cursor效率）
                "case_review": 0.5,  # 动态：中等需求0.5天
                "case_execution": 2.5,  # 合并：执行2.0 + 环境测试0.5（中等环境）
                "bug_regression": 1.0
            },
            "complex": {
                "requirement_understanding": 1.5,
                "data_preparation": 1.0,
                "case_design_and_writing": 3.0,  # 合并：设计2.5 + 编写1.0（已考虑Cursor效率）
                "case_review": 0.8,  # 动态：复杂需求0.8天
                "case_execution": 3.0,  # 合并：执行3.0（复杂环境）
                "bug_regression": 1.5
            },
            "very_complex": {
                "requirement_understanding": 2.0,
                "data_preparation": 1.5,
                "case_design_and_writing": 4.0,  # 合并：设计3.5 + 编写1.25（已考虑Cursor效率）
                "case_review": 1.0,  # 动态：非常复杂需求1.0天
                "case_execution": 3.5,  # 合并：执行4.0（非常复杂环境，但合并后优化）
                "bug_regression": 2.0
            }
        }
        
        stage_map = {
            "需求理解时间": "requirement_understanding",
            "测试数据准备时间": "data_preparation",
            "用例设计与编写时间": "case_design_and_writing",
            "用例评审时间": "case_review",
            "用例执行时间": "case_execution",
            "Bug回归验证时间": "bug_regression"
        }
        
        stage_key = stage_map.get(stage)
        if not stage_key:
            return 0.0
        
        return complexity_map[complexity][stage_key]
    
    def evaluate(self) -> Dict:
        """执行评估"""
        complexity = self.analyzer.complexity["base_complexity"]
        
        stages = [
            "需求理解时间",
            "测试数据准备时间",
            "用例设计与编写时间",
            "用例评审时间",
            "用例执行时间",
            "Bug回归验证时间"
        ]
        
        stage_times = {}
        total_time = 0.0
        
        automation_coeff = self._get_automation_coefficient()
        execution_strategy_coeff = self._get_execution_strategy_coefficient()
        bug_severity_coeff_regression = self._get_bug_severity_coefficient_regression()
        
        for stage in stages:
            base_time = self._get_base_time(stage, complexity)
            
            # 用例设计与编写时间需要考虑AI已生成用例比例
            if stage == "用例设计与编写时间":
                adjusted_time = self._calculate_case_design_and_writing_time(base_time)
            # 用例执行时间：优先使用实际用例数量（方式3），否则使用需求复杂度估算（方式1）
            elif stage == "用例执行时间":
                # 尝试使用实际用例数量（方式3）
                case_based_time = self._get_case_execution_base_time()
                if case_based_time is not None:
                    # 方式3：基于实际用例数量
                    adjusted_time = case_based_time * self.comprehensive_coefficient * automation_coeff * execution_strategy_coeff
                else:
                    # 方式1：基于需求复杂度估算
                    adjusted_time = base_time * self.comprehensive_coefficient * automation_coeff * execution_strategy_coeff
            # Bug回归验证时间需要乘以严重程度系数
            elif stage == "Bug回归验证时间":
                adjusted_time = base_time * self.comprehensive_coefficient * bug_severity_coeff_regression
            else:
                adjusted_time = base_time * self.comprehensive_coefficient
            
            stage_times[stage] = round(adjusted_time, 1)
            total_time += adjusted_time
        
        # 总时间乘以需求变更风险系数
        change_risk_coeff = self._get_change_risk_coefficient()
        final_total_time = total_time * change_risk_coeff
        
        # 判断评估方式
        evaluation_mode = "方式3（需求+用例）" if (self.case_analyzer and self.case_analyzer.case_count is not None) else "方式1（仅需求）"
        
        return {
            "requirement_name": os.path.basename(self.requirement_file_path),
            "member_name": self.member.name,
            "rank": self.member.rank,
            "years": self.member.years,
            "familiarity": self.familiarity,
            "complexity": complexity,
            "complexity_level": self.analyzer.complexity["complexity_level"],
            "function_points": self.analyzer.complexity["function_points"],
            "business_complexity_weight": self.analyzer.complexity.get("business_complexity_weight", 0),
            "evaluation_mode": evaluation_mode,
            "case_count": self.case_analyzer.case_count if self.case_analyzer else None,
            "environment_complexity": self.environment_complexity,
            "comprehensive_coefficient": round(self.comprehensive_coefficient, 2),
            "ai_case_ratio": self.ai_case_ratio,
            "ai_case_time": round(self._get_ai_case_time(), 2),
            "ai_quality_rate": self.ai_quality_rate,
            "ai_quality_coefficient": round(self._get_ai_quality_coefficient(), 2),
            "automation_rate": self.automation_rate,
            "automation_coefficient": round(automation_coeff, 2),
            "requirement_change_risk": self.requirement_change_risk,
            "change_risk_coefficient": round(change_risk_coeff, 2),
            "execution_strategy": self.execution_strategy,
            "execution_strategy_coefficient": round(execution_strategy_coeff, 2),
            "bug_severity_ratio": self.bug_severity_ratio,
            "stage_times": stage_times,
            "subtotal_time": round(total_time, 1),
            "total_time": round(final_total_time, 1)
        }
    
    def format_output(self, result: Dict) -> str:
        """格式化输出评估结果"""
        output = []
        output.append("=" * 60)
        output.append("测试周期评估结果")
        output.append("=" * 60)
        output.append(f"\n需求文档：{result['requirement_name']}")
        output.append(f"测试人员：{result['member_name']}")
        output.append(f"职级：{result['rank']}")
        output.append(f"工作年限：{result['years']}")
        output.append(f"对需求熟悉程度：{result['familiarity']}")
        output.append(f"\n评估方式：{result.get('evaluation_mode', '方式1（仅需求）')}")
        if result.get('case_count') is not None:
            output.append(f"  - 实际用例数量：{result['case_count']}个")
            output.append(f"  - 环境复杂度：{result.get('environment_complexity', '中等')}")
        output.append(f"\n需求复杂度分析：")
        output.append(f"  - 复杂度等级：{result['complexity_level']}")
        output.append(f"  - 功能点总数：{result['function_points']}")
        if result.get('business_complexity_weight', 0) > 0:
            output.append(f"  - 业务逻辑复杂度权重：{result['business_complexity_weight']}")
        output.append(f"  - 综合系数：{result['comprehensive_coefficient']}（限制范围：0.7~2.0）")
        output.append(f"\n其他调整系数：")
        if result.get('ai_case_ratio', 0) > 0:
            output.append(f"  - AI已生成用例比例：{result.get('ai_case_ratio', 0)*100:.0f}%，AI生成时间：{result.get('ai_case_time', 0)}天")
            output.append(f"  - AI用例合格率：{result.get('ai_quality_rate', 0.8)*100:.0f}%，合格率系数：{result.get('ai_quality_coefficient', 1.0)}")
        output.append(f"  - 自动化率：{result.get('automation_rate', 0)*100:.0f}%，系数：{result.get('automation_coefficient', 1.0)}")
        output.append(f"  - 需求变更风险：{result.get('requirement_change_risk', '低')}，系数：{result.get('change_risk_coefficient', 1.0)}")
        output.append(f"  - 执行策略：{result.get('execution_strategy', '串行')}，系数：{result.get('execution_strategy_coefficient', 1.0)}")
        output.append(f"  - BUG严重程度占比：{result.get('bug_severity_ratio', 0.1)*100:.0f}%")
        output.append(f"\n各阶段时间评估：")
        
        stage_names = [
            "需求理解时间",
            "测试数据准备时间",
            "用例设计与编写时间",
            "用例评审时间",
            "用例执行时间",
            "Bug回归验证时间"
        ]
        
        for i, stage in enumerate(stage_names, 1):
            time = result['stage_times'].get(stage, 0)
            output.append(f"{i}. {stage}：{time}天")
        
        output.append(f"\n各阶段时间小计：{result.get('subtotal_time', 0)}天")
        output.append(f"需求变更风险系数：{result.get('change_risk_coefficient', 1.0)}")
        output.append(f"总测试周期：{result['total_time']}天")
        output.append("=" * 60)
        
        return "\n".join(output)


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 3:
        print("使用方法：")
        print("  方式1（仅需求文档）：")
        print("    python 测试周期评估工具.py <需求文档路径> <团队成员姓名> [熟悉程度] [AI已生成用例比例] [AI用例合格率] [自动化率] [需求变更风险] [执行策略] [BUG严重程度占比]")
        print("  方式3（需求+用例，推荐）：")
        print("    python 测试周期评估工具.py <需求文档路径> <团队成员姓名> <测试用例CSV文件路径> [熟悉程度] [AI已生成用例比例] [AI用例合格率] [自动化率] [需求变更风险] [执行策略] [BUG严重程度占比] [环境复杂度]")
        print("\n示例：")
        print("  方式1：")
        print("    python 测试周期评估工具.py 需求文档/需求文档存放处/ARM合同审批需求文档2025年12月10日001.mdc 赵忠浩 熟悉")
        print("    python 测试周期评估工具.py 需求文档/需求文档存放处/ARM合同审批需求文档2025年12月10日001.mdc 赵忠浩 熟悉 0.8 0.6 中 并行 0.2")
        print("  方式3（推荐）：")
        print("    python 测试周期评估工具.py 需求文档/需求文档存放处/研发预算管理系统需求文档001.mdc 亢晓松 testcases/CSV/79739873_20260126_研发预算管理系统_001.csv 不熟悉 0.8")
        print("\n参数说明：")
        print("  测试用例CSV文件路径（可选）：如果提供，使用方式3（需求+用例），否则使用方式1（仅需求）")
        print("  熟悉程度：不熟悉、一般、熟悉（默认）、非常熟悉")
        print("  AI已生成用例比例：0.0-1.0之间的浮点数，默认0.0（纯人工），通常为0.8（80%）")
        print("  AI用例合格率：0.0-1.0之间的浮点数，默认0.8（80%）")
        print("  自动化率：0.0-1.0之间的浮点数，默认0.0（纯手工）")
        print("  需求变更风险：低（默认）、中、高")
        print("  执行策略：串行（默认）、并行")
        print("  BUG严重程度占比：0.0-1.0之间的浮点数，默认0.1（10%）")
        print("  环境复杂度：简单、中等（默认）、复杂")
        sys.exit(1)
    
    requirement_file = sys.argv[1]
    member_name = sys.argv[2]
    
    # 判断第二个参数是否为CSV文件路径（方式3）
    test_case_file = None
    if len(sys.argv) > 3 and sys.argv[3].endswith('.csv'):
        test_case_file = sys.argv[3]
        familiarity = sys.argv[4] if len(sys.argv) > 4 else "熟悉"
        ai_case_ratio = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
        ai_quality_rate = float(sys.argv[6]) if len(sys.argv) > 6 else 0.8
        automation_rate = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
        requirement_change_risk = sys.argv[8] if len(sys.argv) > 8 else "低"
        execution_strategy = sys.argv[9] if len(sys.argv) > 9 else "串行"
        bug_severity_ratio = float(sys.argv[10]) if len(sys.argv) > 10 else 0.1
        environment_complexity = sys.argv[11] if len(sys.argv) > 11 else "中等"
    else:
        # 方式1：仅需求文档
        familiarity = sys.argv[3] if len(sys.argv) > 3 else "熟悉"
        ai_case_ratio = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
        ai_quality_rate = float(sys.argv[5]) if len(sys.argv) > 5 else 0.8
        automation_rate = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
        requirement_change_risk = sys.argv[7] if len(sys.argv) > 7 else "低"
        execution_strategy = sys.argv[8] if len(sys.argv) > 8 else "串行"
        bug_severity_ratio = float(sys.argv[9]) if len(sys.argv) > 9 else 0.1
        environment_complexity = "中等"  # 方式1默认中等环境
    
    # 检查文件是否存在
    if not os.path.exists(requirement_file):
        print(f"错误：需求文档不存在: {requirement_file}")
        sys.exit(1)
    
    try:
        evaluator = TestCycleEvaluator(
            requirement_file, 
            member_name, 
            familiarity,
            automation_rate=automation_rate,
            requirement_change_risk=requirement_change_risk,
            execution_strategy=execution_strategy,
            bug_severity_ratio=bug_severity_ratio,
            ai_case_ratio=ai_case_ratio,
            ai_quality_rate=ai_quality_rate,
            test_case_file_path=test_case_file,
            environment_complexity=environment_complexity
        )
        result = evaluator.evaluate()
        output = evaluator.format_output(result)
        print(output)
    except Exception as e:
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
