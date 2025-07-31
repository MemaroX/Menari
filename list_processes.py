import psutil

def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        processes.append(proc.info)
    return processes

if __name__ == "__main__":
    import json
    print(json.dumps(list_processes(), indent=2))