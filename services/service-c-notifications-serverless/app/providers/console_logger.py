"""Console logger provider"""
from datetime import datetime
from typing import Dict


def log_notification(event_type: str, data: Dict):
    """Log notification to console"""
    timestamp = datetime.utcnow().isoformat()
    print(f"\n{'='*60}")
    print(f"🔔 NOTIFICATION EVENT")
    print(f"{'='*60}")
    print(f"Timestamp: {timestamp}")
    print(f"Type: {event_type}")
    print(f"Data: {data}")
    print(f"{'='*60}\n")
