def my_permutation(n):
    result = []  # 用來儲存所有排列結果
    p = []  # p 代表當前排列
    generate_permutations(n, p, result)
    return result

def generate_permutations(n, p, result):
    if len(p) == n:  # 當排列長度達到 n
        result.append(p[:])  # 儲存排列的副本
        return

    for x in range(n):
        if x not in p:  # 確保 x 尚未出現在當前排列中
            p.append(x)  # 加入 x 到排列
            generate_permutations(n, p, result)  # 遞迴
            p.pop()  # 移除 x，回到上一層狀態

# 測試函數
if __name__ == "__main__":
    n = 3  # 可以更改 n 的值測試
    permutations = my_permutation(n)
    print(f"All permutations of {n} elements:")
    for perm in permutations:
        print(perm)
