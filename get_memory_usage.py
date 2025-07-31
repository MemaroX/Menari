import psutil

def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent,
        "used": memory.used,
        "free": memory.free
    }

if __name__ == "__main__":
    print(get_memory_usage())