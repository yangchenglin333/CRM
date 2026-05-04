# Markdown 转 Word 工具 - 团队使用说明

## 一、适用场景

在生成需求文档相关产出时，通常先得到 **Markdown（.md）** 格式，例如：
- 需求提炼分析
- 测试关键点分析

如需提交给业务方或归档为 Word 格式，可使用本工具将 `.md` 转为 `.docx`。

---

## 二、分享给团队的方式

### 方式 A：分享整个「文件转换」文件夹（推荐）

将 `其他/文件转换/` 文件夹打包发给同事，包含：
- `Markdown转Word.py` - 主脚本
- `快速转换Markdown为Word.bat` - Windows 拖拽入口（可选）
- `Markdown转Word使用说明.md` - 本说明

### 方式 B：只分享脚本

若同事已有 Python 环境，只需分享 `Markdown转Word.py` 即可。

---

## 三、使用前准备

### 1. 安装 Python

确保已安装 Python 3.6+，命令行输入 `python --version` 可检查。

### 2. 安装依赖

```bash
pip install python-docx
```

---

## 四、使用方法

### 方法 1：拖拽到 bat 上（Windows，最简单）

1. 双击运行一次 `快速转换Markdown为Word.bat`，确认能正常打开
2. 将 `.md` 文件拖到 `快速转换Markdown为Word.bat` 上
3. 同目录下会生成同名 `.docx` 文件

### 方法 2：命令行

在**脚本所在目录**或**项目根目录**打开命令行，执行：

```bash
python Markdown转Word.py "你的md文件路径"
```

**示例：**

```bash
# 转换单个文件（输出到同目录，文件名相同、扩展名为 .docx）
python Markdown转Word.py "需求文档/需求理解输出/20260203_ARM域内外配置_需求提炼分析.md"

# 使用绝对路径
python Markdown转Word.py "D:\文档\测试关键点分析.md"
```

### 方法 3：在 Cursor / 其他 IDE 中运行

在脚本中调用函数：

```python
from Markdown转Word import md_to_docx

# 转换，输出到同目录同名 .docx
md_to_docx("需求文档/需求理解输出/xxx_需求提炼分析.md")

# 指定输出路径
md_to_docx("输入.md", "输出.docx")
```

---

## 五、生成需求文档时的典型流程

1. **在 Cursor 中**根据需求文档生成「需求提炼分析」「测试关键点分析」等，得到 `.md` 文件
2. **使用本工具**将 `.md` 转为 `.docx`
3. **将 .docx** 发给业务方或归档

---

## 六、常见问题

**Q：转换后表格错乱？**  
A：确保 Markdown 表格格式正确，表头与分隔行 `|---|---|` 完整。

**Q：中文乱码？**  
A：脚本使用 UTF-8 编码，一般不会乱码。若 Word 打开异常，可尝试「另存为」选择 UTF-8 编码。

**Q：提示「需要安装 python-docx」？**  
A：执行 `pip install python-docx` 安装依赖。
