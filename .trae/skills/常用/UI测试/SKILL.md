---
name: "ui-automation-mcp-executor"
description: "使用AI MCP模式执行UI自动化测试，支持AI自愈逻辑，生成详细测试报告。Invoke when user asks to run UI automation with AI MCP mode."
---

# UI自动化AI MCP执行器

## 功能说明

基于AI MCP模式的UI自动化测试执行器，通过AI浏览器工具完成UI自动化测试，支持AI自愈逻辑进行元素定位兜底，测试完成后生成包含编号、步骤、实际结果、截图的详细报告。

## 应用场景

当用户提出以下任一诉求时，**自动应用本规则**：

- 要求做UI自动化
- 要求使用AI MCP模式执行UI自动化
- 要求生成详细测试报告（含截图）
- 要求AI自愈逻辑兜底

## 执行模式（强制）

### ⚠️ 重要声明（绝对禁止脚本模式）

**本Skill必须使用MCP模式执行UI自动化测试，禁止直接编写或执行Python/Playwright脚本。**

**🚫 绝对禁止的行为：**
- ❌ 编写任何Python/Playwright脚本
- ❌ 执行任何Python/Playwright脚本
- ❌ 创建任何 `.py` 格式的测试脚本文件
- ❌ 使用 `python3`、`pytest` 等命令运行测试
- ❌ 在MCP工具不可用时绕过使用脚本模式

**✅ 必须执行的行为：**
- ✅ 所有UI自动化操作必须通过MCP工具调用完成
- ✅ 浏览器导航、点击、输入等操作使用MCP工具
- ✅ 元素定位和等待使用MCP工具
- ✅ 页面截图和分析使用MCP工具
- ✅ 测试结果记录使用MCP工具

### 模式说明

| 模式 | 状态 | 说明 |
|------|------|------|
| MCP模式 | ✅ 强制使用 | 通过MCP工具调用执行所有操作 |
| 脚本模式 | ❌ 绝对禁止 | 禁止编写或执行任何Playwright/Python脚本 |

### MCP工具集

必须使用的MCP工具（按执行顺序）：

| 工具名称 | 功能 | 参数 |
|---------|------|------|
| `browser_navigate` | 导航到URL | `url`: 目标URL |
| `browser_snapshot` | 获取页面快照分析 | `target`, `filename`, `depth`, `boxes` |
| `browser_type` | 输入文本（含聚焦） | `element`, `target`, `text`, `submit`, `slowly` |
| `browser_click` | 点击元素 | `element`, `target`, `doubleClick`, `button`, `modifiers` |
| `browser_take_screenshot` | 页面截图 | `element`, `target`, `type`, `filename`, `fullPage` |
| `browser_wait_for` | 等待文本或时间 | `time`, `text`, `textGone` |
| `browser_resize` | 调整浏览器窗口大小 | `width`, `height` |
| `browser_evaluate` | 执行JavaScript（清理弹窗等） | `element`, `target`, `function`, `filename` |

### 弹窗处理机制（强制要求）

#### 登录后自动清理弹窗：

在登录成功后，必须执行以下操作清理可能的弹窗：

```
1. 等待1-2秒让页面加载
2. 使用 browser_snapshot 分析页面
3. 检查是否存在弹窗元素：
   - 关闭按钮：text="关闭" / class*="close" / id*="close"
   - 确认按钮：text="确认" / text="确定"
   - 模态框：class*="modal" / class*="dialog"
4. 使用 browser_click 点击关闭按钮
5. 如果没有找到关闭按钮，使用 browser_evaluate 执行：
   - 移除所有modal元素
   - 移除所有overlay元素
   - 恢复页面滚动
```

#### JavaScript清理示例：

```javascript
// 移除所有模态框
document.querySelectorAll('.modal, .dialog, [role="dialog"], [class*="modal"], [class*="dialog"]')
  .forEach(el => el.remove());

// 移除遮罩层
document.querySelectorAll('.overlay, [class*="overlay"], [class*="backdrop"]')
  .forEach(el => el.remove());

// 恢复滚动
document.body.style.overflow = 'auto';
document.documentElement.style.overflow = 'auto';
```

### 浏览器窗口调整（强制要求）

#### 执行流程：

```
1. 测试开始前：调整到标准分辨率 1920x1080
2. 每个用例截图前：确保窗口大小正确
3. 如果页面显示错位：调整窗口大小并重试
```

#### 调整顺序：

```
browser_resize(width=1920, height=1080)
↓
等待500ms让页面重排
↓
继续执行测试
```

### MCP工具可用性检查

#### 检查步骤：

1. **检查MCP服务器状态**
   ```bash
   # 检查是否有MCP服务器运行
   ps aux | grep mcp
   ```

2. **验证MCP工具是否可用**
   在执行前尝试调用 `browser_navigate` 工具，如果返回错误"工具不存在"，则MCP工具不可用。

3. **检查配置文件**
   查看是否存在MCP配置文件：
   - `~/.trae/mcp_config.json`
   - `~/.mcp/mcp_config.json`
   - 项目根目录下的 `mcp.json`

