from fastapi import Response
from fastapi.responses import JSONResponse
from typing import Dict

def response_formatter(data: Dict, status_code: int = 200):
    """Format a response with a JSON body and a status code"""
    return JSONResponse(content=data, status_code=status_code)

def error_formatter(error: str, status_code: int = 400):
    """Format an error response with a JSON body and a status code"""
    return JSONResponse(content={"error": error}, status_code=status_code)