
# Timetable

## どんなアプリか
やらなければならない大学の課題が一目でわかる時間割アプリケーションです。<br>
時間割に科目を自由に追加することができ、その科目の課題や締め切りなども登録することができるようになっています。<br>
時間割には、その科目の登録した課題の中で一番締め切りが近いものの期限を表示するようにしています。<br>
また、締め切りが近くなるにつれてその科目のコマの色が変化するよう設定しているため、時間割全体を一目みるだけで、締め切りの近い課題がどれなのかを簡単に把握できるようにしています。<br>
<br>
![image](https://user-images.githubusercontent.com/91676218/157192770-304feb61-4866-43da-b286-a8badab88e9c.png)


## 必要要件
Python 3.9.7で動作確認済み<br>
windowsを対象としています

## インストール方法と起動方法
- pythonとgitがある方
```
git clone https://github.com/Takeda-Takumi/Timetable.git
```
```
python main.py
```

- それ以外の方<br>
  - zipファイルをダウンロード<br>
![zipdownload](https://user-images.githubusercontent.com/91676218/157037646-543fad60-cdf0-40bf-8099-7b65c6b544e1.gif)<br>
  - zipファイルを解凍して、timetable.exeを起動してください



## 使い方
- 編集したい時限をクリック
![clicklesson](https://user-images.githubusercontent.com/91676218/157038769-292538a4-224f-4f8c-a2b2-22446144ab25.gif)

- 科目名の入力<br>
![enter_subject_name](https://user-images.githubusercontent.com/91676218/157039647-3edc60b3-e8f1-4d5d-a4bc-24d1da5570d3.gif)

- 課題の追加<br>
![add_assignment](https://user-images.githubusercontent.com/91676218/157041563-b9f15c1d-e6be-48a8-a978-485c3daf3b61.gif)

- 課題の削除<br>
![delete_assignment](https://user-images.githubusercontent.com/91676218/157186923-40b206b4-5601-4006-9ef0-8e637db560e9.gif)

- 編集内容の保存<br>
![save_](https://user-images.githubusercontent.com/91676218/157056915-71c1e141-0fc0-436e-ae3c-b5b4d5b88a03.gif)

- 何日後の締め切りかによってコマの色が変わります<br>
  - 1週間後以上なら赤<br>
  ![green](https://user-images.githubusercontent.com/91676218/157188966-05e87090-8289-40a1-86aa-938a69901bb8.png)

  - 3日後以上なら黄色<br>
  ![yellow](https://user-images.githubusercontent.com/91676218/157188995-f6d560c0-3197-4086-9460-cae65165e272.png)

  - 3日以内なら赤<br>
  ![red](https://user-images.githubusercontent.com/91676218/157189009-c1f7f3ac-17fb-41dd-82af-b29055b14fb1.png)
 

## 作者
Takeda-Takumi   https://github.com/Takeda-Takumi<br>
kohinigeee https://github.com/kohinigeee<br>
yakitamago https://github.com/yakitamago<br>
lach23 https://github.com/lach23<br>

## 感想・要望・バグ報告フォーム
https://forms.gle/ajpqNdLnmCjTHA9b6



