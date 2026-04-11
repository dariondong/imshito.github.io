#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
业余无线电 A 类模拟试卷生成器
仿照 exam.html 的逻辑，随机抽取题目生成 20 份不同的模拟试卷
"""

import csv
import random
import os
from datetime import datetime

# 考试配置（与 exam.html 一致）
EXAM_CONFIG = {
    'TOTAL_QUESTIONS': 40,       # 总题数
    'SINGLE_CHOICE': 30,         # 单选题数量
    'MULTIPLE_CHOICE': 10,       # 多选题数量
    'DURATION_MINUTES': 30,      # 考试时长（分钟）
    'PASS_SCORE': 30             # 合格标准（答对题数）
}

def load_questions(csv_file):
    """
    加载题库，处理 BOM 头和换行符
    """
    questions = []
    
    # 读取 CSV 文件，处理 BOM 头
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # 跳过表头，从第 2 行开始
    for i, row in enumerate(rows[1:], start=2):
        if len(row) < 8:
            continue
        
        question = {
            'id': row[0],
            'chapter': row[1],
            'code': row[2],
            'question': row[3],
            'answer': row[4],
            'optionA': row[5],
            'optionB': row[6],
            'optionC': row[7],
            'optionD': row[8] if len(row) > 8 else ''
        }
        questions.append(question)
    
    return questions


def generate_exam_paper(questions, paper_index):
    """
    生成一份模拟试卷
    仿照 exam.html 的 randomExamQuestions 函数逻辑
    """
    # 分离单选题和多选题
    single_choice = [q for q in questions if len(q['answer']) == 1]
    multiple_choice = [q for q in questions if len(q['answer']) > 1]
    
    # 随机抽取题目
    selected_single = random.sample(single_choice, EXAM_CONFIG['SINGLE_CHOICE'])
    selected_multiple = random.sample(multiple_choice, EXAM_CONFIG['MULTIPLE_CHOICE'])
    
    # 合并题目（先单选后多选）
    exam_questions = selected_single + selected_multiple
    
    return exam_questions


def export_to_txt(questions, output_file, paper_index):
    """
    导出试卷为 TXT 格式
    """
    content = f'业余无线电 A 类考试模拟试卷（第{paper_index + 1}套）\n'
    content += '=' * 60 + '\n\n'
    content += f'考试时间：{EXAM_CONFIG["DURATION_MINUTES"]} 分钟\n'
    content += f'总题数：{len(questions)} 题\n'
    content += f'合格标准：答对 {EXAM_CONFIG["PASS_SCORE"]} 题为合格（正确率 75%）\n'
    content += f'试卷结构：单选题 {EXAM_CONFIG["SINGLE_CHOICE"]} 题 + 多选题 {EXAM_CONFIG["MULTIPLE_CHOICE"]} 题\n'
    content += f'生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'
    
    # 单选题部分
    single_choice = [q for q in questions if len(q['answer']) == 1]
    content += f'【单选题】共 {len(single_choice)} 题\n'
    content += '=' * 60 + '\n\n'
    
    for i, q in enumerate(single_choice, 1):
        content += f'{i}. {q["question"]}\n'
        content += f'   A. {q["optionA"]}\n'
        content += f'   B. {q["optionB"]}\n'
        if q['optionC']:
            content += f'   C. {q["optionC"]}\n'
        if q['optionD']:
            content += f'   D. {q["optionD"]}\n'
        content += '\n'
    
    # 多选题部分
    multiple_choice = [q for q in questions if len(q['answer']) > 1]
    content += f'【多选题】共 {len(multiple_choice)} 题\n'
    content += '=' * 60 + '\n\n'
    
    for i, q in enumerate(multiple_choice, 1):
        content += f'{i}. {q["question"]}\n'
        content += f'   A. {q["optionA"]}\n'
        content += f'   B. {q["optionB"]}\n'
        if q['optionC']:
            content += f'   C. {q["optionC"]}\n'
        if q['optionD']:
            content += f'   D. {q["optionD"]}\n'
        content += '\n'
    
    # 答案部分
    content += '=' * 60 + '\n'
    content += '【参考答案】\n'
    content += '=' * 60 + '\n\n'
    
    content += '单选题答案：\n'
    for i, q in enumerate(single_choice, 1):
        content += f'{i}. {q["answer"]}  '
        if i % 5 == 0:
            content += '\n'
    content += '\n\n'
    
    content += '多选题答案：\n'
    for i, q in enumerate(multiple_choice, 1):
        content += f'{i}. {q["answer"]}  '
        if i % 5 == 0:
            content += '\n'
    content += '\n'
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)


def export_to_word(questions, output_file, paper_index):
    """
    导出试卷为 Word 格式（HTML 格式的 .doc 文件）
    """
    html = '<html xmlns:o="urn:schemas-microsoft-com:office:office" '
    html += 'xmlns:w="urn:schemas-microsoft-com:office:word" '
    html += 'xmlns="http://www.w3.org/TR/REC-html40">'
    html += '<head><meta charset="utf-8">'
    html += '<style>'
    html += 'body { font-family: "Microsoft YaHei", "SimSun", sans-serif; font-size: 12pt; line-height: 1.6; }'
    html += 'h1 { font-size: 18pt; font-weight: bold; text-align: center; margin-bottom: 20px; }'
    html += 'h2 { font-size: 14pt; font-weight: bold; margin-top: 20px; margin-bottom: 10px; border-bottom: 2px solid #000; padding-bottom: 5px; }'
    html += '.info { margin: 15px 0; padding: 10px; background-color: #f5f5f5; border-left: 4px solid #333; }'
    html += '.question { margin: 15px 0; page-break-inside: avoid; }'
    html += '.question-number { font-weight: bold; }'
    html += '.option { margin-left: 20px; }'
    html += '</style>'
    html += '</head><body>'
    
    html += f'<h1>业余无线电 A 类考试模拟试卷（第{paper_index + 1}套）</h1>'
    
    html += '<div class="info">'
    html += f'<p><strong>考试时间：</strong>{EXAM_CONFIG["DURATION_MINUTES"]} 分钟</p>'
    html += f'<p><strong>总题数：</strong>{len(questions)} 题</p>'
    html += f'<p><strong>合格标准：</strong>答对 {EXAM_CONFIG["PASS_SCORE"]} 题为合格（正确率 75%）</p>'
    html += f'<p><strong>试卷结构：</strong>单选题 {EXAM_CONFIG["SINGLE_CHOICE"]} 题 + 多选题 {EXAM_CONFIG["MULTIPLE_CHOICE"]} 题</p>'
    html += f'<p><strong>生成时间：</strong>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>'
    html += '</div>'
    
    # 单选题部分
    single_choice = [q for q in questions if len(q['answer']) == 1]
    html += f'<h2>【单选题】（共 {len(single_choice)} 题）</h2>'
    
    for i, q in enumerate(single_choice, 1):
        html += '<div class="question">'
        html += f'<div class="question-number">{i}. {q["question"]}</div>'
        html += f'<div class="option">A. {q["optionA"]}</div>'
        html += f'<div class="option">B. {q["optionB"]}</div>'
        if q['optionC']:
            html += f'<div class="option">C. {q["optionC"]}</div>'
        if q['optionD']:
            html += f'<div class="option">D. {q["optionD"]}</div>'
        html += '</div>'
    
    # 多选题部分
    multiple_choice = [q for q in questions if len(q['answer']) > 1]
    html += f'<h2>【多选题】（共 {len(multiple_choice)} 题）</h2>'
    
    for i, q in enumerate(multiple_choice, 1):
        html += '<div class="question">'
        html += f'<div class="question-number">{i}. {q["question"]}</div>'
        html += f'<div class="option">A. {q["optionA"]}</div>'
        html += f'<div class="option">B. {q["optionB"]}</div>'
        if q['optionC']:
            html += f'<div class="option">C. {q["optionC"]}</div>'
        if q['optionD']:
            html += f'<div class="option">D. {q["optionD"]}</div>'
        html += '</div>'
    
    # 答案部分
    html += '<h2>【参考答案】</h2>'
    html += '<div class="info">'
    html += '<p><strong>单选题答案：</strong></p>'
    html += '<p style="line-height: 2;">'
    for i, q in enumerate(single_choice, 1):
        html += f'{i}. {q["answer"]} &nbsp;&nbsp; '
        if i % 5 == 0:
            html += '<br>'
    html += '</p>'
    
    html += '<p style="margin-top: 15px;"><strong>多选题答案：</strong></p>'
    html += '<p style="line-height: 2;">'
    for i, q in enumerate(multiple_choice, 1):
        html += f'{i}. {q["answer"]} &nbsp;&nbsp; '
        if i % 5 == 0:
            html += '<br>'
    html += '</p>'
    html += '</div>'
    
    html += '</body></html>'
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    """
    主函数：生成 20 份模拟试卷
    """
    print('=' * 60)
    print('业余无线电 A 类模拟试卷生成器')
    print('=' * 60)
    print()
    
    # 加载题库
    csv_file = '业余无线电 A 类.csv'
    if not os.path.exists(csv_file):
        print(f'[ERROR] 找不到题库文件：{csv_file}')
        print('请确保文件在当前目录下')
        return
    
    print(f'正在加载题库：{csv_file} ...')
    questions = load_questions(csv_file)
    print(f'[OK] 加载成功，共 {len(questions)} 题')
    print()
    
    # 统计题型
    single_count = sum(1 for q in questions if len(q['answer']) == 1)
    multiple_count = sum(1 for q in questions if len(q['answer']) > 1)
    print(f'题库构成：')
    print(f'  单选题：{single_count} 题')
    print(f'  多选题：{multiple_count} 题')
    print()
    
    # 检查题库是否足够
    if single_count < EXAM_CONFIG['SINGLE_CHOICE']:
        print(f'[ERROR] 单选题数量不足！需要 {EXAM_CONFIG["SINGLE_CHOICE"]} 题，实际只有 {single_count} 题')
        return
    
    if multiple_count < EXAM_CONFIG['MULTIPLE_CHOICE']:
        print(f'[ERROR] 多选题数量不足！需要 {EXAM_CONFIG["MULTIPLE_CHOICE"]} 题，实际只有 {multiple_count} 题')
        return
    
    # 创建输出目录
    output_dir = '模拟试卷'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f'[OK] 创建输出目录：{output_dir}')
    
    # 生成试卷
    num_papers = 200
    print(f'\n开始生成 {num_papers} 份模拟试卷...')
    print()
    
    for i in range(num_papers):
        # 生成试卷
        exam_questions = generate_exam_paper(questions, i)
        
        # 导出为 TXT
        txt_file = os.path.join(output_dir, f'A 类模拟试卷_{i + 1:02d}.txt')
        export_to_txt(exam_questions, txt_file, i)
        
        # 导出为 Word
        word_file = os.path.join(output_dir, f'A 类模拟试卷_{i + 1:02d}.doc')
        export_to_word(exam_questions, word_file, i)
        
        print(f'[OK] 第{i + 1:02d}套试卷已生成')
        print(f'     TXT: {txt_file}')
        print(f'     DOC: {word_file}')
    
    print()
    print('=' * 60)
    print(f'[OK] 所有试卷生成完成！')
    print(f'输出目录：{output_dir}/')
    print('=' * 60)
    print()
    print('提示：')
    print('  - .txt 文件可用记事本打开')
    print('  - .doc 文件可用 Word 打开')
    print('  - 每份试卷都包含题目和参考答案')
    print()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'\n[ERROR] 生成失败：{e}')
        import traceback
        traceback.print_exc()
