#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
题库选项打乱脚本
用于随机打乱 CSV 题库中的选项顺序，并相应更新正确答案
"""

import csv
import random
from itertools import permutations

def shuffle_options(input_file, output_file=None):
    """
    打乱题库中的选项顺序
    
    Args:
        input_file: 输入的 CSV 文件路径
        output_file: 输出的 CSV 文件路径（如果为 None，则覆盖原文件）
    """
    if output_file is None:
        output_file = input_file
    
    # 读取 CSV 文件，处理 BOM 头
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        print("错误：CSV 文件为空")
        return
    
    # 保存表头
    header = rows[0]
    print(f"表头：{header}")
    
    # 统计信息
    total_questions = 0
    shuffled_count = 0
    
    # 处理每一道题目
    shuffled_rows = [header]
    
    for i, row in enumerate(rows[1:], start=2):
        if len(row) < 8:
            print(f"警告：第 {i} 行数据不完整，跳过")
            shuffled_rows.append(row)
            continue
        
        total_questions += 1
        
        # 提取题目信息
        question_id = row[0]      # 题目编号
        chapter = row[1]          # 章节
        code = row[2]             # 题目代码
        question = row[3]         # 问题
        answer = row[4]           # 正确答案
        options = {
            'A': row[5],          # 选项 A
            'B': row[6],          # 选项 B
            'C': row[7],          # 选项 C
        }
        option_d = row[8] if len(row) > 8 else ''  # 选项 D
        
        # 如果有选项 D，加入选项字典
        if option_d:
            options['D'] = option_d
        
        # 创建选项列表并打乱
        option_keys = list(options.keys())
        random.shuffle(option_keys)
        
        # 创建答案映射（原答案字母 -> 新答案字母）
        answer_mapping = {}
        for new_pos, old_key in enumerate(option_keys):
            answer_mapping[old_key] = chr(ord('A') + new_pos)
        
        # 更新答案（保持字母顺序）
        new_answer_chars = []
        for char in answer:
            if char in answer_mapping:
                new_answer_chars.append(answer_mapping[char])
            else:
                new_answer_chars.append(char)
        
        # 对答案字母排序，确保答案是标准格式（如 AB 而不是 BA）
        new_answer = ''.join(sorted(new_answer_chars))
        
        # 按新顺序排列选项
        new_row = [
            question_id,
            chapter,
            code,
            question,
            new_answer,  # 更新后的答案
        ]
        
        # 添加打乱后的选项
        for key in option_keys:
            new_row.append(options[key])
        
        # 确保有 4 个选项（如果 D 选项为空，也要保留空位）
        while len(new_row) < 9:
            new_row.append('')
        
        shuffled_rows.append(new_row)
        shuffled_count += 1
        
        # 打印前 5 题的详细信息
        if shuffled_count <= 5:
            print(f"\n题目 {shuffled_count}:")
            print(f"  原答案：{answer} -> 新答案：{new_answer}")
            print(f"  原顺序：A={options['A'][:20]}...")
            print(f"  新顺序：A={new_row[5][:20]}...")
    
    # 写入新文件
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(shuffled_rows)
    
    print(f"\n[OK] 完成！")
    print(f"总题数：{total_questions}")
    print(f"已打乱：{shuffled_count}")
    print(f"输出文件：{output_file}")
    
    # 统计答案分布
    answer_stats = {}
    for row in shuffled_rows[1:]:
        if len(row) >= 5:
            ans = row[4]
            answer_stats[ans] = answer_stats.get(ans, 0) + 1
    
    print(f"\n答案分布统计：")
    for ans in sorted(answer_stats.keys()):
        count = answer_stats[ans]
        percent = (count / total_questions * 100) if total_questions > 0 else 0
        print(f"  {ans}: {count} 题 ({percent:.1f}%)")


def verify_csv(file_path):
    """
    验证 CSV 文件格式和答案分布
    """
    print(f"\n验证文件：{file_path}")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        print("错误：文件为空")
        return
    
    print(f"总行数：{len(rows)}")
    print(f"表头：{rows[0]}")
    
    # 统计答案分布
    answer_stats = {}
    total = 0
    
    for i, row in enumerate(rows[1:], start=2):
        if len(row) >= 5:
            ans = row[4]
            answer_stats[ans] = answer_stats.get(ans, 0) + 1
            total += 1
    
    print(f"\n答案分布：")
    for ans in sorted(answer_stats.keys()):
        count = answer_stats[ans]
        percent = (count / total * 100) if total > 0 else 0
        bar = '█' * int(percent / 2)
        print(f"  {ans:6s}: {count:4d} 题 ({percent:5.1f}%) {bar}")
    
    # 检查选项 A 的比例
    a_count = answer_stats.get('A', 0)
    a_percent = (a_count / total * 100) if total > 0 else 0
    
    print(f"\n{'[OK]' if 20 <= a_percent <= 30 else '[WARN]'} 选项 A 作为答案的比例：{a_percent:.1f}%")
    if a_percent > 50:
        print("[WARN] 警告：答案分布不均匀，建议打乱选项！")
    elif a_percent < 20:
        print("[WARN] 警告：答案分布可能异常！")
    else:
        print("[OK] 答案分布正常")


if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("业余无线电题库选项打乱工具")
    print("=" * 60)
    
    # 定义要处理的文件列表
    files_to_process = [
        ('业余无线电 A 类.csv', '业余无线电 A 类_已打乱.csv'),
        ('业余无线电 B 类.csv', '业余无线电 B 类_已打乱.csv'),
    ]
    
    print(f"\n将要处理以下文件：")
    for input_file, output_file in files_to_process:
        print(f"  {input_file} -> {output_file}")
    
    response = input("\n输入 Y 继续，或直接按 Enter 跳过：").strip().upper()
    
    if response == 'Y' or not response:
        for input_file, output_file in files_to_process:
            try:
                print(f"\n{'=' * 60}")
                print(f"处理文件：{input_file}")
                print('=' * 60)
                
                # 先验证原文件
                verify_csv(input_file)
                
                # 打乱选项
                shuffle_options(input_file, output_file)
                
                # 验证打乱后的文件
                print("\n" + "=" * 60)
                verify_csv(output_file)
                
                print(f"\n[OK] {input_file} 处理完成！")
                
            except FileNotFoundError:
                print(f"\n[WARN] 文件不存在，跳过：{input_file}")
            except Exception as e:
                print(f"\n[ERROR] 处理失败：{e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n{'=' * 60}")
        print("[OK] 所有文件处理完成！")
        print("=" * 60)
        print(f"\n如果满意结果，可以手动替换原文件")
