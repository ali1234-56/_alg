import threading

def run_with_timeout(func, args=(), timeout=1):
    """
    執行一個函數，若超過指定時間則認定為無窮執行。
    :param func: 要執行的函數
    :param args: 函數的參數
    :param timeout: 時間限制（秒）
    :return: True（停止）或 False（可能無窮執行）
    """
    def wrapper():
        try:
            func(*args)
        except Exception:
            pass

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return False  # 程式可能無窮執行
    return True  # 程式已停止

# 測試範例程式
def test_program_1():
    return sum(range(1000))  # 快速結束

def test_program_2():
    while True:  # 無窮迴圈
        pass

# 停止測試
print("test_program_1:", "stops" if run_with_timeout(test_program_1) else "may not stop")
print("test_program_2:", "stops" if run_with_timeout(test_program_2) else "may not stop")
