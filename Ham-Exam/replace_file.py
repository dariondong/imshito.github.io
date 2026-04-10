#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
替换原题库文件为已打乱的版本
"""

import shutil
import os

def backup_and_replace(original_file, shuffled_file):
    """
    备份原文件并替换为打乱后的文件
    """
    # 创建备份
    backup_file = original_file + '.backup'
    
    if os.path.exists(original_file):
        print(f"正在备份原文件：{backup_file}")
        shutil.copy2(original_file, backup_file)
        print(f"[OK] 备份完成")
    else:
        print(f"[WARN] 原文件不存在：{original_file}")
        return False
    
    # 替换文件
    if os.path.exists(shuffled_file):
        print(f"正在替换原文件：{original_file}")
        shutil.copy2(shuffled_file, original_file)
        print(f"[OK] 替换完成")
        print(f"\n原文件已备份为：{backup_file}")
        print(f"如果需要恢复，可以手动删除 {original_file} 并重命名 {backup_file}")
        return True
    else:
        print(f"[ERROR] 打乱后的文件不存在：{shuffled_file}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("题库文件替换工具")
    print("=" * 60)
    
    original = '业余无线电 A 类.csv'
    shuffled = '业余无线电 A 类_已打乱.csv'
    
    print(f"\n原文件：{original}")
    print(f"新文件：{shuffled}")
    
    response = input("\n确定要替换原文件吗？(输入 Y 确认): ").strip().upper()
    
    if response == 'Y':
        if backup_and_replace(original, shuffled):
            print("\n[OK] 替换成功！现在可以刷新浏览器重新加载题库了。")
        else:
            print("\n[ERROR] 替换失败")
    else:
        print("\n已取消操作")
        print(f"\n您可以手动操作：")
        print(f"1. 备份原文件：复制 {original} 到 {original}.backup")
        print(f"2. 替换文件：复制 {shuffled} 覆盖 {original}")
