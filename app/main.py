from fastapi import FastAPI, UploadFile, File
from app.log_parser import parse_log_file
from app.analyzer import analyze_logs
from app.report_generator import generate_report

app = FastAPI(title="AI Log Detective")


@app.get("/")
def home():
    return {
        "message": "AI Log Detective API is running",
        "endpoint": "POST /analyze-log"
    }


@app.post("/analyze-log")
async def analyze_log(file: UploadFile = File(...)):
    content = await file.read()
    file_content = content.decode("utf-8")

    logs = parse_log_file(file_content)
    analysis = analyze_logs(logs)
    report = generate_report(analysis)

    return report