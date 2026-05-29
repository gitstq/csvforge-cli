#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 CSVForge-CLI - Lightweight Terminal CSV Data Processing Engine
轻量级终端CSV数据处理引擎

A zero-dependency, powerful CSV processing toolkit for the terminal.
Features: query, transform, merge, split, stats, format conversion, and more.

Author: CSVForge Team
License: MIT
Version: 1.0.0
"""

import csv
import sys
import os
import re
import json
import argparse
from io import StringIO
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional, Callable, Iterator, Tuple
from datetime import datetime

__version__ = "1.0.0"
__author__ = "CSVForge Team"


class CSVForgeError(Exception):
    """Base exception for CSVForge"""
    pass


class CSVParser:
    """Core CSV parsing and processing engine"""

    def __init__(self, delimiter: str = ',', quotechar: str = '"',
                 encoding: str = 'utf-8', has_header: bool = True):
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.encoding = encoding
        self.has_header = has_header
        self.headers: List[str] = []
        self.rows: List[Dict[str, str]] = []

    def read_file(self, filepath: str) -> 'CSVParser':
        """Read CSV from file"""
        try:
            with open(filepath, 'r', encoding=self.encoding, newline='') as f:
                return self.read_stream(f)
        except FileNotFoundError:
            raise CSVForgeError(f"File not found: {filepath}")
        except UnicodeDecodeError:
            raise CSVForgeError(f"Unable to decode file with {self.encoding} encoding")

    def read_stream(self, stream) -> 'CSVParser':
        """Read CSV from stream"""
        reader = csv.reader(stream, delimiter=self.delimiter, quotechar=self.quotechar)
        rows = list(reader)

        if not rows:
            self.headers = []
            self.rows = []
            return self

        if self.has_header:
            self.headers = rows[0]
            data_rows = rows[1:]
        else:
            self.headers = [f"col_{i}" for i in range(len(rows[0]))]
            data_rows = rows

        self.rows = [
            {self.headers[i]: row[i] if i < len(row) else ''
             for i in range(len(self.headers))}
            for row in data_rows
        ]
        return self

    def read_string(self, data: str) -> 'CSVParser':
        """Read CSV from string"""
        return self.read_stream(StringIO(data))

    def write_file(self, filepath: str) -> None:
        """Write CSV to file"""
        with open(filepath, 'w', encoding=self.encoding, newline='') as f:
            writer = csv.writer(f, delimiter=self.delimiter, quotechar=self.quotechar,
                               quoting=csv.QUOTE_MINIMAL)
            if self.has_header:
                writer.writerow(self.headers)
            for row in self.rows:
                writer.writerow([row.get(h, '') for h in self.headers])

    def write_string(self) -> str:
        """Write CSV to string"""
        output = StringIO()
        writer = csv.writer(output, delimiter=self.delimiter, quotechar=self.quotechar,
                           quoting=csv.QUOTE_MINIMAL)
        if self.has_header:
            writer.writerow(self.headers)
        for row in self.rows:
            writer.writerow([row.get(h, '') for h in self.headers])
        return output.getvalue()

    def to_json(self) -> List[Dict[str, str]]:
        """Convert to JSON format"""
        return self.rows

    def to_markdown(self) -> str:
        """Convert to Markdown table"""
        if not self.headers:
            return ""

        lines = []
        # Header
        lines.append("| " + " | ".join(self.headers) + " |")
        # Separator
        lines.append("|" + "|".join([" --- " for _ in self.headers]) + "|")
        # Data rows
        for row in self.rows:
            lines.append("| " + " | ".join([str(row.get(h, '')) for h in self.headers]) + " |")

        return "\n".join(lines)

    def to_html(self) -> str:
        """Convert to HTML table"""
        html = ['<table border="1">']
        if self.headers:
            html.append('<thead><tr>')
            for h in self.headers:
                html.append(f'<th>{self._escape_html(h)}</th>')
            html.append('</tr></thead>')

        html.append('<tbody>')
        for row in self.rows:
            html.append('<tr>')
            for h in self.headers:
                html.append(f'<td>{self._escape_html(str(row.get(h, "")))}</td>')
            html.append('</tr>')
        html.append('</tbody></table>')
        return "\n".join(html)

    def to_tsv(self) -> str:
        """Convert to TSV format"""
        output = StringIO()
        writer = csv.writer(output, delimiter='\t', quotechar=self.quotechar)
        if self.has_header:
            writer.writerow(self.headers)
        for row in self.rows:
            writer.writerow([row.get(h, '') for h in self.headers])
        return output.getvalue()

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML special characters"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))


class CSVQuery:
    """SQL-like query engine for CSV data"""

    def __init__(self, parser: CSVParser):
        self.parser = parser

    def select(self, columns: Optional[List[str]] = None) -> 'CSVQuery':
        """Select specific columns"""
        if columns is None:
            return self

        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )
        new_parser.headers = [c for c in columns if c in self.parser.headers]
        new_parser.rows = [
            {c: row.get(c, '') for c in new_parser.headers}
            for row in self.parser.rows
        ]
        return CSVQuery(new_parser)

    def where(self, condition: Callable[[Dict[str, str]], bool]) -> 'CSVQuery':
        """Filter rows by condition"""
        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )
        new_parser.headers = self.parser.headers.copy()
        new_parser.rows = [row for row in self.parser.rows if condition(row)]
        return CSVQuery(new_parser)

    def where_expr(self, expression: str) -> 'CSVQuery':
        """Filter rows using expression (e.g., 'age > 18')"""
        condition = self._parse_expression(expression)
        return self.where(condition)

    def order_by(self, column: str, reverse: bool = False) -> 'CSVQuery':
        """Sort rows by column"""
        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )
        new_parser.headers = self.parser.headers.copy()
        new_parser.rows = sorted(
            self.parser.rows,
            key=lambda r: self._smart_convert(r.get(column, '')),
            reverse=reverse
        )
        return CSVQuery(new_parser)

    def limit(self, n: int) -> 'CSVQuery':
        """Limit number of rows"""
        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )
        new_parser.headers = self.parser.headers.copy()
        new_parser.rows = self.parser.rows[:n]
        return CSVQuery(new_parser)

    def distinct(self, column: Optional[str] = None) -> 'CSVQuery':
        """Get distinct rows or values"""
        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )

        if column:
            seen = set()
            distinct_rows = []
            for row in self.parser.rows:
                val = row.get(column, '')
                if val not in seen:
                    seen.add(val)
                    distinct_rows.append(row)
            new_parser.headers = self.parser.headers.copy()
            new_parser.rows = distinct_rows
        else:
            # Distinct across all columns
            seen = set()
            distinct_rows = []
            for row in self.parser.rows:
                key = tuple(row.get(h, '') for h in self.parser.headers)
                if key not in seen:
                    seen.add(key)
                    distinct_rows.append(row)
            new_parser.headers = self.parser.headers.copy()
            new_parser.rows = distinct_rows

        return CSVQuery(new_parser)

    def aggregate(self, column: str, func: str) -> Any:
        """Aggregate functions: sum, avg, min, max, count"""
        values = [self._smart_convert(row.get(column, '0')) for row in self.parser.rows]

        if func == 'sum':
            return sum(values)
        elif func == 'avg':
            return sum(values) / len(values) if values else 0
        elif func == 'min':
            return min(values) if values else None
        elif func == 'max':
            return max(values) if values else None
        elif func == 'count':
            return len(values)
        else:
            raise CSVForgeError(f"Unknown aggregate function: {func}")

    def group_by(self, column: str) -> Dict[str, List[Dict[str, str]]]:
        """Group rows by column value"""
        groups = defaultdict(list)
        for row in self.parser.rows:
            key = row.get(column, '')
            groups[key].append(row)
        return dict(groups)

    def _parse_expression(self, expr: str) -> Callable[[Dict[str, str]], bool]:
        """Parse simple expression into condition function"""
        # Support: col > value, col < value, col = value, col != value, col contains value
        expr = expr.strip()

        # Handle different operators
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if op in expr:
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    col = parts[0].strip()
                    val = parts[1].strip().strip('"\'')

                    def make_condition(c, v, operator):
                        def condition(row):
                            cell_val = row.get(c, '')
                            try:
                                cell_num = float(cell_val)
                                val_num = float(v)
                                if operator == '>':
                                    return cell_num > val_num
                                elif operator == '<':
                                    return cell_num < val_num
                                elif operator == '>=':
                                    return cell_num >= val_num
                                elif operator == '<=':
                                    return cell_num <= val_num
                                elif operator == '=':
                                    return cell_num == val_num
                                elif operator == '!=':
                                    return cell_num != val_num
                            except ValueError:
                                # String comparison
                                if operator == '=':
                                    return cell_val == v
                                elif operator == '!=':
                                    return cell_val != v
                                elif operator == '>':
                                    return cell_val > v
                                elif operator == '<':
                                    return cell_val < v
                            return False
                        return condition

                    return make_condition(col, val, op)

        # Handle contains
        if ' contains ' in expr.lower():
            parts = expr.lower().split(' contains ')
            col = parts[0].strip()
            val = parts[1].strip().strip('"\'')
            return lambda row: val.lower() in row.get(col, '').lower()

        raise CSVForgeError(f"Unable to parse expression: {expr}")

    @staticmethod
    def _smart_convert(value: str) -> Any:
        """Try to convert string to number"""
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value


class CSVStats:
    """Statistics engine for CSV data"""

    def __init__(self, parser: CSVParser):
        self.parser = parser

    def summary(self) -> Dict[str, Any]:
        """Generate comprehensive statistics"""
        stats = {
            'total_rows': len(self.parser.rows),
            'total_columns': len(self.parser.headers),
            'columns': {}
        }

        for col in self.parser.headers:
            col_stats = self._column_stats(col)
            stats['columns'][col] = col_stats

        return stats

    def _column_stats(self, column: str) -> Dict[str, Any]:
        """Statistics for a single column"""
        values = [row.get(column, '') for row in self.parser.rows]
        non_empty = [v for v in values if v.strip()]

        stats = {
            'type': self._detect_type(values),
            'non_empty': len(non_empty),
            'empty': len(values) - len(non_empty),
            'unique': len(set(values)),
            'most_common': Counter(values).most_common(5)
        }

        # Numeric stats if applicable
        numeric_values = self._extract_numeric(values)
        if numeric_values:
            stats['numeric'] = {
                'min': min(numeric_values),
                'max': max(numeric_values),
                'sum': sum(numeric_values),
                'avg': sum(numeric_values) / len(numeric_values),
                'count': len(numeric_values)
            }

        return stats

    def _detect_type(self, values: List[str]) -> str:
        """Detect data type of column"""
        if not values:
            return 'empty'

        # Check if all numeric
        numeric_count = sum(1 for v in values if v.strip() and self._is_numeric(v))
        if numeric_count == len([v for v in values if v.strip()]):
            return 'numeric'

        # Check if date
        date_count = sum(1 for v in values if self._is_date(v))
        if date_count > len(values) * 0.5:
            return 'date'

        # Check if boolean
        bool_values = {'true', 'false', 'yes', 'no', '1', '0'}
        bool_count = sum(1 for v in values if v.lower() in bool_values)
        if bool_count == len([v for v in values if v.strip()]):
            return 'boolean'

        return 'text'

    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Check if value is numeric"""
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_date(value: str) -> bool:
        """Check if value looks like a date"""
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
            r'\d{2}-\d{2}-\d{4}',
            r'\d{4}/\d{2}/\d{2}'
        ]
        return any(re.match(p, value.strip()) for p in date_patterns)

    def _extract_numeric(self, values: List[str]) -> List[float]:
        """Extract numeric values from list"""
        result = []
        for v in values:
            try:
                result.append(float(v))
            except ValueError:
                pass
        return result


