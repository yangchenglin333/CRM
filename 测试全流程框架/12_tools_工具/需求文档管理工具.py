#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
需求文档管理工具（统一版）
合并了所有需求文档相关的操作功能：
1. 添加日期前缀（使文件浏览器按时间排序）
2. 修复错误前缀（79731117_20260114_xxx → 20260114_xxx）
3. 校验文件名是否符合 YYYYMMDD_ 格式
4. 移除文件名中的中文日期
5. 按时间排序并生成列表
"""
import atexit
import os
import sys

# 脚本结束时自动清理 __pycache__
def _find_project_root():
    p = os.path.dirname(os.path.abspath(__file__))
    while p and p != os.path.dirname(p):
        if os.path.exists(os.path.join(p, ".cursorrules")):
            return p
        p = os.path.dirname(p)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_root = _find_project_root()
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
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional


def extract_date_from_chinese_format(filename: str) -> Tuple[Optional[int], Optional[int], Optional[int], bool]:
    """
    从文件名中提取中文日期格式的日期
    
    匹配格式：YYYY年MM月DD日
    返回：(年, 月, 日, 是否找到日期)
    """
    pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    match = re.search(pattern, filename)
    
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        return (year, month, day, True)
    return (None, None, None, False)


def extract_date_from_prefix(filename: str) -> Tuple[Optional[int], Optional[int], Optional[int], bool]:
    """
    从文件名前缀中提取日期
    
    匹配格式：YYYYMMDD_
    返回：(年, 月, 日, 是否找到日期)
    """
    pattern = r'^(\d{4})(\d{2})(\d{2})_'
    match = re.match(pattern, filename)
    
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        return (year, month, day, True)
    return (None, None, None, False)


def get_file_date(filename: str) -> datetime:
    """
    从文件名中提取日期（优先从前缀提取，其次从中文格式提取）
    
    返回：datetime对象，用于排序
    """
    # 优先从日期前缀提取
    year, month, day, has_prefix = extract_date_from_prefix(filename)
    if has_prefix:
        try:
            return datetime(year, month, day)
        except ValueError:
            pass
    
    # 其次从中文日期格式提取
    year, month, day, has_chinese = extract_date_from_chinese_format(filename)
    if has_chinese:
        try:
            return datetime(year, month, day)
        except ValueError:
            pass
    
    # 都没有则返回一个很早的日期，使其排在最后
    return datetime(1900, 1, 1)


# ==================== 功能1：添加日期前缀 ====================

def add_date_prefix(directory: str, dry_run: bool = True):
    """
    在文件名前添加日期前缀，使文件浏览器按时间排序
    格式：YYYYMMDD_原文件名.mdc
    """
    if not os.path.exists(directory):
        print(f"错误：目录不存在: {directory}")
        return
    
    files = [f for f in os.listdir(directory) if f.endswith('.mdc')]
    
    if not files:
        print(f"目录中没有找到.mdc文件: {directory}")
        return
    
    # 提取日期并排序
    files_with_dates = []
    for filename in files:
        # 检查是否已经有日期前缀
        if re.match(r'^\d{8}_', filename):
            continue  # 跳过已有前缀的文件
            
        year, month, day, has_date = extract_date_from_chinese_format(filename)
        if has_date:
            date_str = f"{year:04d}{month:02d}{day:02d}"
            new_filename = f"{date_str}_{filename}"
            files_with_dates.append((datetime(year, month, day), filename, new_filename))
        else:
            # 没有日期的文件，使用00000000前缀，排在最后
            new_filename = f"00000000_{filename}"
            files_with_dates.append((datetime(1900, 1, 1), filename, new_filename))
    
    # 按日期排序
    files_with_dates.sort(key=lambda x: x[0], reverse=True)
    
    print("=" * 80)
    if dry_run:
        print("预览模式：以下是将要执行的重命名操作（不会实际修改文件）")
    else:
        print("执行重命名操作：添加日期前缀")
    print("=" * 80)
    print(f"\n目录：{os.path.abspath(directory)}\n")
    
    renamed_count = 0
    skipped_count = 0
    
    for date_obj, old_filename, new_filename in files_with_dates:
        old_path = os.path.join(directory, old_filename)
        new_path = os.path.join(directory, new_filename)
        
        # 如果新文件名已存在，跳过
        if os.path.exists(new_path) and old_filename != new_filename:
            print(f"[跳过] {old_filename}")
            print(f"   原因：目标文件已存在\n")
            skipped_count += 1
            continue
        
        if old_filename == new_filename:
            skipped_count += 1
            continue
        
        if dry_run:
            print(f"[将重命名]")
            print(f"   旧名称：{old_filename}")
            print(f"   新名称：{new_filename}\n")
        else:
            try:
                os.rename(old_path, new_path)
                print(f"[已重命名] {old_filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"[重命名失败] {old_filename}")
                print(f"   错误：{e}\n")
    
    print("=" * 80)
    if dry_run:
        print(f"预览完成！共 {len(files_with_dates)} 个文件需要重命名")
        print(f"\n如需执行实际重命名，请运行：")
        print(f"python 需求文档管理工具.py --add-prefix --execute")
    else:
        print(f"重命名完成！")
        print(f"成功：{renamed_count} 个文件")
        print(f"跳过：{skipped_count} 个文件")


# ==================== 统一目录与扩展名配置 ====================

# 需求文档、需求理解输出、CSV、Xmind 四个目录的配置：(相对路径, 扩展名列表)
# 文件按修改时间排序时，日期大的在上（时间由大到小）
UNIFIED_DIRS = [
    ("需求文档/需求文档存放处", [".mdc"]),
    ("需求文档/需求理解输出", [".md"]),
    ("testcases/CSV", [".csv"]),
    ("testcases/Xmind", [".md"]),
]

# 支持的前缀修复扩展名
PREFIX_EXTENSIONS = (".mdc", ".csv", ".md")


# ==================== 功能2：修复错误前缀（ID前缀+日期 → 仅日期） ====================

def fix_wrong_prefix(directory: str, dry_run: bool = True, extensions: Optional[Tuple[str, ...]] = None):
    """
    修复错误的前缀格式：将 79731117_20260114_xxx 改为 20260114_xxx
    
    错误格式：非日期数字_YYYYMMDD_模块名.扩展名（如 79731117_20260114_xxx.mdc/.csv/.md）
    正确格式：YYYYMMDD_模块名.扩展名
    
    支持 .mdc（需求文档）、.csv（测试用例）、.md（Xmind）
    """
    if not os.path.exists(directory):
        print(f"错误：目录不存在: {directory}")
        return
    
    ext_tuple = extensions or PREFIX_EXTENSIONS
    ext_suffix = "|".join(re.escape(e) for e in ext_tuple)
    files = [f for f in os.listdir(directory) if any(f.endswith(e) for e in ext_tuple)]
    
    if not files:
        print(f"目录中没有找到 {ext_tuple} 文件: {directory}")
        return
    
    # 匹配错误格式：8位数字_8位数字_xxx.扩展名，且第一个8位不是有效年份(2020-2030)
    wrong_prefix_pattern = re.compile(r'^(\d{8})_(\d{8})_(.+(' + ext_suffix + r'))$')
    
    files_to_rename = []
    for filename in files:
        match = wrong_prefix_pattern.match(filename)
        if match:
            first_prefix = match.group(1)  # 如 79731117
            date_prefix = match.group(2)   # 如 20260114
            rest = match.group(3)          # 如 客户管理系统合同风险贯通需求文档001.mdc
            
            # 检查第一个前缀是否为非日期（年份不在2020-2030）
            year_part = int(first_prefix[:4])
            if year_part < 2020 or year_part > 2030:
                new_filename = f"{date_prefix}_{rest}"
                files_to_rename.append((filename, new_filename))
    
    if not files_to_rename:
        print("所有文件名格式正确，无需修复。")
        return
    
    print("=" * 80)
    if dry_run:
        print("预览模式：以下是将要执行的重命名操作（不会实际修改文件）")
    else:
        print("执行重命名操作：修复错误前缀（移除ID前缀，保留日期前缀）")
    print("=" * 80)
    print(f"\n目录：{os.path.abspath(directory)}\n")
    
    renamed_count = 0
    skipped_count = 0
    
    for old_filename, new_filename in files_to_rename:
        old_path = os.path.join(directory, old_filename)
        new_path = os.path.join(directory, new_filename)
        
        if os.path.exists(new_path) and old_filename != new_filename:
            print(f"[跳过] {old_filename}")
            print(f"   原因：目标文件已存在\n")
            skipped_count += 1
            continue
        
        if dry_run:
            print(f"[将重命名]")
            print(f"   旧名称：{old_filename}")
            print(f"   新名称：{new_filename}\n")
        else:
            try:
                os.rename(old_path, new_path)
                print(f"[已重命名] {old_filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"[重命名失败] {old_filename}")
                print(f"   错误：{e}\n")
    
    print("=" * 80)
    if dry_run:
        print(f"预览完成！共 {len(files_to_rename)} 个文件需要修复")
        print(f"\n如需执行实际重命名，请运行：")
        print(f"python 需求文档管理工具.py --fix-prefix --execute")
    else:
        print(f"修复完成！")
        print(f"成功：{renamed_count} 个文件")
        print(f"跳过：{skipped_count} 个文件")


def validate_naming(directory: str, extensions: Optional[Tuple[str, ...]] = None) -> Tuple[bool, List[str]]:
    """
    校验目录中的文件名是否符合 YYYYMMDD_ 格式
    返回：(是否全部通过, 错误文件列表)
    支持 .mdc、.csv、.md
    """
    if not os.path.exists(directory):
        return False, [f"目录不存在: {directory}"]
    
    ext_tuple = extensions or PREFIX_EXTENSIONS
    ext_suffix = "|".join(re.escape(e) for e in ext_tuple)
    files = [f for f in os.listdir(directory) if any(f.endswith(e) for e in ext_tuple)]
    errors = []
    
    # 扩展名组已含点号，如 (\.mdc|\.csv|\.md)
    correct_pattern = re.compile(r'^(\d{4})(\d{2})(\d{2})_.+(' + ext_suffix + r')$')
    
    for filename in files:
        match = correct_pattern.match(filename)
        if not match:
            errors.append(f"格式错误：{filename}（应以 YYYYMMDD_ 开头）")
            continue
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if year < 2020 or year > 2030 or month < 1 or month > 12 or day < 1 or day > 31:
            errors.append(f"日期无效：{filename}")
    
    return len(errors) == 0, errors


# 根目录文件夹固定排序（由上到下）：rules(.cursor)、需求文档、testcases、其他、自动化脚本、.vscode
_FOLDER_ORDER = (".cursor", "需求文档", "testcases", "其他", "自动化脚本", ".vscode")


def _touch_folders_for_order(project_root: str):
    """touch 根目录文件夹，使 explorer.sortOrder=modified 时按固定顺序显示（由上到下）；
    固定六项之外的文件夹统一设为更旧 mtime，排在最下方。"""
    import time
    now = time.time()
    fixed_set = set(_FOLDER_ORDER)
    n = len(_FOLDER_ORDER) - 1
    # 1) 固定六项：倒序 touch，.cursor 最新(now)，.vscode 最旧(now-n)
    for i, rel_path in enumerate(reversed(_FOLDER_ORDER)):
        path = os.path.join(project_root, rel_path)
        if os.path.isdir(path):
            try:
                ts = now - (n - i)
                os.utime(path, (ts, ts))
            except Exception:
                pass
        if rel_path == ".cursor":
            rules_path = os.path.join(project_root, ".cursor", "rules")
            if os.path.isdir(rules_path):
                try:
                    os.utime(rules_path, (now, now))
                except Exception:
                    pass
    # 2) 其他根目录文件夹（如「项目」）：设为更旧 mtime，排在最下方
    try:
        other_dirs = [d for d in os.listdir(project_root)
                      if os.path.isdir(os.path.join(project_root, d)) and d not in fixed_set]
        for j, name in enumerate(sorted(other_dirs)):
            path = os.path.join(project_root, name)
            try:
                os.utime(path, (now - n - 1 - j, now - n - 1 - j))
            except Exception:
                pass
    except Exception:
        pass


def _touch_cursor_for_top_position(project_root: str):
    """兼容旧逻辑：touch 文件夹使 rules 置顶（现由 _touch_folders_for_order 统一处理）"""
    _touch_folders_for_order(project_root)


def _get_project_root(from_path: str) -> str:
    """从任意路径向上查找含 .cursorrules 的项目根目录"""
    path = os.path.abspath(from_path)
    if os.path.isfile(path):
        path = os.path.dirname(path)
    while path and path != os.path.dirname(path):
        if os.path.exists(os.path.join(path, ".cursorrules")):
            return path
        path = os.path.dirname(path)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fix_mtime_by_date(directory: str, dry_run: bool = True, extensions: Optional[Tuple[str, ...]] = None):
    """
    根据文件名中的日期前缀，同步文件的修改时间
    使「按修改时间排序」时，日期越大的文件显示越靠上（最新在前）
    支持 .mdc、.csv、.md
    """
    if not os.path.exists(directory):
        print(f"错误：目录不存在: {directory}")
        return
    
    ext_tuple = extensions or PREFIX_EXTENSIONS
    ext_suffix = "|".join(re.escape(e) for e in ext_tuple)
    files = [f for f in os.listdir(directory) if any(f.endswith(e) for e in ext_tuple)]
    correct_pattern = re.compile(r'^(\d{4})(\d{2})(\d{2})_.+(' + ext_suffix + r')$')
    
    to_fix = []
    for filename in files:
        match = correct_pattern.match(filename)
        if match:
            year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            try:
                dt = datetime(year, month, day, 12, 0, 0)
                to_fix.append((filename, dt))
            except ValueError:
                pass
    
    if not to_fix:
        print("没有找到符合 YYYYMMDD_ 格式的文件，无需同步修改时间。")
        return
    
    print("=" * 80)
    if dry_run:
        print("预览模式：以下文件将同步修改时间（按文件名日期）")
    else:
        print("执行：根据文件名日期同步修改时间")
    print("=" * 80)
    print(f"\n目录：{os.path.abspath(directory)}\n")
    
    import time
    fixed = 0
    for filename, dt in to_fix:
        path = os.path.join(directory, filename)
        mtime = time.mktime(dt.timetuple())
        if dry_run:
            print(f"[将同步] {filename} -> 修改时间设为 {dt.strftime('%Y-%m-%d')}")
        else:
            try:
                os.utime(path, (mtime, mtime))
                fixed += 1
            except Exception as e:
                print(f"[失败] {filename}: {e}")
    
    if not dry_run:
        print(f"\n完成：已同步 {fixed} 个文件的修改时间")
        # 不在本函数内 touch，由调用方在所有 fix_mtime 完成后统一 touch，避免需求文档子目录被后续处理更新 mtime 后超过 .cursor


# ==================== 功能3：移除中文日期 ====================

def remove_chinese_date_from_filename(filename: str) -> str:
    """
    移除文件名中的中文日期部分
    
    例如：
    输入：20251212_经理工作台需求文档2025年12月12日001.mdc
    输出：20251212_经理工作台需求文档001.mdc
    """
    pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    new_filename = re.sub(pattern, '', filename)
    return new_filename


def clean_chinese_date(directory: str, dry_run: bool = True):
    """
    清理文件名：移除中文日期，只保留前缀日期
    """
    if not os.path.exists(directory):
        print(f"错误：目录不存在: {directory}")
        return
    
    files = [f for f in os.listdir(directory) if f.endswith('.mdc')]
    
    if not files:
        print(f"目录中没有找到.mdc文件: {directory}")
        return
    
    # 处理文件：移除中文日期
    files_to_rename = []
    for filename in files:
        pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        if re.search(pattern, filename):
            new_filename = remove_chinese_date_from_filename(filename)
            if new_filename != filename:
                files_to_rename.append((filename, new_filename))
    
    if not files_to_rename:
        print("所有文件名都已清理完成，无需重命名。")
        return
    
    print("=" * 80)
    if dry_run:
        print("预览模式：以下是将要执行的重命名操作（不会实际修改文件）")
    else:
        print("执行重命名操作：移除文件名中的中文日期")
    print("=" * 80)
    print(f"\n目录：{os.path.abspath(directory)}\n")
    
    renamed_count = 0
    skipped_count = 0
    
    for old_filename, new_filename in files_to_rename:
        old_path = os.path.join(directory, old_filename)
        new_path = os.path.join(directory, new_filename)
        
        # 如果新文件名已存在，跳过
        if os.path.exists(new_path) and old_filename != new_filename:
            print(f"[跳过] {old_filename}")
            print(f"   原因：目标文件已存在\n")
            skipped_count += 1
            continue
        
        if dry_run:
            print(f"[将重命名]")
            print(f"   旧名称：{old_filename}")
            print(f"   新名称：{new_filename}\n")
        else:
            try:
                os.rename(old_path, new_path)
                print(f"[已重命名] {old_filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"[重命名失败] {old_filename}")
                print(f"   错误：{e}\n")
    
    print("=" * 80)
    if dry_run:
        print(f"预览完成！共 {len(files_to_rename)} 个文件需要重命名")
        print(f"\n如需执行实际重命名，请运行：")
        print(f"python 需求文档管理工具.py --clean --execute")
    else:
        print(f"重命名完成！")
        print(f"成功：{renamed_count} 个文件")
        print(f"跳过：{skipped_count} 个文件")


# ==================== 功能3：排序并生成列表 ====================

def sort_and_list(directory: str, output_file: Optional[str] = None):
    """
    对需求文档目录中的文件按时间降序排序，并生成列表
    """
    if not os.path.exists(directory):
        print(f"错误：目录不存在: {directory}")
        return
    
    files = [f for f in os.listdir(directory) if f.endswith('.mdc')]
    
    if not files:
        print(f"目录中没有找到.mdc文件: {directory}")
        return
    
    # 按日期降序排序
    sorted_files = sorted(files, key=get_file_date, reverse=True)
    
    # 生成列表内容
    lines = []
    lines.append("# 需求文档列表（按时间降序排序）\n")
    lines.append(f"生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
    lines.append(f"目录：{os.path.abspath(directory)}\n")
    lines.append(f"共 {len(sorted_files)} 个文件\n\n")
    lines.append("| 序号 | 日期 | 文件名 |\n")
    lines.append("|------|------|--------|\n")
    
    # 提取日期用于显示
    chinese_date_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    prefix_date_pattern = r'^(\d{4})(\d{2})(\d{2})_'
    
    for i, filename in enumerate(sorted_files, 1):
        date_str = "无日期"
        
        # 优先从日期前缀提取
        prefix_match = re.match(prefix_date_pattern, filename)
        if prefix_match:
            year = prefix_match.group(1)
            month = prefix_match.group(2)
            day = prefix_match.group(3)
            date_str = f"{year}年{month}月{day}日"
        else:
            # 其次从中文日期格式提取
            chinese_match = re.search(chinese_date_pattern, filename)
            if chinese_match:
                date_str = chinese_match.group(0)
        
        lines.append(f"| {i} | {date_str} | {filename} |\n")
    
    content = "".join(lines)
    
    # 输出到控制台
    print(content)
    
    # 如果指定了输出文件，写入文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n排序列表已保存到：{output_file}")


# ==================== 主函数 ====================

def _get_extensions_for_dir(directory: str) -> Tuple[str, ...]:
    """根据目录路径推断适用的文件扩展名"""
    if "CSV" in directory or "csv" in directory.lower():
        return (".csv",)  # 测试用例仅生成 CSV
    if "Xmind" in directory or "xmind" in directory.lower():
        return (".md",)
    return (".mdc",)


def print_usage():
    """打印使用说明"""
    print("=" * 80)
    print("需求文档管理工具（统一版：需求文档 + CSV + Xmind）")
    print("=" * 80)
    print("\n使用方法：")
    print("  python 需求文档管理工具.py [选项] [参数]")
    print("\n功能选项：")
    print("  --add-prefix, --prefix    添加日期前缀（从中文日期提取，仅.mdc）")
    print("  --fix-prefix              修复错误前缀（ID_YYYYMMDD_xxx → YYYYMMDD_xxx）")
    print("  --fix-mtime               同步修改时间（使按修改时间排序时，日期大的在上）")
    print("  --touch-cursor            仅 touch .cursor/rules 使其置顶（轻量，可配合 folderOpen 自动执行）")
    print("  --clean, --remove         移除文件名中的中文日期（仅.mdc）")
    print("  --validate                校验文件名是否符合 YYYYMMDD_ 格式")
    print("  --sort, --list            按时间排序并生成列表")
    print("\n通用选项：")
    print("  --execute                 执行实际操作（默认是预览模式）")
    print("  --all                     对四个目录统一执行（需求文档存放处、需求理解输出、CSV、Xmind）")
    print("  --output <文件路径>       指定输出文件路径（用于--sort模式）")
    print("  --dir <目录路径>          指定目录（默认：需求文档/需求文档存放处）")
    print("\n示例：")
    print("  # 预览：添加日期前缀")
    print("  python 需求文档管理工具.py --add-prefix")
    print("\n  # 执行：添加日期前缀")
    print("  python 需求文档管理工具.py --add-prefix --execute")
    print("\n  # 预览：移除中文日期")
    print("  python 需求文档管理工具.py --clean")
    print("\n  # 执行：移除中文日期")
    print("  python 需求文档管理工具.py --clean --execute")
    print("\n  # 排序并显示列表")
    print("  python 需求文档管理工具.py --sort")
    print("\n  # 排序并保存到文件")
    print("  python 需求文档管理工具.py --sort --output 需求文档/需求文档列表.md")
    print("\n  # 对三个目录统一修复前缀并同步修改时间（倒序排序）")
    print("  python 需求文档管理工具.py --fix-prefix --fix-mtime --all --execute")
    print("=" * 80)


def main():
    """主函数"""
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print_usage()
        return
    
    # 默认目录
    directory = "需求文档/需求文档存放处"
    dry_run = "--execute" not in sys.argv
    output_file = None
    use_all_dirs = "--all" in sys.argv
    
    # 解析命令行参数
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ['--dir', '-d']:
            if i + 1 < len(sys.argv):
                directory = sys.argv[i + 1]
                i += 2
            else:
                print("错误：--dir 参数需要指定目录路径")
                return
        elif arg in ['--output', '-o']:
            if i + 1 < len(sys.argv):
                output_file = sys.argv[i + 1]
                i += 2
            else:
                print("错误：--output 参数需要指定文件路径")
                return
        else:
            i += 1
    
    # 获取项目根目录
    base_dir = _root
    full_path = os.path.join(base_dir, directory) if not os.path.isabs(directory) else directory
    
    # 执行相应功能
    if '--touch-cursor' in sys.argv:
        _touch_cursor_for_top_position(base_dir)
        print("[OK] 已 touch 根目录文件夹，固定顺序：rules、需求文档、testcases、其他、自动化脚本、.vscode")
        return
    
    if '--add-prefix' in sys.argv or '--prefix' in sys.argv:
        if use_all_dirs:
            print("注意：--add-prefix 仅支持需求文档目录，--all 时仅处理需求文档存放处")
        if dry_run:
            print("注意：这是预览模式，不会实际修改文件")
            print("   如需执行实际重命名，请添加 --execute 参数\n")
        add_date_prefix(os.path.join(base_dir, directory) if not os.path.isabs(directory) else directory, dry_run)
    
    elif '--fix-prefix' in sys.argv:
        if dry_run:
            print("注意：这是预览模式，不会实际修改文件")
            print("   如需执行实际重命名，请添加 --execute 参数\n")
        if use_all_dirs:
            for rel_path, ext_list in UNIFIED_DIRS:
                full_path = os.path.join(base_dir, rel_path)
                exts = tuple(ext_list) if ext_list else PREFIX_EXTENSIONS
                print(f"\n{'='*80}\n目录：{full_path} （扩展名：{exts}）\n{'='*80}")
                fix_wrong_prefix(full_path, dry_run, exts)
        else:
            full_path = os.path.join(base_dir, directory) if not os.path.isabs(directory) else directory
            fix_wrong_prefix(full_path, dry_run, _get_extensions_for_dir(full_path))
    
    elif '--fix-mtime' in sys.argv:
        if dry_run:
            print("注意：这是预览模式，不会实际修改文件")
            print("   如需执行，请添加 --execute 参数\n")
        if use_all_dirs:
            for rel_path, ext_list in UNIFIED_DIRS:
                full_path = os.path.join(base_dir, rel_path)
                exts = tuple(ext_list) if ext_list else PREFIX_EXTENSIONS
                print(f"\n{'='*80}\n目录：{full_path} （扩展名：{exts}）\n{'='*80}")
                fix_mtime_by_date(full_path, dry_run, exts)
            if not dry_run:
                _touch_folders_for_order(base_dir)
                print("\n✓ 已 touch 根目录文件夹，固定顺序：.cursor/rules、需求文档、testcases、其他、自动化脚本、.vscode")
        else:
            full_path = os.path.join(base_dir, directory) if not os.path.isabs(directory) else directory
            fix_mtime_by_date(full_path, dry_run, _get_extensions_for_dir(full_path))
            if not dry_run:
                _touch_folders_for_order(base_dir)
                print("\n✓ 已 touch 根目录文件夹，固定顺序：.cursor/rules、需求文档、testcases、其他、自动化脚本、.vscode")
    
    elif '--validate' in sys.argv:
        if use_all_dirs:
            all_passed = True
            for rel_path, ext_list in UNIFIED_DIRS:
                full_path = os.path.join(base_dir, rel_path)
                exts = tuple(ext_list) if ext_list else PREFIX_EXTENSIONS
                passed, errors = validate_naming(full_path, exts)
                if passed:
                    print(f"✓ [{rel_path}] 校验通过")
                else:
                    all_passed = False
                    print(f"✗ [{rel_path}] 校验失败：")
                    for err in errors:
                        print(f"  - {err}")
            if not all_passed:
                print("\n建议运行：python run_doc_tool.py --fix-prefix --all --execute 修复错误前缀")
            else:
                # 校验通过后自动执行 fix-mtime 同步修改时间
                print("\n正在执行 fix-mtime 同步修改时间...")
                for rel_path, ext_list in UNIFIED_DIRS:
                    full_path = os.path.join(base_dir, rel_path)
                    exts = tuple(ext_list) if ext_list else PREFIX_EXTENSIONS
                    fix_mtime_by_date(full_path, dry_run=False, extensions=exts)
                _touch_folders_for_order(base_dir)
                print("✓ fix-mtime 执行完成（.cursor/rules 已置顶）")
        else:
            full_path = os.path.join(base_dir, directory) if not os.path.isabs(directory) else directory
            passed, errors = validate_naming(full_path, _get_extensions_for_dir(full_path))
            if passed:
                print("✓ 校验通过：所有文件名符合 YYYYMMDD_ 格式")
                # 校验通过后自动执行 fix-mtime
                print("\n正在执行 fix-mtime 同步修改时间...")
                fix_mtime_by_date(full_path, dry_run=False, extensions=_get_extensions_for_dir(full_path))
                _touch_folders_for_order(base_dir)
                print("✓ fix-mtime 执行完成（.cursor/rules 已置顶）")
            else:
                print("✗ 校验失败：以下文件命名格式错误：")
                for err in errors:
                    print(f"  - {err}")
                print("\n建议运行：python run_doc_tool.py --fix-prefix --execute 修复错误前缀")
    
    elif '--clean' in sys.argv or '--remove' in sys.argv:
        if dry_run:
            print("注意：这是预览模式，不会实际修改文件")
            print("   如需执行实际重命名，请添加 --execute 参数\n")
        clean_chinese_date(full_path, dry_run)
    
    elif '--sort' in sys.argv or '--list' in sys.argv:
        if output_file:
            # 如果指定了输出文件，使用绝对路径
            if not os.path.isabs(output_file):
                output_file = os.path.join(base_dir, output_file)
        else:
            # 默认输出文件
            output_file = os.path.join(base_dir, "需求文档/需求文档列表（按时间排序）.md")
        sort_and_list(full_path, output_file)
    
    else:
        print("错误：请指定功能选项（--add-prefix、--fix-prefix、--fix-mtime、--touch-cursor、--clean、--validate 或 --sort）")
        print_usage()


if __name__ == "__main__":
    main()
