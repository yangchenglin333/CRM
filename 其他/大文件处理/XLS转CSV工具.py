# -*- coding: utf-8 -*-
"""
XLS 转 CSV 工具（仅处理 .xls / Excel 97-2003）

用途：将 .xls 文件转换为 CSV，输出 UTF-8 BOM，便于在 Cursor 中查看和 Excel 正确打开中文。

使用方法：
  1. 拖放：将 .xls 文件拖到 快速转换XLS为CSV.bat 上
  2. 命令行：python XLS转CSV工具.py <xls文件路径> [输出csv路径]
  3. 指定工作表：python XLS转CSV工具.py --sheet 1 文件.xls
  4. 批量：python XLS转CSV工具.py <文件夹路径>

依赖：xlrd（缺失时自动 pip 安装）
"""
import csv
import os
import subprocess
import sys

xlrd = None


def _ensure_xlrd():
    global xlrd
    if xlrd is not None:
        return
    try:
        import xlrd as _x
        xlrd = _x
        return
    except ImportError:
        pass
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "xlrd", "-q"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        import xlrd as _x
        xlrd = _x
    except Exception as e:
        raise ImportError("请安装 xlrd：pip install xlrd") from e


def xls_to_csv(xls_path: str, csv_path: str = None, sheet_index: int = 0) -> str:
    """将 .xls 转为 CSV，返回生成的 csv 路径。"""
    _ensure_xlrd()
    if not os.path.exists(xls_path):
        raise FileNotFoundError(f"文件不存在: {xls_path}")
    if not xls_path.lower().endswith(".xls"):
        raise ValueError(f"仅支持 .xls 格式: {xls_path}")

    if csv_path is None:
        csv_path = os.path.splitext(xls_path)[0] + ".csv"

    book = xlrd.open_workbook(xls_path)
    sheet = book.sheet_by_index(sheet_index)

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for row_idx in range(sheet.nrows):
            row = sheet.row_values(row_idx)
            writer.writerow([
                "" if c is None else (str(c).strip() if isinstance(c, str) else str(c))
                for c in row
            ])
    return csv_path


def convert_folder(folder_path: str, output_dir: str = None) -> list:
    """批量转换文件夹内所有 .xls 文件。"""
    if output_dir is None:
        output_dir = folder_path
    os.makedirs(output_dir, exist_ok=True)
    results = []
    for name in sorted(os.listdir(folder_path)):
        if not name.lower().endswith(".xls"):
            continue
        path = os.path.join(folder_path, name)
        if not os.path.isfile(path):
            continue
        try:
            out = xls_to_csv(path, os.path.join(output_dir, os.path.splitext(name)[0] + ".csv"))
            results.append(out)
            print(f"✓ {name} -> {os.path.basename(out)}")
        except Exception as e:
            print(f"✗ {name}: {e}")
    return results


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        print("\n示例：")
        print('  python XLS转CSV工具.py "报表.xls"')
        print('  python XLS转CSV工具.py "报表.xls" "输出.csv"')
        print('  python XLS转CSV工具.py --sheet 1 "多表.xls"')
        print('  python XLS转CSV工具.py "文件夹路径"  # 批量')
        sys.exit(0)

    sheet_index = 0
    args = list(sys.argv[1:])
    if args and args[0] == "--sheet" and len(args) >= 3:
        try:
            sheet_index = int(args[1])
        except ValueError:
            print("✗ --sheet 后应为数字")
            sys.exit(1)
        args = args[2:]

    if not args:
        print("✗ 请指定 .xls 文件或文件夹路径")
        sys.exit(1)

    path = args[0].strip('"').strip("'")
    csv_out = args[1].strip('"').strip("'") if len(args) > 1 else None

    if not os.path.exists(path):
        print(f"✗ 路径不存在: {path}")
        sys.exit(1)

    if os.path.isfile(path):
        try:
            out = xls_to_csv(path, csv_out, sheet_index=sheet_index)
            print(f"✓ 转换完成: {out}")
        except Exception as e:
            print(f"✗ 转换失败: {e}")
            sys.exit(1)
    else:
        convert_folder(path, csv_out if csv_out and os.path.isdir(csv_out) else None)


if __name__ == "__main__":
    main()