class CSVTransform:
    """Data transformation utilities"""

    def __init__(self, parser: CSVParser):
        self.parser = parser

    def add_column(self, name: str, value: str = '') -> CSVParser:
        """Add a new column with optional default value"""
        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )
        new_parser.headers = self.parser.headers + [name]
        new_parser.rows = [
            {**row, name: value} for row in self.parser.rows
        ]
        return new_parser

    def rename_column(self, old_name: str, new_name: str) -> CSVParser:
        """Rename a column"""
        if old_name not in self.parser.headers:
            raise CSVForgeError(f"Column not found: {old_name}")

        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )
        new_parser.headers = [new_name if h == old_name else h
                             for h in self.parser.headers]
        new_parser.rows = [
            {new_name if k == old_name else k: v for k, v in row.items()}
            for row in self.parser.rows
        ]
        return new_parser

    def delete_column(self, name: str) -> CSVParser:
        """Delete a column"""
        if name not in self.parser.headers:
            raise CSVForgeError(f"Column not found: {name}")

        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )
        new_parser.headers = [h for h in self.parser.headers if h != name]
        new_parser.rows = [
            {k: v for k, v in row.items() if k != name}
            for row in self.parser.rows
        ]
        return new_parser

    def merge_columns(self, columns: List[str], new_name: str,
                     separator: str = ' ') -> CSVParser:
        """Merge multiple columns into one"""
        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )
        new_parser.headers = [h for h in self.parser.headers if h not in columns] + [new_name]
        new_parser.rows = []
        for row in self.parser.rows:
            merged_value = separator.join(str(row.get(c, '')) for c in columns)
            new_row = {k: v for k, v in row.items() if k not in columns}
            new_row[new_name] = merged_value
            new_parser.rows.append(new_row)
        return new_parser

    def split_column(self, column: str, separator: str,
                    new_columns: List[str]) -> CSVParser:
        """Split a column into multiple columns"""
        if column not in self.parser.headers:
            raise CSVForgeError(f"Column not found: {column}")

        new_parser = CSVParser(
            delimiter=self.parser.delimiter,
            quotechar=self.parser.quotechar,
            encoding=self.parser.encoding,
            has_header=self.parser.has_header
        )

        col_idx = self.parser.headers.index(column)
        new_parser.headers = (self.parser.headers[:col_idx] +
                            new_columns +
                            self.parser.headers[col_idx + 1:])

        new_parser.rows = []
        for row in self.parser.rows:
            parts = row.get(column, '').split(separator)
            new_row = {k: v for k, v in row.items() if k != column}
            for i, nc in enumerate(new_columns):
                new_row[nc] = parts[i] if i < len(parts) else ''
            new_parser.rows.append(new_row)

        return new_parser


