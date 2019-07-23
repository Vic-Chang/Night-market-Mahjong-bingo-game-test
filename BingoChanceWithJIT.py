import random
import sys, os
import time
import numpy as np
from numba import jit
import numba as nb

# 各類參數
size = 1  # 方陣大小
matrix = np.zeros([size, size], dtype=int)  # 二維矩陣
grab_quant = 0  # 每次抓取數量
ting_mechanism = True  # 是否有聽牌機制
ting_grab_quant = 0  # 若有聽牌機制,可額外抓取數量
loop_limit = 10  # 跑測試次數
total_count = 0  # 當前已跑次數
success_count = 0  # 成功連線次數
ting_count = 0  # 聽牌次數
ting_success_count = 0  # 聽牌後成功連線次數


@jit(nb.void(nb.int32[:, :], nb.int32, nb.int32))
def get_new_chess_jit(matrix, quantity, size):
    for i in range(quantity):
        _hPoint = random.randint(0, size - 1)
        _vPoint = random.randint(0, size - 1)

        while matrix[(_hPoint, _vPoint)] == 1:
            _hPoint = random.randint(0, size - 1)
            _vPoint = random.randint(0, size - 1)
        else:
            matrix[(_hPoint, _vPoint)] = 1


@jit(nb.boolean(nb.int32[:, :], nb.int32))
# 檢查是否有連線
def check_line_jit(jit_matrix, size):
    # 檢查直線
    if np.any(np.sum(jit_matrix, axis=1) == size):
        return True

    # 檢查恆線
    if np.any(np.sum(jit_matrix, axis=0) == size):
        return True

    # 檢查斜線( 正斜線 \ )
    _isLine = True
    for i in range(size):
        if jit_matrix[(i, i)] == 0:
            _isLine = False
            break
    if _isLine:  # 若有成線則回傳
        return True

    # 反斜線 /
    _isLine = True
    for i in range(size):
        if jit_matrix[(i, size - i - 1)] == 0:  # Numba不支援Reversed
            _isLine = False
            break
    if _isLine:  # 若有成線則回傳
        return True

    return _isLine


# 重新reset陣列
@jit(nb.void(nb.int32[:, :]))
def reset_matrix_jit(jitmatrix):
    for index, x in np.ndenumerate(jitmatrix):
        jitmatrix[index] = 0


@jit(nb.boolean(nb.int32[:, :], nb.int32))
# 檢查是否聽牌(差一號連線)
def second_chance_jit(jit_matrix, size):
    # 檢查直線
    if np.any(np.sum(jit_matrix, axis=1) == size - 1):
        return True

    # 檢查恆線
    if np.any(np.sum(jit_matrix, axis=0) == size - 1):
        return True

    _isLine = False
    # 檢查斜線( 正斜線 \ )
    _total = 0
    for i in range(size):
        _total += jit_matrix[(i, i)]
    if _total == size - 1:
        return True

    # 檢查斜線( 反斜線 \ )
    _total = 0
    for i in range(size):
        if jit_matrix[(i, size - i - 1)] != 0:  # Numba不支援Reversed
            _total += jit_matrix[(i, size - i - 1)]
    if _total == size - 1:
        return True

    return False


# 開始運行流程, 回傳是否連線
def start_process():
    # 開始運行

    # 重設棋盤
    reset_matrix_jit(matrix)

    # 抓取棋子
    get_new_chess_jit(matrix, grab_quant, size)

    # 是否有成線
    have_line = check_line_jit(matrix, size)

    if have_line:
        return True

    # 如果有聽牌機制，且不成線則開啟聽牌檢查
    if ting_mechanism and not have_line:
        ting = second_chance_jit(matrix, size)
        if ting:
            get_new_chess_jit(matrix, ting_grab_quant, size)
            global ting_count
            ting_count += 1
            have_line = check_line_jit(matrix, size)
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
        size = 6
        grab_quant = 15
        ting_mechanism = True
        ting_grab_quant = 5
        loop_limit = 20
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

    matrix = np.zeros([size, size], dtype=int)  # 初始化二維矩陣
    runtime = time.time()
    # 跑測試
    for i in range(loop_limit):
        total_count += 1
        if start_process():
            success_count += 1

    # 統計
    analysis()
    print('使用耗時: {} 秒'.format(time.time() - runtime))
