# 夜市麻將連線遊戲機率測試


## 功能
因為在夜市玩了這個遊戲，~~越想越不對勁~~，所以寫了這個用來測試夜市麻將連線的成功連線機率。
可以自定義棋盤大小、一次抽取數量、是否有聽牌機制、聽牌後多抽取幾張。並且循環測試後，得出機率。



## 說明
專案內三個python檔案，一個是純python撰寫之檔案，一個是使用了 [Numba](https://www.jianshu.com/p/69d9d7e37bc5 "Numba") 將python的矩陣運算式compiler，將可以提高循環運算速度(約提升30倍)。

另一個檔案是Unit test，用來測試是否程式異動後有造成判斷錯誤。



## 總結
依夜市規則，若是6 * 6棋盤，一次抽取15張。沒聽牌機制下，只有 **3.58 %** 的機率成功，若有聽牌機制，聽牌後再抽5張，則機率來到 **17.30 %**




# Night Market Mahjong Bingo Game Test



## Features
This project use for testing what the chance of traditional night market Mahjong game success.



## Final Running Result 

### The result that running 50 million times.

![50m](https://user-images.githubusercontent.com/16682813/61787322-239bd300-ae42-11e9-8a00-2da62bde0de9.PNG "50 million times")


### The result that running 50 million times with Numba. 

![50m_Jit](https://user-images.githubusercontent.com/16682813/61787324-239bd300-ae42-11e9-9ff4-63d91afc6aeb.PNG "50 million times with Numba")
>This result's running time show python using Numba more faster then normal python, use less time and more efficient.(About more 30x faster)


### The result that running 100 million times with Numba.

![100m_Jit](https://user-images.githubusercontent.com/16682813/61787323-239bd300-ae42-11e9-864c-16175828db7b.PNG "100 million times with Numba")



## Compare Normal Python With Python Numba

| X  | Run 50 milion time's  | Run 100 milion time's  |
| ------------- | :-------------: | :-------------: |
| Normal Python  | 12,351 sec  | `None`  |
| Python Numba  | **399 sec**  | **780 sec**  |



## summary

If the chessboard is 6 * 6 and take 15 chesses once at random (doent't have second chance), only **3.58 %** chance to win a prize.
And if have a second chance(missing one chess to get a line) to take 5 more chess, then you got a **17.30 %** chance to win a prize.



## Unit Test
![UnitTestResult](https://user-images.githubusercontent.com/16682813/61808908-eb5eb980-ae6e-11e9-97a7-215d8db43947.PNG "Bingo game unit test")
