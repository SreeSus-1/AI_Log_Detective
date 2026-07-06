from collections import Counter, defaultdict

def analyze_logs(logs):
    total_logs = len(logs)

    level_counts = Counter(log["level"] for log in logs)
    service_counts = Counter(log["service"] for log in logs)

    errors = [log for log in logs if log["level"] == "ERROR"]
    warnings = [log for log in logs if log["level"] == "WARN"]

    affected_services = sorted(set(log["service"] for log in errors + warnings))

    first_error = errors[0] if errors else None
    last_error = errors[-1] if errors else None

    grouped_errors = defaultdict(int)

    for error in errors:
        msg = error["message"].lower()

        if "database connection timeout" in msg:
            grouped_errors["Database connection timeout"] += 1
        elif "http 500" in msg:
            grouped_errors["HTTP 500 checkout failure"] += 1
        elif "payment" in msg:
            grouped_errors["Payment failure"] += 1
        else:
            grouped_errors["Other error"] += 1

    root_cause = detect_root_cause(logs)

    return {
        "total_logs": total_logs,
        "level_counts": dict(level_counts),
        "service_counts": dict(service_counts),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "affected_services": affected_services,
        "first_error": first_error,
        "last_error": last_error,
        "grouped_errors": dict(grouped_errors),
        "root_cause": root_cause
    }


def detect_root_cause(logs):
    messages = " ".join(log["message"].lower() for log in logs)

    if "activeconnections=30" in messages and "database connection timeout" in messages:
        return (
            "Database connection pool reached maximum capacity, "
            "causing connection timeouts and checkout failures."
        )

    if "http 500" in messages:
        return "API gateway returned HTTP 500 errors due to downstream service failure."

    if "payment authorization failed" in messages:
        return "Payment service failure detected."

    return "Root cause could not be confidently detected."