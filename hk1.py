# 方法 a
def power2n_a(n):
    return 2**n

# 方法 b：用遞迴 （慢）
def power2n_b(n):
    if n == 0: return 1
    return power2n_b(n-1)+power2n_b(n-1)

# 方法 c：用遞迴 (快)
def power2n_c(n):
    # pass
    if n == 0: return 1
    return 2*power2n_c(n-1)

# 方法 d：用遞迴+查表
def power2n_d(n, memo={}):
    # 如果結果已經在查表中，直接返回
    if n in memo:
        return memo[n]
    
    # 基本情況
    if n == 0:
        memo[n] = 1
        return 1
    
    # 遞迴計算，並將結果存入查表中
    memo[n] = 2 * power2n_d(n - 1, memo)
    return memo[n]

# 測試
print('power2n_d(10) =', power2n_d(10))
print('power2n_d(40) =', power2n_d(40))

