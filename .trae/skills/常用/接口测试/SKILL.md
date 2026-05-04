---
name: "api-test-generator"
description: "根据API文档生成API测试文档(CSV/JSON)并执行API测试。当用户提供API文档或代码并要求生成API测试或测试文档时调用。"
---

# API接口测试生成器

根据提供的API文档，生成API测试文档并执行接口测试。

## 功能说明

1. **生成测试文档**：从API文档创建CSV（给人看）和JSON（给程序执行）格式的测试用例
2. **单接口测试**：对单个API端点进行测试，包含断言验证
3. **业务流测试**：将多个API串联起来进行端到端工作流测试
4. **Mock测试**：使用模拟数据进行测试，无需依赖真实后端
5. **Bug记录**：规范记录测试过程中发现的问题，便于后期维护

## 使用场景

### 输入要求

用户提供以下任一内容：
- API文档（Swagger、OpenAPI或自定义格式）
- API代码/定义
- API端点详情（路径、方法、参数、预期响应）
- CSV格式测试用例（需转换为JSON执行）

### 生成输出

| 输出类型 | 文件位置 | 说明 |
|----------|----------|------|
| CSV测试用例 | `10_api_test_接口测试/02_api_testcases/csv/` | 人类可读的测试用例 |
| JSON测试用例 | `10_api_test_接口测试/02_api_testcases/json/` | 程序可执行的测试用例 |
| 测试脚本 | `10_api_test_接口测试/03_api_tests/` | Python测试文件 |
| Mock服务 | `10_api_test_接口测试/04_mock_server/` | Mock数据和服务配置 |
| 测试报告 | `10_api_test_接口测试/05_api_reports/allure/` | Allure格式测试报告 |
| Bug记录 | `10_api_test_接口测试/06_bug_records/` | 问题记录文档 |

## 工作流程

1. 解析用户提供的API文档
2. 生成结构化的API测试用例
3. 创建CSV和JSON格式的测试文档（确保两者同步）
4. 执行单接口测试（带断言）
5. 执行业务流测试（多步骤API链）
6. 生成详细的Allure测试报告
7. 按规范记录发现的Bug

## 测试类型说明

### 1. Mock测试
- 使用模拟数据进行测试，无需真实后端服务
- 支持自定义响应数据
- 文件位置：`10_api_test_接口测试/04_mock_server/`

### 2. 单接口测试
- 对单个API端点进行独立测试
- 包含正常请求、参数缺失、未授权访问等场景
- 验证状态码、响应结构、响应数据

### 3. 业务流程测试
- 将多个API串联成完整业务流程
- 支持从响应中提取变量并传递给后续请求
- 模拟真实业务场景

## 测试断言支持

- 状态码验证
- 响应JSON字段存在性验证
- 响应JSON值匹配验证
- 响应时间验证

## 业务流特性

- 从响应中提取上下文变量
- 在后续请求中使用变量替换
- 分步骤执行并记录日志

## 测试报告

使用 **Allure** 生成精美的可视化测试报告，包含：

### 报告特性
- **测试概览**：总用例数、通过/失败/跳过统计
- **执行历史**：显示每次测试运行的趋势
- **分类展示**：按模块/优先级/测试类型分类
- **详细日志**：包含请求/响应数据、错误堆栈
- **图表展示**：成功率、失败率饼图，趋势图
- **附件支持**：可添加请求/响应截图、文件

### 报告内容增强
- **请求参数展示**：自动记录请求URL、方法、请求头、查询参数、请求体
- **响应数据展示**：自动记录响应状态码、响应头、响应体
- **前置后置说明**：清晰标注测试的前置操作和后置清理

### 报告位置
- **报告目录**：`10_api_test_接口测试/05_api_reports/YYYYMMDD_{系统名}接口测试{序号}/`
  - 例如：`10_api_test_接口测试/05_api_reports/20260503_CRM接口测试015/`
- **Allure数据目录**：`{报告目录}/allure-results/`
- **Allure报告目录**：`{报告目录}/allure-report/`

### 查看报告
```bash
# 进入接口测试目录
cd 10_api_test_接口测试

# 方式1：使用Allure直接打开
allure serve 05_api_reports/YYYYMMDD_{系统名}接口测试{序号}/allure-results

# 方式2：生成HTML报告后打开
allure generate 05_api_reports/YYYYMMDD_{系统名}接口测试{序号}/allure-results -o 05_api_reports/YYYYMMDD_{系统名}接口测试{序号}/allure-report --clean
allure open 05_api_reports/YYYYMMDD_{系统名}接口测试{序号}/allure-report
```

