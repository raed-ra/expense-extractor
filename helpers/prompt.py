def build_prompt(text):
    return f"""
    Extract each expense line item from the following bank statement text. Return a **valid JSON array only** — no explanations, headings, markdown, or extra text — just the JSON array.

    Each item must include:
    - "date": The transaction date in ISO format (YYYY-MM-DD), or null if not found.
    - "description": A concise human-readable description of the transaction.
    - "amount": A float with no currency symbols or commas (e.g., 256.00).
    - "type": Use "debit" for expenses or payments made, and "credit" for incoming funds or refunds.
    - "category": Use your best guess based on description.

    Bank statement text:
    {text}
    """
