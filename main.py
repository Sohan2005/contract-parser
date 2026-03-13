# main.py
import json
from app.pipeline import run_pipeline
from app.database import init_db, save_result, get_all_results

# Initialize database
init_db()

# Run pipeline
result = run_pipeline("test_contract.pdf")

# Save to database
save_result("test_contract.pdf", result)

# Verify it saved
print()
print("=== SAVED RECORDS IN DATABASE ===")
rows = get_all_results()
for row in rows:
    print(f"ID: {row[0]} | File: {row[1]} | Type: {row[2]} | Created: {row[4]}")