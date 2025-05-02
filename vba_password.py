#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VBA密码分析工具 - 尝试处理VBA项目的密码保护
"""

import os
import sys
import argparse
import struct
import binascii
from io import BytesIO

try:
    from oletools.olevba import VBA_Parser
    from oletools.common.io_encoding import ensure_stdout_handles_unicode
except ImportError:
    print("错误: 未安装oletools库。请使用以下命令安装:")
    print("pip install oletools")
    sys.exit(1)

def find_vba_project(ole_file):
    """
    在OLE文件中查找VBA项目的位置
    """
    if not ole_file:
        return None
    
    for stream_name in ole_file.listdir():
        # VBA项目通常存储在这个位置
        if len(stream_name) > 1 and stream_name[0] == 'VBA':
            if stream_name[1] == 'PROJECT':
                return '/'.join(stream_name)
    return None

def check_vba_protection(ole_file):
    """
    检查VBA项目是否启用了密码保护
    """
    project_path = find_vba_project(ole_file)
    if not project_path:
        return False, None
    
    # 读取项目信息
    project_stream = ole_file.openstream(project_path)
    project_data = project_stream.read()
    
    # 检查是否有密码保护的特征
    if b'DPB=' in project_data or b'CMG=' in project_data:
        return True, project_data
    
    return False, project_data

def extract_vba_protection_key(project_data):
    """
    尝试从项目数据中提取密码保护的密钥
    注意: 这不是直接破解密码，而是提取密钥信息
    """
    if not project_data:
        return None
    
    # 查找密钥标记
    protection_info = {}
    
    # 常见的保护标记
    markers = [b'DPB=', b'CMG=', b'GC=', b'ID=']
    
    for marker in markers:
        pos = project_data.find(marker)
        if pos >= 0:
            # 提取信息 (通常是Hex编码的字符串)
            end_pos = project_data.find(b'\r', pos)
            if end_pos < 0:
                end_pos = len(project_data)
            
            value = project_data[pos+len(marker):end_pos].decode('ascii', errors='ignore')
            protection_info[marker.decode('ascii', errors='ignore')] = value.strip()
    
    return protection_info

def analyze_vba_protection(filename):
    """
    分析文件中VBA项目的密码保护状态
    """
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在")
        return
    
    print(f"\n正在分析VBA密码保护: {filename}\n" + "="*60)
    
    try:
        vbaparser = VBA_Parser(filename)
        
        if vbaparser.ole_file is None:
            print("不是标准的OLE文件，无法分析VBA密码保护")
            return
        
        is_protected, project_data = check_vba_protection(vbaparser.ole_file)
        
        if is_protected:
            print("【发现VBA项目密码保护】")
            
            protection_keys = extract_vba_protection_key(project_data)
            if protection_keys:
                print("\n保护密钥信息:")
                for key, value in protection_keys.items():
                    print(f"- {key}: {value}")
                
                print("\n注意: 对于Office 97-2003格式(.doc, .xls等)，密码保护较弱")
                print("对于较新的Office格式(.docm, .xlsm等)，密码保护使用了更强的加密")
                print("\n你可以:")
                print("1. 使用olevba工具提取宏代码 (即使不知道密码)")
                print("2. 对于早期版本，可以尝试使用标准16位密码0x0000-0xFFFF进行爆破")
            else:
                print("未找到密码保护的密钥信息")
        else:
            print("未检测到VBA项目密码保护")
        
    except Exception as e:
        print(f"错误: {str(e)}")
    finally:
        if 'vbaparser' in locals():
            vbaparser.close()

def main():
    parser = argparse.ArgumentParser(description="VBA密码保护分析工具")
    parser.add_argument("filename", help="要分析的Office文档")
    
    args = parser.parse_args()
    ensure_stdout_handles_unicode()
    analyze_vba_protection(args.filename)

if __name__ == "__main__":
    main()