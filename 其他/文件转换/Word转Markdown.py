# -*- coding: utf-8 -*-
"""
Word文档转Markdown工具
使用pandoc将docx文件转换为markdown格式
"""

import os
import sys
import subprocess
import argparse

def docx_to_md(input_path, output_path=None, preserve_links=True):
    """
    将docx文件转换为markdown格式

    Args:
        input_path: 输入的docx文件路径
        output_path: 输出的md文件路径，如果为None则自动生成
        preserve_links: 是否保留链接，默认为True

    Returns:
        转换后的md文件路径
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"文件不存在: {input_path}")

    if not input_path.lower().endswith('.docx'):
        raise ValueError("输入文件必须是.docx格式")

    if output_path is None:
        output_path = input_path.rsplit('.', 1)[0] + '.md'

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    pandoc_cmd = [
        'pandoc',
        input_path,
        '-o', output_path,
        '--from', 'docx',
        '--to', 'markdown',
        '--wrap', 'none'
    ]

    if preserve_links:
        pandoc_cmd.append('--reference-links')

    try:
        subprocess.run(pandoc_cmd, check=True, capture_output=True, text=True)
        print(f"转换成功: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e.stderr}")
        raise

def batch_convert(input_dir, output_dir=None, extension='.docx'):
    """
    批量转换目录下的docx文件为md

    Args:
        input_dir: 输入目录
        output_dir: 输出目录，如果为None则在原目录生成md文件
        extension: 要转换的文件扩展名

    Returns:
        转换成功的文件列表
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"目录不存在: {input_dir}")

    if output_dir is None:
        output_dir = input_dir

    os.makedirs(output_dir, exist_ok=True)

    converted_files = []

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(extension):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path.rsplit('.', 1)[0] + '.md')

                try:
                    docx_to_md(input_path, output_path)
                    converted_files.append(output_path)
                except Exception as e:
                    print(f"跳过 {input_path}: {e}")

    return converted_files

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='将Word文档(docx)转换为Markdown格式')
    parser.add_argument('input', help='输入的docx文件或包含docx文件的目录')
    parser.add_argument('-o', '--output', help='输出的md文件路径或目录')
    parser.add_argument('-b', '--batch', action='store_true', help='批量转换目录下的所有docx文件')

    args = parser.parse_args()

    if os.path.isdir(args.input):
        results = batch_convert(args.input, args.output)
        print(f"\n共转换 {len(results)} 个文件")
    else:
        docx_to_md(args.input, args.output)
