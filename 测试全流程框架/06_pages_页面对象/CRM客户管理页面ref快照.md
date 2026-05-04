# CRM 客户管理 - 客户查询与新建客户 页面 Ref 快照

> 记录来源：Agent Browser `browser_snapshot`  
> 系统链接：https://xin-uat.asiainfo.com/webapps/ai-crm-web/cust/query  
> 用途：快照中的 **ref** 供 MCP 当次会话操作使用；**role / text / xpath** 多维度选择器供 Playwright 脚本编写与鲁棒性代码生成。

---
## 使用到方式
## 用浏览器打开 CRM，按 @CRM客户管理页面ref快照.md 顶部的操作步骤帮我执行一遍，不要生成脚本，就在对话里用浏览器操作；遇到页面要加载或弹窗，你自己判断什么时候等、什么时候点下一步。
## 用 Agent Browser 按操作手册帮我走一遍客户查询再新建客户，全程你根据 snapshot 自己判断等待和下一步，不要写 Playwright 代码。

## 操作步骤（可随时修改）

下面这段描述即「具体操作流程」，可直接改文字，改完后用下方「如何生成 Playwright 脚本」生成或更新脚本。

**当前步骤：**

登录网址，输入账户和密码，点击客户查询，在客户编号输入框中输入87855，点击查询，点击客户管理中的新建客户，客户名称输入框中输入测试1，统一社会信用代码输入框输入91110108MA01XXY234，点击下一步，填写所有的必填字段后，点击提交审批。 

### 如何生成 Playwright 脚本

1. 在 Cursor 对话中说一句即可，例如：
   - **「根据 `CRM客户管理页面ref快照.md` 顶部的操作步骤和本页的多维度选择器，生成 Playwright 脚本，遵守本页第五部分的鲁棒性要求。」**
   - 或简写：**「根据本页快照生成 CRM 客户查询+新建客户的 Playwright 脚本。」**
2. Agent 会结合**本页顶部的操作步骤**与**下方各节的“关键元素多维度选择器”**生成代码，并自动遵守本页「五、Playwright 代码生成指令」中的智能等待、text/role 优先、try/except、模块化等要求。
3. 生成后的脚本可放在 `自动化脚本/CRM/` 下（如 `CRM-客户查询与新建客户.py`），运行前在脚本中配置登录 URL、用户名、密码等。

---

## 一、客户管理 - 客户查询 页面

**页面 URL：** `https://xin-uat.asiainfo.com/webapps/ai-crm-web/cust/query`  
**页面标题：** 客户管理-客户查询  
**核心区域位置：** 查询表单位于主内容区顶部（客户管理 > 客户查询 面包屑下方），表格与分页在其下方。

### 页面快照（含全部 ref）

