# Работа с Redis-кластером и большими JSON-данными

## 1.Развёртывание Redis с помощью Docker Compose

### 1.1 Создать файл `docker-compose.yml`:

```yaml
version: '3.8'

services:
  redis-node-1:
    image: redis:7
    ports:
      - "7001:6379"
    command: ["redis-server", "--port", "6379", "--cluster-enabled", "yes", "--cluster-config-file", "nodes.conf", "--cluster-node-timeout", "5000", "--appendonly", "yes"]
    volumes:
      - ./data/node-1:/data

  redis-node-2:
    image: redis:7
    ports:
      - "7002:6379"
    command: ["redis-server", "--port", "6379", "--cluster-enabled", "yes", "--cluster-config-file", "nodes.conf", "--cluster-node-timeout", "5000", "--appendonly", "yes"]
    volumes:
      - ./data/node-2:/data

  redis-node-3:
    image: redis:7
    ports:
      - "7003:6379"
    command: ["redis-server", "--port", "6379", "--cluster-enabled", "yes", "--cluster-config-file", "nodes.conf", "--cluster-node-timeout", "5000", "--appendonly", "yes"]
    volumes:
      - ./data/node-3:/data
```

### 1.2 Запуск:

```bash
docker-compose up -d
```

### 1.3 Подключиться в один из контейнеров:

```bash
docker exec -it redis-cluster-lab-redis-node-1-1 bash
```

### 1.3 Выполнить команду для создания кластера:

```bash
redis-cli --cluster create 127.0.0.1:6379 172.18.0.2:6379 172.18.0.3:6379 --cluster-replicas 0
```
> Заменить IP-адреса на реальные IP ваших контейнеров (docker inspect <container_id>).

Подтвердить создание кластера (yes).

---
## 2.Генерация большого JSON

Создать и выполнить скрипт generate_json.py:

```python
import json
import random
import string

big_data = {
    "string_data": ''.join(random.choices(string.ascii_letters + string.digits, k=5_000_000)),
    "hash_data": {f"field_{i}": ''.join(random.choices(string.ascii_letters, k=50)) for i in range(50000)},
    "zset_data": [[f"member_{i}", random.randint(1, 10000)] for i in range(50000)],
    "list_data": [ ''.join(random.choices(string.ascii_lowercase, k=100)) for _ in range(200000)]
}

with open("big_data.json", "w") as f:
    json.dump(big_data, f)
```

---
## 3.Загрузка данных в Redis

### 3.1 Подключение к Redis

```bash
redis-cli -c -p 7001
```

### 3.2 Сохранение данных

Сохранить строку:
```bash
SET big_string "<значение из big_data.json['string_data']>"
```

Сохранить хеш:
```bash
HMSET big_hash field_1 "значение" field_2 "значение" ... (и так далее)
```

Сохранить ZSET:
```bash
ZADD big_zset 1 "member_1" 2 "member_2" ... (и так далее)
```

Сохранить список:
```bash
RPUSH big_list "элемент1" "элемент2" ... (и так далее)
```

