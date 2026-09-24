# Tối ưu hiệu năng và nhất quán dữ liệu với Cache-Aside Pattern & Redis

## Giới thiệu
Bài tập này minh họa cách triển khai Cache-Aside Pattern, chống Cache Stampede, xử lý luồng ghi nhất quán dữ liệu và cơ chế Fallback khi Redis sập trong môi trường Python (giả lập Spring Boot & Redis).

## Hướng dẫn chạy chương trình
1. Cài đặt các thư viện cần thiết: `pip install redis`
2. Chạy Redis server (ví dụ qua Docker): `docker run -d -p 6379:6379 redis:alpine`
3. Chạy ứng dụng: `python main.py`