### MCP工具不可用时的处理

#### ❌ 禁止的行为

- ❌ 直接编写Python/Playwright脚本
- ❌ 使用 `python3 script.py` 执行测试
- ❌ 使用 `pytest` 运行测试
- ❌ 创建 `.py` 格式的测试脚本文件

#### ✅ 正确处理方式

当检测到MCP工具不可用时，应该：

1. **立即停止并报告**
   ```
   错误：AI MCP浏览器工具不可用
   原因：未检测到MCP服务器或工具配置
   解决方案：请配置并启动MCP服务器
   ```

2. **提供配置指导**
   向用户说明如何配置MCP工具：
   - 安装MCP服务器
   - 配置MCP工具连接
   - 验证工具可用性

3. **示例错误消息**
   ```
   ╔══════════════════════════════════════════════════════════════╗
   ║                     MCP工具不可用                            ║
   ╠══════════════════════════════════════════════════════════════╣
   ║ 当前状态：MCP服务器未运行或工具未配置                        ║
   ║                                                           ║
   ║ 需要配置：                                                  ║
   ║ 1. 安装AI Browser MCP服务器                                ║
   ║ 2. 在~/.trae/mcp_config.json中配置服务器连接               ║
   ║ 3. 重启Trae IDE使配置生效                                  ║
   ║                                                           ║
   ║ 可用工具检查：                                             ║
   ║ - browser_navigate: ❌ 不可用                             ║
   ║ - browser_click: ❌ 不可用                                ║
   ║ - browser_type: ❌ 不可用                                 ║
   ║ - browser_snapshot: ❌ 不可用                              ║
   ║                                                           ║
   ║ 当前操作：已禁止使用脚本模式执行UI自动化                    ║
   ╚══════════════════════════════════════════════════════════════╝
   ```

## 前置条件

### 1. AI MCP工具可用性（必需）

**必须确保以下Playwright MCP浏览器工具可用才能执行：**
- `browser_navigate` - 导航
- `browser_click` - 点击
- `browser_type` - 输入
- `browser_snapshot` - 页面快照
- `browser_take_screenshot` - 截图
- `browser_wait_for` - 等待
- `browser_resize` - 调整窗口大小

**工具检查方法：**
尝试调用上述任一工具，如果返回"工具不存在"或连接错误，则立即报告MCP不可用，禁止使用脚本模式。

### 2. JSON测试用例格式

JSON用例作为AI执行的指引，提供测试步骤和预期结果：

```json
{
  "project_name": "CRM系统",
  "version": "v1.1",
  "test_cases": [
    {
      "test_case_id": "TC-001",
      "name": "用户登录-正常登录成功",
      "priority": "P0",
      "module": "用户登录",
      "precondition": "系统已启动；存在测试用户账号",
      "steps": [
        {
          "step_name": "步骤1",
          "action": "navigate",
          "target": "/login",
          "value": "",
          "expected": "登录页面正常显示"
        },
        {
          "step_name": "步骤2",
          "action": "type",
          "target": "#username",
          "value": "admin",
          "expected": "用户名输入成功"
        }
      ]
    }
  ]
}
```

### 3. 框架目录

确保测试框架位于：
`/Users/admin/Desktop/test-management-platform 2/测试全流程框架/`

## 工作流程

### 1. 测试准备

```
1. 解析JSON测试用例
2. 确认测试环境URL和账号
3. 创建测试报告目录
```

### 2. AI MCP模式执行（含自愈逻辑）

#### AI自愈流程：

```
元素定位失败
    ↓
AI分析页面结构 → 尝试备用定位符（id→class→text→xpath）
    ↓
仍失败 → AI生成新定位符
    ↓
记录失败 → 截图 → 继续下一用例
```

#### AI工具使用规范：

| 步骤类型 | Playwright MCP工具 | 自愈逻辑 |
|---------|-----------|---------|
| 导航 | `browser_navigate` | 自动重试+截图 |
| 点击 | `browser_click` | 多定位符递进+AI生成xpath |
| 输入 | `browser_type` | 清理后输入+聚焦重试 |
| 等待 | `browser_wait_for` | 显示等待+超时处理 |
| 快照 | `browser_snapshot` | AI分析页面状态 |

### 3. 执行单个测试用例

```
开始执行 {case_id}
    ↓
1. 前置条件检查
    ↓
2. AI执行测试步骤
   - 每步执行前AI分析页面
   - 执行后截图保存
   - 记录实际结果 vs 预期结果
    ↓
3. 步骤级别的结果记录
   - step_name: 步骤名称
   - action: 执行动作
   - target: 目标元素
   - expected: 预期结果
   - actual: 实际结果
   - status: passed/failed
   - screenshot: 截图路径
    ↓
4. 用例级别汇总
    ↓
5. 后置条件处理
```

### 4. 生成测试报告

#### 报告目录：
`/Users/admin/Desktop/test-management-platform 2/测试全流程框架/09_reports_测试报告/UI自动化测试报告/`

#### 报告子文件夹命名规则：
`{YYYYMMDD}-{项目名}测试`
例如：`20260503-CRM登录测试`

