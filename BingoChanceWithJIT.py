import random
import sys, os
import time
import numpy as np
from numba import jit
import numba as nb


# Disable print function
def block_print():
    sys.stdout = open(os.devnull, 'w')


# Restore print function
def enable_print():
    sys.stdout = sys.__stdout__


# 各類參數
size = 1  # 方陣大小
matrix = []  # 二違矩陣
# matrix = np.zeros([size, size], dtype=int)  # 二維矩陣
grab_quant = 0  # 每次抓取數量
ting_mechanism = True  # 是否有聽牌機制
ting_grab_quant = 0  # 若有聽牌機制,可額外抓取數量
loop_limit = 10  # 跑測試次數
total_count = 0  # 當前已跑次數
success_count = 0  # 成功連線次數
ting_count = 0  # 聽牌次數
ting_success_count = 0  # 聽牌後成功連線次數


# 抓棋子
# parameter:quantity 抓棋子的數量
def get_new_chess(quantity):
    for i in range(quantity):
        _hPoint = random.randint(0, size - 1)
        _vPoint = random.randint(0, size - 1)
        while matrix[_hPoint][_vPoint] == 1:
            _hPoint = random.randint(0, size - 1)
            _vPoint = random.randint(0, size - 1)
        else:
            matrix[_hPoint][_vPoint] = 1


@jit(nb.void(nb.int32[:, :], nb.int32))
def get_new_chess_jit(matrix, quantity):
    for i in range(quantity):
        _hPoint = random.randint(0, size - 1)
        _vPoint = random.randint(0, size - 1)

        while matrix[(_hPoint, _vPoint)] == 1:
            _hPoint = random.randint(0, size - 1)
            _vPoint = random.randint(0, size - 1)
        else:
            matrix[(_hPoint, _vPoint)] = 1


# 檢查是否有連線
def check_line():
    _isLine = False

    # 檢查橫線
    for i in range(size):
        _isLine = True
        for j in range(size):
            if matrix[i][j] == 0:
                _isLine = False
                break
        if _isLine:  # 若有成線則回傳
            return True

    # 檢查直線
    for i in range(size):
        _isLine = True
        for j in range(size):
            if matrix[j][i] == 0:
                _isLine = False
                break
        if _isLine:  # 若有成線則回傳
            return True

    # 檢查斜線( 正斜線 \ )
    _isLine = True
    for i in range(size):
        if matrix[i][i] == 0:
            _isLine = False
            break
    if _isLine:  # 若有成線則回傳
        return True

    # 反斜線 /
    _isLine = True
    for i in zip(range(size), reversed(range(size))):
        if matrix[i[0]][i[1]] == 0:
            _isLine = False
            break
    if _isLine:  # 若有成線則回傳
        return True

    return _isLine


@jit(nb.boolean(nb.int32[:, :], nb.int32))
# 檢查是否有連線
def check_line_jit(jit_matrix, size):
    _isLine = False
    # 檢查橫線
    for i in range(size):
        _isLine = True
        for j in range(size):
            if jit_matrix[i][j] == 0:
                _isLine = False
                break
        if _isLine:  # 若有成線則回傳
            print('橫線bingo')
            print('第 ')
            print(i)
            print('行')
            return True

    # 檢查直線
    for i in range(size):
        _isLine = True
        for j in range(size):
            if jit_matrix[j][i] == 0:
                _isLine = False
                break
        if _isLine:  # 若有成線則回傳
            print('直線bingo')
            print('第 ')
            print(i)
            print('行')
            return True

    # 檢查斜線( 正斜線 \ )
    _isLine = True
    for i in range(size):
        if jit_matrix[i][i] == 0:
            _isLine = False
            break
    if _isLine:  # 若有成線則回傳
        print('斜線bingo')
        print('第 ')
        print(i)
        print('行')
        return True

    # 反斜線 /
    _isLine = True
    for i in range(size):
        if jit_matrix[i][size - i - 1] == 0:  # Numba不支援Reversed
            _isLine = False
            break
    if _isLine:  # 若有成線則回傳
        print('反橫線bingo')
        print('第 ')
        print(i)
        print('行')
        return True

    return _isLine


# 重新reset陣列
def reset_matrix(size):
    global matrix
    matrix = [[0 for i in range(size)] for j in range(size)]


# 重新reset陣列
@jit(nb.void(nb.int32[:, :]))
def reset_matrix_jit(jitmatrix):
    for index, x in np.ndenumerate(jitmatrix):
        jitmatrix[index] = 0


# 檢查是否聽牌(差一號連線)
def second_chance():
    # 檢查橫線
    for i in range(size):
        _total = 0
        for j in range(size):
            _total += matrix[i][j]
        if _total == size - 1:
            return True

    # 檢查直線
    for i in range(size):
        _total = 0
        for j in range(size):
            _total += matrix[j][i]
        if _total == size - 1:
            return True

    # 檢查斜線( 正斜線 \ )
    _total = 0
    for i in range(size):
        _total += matrix[i][i]
    if _total == size - 1:
        return True

    # 檢查斜線( 反斜線 \ )
    _total = 0
    for i in zip(range(size), reversed(range(size))):
        _total += matrix[i[0]][i[1]]
    if _total == size - 1:
        return True

    return False


