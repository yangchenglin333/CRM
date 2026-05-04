---
name: "md-to-word-converter"
description: "将Markdown文档转换为Word格式。当用户提供MD文件并要求转换为Word文档时调用。"
---

# Markdown 转 Word 文档转换器

## 功能说明

将 Markdown 格式文档转换为 Word 格式，支持批量转换，自定义样式设置。

## 应用场景

- 需求文档格式转换
- 测试用例导出为Word
- PRD文档格式转换
- 报告导出

## 工作流程

### Step 1: 准备MD文件
确保Markdown文件语法正确：
- 标题层级使用 `#`
- 列表使用 `-` 或 `1.`
- 代码块使用 ```
- 表格使用标准语法

### Step 2: 执行转换
```bash
# 命令行转换
python3 Markdown转Word.py input.md output.docx

# 批量转换
python3 Markdown转Word.py ./docs/ -o ./output/
```

### Step 3: 检查结果
- 确认格式正确
- 检查图片嵌入
- 验证目录结构

## 文件位置

```
其他/文件转换/
├── Markdown转Word.py          # 转换工具
├── Markdown转Word使用说明.md  # 使用说明
└── 快速转换Markdown为Word.bat # Windows快速转换脚本
```

## 转换规则

| MD元素 | Word元素 |
|--------|----------|
| # 标题1 | 标题1 |
| ## 标题2 | 标题2 |
| **粗体** | 粗体 |
| *斜体* | 斜体 |
| `代码` | 嵌入式等宽字体 |
| ```代码块``` | 代码块（保留格式） |
| 表格 | Word表格 |
| 图片 | 嵌入式图片 |
| 链接 | 超链接 |

## 使用示例

### 单文件转换
```bash
python3 Markdown转Word.py 需求文档.md 需求文档.docx
```

### 批量转换
```bash
python3 Markdown转Word.py ./测试用例/ -o ./输出/
```

### 指定样式
```bash
python3 Markdown转Word.py input.md output.docx --style formal
```

## 注意事项

1. **图片路径**：确保图片使用相对路径
2. **编码格式**：使用UTF-8编码
3. **表格嵌套**：避免复杂的嵌套表格
4. **特殊字符**：检查数学公式和特殊符号
