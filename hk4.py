import numpy as np
import random

def riemann_integral(f, a, b, n):
    """
    計算一維函數 f 在區間 [a, b] 上的黎曼積分
    """
    dx = (b - a) / n
    x = np.linspace(a + dx/2, b - dx/2, n)
    return np.sum(f(x)) * dx

def monte_carlo_integral(f, a, b, n):
    """
    計算一維函數 f 在區間 [a, b] 上的蒙地卡羅積分
    """
    volume = b - a
    return volume * np.mean([f(random.uniform(a, b)) for _ in range(n)])

def triple_integral(f, a, b, n, method='riemann'):
    """
    計算三重積分
    
    參數:
        f: 被積函數
        a, b: 積分上下限
        n: 分割數或採樣點數
        method: 積分方法，'riemann' 或 'monte_carlo'
    """
    if method == 'riemann':
        return riemann_integral(lambda x: riemann_integral(lambda y: riemann_integral(lambda z: f(x, y, z), a, b, n), a, b, n), a, b, n)
    elif method == 'monte_carlo':
        volume = (b - a)**3
        return volume * np.mean([f(random.uniform(a, b), random.uniform(a, b), random.uniform(a, b)) for _ in range(n)])
    else:
        raise ValueError("Invalid method. Please choose 'riemann' or 'monte_carlo'.")

# 定義函數
def f(x, y, z):
    return 3*x**2 + y**2 + 2*z**2

# 計算三重積分
result_riemann = triple_integral(f, 0, 1, 1000, 'riemann')
print("黎曼積分結果:", result_riemann)

result_monte_carlo = triple_integral(f, 0, 1, 100000, 'monte_carlo')
print("蒙地卡羅積分結果:", result_monte_carlo)