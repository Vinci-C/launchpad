import pytest
from app.agent import get_company_doc, update_progress, get_current_status, STATE

def test_get_company_doc():
    doc = get_company_doc("policies")
    assert "Acme Corp" in doc

    doc2 = get_company_doc("nonexistent")
    assert "No matching document found" in doc2

def test_progress_tracking():
    # Reset state
    STATE.completed_tasks = []

    status = get_current_status()
    assert "haven't completed any tasks" in status

    update_progress("Read HR Handbook")
    status = get_current_status()
    assert "Read HR Handbook" in status