class CSVForge:
    """Main CSVForge CLI interface"""

    def __init__(self):
        self.parser = None

    def load(self, source: str, **kwargs) -> 'CSVForge':
        """Load CSV from file or stdin"""
        self.parser = CSVParser(**kwargs)
        if source == '-':
            self.parser.read_stream(sys.stdin)
        else:
            self.parser.read_file(source)
        return self

    def query(self) -> CSVQuery:
        """Get query interface"""
        if self.parser is None:
            raise CSVForgeError("No data loaded. Call load() first.")
        return CSVQuery(self.parser)

    def stats(self) -> CSVStats:
        """Get stats interface"""
        if self.parser is None:
            raise CSVForgeError("No data loaded. Call load() first.")
        return CSVStats(self.parser)

    def transform(self) -> CSVTransform:
        """Get transform interface"""
        if self.parser is None:
            raise CSVForgeError("No data loaded. Call load() first.")
        return CSVTransform(self.parser)

    def save(self, destination: str = '-', format: str = 'csv') -> None:
        """Save data to file or stdout"""
        if self.parser is None:
            raise CSVForgeError("No data loaded. Call load() first.")

        if format == 'csv':
            output = self.parser.write_string()
        elif format == 'json':
            output = json.dumps(self.parser.to_json(), indent=2, ensure_ascii=False)
        elif format == 'markdown' or format == 'md':
            output = self.parser.to_markdown()
        elif format == 'html':
            output = self.parser.to_html()
        elif format == 'tsv':
            output = self.parser.to_tsv()
        else:
            raise CSVForgeError(f"Unknown format: {format}")

        if destination == '-':
            print(output)
        else:
            if format == 'csv':
                self.parser.write_file(destination)
            else:
                with open(destination, 'w', encoding='utf-8') as f:
                    f.write(output)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog='csvforge',
        description='📊 CSVForge-CLI - Lightweight Terminal CSV Data Processing Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  csvforge view data.csv                    # View CSV file
  csvforge stats data.csv                   # Show statistics
  csvforge query data.csv -w "age > 18"     # Query with condition
  csvforge convert data.csv -f json         # Convert to JSON
  csvforge transform data.csv --rename "old:new"  # Rename column
  cat data.csv | csvforge view -            # Read from stdin

