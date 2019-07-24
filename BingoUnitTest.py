import unittest
import numpy as np
import BingoChance as bingo
import BingoChanceWithJIT as bingoJit


# 測試 Bingo function
class BingoTest(unittest.TestCase):
    # 檢查是否矩陣重置
    def test_bingo_reset(self):
        # 因該function都是抓global參數，所以要先設定子參數
        bingo.size = 6
        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0]]
        bingo.reset_matrix(bingo.size)
        self.assertEqual(0, np.sum(bingo.matrix))

    # 檢查有正確抓取數量, 並執行兩次抓取數量應提升
    def test_bingo_get_new_chess(self):
        get_chess = 6
        bingo.size = 6
        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]]
        bingo.get_new_chess(get_chess)
        self.assertEqual(get_chess, np.sum(bingo.matrix))
        bingo.get_new_chess(get_chess)
        self.assertEqual(get_chess * 2, np.sum(bingo.matrix))

    # 檢查是否有正確檢查連線
    def test_bingo_check_line(self):
        bingo.size = 6

        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0]]
        self.assertTrue(bingo.check_line())
        bingo.matrix = [[0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0]]
        self.assertTrue(bingo.check_line())
        bingo.matrix = [[0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]
        self.assertTrue(bingo.check_line())
        bingo.matrix = [[1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1]]
        self.assertTrue(bingo.check_line())

        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0]]
        self.assertFalse(bingo.check_line())
        bingo.matrix = [[0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0]]
        self.assertFalse(bingo.check_line())
        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]
        self.assertFalse(bingo.check_line())
        bingo.matrix = [[1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1]]
        self.assertFalse(bingo.check_line())

    # 檢查是否有正確檢查聽牌
    def test_bingo_second_chance(self):
        bingo.size = 6
        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]]
        self.assertTrue(bingo.second_chance())
        bingo.matrix = [[0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0]]
        self.assertTrue(bingo.second_chance())
        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1]]
        self.assertTrue(bingo.second_chance())
        bingo.matrix = [[0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]
        self.assertTrue(bingo.second_chance())
        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 1, 0],
                        [0, 0, 0, 0, 0, 0]]
        self.assertFalse(bingo.second_chance())
        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]]
        self.assertFalse(bingo.second_chance())
        bingo.matrix = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]
        self.assertFalse(bingo.second_chance())
        bingo.matrix = [[0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]
        self.assertFalse(bingo.second_chance())
        bingo.matrix = [[0, 0, 0, 0, 0, 1],
                        [0, 1, 0, 0, 1, 0],
                        [1, 0, 0, 0, 0, 0],
                        [1, 0, 1, 1, 1, 0],
                        [1, 0, 0, 0, 1, 0],
                        [1, 0, 0, 0, 0, 1]]
        self.assertFalse(bingo.second_chance())


# 測試 Bingo with JIT function
class BingoTestJit(unittest.TestCase):
    # 檢查是否矩陣重置
    def test_bingoJit_reset(self):
        matrix = np.ones([6, 6], dtype=int)
        bingoJit.reset_matrix_jit(matrix)
        self.assertEqual(0, np.sum(matrix))

    # 檢查有正確抓取數量, 並執行兩次抓取數量應提升
    def test_bingoJit_get_new_chess_jit(self):
        get_chess = 5
        matrix = np.zeros([6, 6], dtype=int)
        bingoJit.get_new_chess_jit(matrix, get_chess, 6)
        self.assertEqual(get_chess, np.sum(matrix))
        bingoJit.get_new_chess_jit(matrix, get_chess, 6)
        self.assertEqual(get_chess * 2, np.sum(matrix))

    # 檢查是否有正確檢查連線
    def test_bingoJit_check_line(self):
        matrix = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 1, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.assertFalse(bingoJit.check_line_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.assertFalse(bingoJit.check_line_jit(matrix, 6))
        matrix = np.array([[1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1]])
        self.assertFalse(bingoJit.check_line_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0]])
        self.assertFalse(bingoJit.check_line_jit(matrix, 6))
        matrix = np.array([[1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 1, 1],
                           [0, 0, 1, 1, 0, 1],
                           [1, 1, 1, 0, 1, 1],
                           [0, 1, 0, 0, 1, 0],
                           [1, 1, 0, 0, 0, 1]])
        self.assertFalse(bingoJit.check_line_jit(matrix, 6))
        matrix = np.array([[1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 1]])
        self.assertTrue(bingoJit.check_line_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0]])
        self.assertTrue(bingoJit.check_line_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0]])
        self.assertTrue(bingoJit.check_line_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0]])
        self.assertTrue(bingoJit.check_line_jit(matrix, 6))

    # 檢查是否有正確檢查聽牌
    def test_bingoJit_second_chance(self):
        matrix = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.assertFalse(bingoJit.second_chance_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.assertFalse(bingoJit.second_chance_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.assertFalse(bingoJit.second_chance_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1]])
        self.assertFalse(bingoJit.second_chance_jit(matrix, 6))
        matrix = np.array([[1, 1, 0, 0, 0, 1],
                           [0, 1, 0, 0, 1, 0],
                           [1, 1, 1, 1, 0, 0],
                           [0, 1, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.assertFalse(bingoJit.second_chance_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 0, 1],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.assertTrue(bingoJit.second_chance_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0]])
        self.assertTrue(bingoJit.second_chance_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.assertTrue(bingoJit.second_chance_jit(matrix, 6))
        matrix = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 1]])
        self.assertTrue(bingoJit.second_chance_jit(matrix, 6))


if __name__ == '__main__':
    unittest.main()
