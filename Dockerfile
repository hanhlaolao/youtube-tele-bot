# Dùng Python nhẹ
FROM python:3.10-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt trước (để pip install có thể cache)
COPY requirements.txt .

# Cài đặt thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code còn lại vào container
COPY . .

# Chạy bot
CMD ["python", "youtube_notifier.py"]