```yaml
- generic [ref=e15]:
  - generic [ref=e18]:
    - img "crm" [ref=e20]
    - menu [ref=e28]:
      - menuitem "首页" [ref=e29] [cursor=pointer]:
        - link "首页" [ref=e30]: /url: /webapps/ai-crm-web/
      - menuitem "客户管理" [ref=e32]:
        - generic [ref=e33] [cursor=pointer]:
          - menu [ref=e36]:
            - menuitem "客户查询" [ref=e37]:
              - link "客户查询" [ref=e38]: /url: /webapps/ai-crm-web/cust/query
            - menuitem "新建客户" [ref=e39]:
              - link "新建客户" [ref=e40]: /url: /webapps/ai-crm-web/cust/newCreateCustomer/customer_sale
            - menuitem "内部客户" [ref=e41]: link [ref=e42]
            - menuitem "客户申请单" [ref=e43]: link [ref=e44]
            - menuitem "信用评估申请单列表" [ref=e45]: link [ref=e46]
      - menuitem "商机管理" [ref=e47]
      - menuitem "商机报备" [ref=e51]
      - menuitem "应标管理" [ref=e55]
      - menuitem "合同审批" [ref=e59]
      - menuitem "合同管理" [ref=e63]
      - menuitem "合同产品拆分" [ref=e67]
      - menuitem "后台" [ref=e71]
      - menuitem "报表" [ref=e75]: link [ref=e76]
      - menuitem "审批干预" [ref=e78]
      - menuitem "我的审批" [ref=e82]: link [ref=e83]
      - menuitem "代理设置" [ref=e85]: link [ref=e86]
      - menuitem "售前项目管理" [ref=e88]: link [ref=e89]
      - menuitem "测试页面" [ref=e91]: link [ref=e92]
  - generic [ref=e94]:
    - generic [ref=e95]:
      - img [ref=e98] [cursor=pointer]
      - list [ref=e101]:
        - listitem [ref=e102]: 客户管理>
        - listitem [ref=e103]: 客户查询
      - generic [ref=e124]:
        - img [ref=e125]
        - generic [ref=e126]: 杨承霖
        - generic [ref=e127]: 欢迎您
    - generic [ref=e138]:
      - generic [ref=e140]:
        - generic [ref=e143]:
          - generic [ref=e144]: "客户编号:"
          - textbox "客户编号:" [ref=e148]: /placeholder: 请输入
        - generic [ref=e150]:
          - generic [ref=e151]: "客户名称:"
          - textbox "客户名称:" [ref=e155]: /placeholder: 请输入
        - generic [ref=e157]:
          - generic [ref=e158]: "客户行业:"
          - combobox [ref=e163] [cursor=pointer]:
            - generic [ref=e165]: 请选择
            - img [ref=e168]
        - generic [ref=e171]:
          - generic [ref=e172]: "统一社会信用代码:"
          - textbox "统一社会信用代码:" [ref=e176]: /placeholder: 请输入
        - generic [ref=e178]:
          - button "查 询" [ref=e179] [cursor=pointer]
          - button "重 置" [ref=e180] [cursor=pointer]
      - generic [ref=e181]:
        - button "信用评估" [disabled] [ref=e182]
        - button "owner申请" [disabled] [ref=e183]
        - button "基本信息变更" [disabled] [ref=e184]
        - button "修改联系人" [disabled] [ref=e185]
        - button "信用评估结果" [disabled] [ref=e186]
        - button "管理信息变更" [disabled] [ref=e187]
        - button "生 效" [disabled] [ref=e188]
        - button "失 效" [disabled] [ref=e189]
      - generic [ref=e192]:
        - table [ref=e196]:
          - rowgroup [ref=e207]:
            - row [ref=e208]:
              - cell "选择" [ref=e209]: generic [ref=e210]
              - cell "客户编号" [ref=e211]
              - cell "客户名称" [ref=e213]
              - cell "统一社会信用代码" [ref=e215]
              - cell "客户行业" [ref=e217]
              - cell "行业归属BU" [ref=e219]
              - cell "客户归属BU" [ref=e221]
              - cell "重点业务" [ref=e223]
              - cell "状态" [ref=e225]
          - rowgroup [ref=e227]:
            - row [ref=e228]:
              - cell [ref=e229]: radio [ref=e233] [cursor=pointer]
              - cell "87855" [ref=e235]: link "87855" [ref=e236]
              - cell [ref=e237]: link [ref=e238]
              - cell [ref=e239]
              - cell "能源-石油" [ref=e240]
              - cell "无归属BU" [ref=e241]
              - cell "无归属BU" [ref=e242]
              - cell [ref=e243]
              - cell "有效" [ref=e244]
            # ... 更多数据行（每行含 radio、客户编号 link、客户名称 link、统一社会信用代码、客户行业、行业归属BU、客户归属BU、重点业务、状态）
        - list [ref=e398]:
          - listitem [ref=e399]: 共 7023 条
          - listitem "上一页" [ref=e400]: img [ref=e403]
          - listitem "1" [ref=e405] [cursor=pointer]
          - listitem "2" [ref=e406] [cursor=pointer]
          - listitem "3" [ref=e407] [cursor=pointer]
          - listitem "4" [ref=e408] [cursor=pointer]
          - listitem "5" [ref=e409] [cursor=pointer]
          - listitem "向后 5 页" [ref=e410] [cursor=pointer]
          - listitem "703" [ref=e417] [cursor=pointer]
          - listitem "下一页" [ref=e418] [cursor=pointer]
          - listitem [ref=e423]:
            - combobox [ref=e425] [cursor=pointer]: generic "10 条/页" [ref=e427]
            - textbox [ref=e433] 跳至 ... 页
```

### 客户查询页 - 关键元素 ref 汇总（供 MCP 操作）

