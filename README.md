"# mtmng 資產信息輔助應用" 

資產信息， 下載 MT CODE, 生成打印標籤， 管理資產圖片， 定義為輔助應用範疇。


init db   
python main.py --initdb   

from datetime import datetime
datetime.strptime(start, '%Y-%m-%d')
Idea.query.filter(Idea.time >= datetime.strptime(start, '%Y-%m-%d'),
                  Idea.time <= datetime.strptime(end, '%Y-%m-%d')).all()
   
run    
python main.py   
設定    
1.號資產類 (為超級不分類別, 無法不需處理, 不屬任一項目/票據 )   
項目/票據 
view
edit
list

2.細項分類定義  

