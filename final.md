# 專案報告 (參考 用到的技術原生論文，編寫內容為原創)

## 專案名稱 : 深度學習之光達自駕車導航
## **出處 :** 為本人今年暑假在臺科大實驗室的實習研究報告書

## 摘要內容 : 

使用3D LiDAR模擬簡易輕量化SLAM的自動導航功能，透過固定在車上的3D LiDAR生成點雲資料傳入到系統中，對場景中的每個環境資訊進行計算，將得到的所有Frame進行結合並建圖和定位，同時透過對大範圍的場景進行Semantic Segmentation來獲得所有點雲資訊所對應的地形和物件類別，最後透過兩者輸出進行軌跡預測完成安全行駛路線。 

傳統SLAM主要使用鏡頭來獲取資料，除了有感測深度較差和光線等環境問題外，在處理複雜或是動態環境下，可能產生資料量龐大、複雜的運算效能等問題導致無法直接繪製軌跡，以及雜訊和誤差所產生精度較低的問題。

使用LOAM的優點是，LiDAR所獲得的三維點雲資料不管是在一般的環境還是大型且複雜的環境下都能生成出更精確的環境模型，這對自動駕駛所需要的高精度環境感知來說非常重要，且LOAM的設計能在低延遲下進行高效的運算，對於需要Real-time的自駕車和機器人來說也十分有幫助。

使用RandLA-Net模型應用在輕量化的大規模點雲Semantic Segmentation，比PointNet++、SPG或KPConv等模型速度還快，記憶體的佔用也是相對較小，mIoU也比以上提到的方法都高。

![](https://hackmd.io/_uploads/BkIFX2YByg.jpg)
校園內資料蒐集

![12 (1)](https://hackmd.io/_uploads/HkxvsBjrJg.png)
台科大校園 3D Point Cloud Map

## 演算法相關內容(深度學習研究): 

RandLA-Net  為本次專案所用到的 Semantic Segmentation 深度學習模型

**其他 Semantic Segmentation 所遇到的問題 :**

1. 點採樣的計算非常耗時
2. 模型的局部特徵萃取器成本較高
3. 無法有效地從大型 point cloud 中(通常包含數以百計的物件)萃取局部特徵

**解決方法 :**

random sample 快速地對 point cloud 進行採樣

Local Feature Aggregation 來避免隨機採樣對模型表現的損害

### Randle Sample

作者採用隨機採樣的方式來取代傳統的FPS 和IDIS採樣方式，並且重複4次，將點雲壓縮至原始數據點的1 / 256，這樣做的好處極大的降低了計算的複雜度使得原本複雜度為O(n²) 的演算法降低至O(1)

### Local Feature Aggregator

為了彌補隨機採樣帶來的更多的資訊損失，作者提出了一個相比於之前pointNet++利用聚類提取特徵的更好的更正提取演算法，可以拆分為三塊內容:


#### Local Spatial Encoding

![yGzD7cN](https://hackmd.io/_uploads/By0njViSyl.png)


1. 首先輸入的是(N , 3+d)代表的是N個點， xyz座標 + d維特徵: PS：這裡的input可以是每次模組的初始輸入，也可以代表的是網路的初始輸入。

2. 對於N個點進行k近鄰的搜索，其每個點都能找到對應的(K , 3 + d)個近鄰用來表示這個點

3. 將步驟2的k個近鄰的空間資訊顯示的空間編碼後輸入給MLP，並且將維度調整至與特徵相同的維度。其中可表示為第i個點的空間特徵拼接上k近鄰的空間特徵拼接上k近鄰與第i個點的相對偏移與其歐式距離

4. 將步驟3的空間位置編碼與步驟2的特徵拼接，並作為下一階段輸入

#### Attentive Pooling

![esaJnMr](https://hackmd.io/_uploads/BysTiViBJl.png)


上一步驟的整合後的空間特徵(K, d)拼接特徵特徵(K , d) 在經過一個MLP並經過softmax後得到了一個注意力權重，與原始輸入相互做點積後得到加權後的(K , 2d)。

經過一個池化以及一個MLP升維後，最終得到一個(1 , d’)的向量，這個就是第i個點整合了k近鄰的信息表示。

#### Dilated Residual Block

![bOxtoJD](https://hackmd.io/_uploads/SyuCoVjrkx.png)

![CBOqTGN](https://hackmd.io/_uploads/B1_khVjSJe.png)



作者採用將上述兩單元堆疊的方式，提昇模型的感受。一個 LocSE/Attentive Pooling 組合單元會聚合鄰近 K 個點的特徵，代表每一次堆疊，感受野就增長 K 倍，如下圖所示。理論上堆疊越多越好，但作者考慮到計算效率以及過擬合的問題，論文中僅堆疊 2 層組成一個殘差模塊。

### 語意分割成果如下 (台科大校園內部做測試)

![image2](https://hackmd.io/_uploads/r1ap54sSJe.png)

![image](https://hackmd.io/_uploads/BJRT9NsSJx.png)

![image](https://hackmd.io/_uploads/H1DGsEjB1x.png)

---

專案使用 **LeGO LOAM** 進行 SLAM ， 透過以下方法完成


#### Segmentation: 

把原始的點雲資料投影為一個距離圖像，投影後將三維變成二維，以像素點到感測器之間的距離作為像素值，隨後將距離圖像分割成很多的群集(Cluster)，然後在同一群集上進行標記，比較少的群集總數 ( < 30 )會被視為雜訊去除，因為雜訊會造成精度下降而干擾物體的特徵提取，所以雜訊去除有利於提高後面處理效率和特徵提取的準確度。
![21](https://hackmd.io/_uploads/BJ876roByx.png)

![22](https://hackmd.io/_uploads/ByaXprsHJg.png)


#### Feature Extraction: 

距離圖像水平分為幾個子圖像，從地面點和點雲分割後的點進行特徵提取，而不是對原始點雲資料進行特徵提取，而特徵提取的輸出會有類別約束的平面點雲Fp、邊緣點雲Fe和子圖像中的平面點雲fp、邊緣點雲fe，如圖3-4、圖3-5。
![23](https://hackmd.io/_uploads/H1uV6HsSkx.png)
![24](https://hackmd.io/_uploads/HJ-HpSiSJx.png)


#### Lidar Odometry: 

特徵提取時，得到四種特徵點雲集{ Fp,Fe,fp,fe }，為了更好的尋找相鄰兩Frame點雲資料之間的對應特徵點，使用如圖3-6的方法進行改善。

![25](https://hackmd.io/_uploads/rJ5Bprsr1l.png)


在連續Frame之間進行邊緣點和平面點的特徵匹配找到連續Frame之
間的姿態變換。
#### Mapping: 

對特徵進一步處理，在全局點雲地圖中進行當前特徵和周圍點雲圖的匹配來改善姿態，全局點雲地圖透過兩種方式來獲得，一是距離當前感測器距離100公尺的特徵群集作為key-frame拼接到點雲地圖中，二是使用因子圖位姿優化估計，此外利用第二種方法還可以構建pose-graph，同時可以改善Loop Closing。

#### Transform integration: 

結合Lidar Odometry和Lidar Mapping的pose estimation，完成最後的 pose estimate。
