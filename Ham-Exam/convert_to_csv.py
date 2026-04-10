import csv
import re

def parse_txt_to_csv(input_file, output_file):
    """将业余无线电题库 TXT 文件转换为 CSV 格式"""
    
    questions = []
    current_question = {}
    current_options = {}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('[J]'):
            # 保存上一题
            if current_question and 'question' in current_question:
                current_question['options'] = current_options
                questions.append(current_question)
            
            # 开始新题目
            current_question = {'id': line[3:]}
            current_options = {}
            
        elif line.startswith('[P]') and current_question:
            current_question['section'] = line[3:]
            
        elif line.startswith('[I]') and current_question:
            current_question['code'] = line[3:]
            
        elif line.startswith('[Q]') and current_question:
            # 问题可能跨多行
            question_text = line[3:]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('['):
                question_text += lines[i].strip()
                i += 1
            current_question['question'] = question_text
            continue  # 因为已经增加了 i，所以跳过最后的 i+=1
            
        elif line.startswith('[T]') and current_question:
            current_question['answer'] = line[3:]
            
        elif len(line) >= 3 and line[0] == '[' and line[1] in 'ABCD' and line[2] == ']':
            # 选项
            option_letter = line[1]
            option_text = line[3:]
            # 选项可能跨多行
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('['):
                option_text += lines[i].strip()
                i += 1
            current_options[option_letter] = option_text
            continue  # 因为已经增加了 i，所以跳过最后的 i+=1
        
        i += 1
    
    # 保存最后一题
    if current_question and 'question' in current_question:
        current_question['options'] = current_options
        questions.append(current_question)
    
    # 写入 CSV
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['题目编号', '章节', '题目代码', '问题', '正确答案', '选项 A', '选项 B', '选项 C', '选项 D'])
        
        # 写入题目
        for q in questions:
            row = [
                q.get('id', ''),
                q.get('section', ''),
                q.get('code', ''),
                q.get('question', ''),
                q.get('answer', ''),
                q.get('options', {}).get('A', ''),
                q.get('options', {}).get('B', ''),
                q.get('options', {}).get('C', ''),
                q.get('options', {}).get('D', '')
            ]
            writer.writerow(row)
    
    print(f"成功转换 {len(questions)} 道题目到 {output_file}")

if __name__ == '__main__':
    import os
    input_file = r'C:\Users\admin\Desktop\Ham-Exam\b.txt'
    output_file = r'C:\Users\admin\Desktop\Ham-Exam\业余无线电 B 类.csv'
    print(f"输入文件：{input_file}")
    print(f"输出文件：{output_file}")
    parse_txt_to_csv(input_file, output_file)
