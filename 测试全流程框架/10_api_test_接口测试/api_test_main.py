import os
import subprocess
from datetime import datetime

def get_next_version_number(base_name, reports_dir):
    if not os.path.exists(reports_dir):
        return "001"
    
    existing = [d for d in os.listdir(reports_dir) if d.startswith(base_name)]
    if not existing:
        return "001"
    
    versions = []
    for name in existing:
        parts = name.replace(base_name, "").split("_")
        if parts and parts[0].isdigit():
            versions.append(int(parts[0]))
    
    next_num = max(versions) + 1 if versions else 1
    return f"{next_num:03d}"

def run_api_tests():
    import pytest
    
    base_dir = os.path.dirname(__file__)
    reports_dir = os.path.join(base_dir, '05_api_reports')
    test_file = os.path.join(base_dir, '03_api_tests', 'test_crm_api.py')
    
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    base_name = f"{date_str}_CRM接口测试"
    version = get_next_version_number(base_name, reports_dir)
    report_name = f"{base_name}{version}"
    allure_results_dir = os.path.join(reports_dir, report_name, 'allure-results')
    allure_report_dir = os.path.join(reports_dir, report_name, 'allure-report')
    
    os.makedirs(allure_results_dir, exist_ok=True)
    
    pytest.main([test_file, '-v', '--alluredir', allure_results_dir, '--tb=short'])
    
    subprocess.run(['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean'], check=True)
    
    print(f"测试报告已生成: {allure_report_dir}")
    print(f"查看报告命令: allure open {allure_report_dir}")

if __name__ == '__main__':
    run_api_tests()
