import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
DATA = Path(__file__).resolve().parent / "personal_income_tax_laws_300.json"
MAX_QUESTION_LEN = 1000

# doi json thanh string, cau hoi ng dung. COng lai -> prompt

LAW_FIELDS = (
    ("Mã", "id"),
    ("Chủ đề", "topic"),
    ("Đối tượng nộp thuế", "target_payer"),
    ("Nội dung", "content"),
    ("Thông tin mức thuế", "tax_rate_info"),
    ("Nguồn tham khảo", "source"),
    ("Ngày có hiệu lực", "effective_date")
)

INSTRUCTION = """
Chỉ trả lời dựa trên dữ liệu được cung cấp.
Không sử dụng kiến thức ở ngoài
Không suy đoán
Trả lời ngắn gọn, dễ hiểu
Câu trả lời phải các ghi nguồn tham khảo, ngày có hiệu lực
"""

def _clean_user_question(question):
    question = question.strip()

    if not question:
        raise ValueError("Please enter question")

    if(len(question) > MAX_QUESTION_LEN):
        raise ValueError("Question exceeds 1000 characters")

    return question

def load_law_data():
    with open(DATA, 'r', encoding="utf-8") as file:
        return json.load(file)

def format_law_context(tax_datas):
    string_law = []

    for data in tax_datas:
        tmp = []
        for lable, col in LAW_FIELDS:
            tmp.append(f"{lable}: {data[col]}")
            
        string_law.append("\n".join(tmp))

    return "\n\n----\n\n".join(string_law)

def _prompt(question, law_context):
    return f"""
Câu hỏi của người dùng:

"{question}"

Tham khảo dữ liệu thuế:

"{law_context}"
""".strip()

def get_openai_ans(question, law_context):
    question = _clean_user_question(question)

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY does not exist in .env")
    if not OPENAI_MODEL:
        raise ValueError("OPENAI_MODEL does not exist in .env")

    try:
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            timeout=30,
            default_headers={"Accept-Encoding": "gzip, deflate"},
        )

        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTION,
            input=_prompt(question, law_context),
            max_output_tokens=700,
        )

        return response.output_text.strip()

    except Exception as e:
        raise RuntimeError(
            "ERROR: Check your API key, model or reconnect your internet"
        ) from e