| 说明           | role / 类型   | name/label           | ref   |
|----------------|---------------|----------------------|-------|
| 客户编号输入框 | textbox       | 客户编号:            | e148  |
| 客户名称输入框 | textbox       | 客户名称:            | e155  |
| 客户行业下拉   | combobox      | 客户行业 / 请选择    | e163  |
| 统一社会信用代码 | textbox     | 统一社会信用代码:    | e176  |
| 查询按钮       | button        | 查 询                | e179  |
| 重置按钮       | button        | 重 置                | e180  |
| 客户查询菜单   | link          | 客户查询             | e38   |
| 新建客户菜单   | link          | 新建客户             | e40   |

### 客户查询页 - 关键元素多维度选择器（供 Playwright 精准定位）

| 元素名称       | role 选择器 | text / label 选择器 | xpath 示例（可从 DevTools 补充） |
|----------------|-------------|----------------------|----------------------------------|
| 客户编号输入框 | `role=textbox, name=客户编号:` | label 文本「客户编号:」、placeholder「请输入」 | `//input[contains(@placeholder,'请输入') and preceding::*[contains(.,'客户编号')]]` |
| 客户名称输入框 | `role=textbox, name=客户名称:` | label 文本「客户名称:」、placeholder「请输入」 | `//input[contains(@placeholder,'请输入') and preceding::*[contains(.,'客户名称')]]` |
| 客户行业下拉   | `role=combobox`，展开后选 option | 可见文本「请选择」 | `//*[@role='combobox']` 或对应 select/div |
| 统一社会信用代码输入框 | `role=textbox, name=统一社会信用代码:` | label「统一社会信用代码:」、placeholder「请输入」 | 同上 pattern |
| 查询按钮       | `role=button, name=查 询` | 按钮文本「查 询」 | `//button[contains(.,'查') and contains(.,'询')]` |
| 重置按钮       | `role=button, name=重 置` | 按钮文本「重 置」 | `//button[contains(.,'重') and contains(.,'置')]` |
| 客户查询菜单   | `role=link, name=客户查询` | 链接文本「客户查询」 | `//a[contains(@href,'cust/query')]` |
| 新建客户菜单   | `role=link, name=新建客户` | 链接文本「新建客户」 | `//a[contains(@href,'newCreateCustomer/customer_sale')]` |

---

## 二、客户管理 - 新建客户 页面

**页面 URL：** `https://xin-uat.asiainfo.com/webapps/ai-crm-web/cust/newCreateCustomer/customer_sale`  
**页面标题：** 客户管理-新建客户  
**核心区域位置：** 表单位于主内容区（客户管理 > 新建客户 面包屑下方），含「请选择填写方式」、客户信息输入区、「下一步」按钮。

### 页面快照（含全部 ref）

```yaml
- generic [ref=e3]:
  - generic [ref=e6]:
    - img "crm" [ref=e8]
    - menu [ref=e16]:
      - menuitem "首页" [ref=e17]: link [ref=e18]
      - menuitem "客户管理" [ref=e20]:
        - generic [ref=e21] [cursor=pointer]
        - menu [ref=e24]:
          - menuitem "客户查询" [ref=e25]: link "客户查询" [ref=e26]
          - menuitem "新建客户" [ref=e27]: link "新建客户" [ref=e28]
          - menuitem "内部客户" [ref=e29]: link [ref=e30]
          - menuitem "客户申请单" [ref=e31]: link [ref=e32]
          - menuitem "信用评估申请单列表" [ref=e33]: link [ref=e34]
      - menuitem "商机管理" [ref=e35]
      - menuitem "商机报备" [ref=e39]
      - menuitem "应标管理" [ref=e43]
      - menuitem "合同审批" [ref=e47]
      - menuitem "合同管理" [ref=e51]
      - menuitem "合同产品拆分" [ref=e55]
      - menuitem "后台" [ref=e59]
      - menuitem "报表" [ref=e63]: link [ref=e64]
      - menuitem "审批干预" [ref=e66]
      - menuitem "我的审批" [ref=e70]: link [ref=e71]
      - menuitem "代理设置" [ref=e73]: link [ref=e74]
      - menuitem "售前项目管理" [ref=e76]: link [ref=e77]
      - menuitem "测试页面" [ref=e79]: link [ref=e80]
  - generic [ref=e82]:
    - generic [ref=e83]:
      - img [ref=e86] [cursor=pointer]
      - list [ref=e89]:
        - listitem [ref=e90]: 客户管理>
        - listitem [ref=e91]: 新建客户
      - generic [ref=e112]:
        - img [ref=e113]
        - generic [ref=e114]: 杨承霖
        - generic [ref=e115]: 欢迎您
    - generic [ref=e122]:
      - generic [ref=e124]:
        - emphasis [ref=e125]: "*"
        - text: 请选择填写方式
      - generic [ref=e126]:
        - generic [ref=e133] [cursor=pointer]:
          - radio "本人填写" [checked] [ref=e135]
          - text: 本人填写
        - generic [ref=e143] [cursor=pointer]:
          - radio "代理人填写" [ref=e145]
          - text: 代理人填写
      - generic [ref=e147]: 客户信息
      - generic [ref=e148]:
        - generic [ref=e149]:
          - generic [ref=e150]: "客户名称:"
          - textbox "客户名称:" [ref=e154]: /placeholder: 请输入客户名称
        - generic [ref=e155]:
          - generic [ref=e156]: "统一社会信用代码:"
          - textbox "统一社会信用代码:" [ref=e160]: /placeholder: 请输入统一社会信用代码
      - button "下一步" [ref=e162] [cursor=pointer]
```

