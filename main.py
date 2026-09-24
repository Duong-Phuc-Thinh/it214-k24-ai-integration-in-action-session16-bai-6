import json
import time
import redis

class Database:
    def __init__(self):
        self.store = {
            1: {"id": 1, "name": "Laptop Gaming", "price": 1500.0},
            2: {"id": 2, "name": "Mechanical Keyboard", "price": 120.0}
        }

    def get_product(self, product_id):
        time.sleep(0.5)
        return self.store.get(product_id)

    def update_product(self, product_id, new_data):
        if product_id in self.store:
            self.store[product_id].update(new_data)
            time.sleep(0.2)
            return self.store[product_id]
        return None

class ProductServiceWithCache:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    def get_product_by_id(self, product_id):
        cache_key = f"product:{product_id}"
        try:
            cached_data = self.redis.get(cache_key)
            if cached_data:
                print("[Cache Hit]")
                return json.loads(cached_data)
        except redis.RedisError:
            print("[Fallback] Redis sập, lấy trực tiếp từ DB")
            return self.db.get_product(product_id)

        print("[Cache Miss] Lấy từ DB và nạp vào Cache")
        product = self.db.get_product(product_id)
        if product:
            try:
                self.redis.set(cache_key, json.dumps(product), ex=60)
            except redis.RedisError:
                pass
        return product

    def update_product(self, product_id, new_data):
        updated_product = self.db.update_product(product_id, new_data)
        if updated_product:
            cache_key = f"product:{product_id}"
            try:
                self.redis.delete(cache_key)
                print(f"[Cache Evict] Đã xóa cache cho key {cache_key}")
            except redis.RedisError:
                print("[Warning] Không thể xóa cache do Redis lỗi")
        return updated_product

if __name__ == "__main__":
    db = Database()
    try:
        redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        redis_client.ping()
    except Exception:
        redis_client = None
        print("Không kết nối được Redis, chạy chế độ giả lập fallback.")

    service = ProductServiceWithCache(db, redis_client)

    print("--- Lần gọi đầu tiên (Cache Miss) ---")
    start = time.time()
    print(service.get_product_by_id(1))
    print(f"Thời gian: {time.time() - start:.4f}s\n")

    print("--- Lần gọi thứ hai (Cache Hit) ---")
    start = time.time()
    print(service.get_product_by_id(1))
    print(f"Thời gian: {time.time() - start:.4f}s\n")

    print("--- Cập nhật sản phẩm (Write & Evict Cache) ---")
    service.update_product(1, {"price": 1400.0})

    print("--- Lần gọi sau khi update (Cache Miss do đã bị Evict) ---")
    start = time.time()
    print(service.get_product_by_id(1))
    print(f"Thời gian: {time.time() - start:.4f}s\n")