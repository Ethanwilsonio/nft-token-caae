import requests
import sys
import time

API_URL = "https://api.blockcypher.com/v1/btc/main/addrs/{}/full"

def fetch_transactions(address, limit=5):
    try:
        response = requests.get(API_URL.format(address), params={"limit": limit})
        response.raise_for_status()
        data = response.json()
        txs = data.get("txs", [])
        return [
            {
                "hash": tx.get("hash"),
                "total": tx.get("total"),
                "confirmed": tx.get("confirmed")
            }
            for tx in txs
        ]
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return []

def analyze_address(address, limit=5, interval=30):
    print(f"Анализ транзакций для адреса: {address}")
    known_txs = set()
    while True:
        txs = fetch_transactions(address, limit)
        for tx in txs:
            if tx["hash"] not in known_txs:
                known_txs.add(tx["hash"])
                print(f"Новая транзакция: {tx['hash']} | Сумма: {tx['total']} | Подтверждена: {tx['confirmed']}")
        print(f"Ожидание {interval} секунд до следующей проверки...")
        time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python BlockTraceAnalyzer.py <btc_address> [limit] [interval]")
        sys.exit(1)
    address = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    analyze_address(address, limit, interval)