For more information: https://github.com/gitstq/csvforge-cli
        """
    )

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # View command
    view_parser = subparsers.add_parser('view', help='View CSV data with formatting')
    view_parser.add_argument('file', help='CSV file path or - for stdin')
    view_parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')
    view_parser.add_argument('-H', '--no-header', action='store_true', help='No header row')
    view_parser.add_argument('-n', '--lines', type=int, help='Limit number of rows')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show CSV statistics')
    stats_parser.add_argument('file', help='CSV file path or - for stdin')
    stats_parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')
    stats_parser.add_argument('-j', '--json', action='store_true', help='Output as JSON')

    # Query command
    query_parser = subparsers.add_parser('query', help='Query CSV data')
    query_parser.add_argument('file', help='CSV file path or - for stdin')
    query_parser.add_argument('-w', '--where', help='Filter condition (e.g., "age > 18")')
    query_parser.add_argument('-s', '--select', help='Select columns (comma-separated)')
    query_parser.add_argument('-o', '--order', help='Order by column')
    query_parser.add_argument('-r', '--reverse', action='store_true', help='Reverse order')
    query_parser.add_argument('-l', '--limit', type=int, help='Limit rows')
    query_parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')

    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert CSV to other formats')
    convert_parser.add_argument('file', help='CSV file path or - for stdin')
    convert_parser.add_argument('-f', '--format', required=True,
                               choices=['json', 'markdown', 'md', 'html', 'tsv'],
                               help='Output format')
    convert_parser.add_argument('-o', '--output', default='-',
                               help='Output file (default: stdout)')
    convert_parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')

    # Transform command
    transform_parser = subparsers.add_parser('transform', help='Transform CSV structure')
    transform_parser.add_argument('file', help='CSV file path or - for stdin')
    transform_parser.add_argument('--rename', help='Rename column (format: old:new)')
    transform_parser.add_argument('--add', help='Add column (format: name:value)')
    transform_parser.add_argument('--delete', help='Delete column')
    transform_parser.add_argument('-o', '--output', default='-',
                                 help='Output file (default: stdout)')
    transform_parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')

    # Head command
    head_parser = subparsers.add_parser('head', help='Show first N rows')
    head_parser.add_argument('file', help='CSV file path or - for stdin')
    head_parser.add_argument('-n', '--lines', type=int, default=10, help='Number of rows')
    head_parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')

    # Tail command
    tail_parser = subparsers.add_parser('tail', help='Show last N rows')
    tail_parser.add_argument('file', help='CSV file path or - for stdin')
    tail_parser.add_argument('-n', '--lines', type=int, default=10, help='Number of rows')
    tail_parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')

    # Schema command
    schema_parser = subparsers.add_parser('schema', help='Show column schema')
    schema_parser.add_argument('file', help='CSV file path or - for stdin')
    schema_parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')

    return parser


def format_table(headers: List[str], rows: List[List[str]], max_width: int = 30) -> str:
    """Format data as aligned table"""
    if not headers:
        return "No data"

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                display = str(cell)[:max_width]
                widths[i] = max(widths[i], len(display))

    # Build table
    lines = []

    # Header
    header_cells = [f" {headers[i]:<{widths[i]}} " for i in range(len(headers))]
    lines.append('│' + '│'.join(header_cells) + '│')

    # Separator
    sep_cells = ['─' * (w + 2) for w in widths]
    lines.append('├' + '┼'.join(sep_cells) + '┤')

    # Rows
    for row in rows:
        row_cells = []
        for i in range(len(headers)):
            cell = str(row[i]) if i < len(row) else ''
            display = (cell[:max_width-3] + '...') if len(cell) > max_width else cell
            row_cells.append(f" {display:<{widths[i]}} ")
        lines.append('│' + '│'.join(row_cells) + '│')

    # Top border
    lines.insert(0, '┌' + '┬'.join(sep_cells) + '┐')
    # Bottom border
    lines.append('└' + '┴'.join(sep_cells) + '┘')

    return '\n'.join(lines)


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        forge = CSVForge()

        if args.command == 'view':
            forge.load(args.file,
                      delimiter=args.delimiter,
                      has_header=not args.no_header)

            rows = forge.parser.rows
            if args.lines:
                rows = rows[:args.lines]

            # Format for display
            display_rows = [[row.get(h, '') for h in forge.parser.headers] for row in rows]
            print(format_table(forge.parser.headers, display_rows))
            print(f"\n📊 Showing {len(rows)} of {len(forge.parser.rows)} rows, {len(forge.parser.headers)} columns")

        elif args.command == 'stats':
            forge.load(args.file, delimiter=args.delimiter)
            stats = forge.stats().summary()

            if args.json:
                print(json.dumps(stats, indent=2, ensure_ascii=False))
            else:
                print(f"📊 CSV Statistics")
                print(f"   Total Rows: {stats['total_rows']}")
                print(f"   Total Columns: {stats['total_columns']}")
                print(f"\n📋 Column Details:")
                for col, col_stats in stats['columns'].items():
                    print(f"   • {col} ({col_stats['type']})")
                    print(f"     Non-empty: {col_stats['non_empty']}, Empty: {col_stats['empty']}, Unique: {col_stats['unique']}")
                    if 'numeric' in col_stats:
                        num = col_stats['numeric']
                        print(f"     Min: {num['min']}, Max: {num['max']}, Avg: {num['avg']:.2f}")

        elif args.command == 'query':
            forge.load(args.file, delimiter=args.delimiter)
            query = forge.query()

            if args.where:
                query = query.where_expr(args.where)
            if args.select:
                columns = [c.strip() for c in args.select.split(',')]
                query = query.select(columns)
            if args.order:
                query = query.order_by(args.order, args.reverse)
            if args.limit:
                query = query.limit(args.limit)

            forge.parser = query.parser
            display_rows = [[row.get(h, '') for h in forge.parser.headers] for row in forge.parser.rows]
            print(format_table(forge.parser.headers, display_rows))
            print(f"\n📊 {len(forge.parser.rows)} rows returned")

        elif args.command == 'convert':
            forge.load(args.file, delimiter=args.delimiter)
            forge.save(args.output, args.format)

        elif args.command == 'transform':
            forge.load(args.file, delimiter=args.delimiter)
            transform = forge.transform()

            if args.rename:
                old, new = args.rename.split(':')
                forge.parser = transform.rename_column(old, new)
            elif args.add:
                name, value = args.add.split(':', 1) if ':' in args.add else (args.add, '')
                forge.parser = transform.add_column(name, value)
            elif args.delete:
                forge.parser = transform.delete_column(args.delete)

            forge.save(args.output, 'csv')

        elif args.command == 'head':
            forge.load(args.file, delimiter=args.delimiter)
            forge.parser.rows = forge.parser.rows[:args.lines]
            display_rows = [[row.get(h, '') for h in forge.parser.headers] for row in forge.parser.rows]
            print(format_table(forge.parser.headers, display_rows))

        elif args.command == 'tail':
            forge.load(args.file, delimiter=args.delimiter)
            forge.parser.rows = forge.parser.rows[-args.lines:]
            display_rows = [[row.get(h, '') for h in forge.parser.headers] for row in forge.parser.rows]
            print(format_table(forge.parser.headers, display_rows))

        elif args.command == 'schema':
            forge.load(args.file, delimiter=args.delimiter)
            stats = forge.stats()
            print("📋 Column Schema:")
            for i, col in enumerate(forge.parser.headers, 1):
                col_stats = stats._column_stats(col)
                print(f"   {i}. {col} ({col_stats['type']})")

    except CSVForgeError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == '__main__':
    main()
