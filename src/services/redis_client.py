import redis
import json

class RedisAsinClient:
    def __init__(self, host='localhost', port=6379, db=0, queue_name='asin_queue'):
        """
        Initializes the Redis connection and sets the queue name.
        
        Args:
        host (str): Hostname of the Redis server.
        port (int): Port on which Redis server is running.
        db (int): Redis database number.
        queue_name (str): The name of the Redis queue to pop ASIN data from.
        """
        self.queue_name = queue_name
        self.redis = redis.Redis(host=host, port=port, db=db)

    def pop(self):
        """
        Pops an ASIN data entry from the Redis queue, parses the JSON, and returns the data.
        
        Returns:
        dict: The next ASIN data dictionary from the queue, or None if the queue is empty.
        """
        raw_data = self.redis.rpop(self.queue_name)
        if raw_data:
            return json.loads(raw_data)
        return None
    
    def push(self, asin_list, type):
        data = {"asin_list": asin_list, "type": type}
        self.redis.lpush(self.queue_name, json.dumps(data))

    def caution_clear(self):
        """
        Clears the Redis queue by deleting the key.
        """
        self.redis.delete(self.queue_name)



def main():
    import argparse
    import time

    parser = argparse.ArgumentParser(description="Redis ASIN Client")
    parser.add_argument('mode', choices=['push', 'pop'], help='Run client in push or pop mode.')
    parser.add_argument('--host', default='localhost', help='Redis server host (default: localhost)')
    args = parser.parse_args()

    client = RedisAsinClient(host=args.host, queue_name='my_asin_queue')

    if args.mode == 'push':
        print(f"Connected to Redis on {args.host}. Push mode active.")
        while True:
            try:
                asin_input = input("Enter ASINs (comma-separated): ")
                if not asin_input:
                    print("No input given, exiting.")
                    break
                asin_list = asin_input.split(',')
                client.push(asin_list, "default")
                print("Pushed ASINs successfully.")
            except KeyboardInterrupt:
                print("Exiting push mode.")
                break

    elif args.mode == 'pop':
        print(f"Connected to Redis on {args.host}. Pop mode active.")
        while True:
            data = client.pop()
            if data is None:
                print("No more data in queue. Waiting.")
                time.sleep(5)
                continue
            print(f"Popped ASIN data: Type={data['type']} ASINs={', '.join(data['asin_list'])}")
            time.sleep(1)  # Adjusted from 5 to 1 second based on typical use-case


if __name__ == "__main__":
    main()