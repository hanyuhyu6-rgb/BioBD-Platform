#!/usr/bin/env python3
"""
BioBD Platform - Utility Functions
"""
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any


def load_json(filepath: str) -> Any:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, filepath: str, indent: int = 2) -> None:
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def json_to_csv(json_data: List[Dict], csv_path: str) -> None:
    """Convert JSON array to CSV"""
    if not json_data:
        return
    
    fieldnames = list(json_data[0].keys())
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(json_data)


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with commas"""
    return f"{num:,.{decimals}f}"


def get_timestamp() -> str:
    """Get current timestamp"""
    return datetime.now().isoformat()


def ensure_dir(path: str) -> None:
    """Ensure directory exists"""
    os.makedirs(path, exist_ok=True)


def get_file_size(filepath: str) -> int:
    """Get file size in bytes"""
    return os.path.getsize(filepath)


def truncate_string(s: str, max_length: int = 50) -> str:
    """Truncate string with ellipsis"""
    if len(s) <= max_length:
        return s
    return s[:max_length-3] + "..."


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split list into chunks"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def count_by_field(data: List[Dict], field: str) -> Dict[str, int]:
    """Count items by field value"""
    counts = {}
    for item in data:
        value = item.get(field, "Unknown")
        counts[value] = counts.get(value, 0) + 1
    return counts


def filter_by_field(data: List[Dict], field: str, value: Any) -> List[Dict]:
    """Filter data by field value"""
    return [item for item in data if item.get(field) == value]


def search_text(data: List[Dict], query: str, fields: List[str]) -> List[Dict]:
    """Search text in multiple fields"""
    query = query.lower()
    results = []
    for item in data:
        for field in fields:
            value = str(item.get(field, "")).lower()
            if query in value:
                results.append(item)
                break
    return results


def calculate_statistics(values: List[float]) -> Dict[str, float]:
    """Calculate basic statistics"""
    if not values:
        return {"count": 0, "mean": 0, "min": 0, "max": 0, "median": 0}
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    return {
        "count": n,
        "mean": sum(sorted_values) / n,
        "min": sorted_values[0],
        "max": sorted_values[-1],
        "median": sorted_values[n // 2] if n % 2 else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    }


def log_message(message: str, level: str = "INFO") -> None:
    """Print log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


class ProgressTracker:
    """Track progress of long operations"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
    
    def update(self, increment: int = 1):
        """Update progress"""
        self.current += increment
        percent = (self.current / self.total) * 100
        print(f"\r{self.description}: {self.current}/{self.total} ({percent:.1f}%)", end="")
    
    def finish(self):
        """Mark as finished"""
        print(f"\n{self.description}: Complete!")


def main():
    """Test utilities"""
    print("Testing BioBD Utilities")
    print("=" * 50)
    
    # Test data
    test_data = [
        {"id": 1, "name": "Asset A", "score": 8.5},
        {"id": 2, "name": "Asset B", "score": 7.2},
        {"id": 3, "name": "Asset C", "score": 9.1}
    ]
    
    # Test count_by_field
    print("\nCount by phase:")
    # Would work with real phase data
    
    # Test statistics
    scores = [d["score"] for d in test_data]
    stats = calculate_statistics(scores)
    print(f"\nScore statistics: {stats}")
    
    # Test progress tracker
    tracker = ProgressTracker(5, "Testing")
    for i in range(5):
        import time
        time.sleep(0.1)
        tracker.update()
    tracker.finish()


if __name__ == "__main__":
    main()
