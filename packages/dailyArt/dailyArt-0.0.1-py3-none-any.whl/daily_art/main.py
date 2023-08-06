import os


def get_system_info():
    """return the system information"""
    print("*"*80)
    print(f"{os.name}")
    print(f"{os.uname().sysname}")
    print(f"{os.uname().nodename}")
    print("*"*80)
    return os.uname()


def add_one(number):
    return number + 1
    

if __name__ == "__main__":
    get_system_info()
    