# Shift_Kun
## 概要
このプロジェクトは、大学生のアルバイトのシフト管理を実現するためのアプリケーションです。

## 目次
1. ダウンロード方法
2. ファイル構成
3. 使用方法
   

## ダウンロード方法
以下のコマンドを実行してダウンロードしてください。
```
git clone https://github.com/bb38122080/Shift_Kun.git
cd Shift_Kun
```

## ファイル構成
├── main.py  
└── README.md

## 使用方法
### 準備
このアプリケーションのGUIは、Pythonのワークスペース[Flet](https://flet.dev/)を利用している。  
GUI表示のためにターミナルで以下のコマンドを実行してください。
```
pip install flet
```

### メインメニュー
以下のコマンドをターミナルで実行するとアプリケーションを実行できます。
```
python main.py
```
  
実行するとメインメニューが起動します。  
このメインメニュー内のボタンをクリックすることで、各機能にアクセスできます。

![image](https://github.com/user-attachments/assets/710e0a83-fdfc-43f0-82d5-c02d694caafb)  

### アルバイト先の登録
最初に、アルバイト先の情報を登録します。  
![アルバイト登録 2024-07-26 00-49-19](https://github.com/user-attachments/assets/3ba271aa-35ed-4313-bb87-3b55bbdefeb8)  
アルバイト先の名称、時給、交通費を入力します。
時給、交通費は半角で入力します。


### シフトの追加  
シフトを追加するアルバイト先を選択し、日付(YYYY-MM-DD)、時間(HH-MM)を入力します。  
![シフト追加](https://github.com/user-attachments/assets/df9b9557-a620-413c-984b-35d85f9a3e5d)  


### シフトの確認・編集
シフトを確認したい年月を入力すると、カレンダーが表示されます。 
シフトが入っている日は、赤で表示されています。  
クリックするとその日のシフトを確認できます。  
![シフト確認](https://github.com/user-attachments/assets/c331f828-6bdf-461c-971d-53482823f3f1)  

また、表示されたシフトの横にある、「編集」ボタンをクリックするとシフトの編集ができます。  
編集画面に移行するので、入力します。

![シフト編集](https://github.com/user-attachments/assets/48084c58-600e-4012-854e-51fd8bcfd856)  



### 給与計算  
給与計算したい年と月をそれぞれ半角数字で入力してください。  
![給与計算](https://github.com/user-attachments/assets/6f606ab6-1461-422e-bbe9-78fbe3876dea)  
給与を確認している時点での、実労働時間から計算された給与と、  
その月の見込みの給与が分けて表示されます。  
交通費を含めた合計と、含めない合計が分かれて表示されるので、課税される所得と、総所得を分けて把握できます。

### アルバイト先の消去
アルバイトを辞めたときなど、アルバイト先情報を削除したい時に使用します。  
![アルバイト削除](https://github.com/user-attachments/assets/46a3180b-85af-4c08-bcb9-6ed0257fbf46)



