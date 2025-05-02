# VBA解密工具集 (oletools)

这个仓库包含了用于分析和解密VBA宏代码的工具集。

## 主要功能

- 提取VBA宏代码（即使是加密的）
- 分析VBA代码的潜在恶意行为
- 绕过VBA项目保护
- 提取嵌入对象和OLE结构

## 工具列表

1. **olevba** - 提取和分析VBA宏
2. **mraptor** - 检测恶意VBA宏
3. **oleobj** - 提取嵌入对象
4. **rtfobj** - 从RTF文件中提取对象
5. **oleid** - 分析OLE文件基本特性
6. **oletimes** - 显示OLE文件时间戳
7. **oledir** - 显示OLE文件目录结构

## 使用方法

1. 对于VBA加密宏的提取：
   ```
   python -m oletools.olevba 你的文件.doc
   ```

2. 检测文件中的宏是否可能恶意：
   ```
   python -m oletools.mraptor 你的文件.xlsm
   ```

3. 分析文件的OLE结构：
   ```
   python -m oletools.oleid 你的文件.docm
   ```

## 安装方法

通过pip安装：
```
pip install oletools
```

或从源码安装：
```
git clone https://github.com/decalage2/oletools.git
cd oletools
pip install -e .
```