### 新建客户页 - 关键元素 ref 汇总（供 MCP 操作）

| 说明               | role / 类型 | name/label           | ref   |
|--------------------|-------------|----------------------|-------|
| 本人填写           | radio       | 本人填写             | e135  |
| 代理人填写         | radio       | 代理人填写           | e145  |
| 客户名称输入框     | textbox     | 客户名称:            | e154  |
| 统一社会信用代码   | textbox     | 统一社会信用代码:    | e160  |
| 下一步按钮         | button      | 下一步               | e162  |
| 客户查询菜单       | link        | 客户查询             | e26   |
| 新建客户菜单       | link        | 新建客户             | e28   |

### 新建客户页 - 关键元素多维度选择器（供 Playwright 精准定位）

| 元素名称           | role 选择器 | text / label 选择器 | xpath 示例（可从 DevTools 补充） |
|--------------------|-------------|----------------------|----------------------------------|
| 本人填写           | `role=radio, name=本人填写` | 单选文案「本人填写」 | `//input[@type='radio' and following-sibling::*[contains(.,'本人填写')]]` |
| 代理人填写         | `role=radio, name=代理人填写` | 单选文案「代理人填写」 | 同上 pattern |
| 客户名称输入框     | `role=textbox, name=客户名称:` | label「客户名称:」、placeholder「请输入客户名称」 | `//input[contains(@placeholder,'客户名称')]` |
| 统一社会信用代码输入框 | `role=textbox, name=统一社会信用代码:` | label「统一社会信用代码:」、placeholder「请输入统一社会信用代码」 | `//input[contains(@placeholder,'统一社会信用代码')]` |
| 下一步按钮         | `role=button, name=下一步` | 按钮文本「下一步」 | `//button[contains(.,'下一步')]` |
| 客户查询菜单       | `role=link, name=客户查询` | 链接文本「客户查询」 | `//a[contains(@href,'cust/query')]` |
| 新建客户菜单       | `role=link, name=新建客户` | 链接文本「新建客户」 | `//a[contains(@href,'newCreateCustomer/customer_sale')]` |

---

## 三、结构化操作步骤（由顶部「操作步骤」解析，供生成脚本参考）

以下与**本页顶部的「操作步骤」**及多维度选择器对应，生成 Playwright 时按此顺序与定位实现；若只改顶部文字，本段可作参考不必逐字改。

### 3.1 登录（SSO 登录页）

- **登录页 URL：** `https://sso-sandbox.asiainfo.com/login?service=...`（从 CRM 入口跳转得到）

1. 打开 URL：登录页（由访问 CRM 入口自动跳转）。
2. 定位元素：用户名输入框（role：textbox，name：用户名），输入值：`<用户名>`。
3. 定位元素：密码输入框（role：textbox，name：密码），输入值：`<密码>`。
4. 点击元素：登录按钮（role：button，text：登录）。
5. 断言：页面 URL 跳转为包含 `xin-uat.asiainfo.com/webapps/ai-crm-web`，且标题为「客户管理-客户查询」或包含「客户管理」。
6. 异常处理：若 10 秒内未跳转到 CRM 或出现「用户名/密码错误」提示，重试 2 次后终止并记录日志。

### 3.2 客户查询页