# @jit(nb.boolean(nb.int32[:, :],nb.int32))
@jit()
# 檢查是否聽牌(差一號連線)
def second_chance_jit(jit_matrix):
    # 檢查橫線
    for i in range(size):
        _total = 0
        for j in range(size):
            _total += jit_matrix[i][j]
        if _total == size - 1:
            print('橫線聽牌')
            print(i)
            return True

    # 檢查直線
    for i in range(size):
        _total = 0
        for j in range(size):
            _total += jit_matrix[j][i]
        if _total == size - 1:
            print('直線聽牌')
            print(i)
            return True

    # 檢查斜線( 正斜線 \ )
    _total = 0
    for i in range(size):
        _total += jit_matrix[i][i]
    if _total == size - 1:
        print('協線聽牌')
        return True

    # 檢查斜線( 反斜線 \ )
    _total = 0
    for i in range(size):
        if jit_matrix[i][size - i - 1] == 0:  # Numba不支援Reversed
            _total += jit_matrix[i][i]
    if _total == size - 1:
        print('反協線聽牌')
        return True

    return False


# show出目前桌面
def show_matrix():
    print(matrix)


# 開始運行流程, 回傳是否連線
def start_process():
    # 開始運行
    print('==========開始==========')
    reset_matrix(size)
    show_matrix()
    print('隨機抓取 %s 張牌' % grab_quant)
    get_new_chess(grab_quant)
    show_matrix()

    have_line = check_line()
    print('是否已連線: ' + str(have_line))
    if have_line:
        return True

    if ting_mechanism and not have_line:
        ting = second_chance()
        print('是否已聽牌: ' + str(ting))
        if ting:
            get_new_chess(ting_grab_quant)
            global ting_count
            ting_count += 1
            print('再次抓取 %s 張牌' % ting_grab_quant)
            have_line = check_line()
            print('是否已連線: ' + str(have_line))
            show_matrix()
            if have_line:
                global ting_success_count
                ting_success_count += 1
                return True

    return False


def analysis():
    print('======統計結果======')
    print('> 棋盤大小 %s * %s ' % (size, size))
    print('> 一次抓牌 %s 次' % grab_quant)
    print('> 聽牌後可再抓 %s 張' % ting_grab_quant)
    print('共執行 %s 次' % loop_limit)
    print('共聽牌 %s 次' % ting_count)
    print('共成功連線 %s 次 (聽牌後連線 %s 次)' % (success_count, ting_success_count))
    print('總連線機率為 %s %%' % round((success_count / loop_limit * 100), 6))
    print('(無聽牌機制)連線機率為 %s %%' % round(((success_count - ting_success_count) / loop_limit * 100), 6))
    print('====================')


if __name__ == '__main__':
    # 測試檢查連線用
    # size=6
    # matrix =[[1, 1, 1, 0, 0, 0],[0, 1, 0, 0, 0, 0],[1, 0, 1, 0, 0, 1],[1, 1, 0, 0, 0, 1],[1, 0, 0, 1, 1, 0],[0, 1, 0, 0, 0, 1]]
    # check_line()

    # 快速設定成夜市參數
    quick_setting = input('啟用夜市快速設定? (y/n):').lower() in ['yes', 'y']
    if quick_setting:
        size = size = 6
        grab_quant = 15
        ting_mechanism = True
        ting_grab_quant = 5
        loop_limit = 10
    else:
        # 設定矩陣大小
        size = int(input('請輸入方形矩陣大小(夜市一般為6):'))
        print('大小為 %s 之方形矩陣' % size)

        # 設定抓牌數
        while grab_quant < size:
            grab_quant = int(input('請輸入抓牌數(不小於 %s):' % size))
        print('抓牌數為 %s ' % grab_quant)

        # 設定是否有聽牌機制
        if input('是否有聽牌機制?(Y/N)').lower() in ["y", "yes"]:
            ting_mechanism = True
            print('開啟聽牌機制')
            ting_grab_quant = int(input('聽牌後可再抓取數量?'))
            print('聽牌後可抓取量: %s' % ting_grab_quant)
        else:
            print('關閉聽牌機制')

        # 設定迴圈次數
        loop_limit = int(input('請輸入執行次數'))
        print('執行次數為 %s 次' % loop_limit)

    runtime = time.time()
    # 跑測試
    if not quick_setting:
        block_print()
    for i in range(loop_limit):
        total_count += 1
        if start_process():
            success_count += 1
    if not quick_setting:
        enable_print()

    # 統計
    analysis()
    print('使用耗時: {} 秒'.format(time.time() - runtime))
