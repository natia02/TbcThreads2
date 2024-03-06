import concurrent.futures
import json
import time
import requests

start = time.perf_counter()

products = []


# ეს არის ფუნქცია რომელიც გზავნის რექვესტებს მოცემულ ლინკზე და აბრუნებს დაბრუნებულ დათას json სახით
def fetch_data(product_id):
    url = f"https://dummyjson.com/products/{product_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for product {product_id}: {e}")


# ამ ფუნქციაში 1 პროცესისთვის 20 სრედი იქმნება და ზემოთ დაწერილ ფუნქქციას პარალელურად უშვებს სხვადასხვა პროდუქტის აიდზე.
def with_thread(product_id):
    product_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_data, product_id + i) for i in range(20)]
        num_threads = len(futures)
        for future in concurrent.futures.as_completed(futures):
            try:
                data = future.result()
                if data:
                    product_data.append(data)
            except Exception as e:
                print(f"Error fetching data: {e}")
    return product_data, num_threads


# აქ კი 5 პროცესი იქმნება რომელიც შემდეგ ჩვენს სრედების ქუნქციას უშვებს პარალელურად.
# range(1, 101, 20) საჭიროა რათა 1-დან 100-მდე ყველა აიდი დავფაროთ
def with_process():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_thread = {executor.submit(with_thread, i): i for i in range(1, 101, 20)}
        num_processes = len(future_to_thread)
        for future in concurrent.futures.as_completed(future_to_thread):
            try:
                num_threads = future.result()[1]
                products.extend(future.result()[0])
            except Exception as e:
                print(f"Error fetching data: {e}")

    return num_processes, num_threads


# ხოლო ეს ფუნქცია წამოღებულ მონაცემებს json ფაილში ინახავს
def to_file(data, filename):
    products_dict = {"products": data}
    with open(filename, 'w') as file:
        json.dump(products_dict, file, indent=2)


if __name__ == '__main__':
    num_process, num_thread = with_process()
    to_file(products, "products.json")
    end = time.perf_counter()
    print(f"Time taken: {round(end - start, 2)} seconds")
    print(f"Number of threads used: {num_thread}")
    print(f"Number of processes used: {num_process}")