#### 报告结构：

```
{报告目录}/{YYYYMMDD}-{项目名}测试/
├── test_report.html          # HTML测试报告
├── test_report.json          # JSON测试报告
├── test_case_details.csv     # 用例详情（含步骤级结果）
└── screenshots/              # 截图目录
    ├── TC-001_final_YYYYMMDD_HHMMSS.png    # 每个Case的最终结果截图
    └── ...
```

### 5. HTML报告格式（使用统一模板）

**⚠️ 重要：UI测试报告必须使用 [测试报告](../测试报告/SKILL.md) 规则定义的统一模板A**

详细模板和样式规范请参阅：[测试报告 - 模板A：UI自动化测试报告模板](../测试报告/SKILL.md#ui自动化测试报告模板模板a)

#### 报告目录：
`/Users/admin/Desktop/test-management-platform 2/测试全流程框架/09_reports_测试报告/UI自动化测试报告/`

#### 报告子文件夹命名规则：
`{YYYYMMDD}-{项目名}测试`
例如：`20260503-CRM登录测试`

#### 报告结构：

```
{报告目录}/{YYYYMMDD}-{项目名}测试/
├── test_report.html          # HTML测试报告
├── test_report.json          # JSON测试报告
├── test_case_details.csv     # 用例详情（含步骤级结果）
└── screenshots/              # 截图目录
    ├── TC-001_final_YYYYMMDD_HHMMSS.png    # 每个Case的最终结果截图
    └── ...
```

## AI MCP工具使用示例

### 示例: 执行登录测试（带AI自愈）

```
# 1. 导航到登录页
browser_navigate(url="/login")

# 2. 截图保存
browser_take_screenshot(name="step1_before_login.png")

# 3. 输入用户名
browser_type(
    target="#username",
    text="admin"
)

# 4. 输入密码
browser_type(
    target="#password",
    text="admin123"
)

# 5. 点击登录按钮
browser_click(
    target="#login-btn"
)

# 6. 等待页面跳转
browser_wait_for(
    text="工作台",
    time=10
)

# 7. 结果截图
browser_take_screenshot(name="step2_after_login.png")
```

## 测试结果记录

### 结果数据结构（JSON）

```json
{
  "summary": {
    "report_id": "UI-20260503-001",
    "total": 10,
    "passed": 8,
    "failed": 2,
    "skipped": 0,
    "start_time": "2026-05-03T10:00:00",
    "end_time": "2026-05-03T10:15:30",
    "duration": 930.5,
    "project": "CRM系统",
    "version": "v1.1"
  },
  "test_results": [
    {
      "case_id": "TC-001",
      "case_name": "用户登录-正常登录成功",
      "priority": "P0",
      "module": "用户登录",
      "status": "passed",
      "start_time": "2026-05-03T10:00:00",
      "end_time": "2026-05-03T10:00:05",
      "duration": 5.2,
      "screenshot": "screenshots/TC-001.png",
      "steps": [
        {
          "step_name": "步骤1",
          "action": "navigate",
          "target": "/login",
          "expected": "登录页面正常显示",
          "actual": "登录页面正常显示",
          "status": "passed",
          "screenshot": "screenshots/TC-001_step-1.png",
          "error_message": null
        },
        {
          "step_name": "步骤2",
          "action": "type",
          "target": "#username",
          "value": "admin",
          "expected": "用户名输入成功",
          "actual": "用户名输入成功",
          "status": "passed",
          "screenshot": "screenshots/TC-001_step-2.png",
          "error_message": null
        }
      ]
    }
  ]
}
```

## 注意事项

### ⚠️ 强制要求

1. **MCP模式绝对优先**：必须使用MCP工具执行所有UI自动化操作，绝对禁止使用脚本模式
2. **工具检查**：执行前必须验证MCP工具可用性，不可用时立即报告，禁止继续
3. **截图保存时机**：每个步骤执行前后都要截图，便于问题定位
4. **步骤级记录**：报告必须包含步骤级详情，不能只记录用例级结果
5. **显示等待**：所有元素操作前必须等待元素可见
6. **报告完整性**：报告需包含编号、步骤、实际结果、截图
7. **HTML报告结构要求**（两部分结构）：
   - **第一部分-用例执行列表**：表格形式，点击"查看截图"在表格下方显示截图
   - **第二部分-详细执行步骤**：每个Case展示所有步骤详情，底部只有一个最终截图
   - 每个Case只有一个最终结果截图，不是每个步骤一个
   - 截图支持点击放大查看（Modal预览）
   - 失败步骤用红色边框标记
   - 截图链接使用 `href="javascript:void(0)"` 防止页面跳转

### 🚫 绝对禁止事项（违者必究）

- **🚫 绝对禁止** 编写Python/Playwright脚本直接执行
- **🚫 绝对禁止** 使用 `python3`、`pytest` 等命令直接运行测试
- **🚫 绝对禁止** 在MCP工具不可用时绕过使用脚本模式
- **🚫 绝对禁止** 创建任何 `.py` 格式的测试脚本文件
- **🚫 绝对禁止** 任何形式的脚本编写或执行行为