### 自动生成报告脚本
```python
import os
import subprocess
from datetime import datetime

def generate_allure_report():
    """自动生成带时间戳的Allure报告"""
    # 生成时间戳格式的报告目录名
    date_str = datetime.now().strftime('%Y%m%d')
    report_name = f"{date_str}_CRM接口测试"
    
    # 确保目录存在
    base_dir = "10_api_test_接口测试/05_api_reports"
    report_dir = os.path.join(base_dir, report_name)
    os.makedirs(report_dir, exist_ok=True)
    
    # 生成报告
    results_dir = os.path.join(report_dir, "allure-results")
    report_output = os.path.join(report_dir, "allure-report")
    
    subprocess.run([
        "allure", "generate",
        results_dir,
        "-o", report_output,
        "--clean"
    ])
    
    return report_dir
```

## 文件命名规范

- CSV：`YYYYMMDD_{系统名}_API测试用例_{版本}.csv`
- JSON：`YYYYMMDD_{系统名}_API测试用例_{版本}.json`
- 测试脚本：`test_api_{模块名}.py`
- Bug记录：`API测试Bug记录_YYYYMMDD.md`

### 版本更新规范
- **每次更新必须生成新版本文件**：不能覆盖之前的用例文件
- **版本号递增**：v1.0 → v1.1 → v2.0
- **保留历史文件**：所有历史版本的用例文件都必须保留
- **报告目录命名**：使用时间戳格式 `YYYYMMDD_{系统名}接口测试{序号}`
  - 例如：`20260503_CRM接口测试016`
  - 序号从001开始，每次测试递增

## CSV格式要求

CSV文件必须包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| ID | 用例编号 | 1 |
| 模块 | 所属模块 | 用户登录 |
| 用例名称 | 用例名称 | 登录-正常登录成功 |
| 优先级 | P0/P1/P2 | P0 |
| 接口名称 | 接口名称 | /users/login |
| 前置条件 | 前置条件 | 已登录 |
| 请求URL | 完整URL | /api/users/login |
| 请求类型 | GET/POST/PUT/DELETE | POST |
| 请求头 | 请求头信息 | Content-Type: application/json |
| 请求参数类型 | Query/Path/JSON | JSON |
| 请求参数 | 请求参数 | {"username":"admin"} |
| 预期响应状态码 | HTTP状态码 | 200 |
| 预期返回数据 | 预期JSON响应 | {"message":"成功"} |
| 描述 | 用例描述 | 使用正确的用户名和密码登录系统 |

## JSON格式说明

JSON文件结构用于程序执行：

```json
{
  "id": "1",
  "name": "用户登录-正常请求成功",
  "path": "/api/users/login",
  "method": "POST",
  "params": {},
  "body": {
    "username": "admin",
    "password": "123456"
  },
  "headers": {"Content-Type": "application/json"},
  "expected_status": 200,
  "expected_response": {
    "token": "string",
    "user": {
      "id": 1,
      "username": "admin"
    }
  },
  "test_type": "单接口",
  "priority": "P0",
  "module": "用户登录",
  "case_name": "正常登录成功",
  "precondition": "无",
  "description": "使用正确的用户名和密码登录系统"
}
```

## 测试用例同步规范

### CSV与JSON同步要求
- **必须保持同步更新**：修改CSV或JSON时，必须同时更新另一个文件
- **字段对应关系**：确保两个文件的字段一一对应
- **定期校验**：执行测试前检查两个文件内容一致性
- **同步触发条件**：以下任一情况发生时，必须同时更新CSV和JSON文件：
  1. 新增测试用例时
  2. 修改测试用例时
  3. 删除测试用例时
  4. 用例ID重新编号时

### 同步字段列表
| CSV列名 | JSON字段 | 说明 |
|----------|----------|------|
| ID | id | 用例编号 |
| 模块 | module | 所属模块 |
| 用例名称 | name | 用例名称 |
| 优先级 | priority | P0/P1/P2 |
| 接口名称 | path | 接口路径 |
| 前置条件 | precondition | 前置条件 |
| 请求URL | path | 请求完整路径 |
| 请求类型 | method | HTTP方法 |
| 请求头 | headers | 请求头信息 |
| 请求参数 | body/params | 请求参数 |
| 预期响应状态码 | expected_status | 预期状态码 |
| 预期返回数据 | expected_response | 预期响应 |
| 描述 | description | 用例描述 |

## 前置后置操作规范

### 前置操作（Setup）
- **命名规范**：使用`setup_test_environment`作为fixture名称
- **内容要求**：明确标注"【前置操作】"，说明具体执行步骤
- **示例**：
  ```python
  @pytest.fixture(scope="session", autouse=True)
  def setup_test_environment():
      """测试环境初始化"""
      with allure.step("【前置操作】初始化测试环境 - 用户登录"):
          login_first()
          allure.attach("登录用户: admin", name="登录信息", attachment_type=allure.attachment_type.TEXT)
      yield
  ```

