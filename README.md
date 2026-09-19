# API Chatbot hỏi đáp thuế thu nhập cá nhân

Project xây dựng API chatbot hỏi đáp về thuế thu nhập cá nhân bằng FastAPI và OpenAI API. Chatbot chỉ trả lời dựa trên dữ liệu trong file `personal_income_tax_laws_300.json`.

## 1. Chức năng

- `GET /`: kiểm tra API có đang hoạt động hay không.
- `POST /chat`: nhận câu hỏi và trả về câu trả lời của chatbot.
- `GET /docs`: mở giao diện Swagger để kiểm thử API.

## 2. Cấu trúc project

```text
btvn8/
├── api.py
├── law.py
├── personal_income_tax_laws_300.json
├── .env
├── .gitignore
└── README.md
```

Trong đó:

- `api.py`: khai báo ứng dụng FastAPI và các endpoint.
- `law.py`: đọc dữ liệu luật, tạo prompt và gọi OpenAI API.
- `personal_income_tax_laws_300.json`: chứa 300 mục dữ liệu về thuế thu nhập cá nhân.
- `.env`: lưu API key và tên model OpenAI.
- `.gitignore`: ngăn các file bí mật và file tạm được đưa lên GitHub.

## 3. Yêu cầu môi trường

- Python 3.10 trở lên.
- OpenAI API key hợp lệ.

## 4. Cài đặt

Di chuyển vào thư mục project:

```bash
cd /home/nghia/Documents/btvn8
```

Tạo môi trường ảo:

```bash
python3 -m venv .venv
```

Kích hoạt môi trường ảo trên Ubuntu/Linux:

```bash
source .venv/bin/activate
```

Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## 5. Cấu hình biến môi trường

Tạo file `.env` trong thư mục gốc của project:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Thay `your_openai_api_key` bằng API key thật. Không đưa file `.env` hoặc API key thật lên GitHub.

## 6. Chạy API

Trong thư mục project, chạy lệnh:

```bash
uvicorn api:app --reload
```

Khi xuất hiện thông báo sau, API đã khởi động thành công:

```text
Uvicorn running on http://127.0.0.1:8000
```

Mở trình duyệt tại:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>

## 7. Kiểm thử API

### Kiểm tra API đang hoạt động

```bash
curl -X GET "http://127.0.0.1:8000/"
```

Kết quả dự kiến:

```json
{
  "message": "Welcome to FastAPI!"
}
```

### Gửi câu hỏi cho chatbot

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"question":"Thu nhập tính thuế 25 triệu đồng một tháng thì áp dụng thuế suất như thế nào?"}'
```

Kết quả trả về có dạng:

```json
{
  "question": "Thu nhập tính thuế 25 triệu đồng một tháng thì áp dụng thuế suất như thế nào?",
  "answer": "Câu trả lời được tạo dựa trên dữ liệu thuế đã cung cấp.",
  "model": "gpt-4.1-mini"
}
```

## 8. Định dạng request của `/chat`

Request body phải có dạng:

```json
{
  "question": "Nội dung câu hỏi"
}
```

Giới hạn độ dài câu hỏi là 1.000 ký tự. Nếu câu hỏi rỗng hoặc vượt quá giới hạn, API sẽ trả về lỗi `400`.

## 9. Lưu ý bảo mật

- Không ghi trực tiếp API key vào mã nguồn.
- Không commit file `.env` lên GitHub.
- Nếu API key bị lộ, cần thu hồi key cũ và tạo key mới ngay.
