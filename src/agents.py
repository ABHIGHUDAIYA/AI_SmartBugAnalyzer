import os
import requests
import json
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

# 1. Structured Output Models using Pydantic
class TriageResult(BaseModel):
    severity: str = Field(description="Classified severity: Critical, High, Medium, or Low")
    priority: str = Field(description="Classified priority: P1, P2, P3, or P4")
    component: str = Field(description="The affected system component (e.g., Database, UI, Network, Auth)")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0")
    reasoning: str = Field(description="A short 1-2 sentence explanation for this classification")

class LogAnalysisResult(BaseModel):
    exception_type: str = Field(description="The exact exception or error thrown")
    failure_point: str = Field(description="The specific file, module, or function where it failed")
    code_path: str = Field(description="The execution path or stack trace summary leading to the error")
    suggested_investigation: str = Field(description="One sentence suggesting where the developer should look first")

class RemediationResult(BaseModel):
    suggested_fix: str = Field(description="A clear 1-2 sentence suggested code fix or configuration change")

# Cache to avoid testing models on every single click
_VALID_MODEL_CACHE = {}

def get_generate_content_url(api_key: str) -> str:
    if api_key in _VALID_MODEL_CACHE:
        return _VALID_MODEL_CACHE[api_key]

    url_v1 = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
    try:
        resp = requests.get(url_v1)
        if resp.status_code == 200:
            models = resp.json().get('models', [])
            
            # Extract names that support text generation
            candidates = [m['name'] for m in models if 'generateContent' in m.get('supportedGenerationMethods', [])]
            
            # Sort candidates to prefer newer models, avoiding deprecated ones like 2.5 or 1.5 if possible
            candidates = sorted(candidates, key=lambda x: ('3.0' in x, '2.0' in x, 'flash' in x, 'pro' in x), reverse=True)
            
            # Actually test the models to see which one Google allows this user to use!
            for name in candidates:
                test_url = f"https://generativelanguage.googleapis.com/v1/{name}:generateContent?key={api_key}"
                test_payload = {"contents": [{"parts": [{"text": "hi"}]}]}
                test_resp = requests.post(test_url, json=test_payload)
                
                # If Google returns 200 OK, we found a working model!
                if test_resp.status_code == 200:
                    _VALID_MODEL_CACHE[api_key] = test_url
                    return test_url
    except Exception:
        pass
        
    return f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"

# 2. Agent Execution Functions using Raw REST API (Bypassing LangChain SDK bugs)
def run_triage_agent(api_key: str, bug_report: str) -> TriageResult:
    if not bug_report.strip():
        return TriageResult(severity="N/A", priority="N/A", component="N/A", confidence=0.0, reasoning="No bug report provided.")
        
    parser = PydanticOutputParser(pydantic_object=TriageResult)
    prompt_text = f"You are an expert QA engineer. Classify the severity, priority, and affected component.\n\nBug Report: {bug_report}\n\n{parser.get_format_instructions()}"
    
    url = get_generate_content_url(api_key)
    payload = {"contents": [{"parts": [{"text": prompt_text}]}], "generationConfig": {"temperature": 0.0}}
    
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            return TriageResult(severity="Error", priority="Error", component="Error", confidence=0.0, reasoning=f"API Rejected: {resp.status_code} - {resp.text}")
        data = resp.json()
        raw_text = data['candidates'][0]['content']['parts'][0]['text']
        return parser.parse(raw_text)
    except Exception as e:
        return TriageResult(severity="Error", priority="Error", component="Error", confidence=0.0, reasoning=f"Parsing Error: {str(e)}")

def run_log_analysis_agent(api_key: str, stack_trace: str, error_log: str) -> LogAnalysisResult:
    if not stack_trace.strip() and not error_log.strip():
        return LogAnalysisResult(exception_type="N/A", failure_point="N/A", code_path="N/A", suggested_investigation="No logs provided.")
        
    parser = PydanticOutputParser(pydantic_object=LogAnalysisResult)
    prompt_text = f"You are an expert backend engineer. Analyze the stack trace and error logs to determine the root cause.\n\nStack Trace:\n{stack_trace}\n\nError Log:\n{error_log}\n\n{parser.get_format_instructions()}"
    
    url = get_generate_content_url(api_key)
    payload = {"contents": [{"parts": [{"text": prompt_text}]}], "generationConfig": {"temperature": 0.0}}
    
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            return LogAnalysisResult(exception_type="API Error", failure_point="Error", code_path="Error", suggested_investigation=f"API Rejected: {resp.status_code} - {resp.text}")
        data = resp.json()
        raw_text = data['candidates'][0]['content']['parts'][0]['text']
        return parser.parse(raw_text)
    except Exception as e:
        return LogAnalysisResult(exception_type="Error", failure_point="Error", code_path="Error", suggested_investigation=f"Parsing Error: {str(e)}")

def run_remediation_agent(api_key: str, triage_res: TriageResult, log_res: LogAnalysisResult) -> RemediationResult:
    if triage_res.severity == "N/A" and log_res.exception_type == "N/A":
        return RemediationResult(suggested_fix="No context provided to generate a fix.")
        
    parser = PydanticOutputParser(pydantic_object=RemediationResult)
    prompt_text = f"You are an expert software remediation engineer. Based on the following AI analysis, suggest a quick, concrete fix for the developer.\n\nSeverity: {triage_res.severity}\nComponent: {triage_res.component}\nException: {log_res.exception_type}\nFailure Point: {log_res.failure_point}\n\n{parser.get_format_instructions()}"
    
    url = get_generate_content_url(api_key)
    payload = {"contents": [{"parts": [{"text": prompt_text}]}], "generationConfig": {"temperature": 0.0}}
    
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            return RemediationResult(suggested_fix=f"API Rejected: {resp.status_code} - {resp.text}")
        data = resp.json()
        raw_text = data['candidates'][0]['content']['parts'][0]['text']
        return parser.parse(raw_text)
    except Exception as e:
        return RemediationResult(suggested_fix=f"Parsing Error: {str(e)}")
