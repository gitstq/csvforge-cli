# 📊 CSVForge-CLI

<p align="center">
  <b>轻量级终端CSV数据处理引擎</b><br>
  <i>零依赖 · 类SQL查询 · 多格式转换</i>
</p>

<p align="center">
  <b>简体中文</b> |
  <a href="./README_zh_TW.md">繁體中文</a> |
  <a href="./README.md">English</a>
</p>

---

## 🎉 项目介绍

**CSVForge-CLI** 是一款功能强大、零依赖的终端CSV数据处理工具包。受JSON处理工具 `jq` 启发，CSVForge将类SQL查询能力、多格式转换和数据转换工具直接带到您的命令行。

### 为什么选择CSVForge？

- **🔥 零依赖设计**：纯Python标准库实现，无需外部包
- **⚡ 极速处理**：针对大型CSV文件优化，支持流式处理
- **🎯 类SQL查询**：使用直观语法进行过滤、排序和聚合
- **🔄 多格式转换**：CSV、JSON、Markdown、HTML、TSV之间自由转换
- **📊 数据分析**：内置统计和模式分析功能
- **🎨 美观输出**：使用Unicode制表符的格式化终端表格

---

## ✨ 核心特性

### 📖 数据查看与探索
- **精美表格展示**：Unicode制表符格式化表格
- **头尾预览**：快速查看前/后N行数据
- **模式检测**：自动检测列类型（数值、文本、日期、布尔值）

### 🔍 类SQL查询引擎
- **SELECT**：选择特定列
- **WHERE**：条件过滤（`age > 30`、`name contains "John"`）
- **ORDER BY**：按任意列排序
- **LIMIT**：限制结果数量
- **DISTINCT**：去除重复行

### 📊 统计与分析
- **列分析**：类型检测、唯一值、最常见值
- **数值统计**：数值列的最小值、最大值、总和、平均值
- **数据质量**：空值检测和报告

### 🔄 格式转换
- **导出为JSON**：对象数组格式
- **导出为Markdown**：GitHub风格表格
- **导出为HTML**：样式化HTML表格
- **导出为TSV**：制表符分隔值

### 🛠️ 数据转换
- **增/删/改列**：轻松修改数据结构
- **合并列**：使用自定义分隔符合并多列
- **拆分列**：分解分隔值

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/csvforge-cli.git
cd csvforge-cli

# 添加执行权限并加入PATH
chmod +x csvforge.py
sudo ln -s $(pwd)/csvforge.py /usr/local/bin/csvforge

# 或通过pip安装
pip install -e .
```

### 环境要求

- **Python**：3.8或更高版本
- **依赖项**：无（零依赖设计）

---

## 📖 使用指南

### 查看CSV数据

```bash
# 以格式化表格显示CSV
csvforge view data.csv

# 显示前5行
csvforge head data.csv -n 5

# 显示后5行
csvforge tail data.csv -n 5

# 无表头查看
csvforge view data.csv --no-header
```

### 数据查询

```bash
# 过滤年龄大于30的行
csvforge query data.csv -w "age > 30"

# 选择特定列
csvforge query data.csv -s "name,email,city"

# 组合查询：过滤、排序并限制结果
csvforge query data.csv -w "salary > 50000" -o salary -r -l 10

# 字符串包含过滤
csvforge query data.csv -w "department contains Engineer"
```

### 格式转换

```bash
# 转换为JSON
csvforge convert data.csv -f json -o output.json

# 转换为Markdown
csvforge convert data.csv -f markdown -o output.md

# 转换为HTML
csvforge convert data.csv -f html -o output.html

# 转换为TSV
csvforge convert data.csv -f tsv -o output.tsv
```

### 统计分析

```bash
# 显示综合统计信息
csvforge stats data.csv

# 以JSON格式输出统计
csvforge stats data.csv --json
```

### 数据转换

```bash
# 重命名列
csvforge transform data.csv --rename "old_name:new_name" -o output.csv

# 添加新列
csvforge transform data.csv --add "status:active" -o output.csv

# 删除列
csvforge transform data.csv --delete "unnecessary_column" -o output.csv
```

### 模式信息

```bash
# 显示列模式
csvforge schema data.csv
```

### 管道支持

```bash
# 从标准输入读取
cat data.csv | csvforge view -

# 命令链式调用
cat data.csv | csvforge query - -w "age > 25" | csvforge convert - -f json
```

---

## 💡 设计理念

### 零依赖原则
CSVForge完全基于Python标准库构建。这意味着：
- **无安装烦恼**：在任何Python 3.8+系统上都能运行
- **无版本冲突**：无需担心依赖更新问题
- **可移植性强**：易于在受限环境中部署

### 类SQL语法
我们相信数据处理应该直观易懂。CSVForge的查询语法借鉴SQL：
- `WHERE` 用于过滤
- `ORDER BY` 用于排序
- `SELECT` 用于投影
- `LIMIT` 用于分页

### Unix哲学
CSVForge遵循Unix"做好一件事"的哲学：
- **可组合性**：通过管道与其他CLI工具链式调用
- **文本导向**：输出始终是人类可读的
- **可脚本化**：易于集成到自动化工作流中

---

## 📦 开发路线图

### v1.1.0（计划中）
- [ ] 多CSV文件JOIN操作
- [ ] 聚合函数（GROUP BY）
- [ ] 正则表达式过滤
- [ ] 列算术运算

### v1.2.0（计划中）
- [ ] 交互式TUI模式
- [ ] 配置文件支持
- [ ] 自定义输出模板
- [ ] 批处理模式

### v2.0.0（未来）
- [ ] 自定义函数插件系统
- [ ] 超大文件流式处理
- [ ] 并行查询执行
- [ ] SQL方言兼容层

---

## 🤝 贡献指南

我们欢迎贡献！请遵循以下准则：

1. **Fork** 本仓库
2. **创建** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 您的更改 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **开启** Pull Request

### 提交规范

我们遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档变更
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具变更

---

## 📄 开源协议

本项目采用 **MIT License** 开源协议 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- 受优秀的JSON处理工具 [jq](https://stedolan.github.io/jq/) 启发
- 基于Python强大的标准库构建
- 感谢所有贡献者和用户

---

<p align="center">
  <b>Made with ❤️ by the CSVForge Team</b><br>
  <a href="https://github.com/gitstq/csvforge-cli">GitHub</a> •
  <a href="https://github.com/gitstq/csvforge-cli/issues">Issues</a> •
  <a href="https://github.com/gitstq/csvforge-cli/discussions">Discussions</a>
</p>
