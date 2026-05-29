# 📊 CSVForge-CLI

<p align="center">
  <b>輕量級終端CSV資料處理引擎</b><br>
  <i>零依賴 · 類SQL查詢 · 多格式轉換</i>
</p>

<p align="center">
  <a href="./README_zh.md">简体中文</a> |
  <b>繁體中文</b> |
  <a href="./README.md">English</a>
</p>

---

## 🎉 專案介紹

**CSVForge-CLI** 是一款功能強大、零依賴的終端CSV資料處理工具包。受JSON處理工具 `jq` 啟發，CSVForge將類SQL查詢能力、多格式轉換和資料轉換工具直接帶到您的命令列。

### 為什麼選擇CSVForge？

- **🔥 零依賴設計**：純Python標準庫實現，無需外部套件
- **⚡ 極速處理**：針對大型CSV檔案優化，支援流式處理
- **🎯 類SQL查詢**：使用直觀語法進行過濾、排序和聚合
- **🔄 多格式轉換**：CSV、JSON、Markdown、HTML、TSV之間自由轉換
- **📊 資料分析**：內建統計和模式分析功能
- **🎨 美觀輸出**：使用Unicode製表符的格式化終端表格

---

## ✨ 核心特性

### 📖 資料查看與探索
- **精美表格展示**：Unicode製表符格式化表格
- **頭尾預覽**：快速查看前/後N行資料
- **模式檢測**：自動檢測欄位類型（數值、文字、日期、布林值）

### 🔍 類SQL查詢引擎
- **SELECT**：選擇特定欄位
- **WHERE**：條件過濾（`age > 30`、`name contains "John"`）
- **ORDER BY**：按任意欄位排序
- **LIMIT**：限制結果數量
- **DISTINCT**：去除重複行

### 📊 統計與分析
- **欄位分析**：類型檢測、唯一值、最常見值
- **數值統計**：數值欄位的最小值、最大值、總和、平均值
- **資料品質**：空值檢測和報告

### 🔄 格式轉換
- **匯出為JSON**：物件陣列格式
- **匯出為Markdown**：GitHub風格表格
- **匯出為HTML**：樣式化HTML表格
- **匯出為TSV**：製表符分隔值

### 🛠️ 資料轉換
- **增/刪/改欄位**：輕鬆修改資料結構
- **合併欄位**：使用自訂分隔符合併多欄
- **拆分欄位**：分解分隔值

---

## 🚀 快速開始

### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/csvforge-cli.git
cd csvforge-cli

# 新增執行權限並加入PATH
chmod +x csvforge.py
sudo ln -s $(pwd)/csvforge.py /usr/local/bin/csvforge

# 或透過pip安裝
pip install -e .
```

### 環境需求

- **Python**：3.8或更高版本
- **依賴項**：無（零依賴設計）

---

## 📖 使用指南

### 查看CSV資料

```bash
# 以格式化表格顯示CSV
csvforge view data.csv

# 顯示前5行
csvforge head data.csv -n 5

# 顯示後5行
csvforge tail data.csv -n 5

# 無表頭查看
csvforge view data.csv --no-header
```

### 資料查詢

```bash
# 過濾年齡大於30的行
csvforge query data.csv -w "age > 30"

# 選擇特定欄位
csvforge query data.csv -s "name,email,city"

# 組合查詢：過濾、排序並限制結果
csvforge query data.csv -w "salary > 50000" -o salary -r -l 10

# 字串包含過濾
csvforge query data.csv -w "department contains Engineer"
```

### 格式轉換

```bash
# 轉換為JSON
csvforge convert data.csv -f json -o output.json

# 轉換為Markdown
csvforge convert data.csv -f markdown -o output.md

# 轉換為HTML
csvforge convert data.csv -f html -o output.html

# 轉換為TSV
csvforge convert data.csv -f tsv -o output.tsv
```

### 統計分析

```bash
# 顯示綜合統計資訊
csvforge stats data.csv

# 以JSON格式輸出統計
csvforge stats data.csv --json
```

### 資料轉換

```bash
# 重新命名欄位
csvforge transform data.csv --rename "old_name:new_name" -o output.csv

# 新增欄位
csvforge transform data.csv --add "status:active" -o output.csv

# 刪除欄位
csvforge transform data.csv --delete "unnecessary_column" -o output.csv
```

### 模式資訊

```bash
# 顯示欄位模式
csvforge schema data.csv
```

### 管道支援

```bash
# 從標準輸入讀取
cat data.csv | csvforge view -

# 命令鏈式呼叫
cat data.csv | csvforge query - -w "age > 25" | csvforge convert - -f json
```

---

## 💡 設計理念

### 零依賴原則
CSVForge完全基於Python標準庫建構。這意味著：
- **無安裝煩惱**：在任何Python 3.8+系統上都能運作
- **無版本衝突**：無需擔心依賴更新問題
- **可攜性強**：易於在受限環境中部署

### 類SQL語法
我們相信資料處理應該直觀易懂。CSVForge的查詢語法借鑑SQL：
- `WHERE` 用於過濾
- `ORDER BY` 用於排序
- `SELECT` 用於投影
- `LIMIT` 用於分頁

### Unix哲學
CSVForge遵循Unix"做好一件事"的哲學：
- **可組合性**：透過管道與其他CLI工具鏈式呼叫
- **文字導向**：輸出始終是人類可讀的
- **可腳本化**：易於整合到自動化工作流程中

---

## 📦 開發路線圖

### v1.1.0（計劃中）
- [ ] 多CSV檔案JOIN操作
- [ ] 聚合函數（GROUP BY）
- [ ] 正規表示式過濾
- [ ] 欄位算術運算

### v1.2.0（計劃中）
- [ ] 互動式TUI模式
- [ ] 設定檔支援
- [ ] 自訂輸出模板
- [ ] 批次處理模式

### v2.0.0（未來）
- [ ] 自訂函數外掛系統
- [ ] 超大檔案流式處理
- [ ] 平行查詢執行
- [ ] SQL方言相容層

---

## 🤝 貢獻指南

我們歡迎貢獻！請遵循以下準則：

1. **Fork** 本倉庫
2. **建立** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 您的變更 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **開啟** Pull Request

### 提交規範

我們遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範：

- `feat:` 新功能
- `fix:` 修復bug
- `docs:` 文件變更
- `refactor:` 程式碼重構
- `test:` 測試相關
- `chore:` 建置/工具變更

---

## 📄 開源協議

本專案採用 **MIT License** 開源協議 - 詳情請參閱 [LICENSE](LICENSE) 檔案。

---

## 🙏 致謝

- 受優秀的JSON處理工具 [jq](https://stedolan.github.io/jq/) 啟發
- 基於Python強大的標準庫建構
- 感謝所有貢獻者和使用者

---

<p align="center">
  <b>Made with ❤️ by the CSVForge Team</b><br>
  <a href="https://github.com/gitstq/csvforge-cli">GitHub</a> •
  <a href="https://github.com/gitstq/csvforge-cli/issues">Issues</a> •
  <a href="https://github.com/gitstq/csvforge-cli/discussions">Discussions</a>
</p>
