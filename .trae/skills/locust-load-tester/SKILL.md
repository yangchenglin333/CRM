---
name: "locust-load-tester"
description: "使用Locust进行压力测试，模拟并发用户，生成性能测试报告。当用户提供接口或URL要求进行压力测试、负载测试、性能测试时调用。"
---

# Locust 压力测试工具

## 功能说明

使用 Locust 进行分布式压力测试，模拟大量并发用户访问系统，生成详细的性能测试报告。

## 应用场景

- 接口压力测试
- 负载测试
- 性能基准测试
- 峰值并发测试
- 系统稳定性测试

## 工作流程

### Step 1: 确定测试目标
1. 分析被测接口
2. 确定并发用户数
3. 确定测试时长
4. 设置性能指标阈值

### Step 2: 创建测试脚本
```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def index_page(self):
        self.client.get("/")
```

### Step 3: 执行测试
```bash
# 单机模式
locust -f locustfile.py --host=http://target.com

# 分布式模式（主节点）
locust -f locustfile.py --master --host=http://target.com

# 分布式模式（工作节点）
locust -f locustfile.py --worker --master-host=<master-ip>
```

### Step 4: 分析报告
- 请求成功率
- 平均响应时间
- 99%分位响应时间
- TPS/并发数关系

## 文件结构

```
13_locust_压力测试/
├── config/              # 测试配置
├── scripts/            # 测试脚本
├── api_docs/            # 接口文档
├── reports/             # 测试报告
└── utils/              # 工具函数
```

## 性能指标

| 指标 | 说明 | 阈值示例 |
|------|------|----------|
| 成功率 | 请求成功比例 | ≥99% |
| 平均响应时间 | 所有请求平均耗时 | <500ms |
| 95分位 | 95%请求耗时 | <1s |
| 99分位 | 99%请求耗时 | <2s |
| TPS | 每秒事务数 | 根据业务定 |

## 输出报告

- HTML格式可视化报告
- CSV格式原始数据
- 图表展示性能趋势
