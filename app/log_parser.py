import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<level>INFO|WARN|ERROR) "
    r"(?P<service>[\w-]+) "
    r"(?P<message>.*)"
)

def parse_log_file(file_content: str):
    logs = []

    for line in file_content.splitlines():
        match = LOG_PATTERN.match(line.strip())

        if match:
            logs.append({
                "timestamp": datetime.strptime(
                    match.group("timestamp"),
                    "%Y-%m-%d %H:%M:%S"
                ),
                "level": match.group("level"),
                "service": match.group("service"),
                "message": match.group("message")
            })

    return logs