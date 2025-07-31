import psutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

if __name__ == "__main__":
    print(get_cpu_usage())