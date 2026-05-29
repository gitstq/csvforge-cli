# 📊 CSVForge-CLI

<p align="center">
  <b>Lightweight Terminal CSV Data Processing Engine</b><br>
  <i>Zero Dependencies · SQL-like Queries · Multi-Format Conversion</i>
</p>

<p align="center">
  <a href="./README_zh.md">简体中文</a> |
  <a href="./README_zh_TW.md">繁體中文</a> |
  <b>English</b>
</p>

---

## 🎉 Introduction

**CSVForge-CLI** is a powerful, zero-dependency terminal toolkit for CSV data processing. Inspired by tools like `jq` for JSON, CSVForge brings SQL-like query capabilities, multi-format conversion, and data transformation utilities directly to your command line.

### Why CSVForge?

- **🔥 Zero Dependencies**: Pure Python standard library, no external packages required
- **⚡ Lightning Fast**: Optimized for large CSV files with streaming support
- **🎯 SQL-like Queries**: Filter, sort, and aggregate data with intuitive syntax
- **🔄 Multi-Format**: Convert between CSV, JSON, Markdown, HTML, and TSV
- **📊 Data Analytics**: Built-in statistics and schema analysis
- **🎨 Beautiful Output**: Formatted terminal tables with Unicode box-drawing

---

## ✨ Core Features

### 📖 Data Viewing & Exploration
- **Beautiful Table Display**: Unicode box-drawing formatted tables
- **Head/Tail Support**: Quick preview of first/last N rows
- **Schema Detection**: Automatic column type detection (numeric, text, date, boolean)

### 🔍 SQL-like Query Engine
- **SELECT**: Choose specific columns
- **WHERE**: Filter with conditions (`age > 30`, `name contains "John"`)
- **ORDER BY**: Sort by any column
- **LIMIT**: Restrict result count
- **DISTINCT**: Remove duplicate rows

### 📊 Statistics & Analytics
- **Column Analysis**: Type detection, unique values, most common values
- **Numeric Statistics**: Min, max, sum, average for numeric columns
- **Data Quality**: Empty value detection and reporting

### 🔄 Format Conversion
- **Export to JSON**: Array of objects format
- **Export to Markdown**: GitHub-flavored tables
- **Export to HTML**: Styled HTML tables
- **Export to TSV**: Tab-separated values

### 🛠️ Data Transformation
- **Add/Rename/Delete Columns**: Easy schema modifications
- **Merge Columns**: Combine multiple columns with custom separators
- **Split Columns**: Break apart delimited values

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/csvforge-cli.git
cd csvforge-cli

# Make executable and add to PATH
chmod +x csvforge.py
sudo ln -s $(pwd)/csvforge.py /usr/local/bin/csvforge

# Or install via pip
pip install -e .
```

### Requirements

- **Python**: 3.8 or higher
- **Dependencies**: None (zero-dependency design)

---

## 📖 Usage Guide

### View CSV Data

```bash
# Display CSV with formatted table
csvforge view data.csv

# Show first 5 rows
csvforge head data.csv -n 5

# Show last 5 rows
csvforge tail data.csv -n 5

# View without header row
csvforge view data.csv --no-header
```

### Query Data

```bash
# Filter rows where age > 30
csvforge query data.csv -w "age > 30"

# Select specific columns
csvforge query data.csv -s "name,email,city"

# Combined query with sort and limit
csvforge query data.csv -w "salary > 50000" -o salary -r -l 10

# String contains filter
csvforge query data.csv -w "department contains Engineer"
```

### Convert Formats

```bash
# Convert to JSON
csvforge convert data.csv -f json -o output.json

# Convert to Markdown
csvforge convert data.csv -f markdown -o output.md

# Convert to HTML
csvforge convert data.csv -f html -o output.html

# Convert to TSV
csvforge convert data.csv -f tsv -o output.tsv
```

### Statistics

```bash
# Show comprehensive statistics
csvforge stats data.csv

# Output stats as JSON
csvforge stats data.csv --json
```

### Transform Data

```bash
# Rename column
csvforge transform data.csv --rename "old_name:new_name" -o output.csv

# Add new column
csvforge transform data.csv --add "status:active" -o output.csv

# Delete column
csvforge transform data.csv --delete "unnecessary_column" -o output.csv
```

### Schema Information

```bash
# Show column schema
csvforge schema data.csv
```

### Pipe Support

```bash
# Read from stdin
cat data.csv | csvforge view -

# Chain commands
cat data.csv | csvforge query - -w "age > 25" | csvforge convert - -f json
```

---

## 💡 Design Philosophy

### Zero-Dependency Principle
CSVForge is built entirely on Python's standard library. This means:
- **No installation hassles**: Works on any Python 3.8+ system
- **No version conflicts**: Never worry about dependency updates
- **Portable**: Easy to deploy in restricted environments

### SQL-like Syntax
We believe data manipulation should be intuitive. CSVForge's query syntax mirrors SQL:
- `WHERE` for filtering
- `ORDER BY` for sorting
- `SELECT` for projection
- `LIMIT` for pagination

### Unix Philosophy
CSVForge follows the Unix philosophy of doing one thing well:
- **Composable**: Chain with other CLI tools via pipes
- **Text-based**: Output is always human-readable
- **Scriptable**: Easy to integrate into automation workflows

---

## 📦 Roadmap

### v1.1.0 (Planned)
- [ ] JOIN operations for multiple CSV files
- [ ] Aggregate functions (GROUP BY)
- [ ] Regular expression filtering
- [ ] Column arithmetic operations

### v1.2.0 (Planned)
- [ ] Interactive TUI mode
- [ ] Configuration file support
- [ ] Custom output templates
- [ ] Batch processing mode

### v2.0.0 (Future)
- [ ] Plugin system for custom functions
- [ ] Streaming processing for huge files
- [ ] Parallel query execution
- [ ] SQL dialect compatibility layer

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Commit Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Build/tooling changes

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by the excellent [jq](https://stedolan.github.io/jq/) tool for JSON
- Built with Python's powerful standard library
- Thanks to all contributors and users

---

<p align="center">
  <b>Made with ❤️ by the CSVForge Team</b><br>
  <a href="https://github.com/gitstq/csvforge-cli">GitHub</a> •
  <a href="https://github.com/gitstq/csvforge-cli/issues">Issues</a> •
  <a href="https://github.com/gitstq/csvforge-cli/discussions">Discussions</a>
</p>
