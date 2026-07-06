def generate_report(analysis):
    first_error = analysis.get("first_error")
    last_error = analysis.get("last_error")

    if first_error and last_error:
        incident_start = first_error["timestamp"]
        incident_end = last_error["timestamp"]
        duration = incident_end - incident_start
    else:
        incident_start = "N/A"
        incident_end = "N/A"
        duration = "N/A"

    report = {
        "incident_summary": {
            "incident_start": str(incident_start),
            "incident_end": str(incident_end),
            "duration": str(duration),
            "total_logs_analyzed": analysis["total_logs"]
        },
        "severity_summary": analysis["level_counts"],
        "affected_services": analysis["affected_services"],
        "grouped_errors": analysis["grouped_errors"],
        "root_cause": analysis["root_cause"],
        "recommended_actions": [
            "Increase database connection pool size.",
            "Investigate possible database connection leaks.",
            "Add alerts when active connections exceed 80%.",
            "Add retry logic with exponential backoff.",
            "Improve monitoring for payment and checkout services."
        ]
    }

    return report