### 后置操作（Teardown）
- **命名规范**：使用`teardown_test_environment`作为fixture名称
- **内容要求**：明确标注"【后置操作】"，说明清理步骤
- **示例**：
  ```python
  @pytest.fixture(scope="session", autouse=True)
  def teardown_test_environment():
      """测试环境清理"""
      yield
      with allure.step("【后置操作】清理测试环境 - 用户退出"):
          session.post(f"{BASE_URL}/api/users/logout")
  ```

## Bug记录规范

### Bug记录文件位置
`10_api_test_接口测试/06_bug_records/API测试Bug记录_YYYYMMDD.md`

### Bug记录格式
| 字段 | 说明 | 示例 |
|------|------|------|
| Bug编号 | 唯一标识 | BUG-20260502-001 |
| 模块 | 问题所属模块 | 用户登录 |
| 用例名称 | 关联测试用例 | 用户登录-未授权访问 |
| 问题描述 | 简明描述问题 | 未登录状态下访问接口返回200而非401 |
| 复现步骤 | 详细复现步骤 | 1. 不登录直接访问/api/users/info |
| 预期结果 | 期望的行为 | 返回401未授权错误 |
| 实际结果 | 当前实际行为 | 返回200成功状态码 |
| 严重程度 | P0/P1/P2 | P1 |
| 状态 | 新建/待修复/已修复/关闭 | 新建 |
| 发现时间 | 发现日期 | 2026-05-02 |
| 修复版本 | 修复的版本号 | - |

### Bug记录示例
```markdown
## Bug编号：BUG-20260502-001
- **模块**：用户登录
- **用例名称**：获取当前用户信息-未授权访问
- **问题描述**：未登录状态下访问/api/users/info接口，预期返回401未授权错误，实际返回200成功
- **复现步骤**：
  1. 确保用户未登录
  2. 发送GET请求到/api/users/info
  3. 检查响应状态码
- **预期结果**：HTTP 401 Unauthorized
- **实际结果**：HTTP 200 OK
- **严重程度**：P1
- **状态**：新建
- **发现时间**：2026-05-02
```

## 统一请求封装

使用`send_request`函数统一处理HTTP请求，自动记录请求和响应信息到Allure报告：

```python
def send_request(method, url, headers=None, params=None, body=None):
    """统一请求发送方法，自动记录请求和响应信息到Allure报告"""
    allure.attach(url, name="请求URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(method, name="请求方法", attachment_type=allure.attachment_type.TEXT)
    if headers:
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=2), 
                     name="请求头", attachment_type=allure.attachment_type.JSON)
    if params:
        allure.attach(json.dumps(params, ensure_ascii=False, indent=2), 
                     name="查询参数", attachment_type=allure.attachment_type.JSON)
    if body:
        allure.attach(json.dumps(body, ensure_ascii=False, indent=2), 
                     name="请求体", attachment_type=allure.attachment_type.JSON)
    
    response = session.request(method, url, headers=headers, params=params, json=body)
    
    allure.attach(str(response.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
    try:
        response_data = response.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2), 
                     name="响应数据", attachment_type=allure.attachment_type.JSON)
    except:
        allure.attach(response.text, name="响应文本", attachment_type=allure.attachment_type.TEXT)
    
    return response
```

## 自检标准

生成完成后必须检查：
- [ ] 正向用例100%覆盖
- [ ] 反向用例≥80%覆盖
- [ ] 边界值/等价类≥20%
- [ ] 包含错误码测试
- [ ] 包含响应时间测试
- [ ] CSV与JSON测试用例同步
- [ ] 测试报告包含详细请求/响应信息
- [ ] 发现的问题已按Bug格式记录

### 更新后自检标准
- [ ] CSV和JSON文件同步更新（同步触发条件）
- [ ] 生成了新版本的用例文件（版本号递增）
- [ ] 历史版本的用例文件已保留
- [ ] 重新生成了新的测试报告（报告目录使用时间戳+序号命名）

## 目录结构

```
10_api_test_接口测试/
├── 01_api_docs/           # API文档
│   ├── swagger.yaml
│   └── swagger.html
├── 02_api_testcases/      # 测试用例
│   ├── csv/               # 人类可读格式
│   └── json/              # 程序执行格式
├── 03_api_tests/          # 测试脚本
│   └── test_crm_api.py
├── 04_mock_server/        # Mock服务
│   ├── mock_data.json
│   └── mock_server.js
├── 05_api_reports/        # 测试报告
│   ├── allure-results/
│   └── allure-report/
└── 06_bug_records/        # Bug记录
    └── API测试Bug记录_YYYYMMDD.md
```
