---
name: "automation-snapshot-rules"
description: "自动化快照与操作流程规范。当用户进行UI自动化测试或要求生成操作快照时调用。"
---

# 自动化快照与操作流程规范

## 快照规则

1. **命名规范**：`{操作类型}_{时间戳}.png`
2. **保存位置**：`测试报告/{模块}/snapshots/`
3. **格式**：PNG格式，清晰可辨
4. **大小**：不超过2MB

## 操作流程

### 页面操作流程
1. 打开目标页面
2. 等待页面加载完成
3. 定位元素
4. 执行操作
5. 验证结果
6. 保存快照

### 元素定位优先级
1. `data-testid` 属性
2. `id` 属性
3. `css selector`
4. `xpath`

## 快照时机

| 场景 | 是否保存快照 |
|------|-------------|
| 操作成功 | 可选 |
| 操作失败 | 必须 |
| 断言失败 | 必须 |
| 异常发生 | 必须 |

## POM模式

```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    @property
    def username_input(self):
        return self.driver.find_element(By.ID, "username")

    def login(self, username, password):
        self.username_input.send_keys(username)
        self.password_input.send_keys(password)
        self.submit_button.click()
```

## 页面对象目录
```
测试全流程框架/06_pages_页面对象/
├── base_page_基础页面.py
├── login_page_登录页面.py
├── dashboard_page_工作台页面.py
└── CRM客户管理页面ref快照.md
```
