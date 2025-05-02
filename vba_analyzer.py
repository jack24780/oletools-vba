#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VBA 宏分析工具 - 基于oletools
这个脚本可以帮助分析Office文档中的VBA宏，包括加密的宏
"""

import os
import sys
import argparse

try:
    from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML
    from oletools.olevba import detect_autoexec, detect_suspicious
    from oletools.olevba import detect_patterns
except ImportError:
    print("错误: 未安装oletools库。请使用以下命令安装:")
    print("pip install oletools")
    sys.exit(1)

def analyze_file(filename, extract_macros=False, analyze=True, show_code=False):
    """
    分析Office文档中的VBA宏
    """
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在")
        return
    
    print(f"\n正在分析文件: {filename}\n" + "="*60)
    
    try:
        vbaparser = VBA_Parser(filename)
        if not vbaparser.detect_vba_macros():
            print("没有检测到VBA宏")
            return
        
        # 打印文件类型信息
        file_type = "未知"
        if vbaparser.type == TYPE_OLE:
            file_type = "OLE文件 (常规Office文档)"
        elif vbaparser.type == TYPE_OpenXML:
            file_type = "OpenXML文件 (Office 2007+)"
        elif vbaparser.type == TYPE_Word2003_XML:
            file_type = "Word 2003 XML"
        elif vbaparser.type == TYPE_MHTML:
            file_type = "MHTML文件"
        
        print(f"文件类型: {file_type}")
        
        # 分析VBA代码
        if analyze:
            print("\n=== 宏分析 ===")
            results = vbaparser.analyze_macros()
            if results:
                for kw_type, keyword, description in results:
                    print(f"- 发现 {kw_type}: {keyword} - {description}")
            else:
                print("未发现可疑特征")
        
        # 提取并显示VBA代码
        if extract_macros or show_code:
            print("\n=== VBA代码 ===")
            for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
                if show_code:
                    print(f"\n--- 模块: {vba_filename} ---")
                    print(vba_code)
                
                if extract_macros:
                    output_filename = f"{os.path.basename(filename)}_{vba_filename}"
                    with open(output_filename, 'w', encoding='utf-8') as f:
                        f.write(vba_code)
                    print(f"已将宏保存至: {output_filename}")
        
    except Exception as e:
        print(f"错误: {str(e)}")
    finally:
        if 'vbaparser' in locals():
            vbaparser.close()

def main():
    parser = argparse.ArgumentParser(description="VBA宏分析工具")
    parser.add_argument("filename", help="要分析的Office文档")
    parser.add_argument("-e", "--extract", action="store_true", help="提取宏到文件")
    parser.add_argument("-a", "--analyze", action="store_true", default=True, help="分析宏代码")
    parser.add_argument("-c", "--code", action="store_true", help="显示宏代码")
    
    args = parser.parse_args()
    
    analyze_file(args.filename, args.extract, args.analyze, args.code)

if __name__ == "__main__":
    main()