1. 打开 URL：`https://xin-uat.asiainfo.com/webapps/ai-crm-web/cust/query`（或登录后已在当前页则跳过）。
2. 定位元素：客户编号输入框（role：textbox，name：客户编号:），输入值：`87855`。
3. 点击元素：查询按钮（role：button，text：查 询）。
4. 断言：表格区域可见，且至少出现「客户编号」列表头或结果行。
5. 异常处理：若 15 秒内表格未加载，重试 1 次点击查询后终止并记录日志。

### 3.3 新建客户页

1. 点击元素：客户管理 → 新建客户（role：link，name：新建客户）；或直接打开 URL：`https://xin-uat.asiainfo.com/webapps/ai-crm-web/cust/newCreateCustomer/customer_sale`。
2. 定位元素：本人填写（role：radio，name：本人填写），点击选中（若已选中则跳过）。
3. 定位元素：客户名称输入框（role：textbox，name：客户名称:），输入值：`测试1`。
4. 定位元素：统一社会信用代码输入框（role：textbox，name：统一社会信用代码:），输入值：`1`。
5. 点击元素：下一步按钮（role：button，text：下一步）。
6. 断言：页面发生跳转或出现下一步表单/成功提示（依实际业务）。
7. 异常处理：若必填校验失败，记录校验文案并终止；若 10 秒内无响应，重试 1 次后终止并记录日志。

---

## 四、Playwright 选器参考（由 role/name 映射）

编写 Playwright 脚本时**优先使用 role + name**，其次 text/label，必要时再使用 xpath。ref 仅用于 Agent Browser 当次会话。

**客户查询页示例：**
- 客户编号：`page.get_by_role("textbox", name="客户编号:")` 或 `page.get_by_label("客户编号:")`
- 客户名称：`page.get_by_role("textbox", name="客户名称:")`
- 统一社会信用代码：`page.get_by_role("textbox", name="统一社会信用代码:")`
- 查询：`page.get_by_role("button", name="查 询")`
- 重置：`page.get_by_role("button", name="重 置")`

**新建客户页示例：**
- 本人填写：`page.get_by_role("radio", name="本人填写")`
- 代理人填写：`page.get_by_role("radio", name="代理人填写")`
- 客户名称：`page.get_by_role("textbox", name="客户名称:")`
- 统一社会信用代码：`page.get_by_role("textbox", name="统一社会信用代码:")`
- 下一步：`page.get_by_role("button", name="下一步")`

---

## 五、Playwright 代码生成指令（鲁棒性要求，效果最大化）

基于**本 md 顶部的操作步骤**与**第三部分结构化操作步骤**及**关键元素多维度选择器**生成 Playwright 代码时，请严格遵循以下要求，以使自动化鲁棒、可维护且高效：

1. **智能等待，禁止固定延时**
   - 使用 `page.wait_for_selector()`、`locator.wait_for(state='visible')`、`expect(locator).to_be_visible()` 等等待目标元素或状态，**禁止使用 `time.sleep()` 或 `page.wait_for_timeout()`**（除非明确要求固定间隔）。

2. **选择器优先级**
   - **优先使用 text/role 选择器**：`get_by_role(role, name=...)`、`get_by_text()`、`get_by_label()`；
   - 其次使用 `data-testid`（若快照或页面有标注）；
   - 再次使用稳定的 id、CSS；
   - 最后才使用 xpath，并尽量用相对路径与语义化条件。

3. **异常处理**
   - 核心操作（登录、点击查询、提交表单、关键断言）必须包在 **try/except** 中，捕获异常后记录日志（如 `logging`），并视情况重试（如登录失败重试 2 次）或终止并抛出/标记失败。

4. **代码模块化**
   - 拆分为可复用函数，例如：`login(page, url, username, password)`、`query_customer(page, cust_no)`、`fill_new_customer(page, name, credit_code)`；
   - 公共配置（URL、账号、超时时间）集中放在配置或常量中，便于维护。

5. **断言与可观测性**
   - 关键步骤后添加断言（如 URL、标题、可见文本、表格行数），使用 Playwright 的 `expect`，避免仅用 Python 原生 `assert`；
   - 关键步骤前后可打日志，便于排查失败原因。

生成代码时可直接引用本 md 中「关键元素多维度选择器」表格与「结构化操作步骤」的步骤编号，保证实现与文档一致。
