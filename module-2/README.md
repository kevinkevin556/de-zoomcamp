### Table of Contents
* [What is Orchestration](#221---what-is-orchestration)

# Version 2025
## 2.2.1 - Workflow Orchestration Introduction
[![](https://img.shields.io/youtube/views/Np6QmmcgLCs?style=social)](https://www.youtube.com/watch?v=Np6QmmcgLCs)
[![Static Badge](https://img.shields.io/badge/back_to_top-8A2BE2)](#table-of-content)

> 協調 (Orchestration) 就像一支音樂管弦樂隊。你有各種不同的樂器——小提琴、喇叭、長笛——每種樂器都發出不同的聲音。它們需要在不同的時間演奏，但有些也需要同時演奏。 
> 
> Orchestration is like a musical orchestra. You have all these different instruments—violins, trumpets, flutes—each making different sounds. They all need to be played at different times, but some also need to be played simultaneously. 

這支影片簡單介紹了 Orchestration 和 Kestra、以及後續將會學到的內容，

## 2.2.2 - Learn Kestra
[![](https://img.shields.io/youtube/views/o79n-EVpics?style=social)](https://www.youtube.com/watch?v=o79n-EVpics)
[![Static Badge](https://img.shields.io/badge/back_to_top-8A2BE2)](#table-of-content)

> 告訴你去哪裡取得 Kestra 的相關資訊，可以跳過不看。
>
> 這邊簡單筆記後續執行所需要的資訊。

### 安裝方法

如果你想要[安裝 Kestra](https://kestra.io/docs/getting-started/quickstart) 的話，最簡單的方法是先安裝 Docker。接著運行環境。
```shell
docker run --pull=always --rm -it -p 8080:8080 --user=root -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp kestra/kestra:latest server local
```
接著在瀏覽器開啟 [http://localhost:8080](http://localhost:8080) 便可以操作 Kestra 的 UI。

### 準備課程環境
如果你要準備下一支 Zoomcamp 影片的操作環境的話，我們需要下載 [DTC 第二周的目錄](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration) (或者這個 repo 中 module-2 的 kestra-zoomcamp)。接著在目錄下運行：

```shell
docker compose up
```

接著在瀏覽器開啟 [http://localhost:8080](http://localhost:8080) 便可以操作 Kestra 的 UI。

### Kestra 的 Hello World 
1. 順利啟動 Kestra 後，可以看到以下畫面。

![](png/kestra-homepage.png)

2. 在右上角點擊 `<Create Flow>`，進入建立流程的頁面。這邊我們先什麼都不要編輯，直接點選右上角的 `<Save>` 儲存這個 Flow。

![](png/kestra-create-flow.png)

3. 此時畫面右上角頂端的資訊列就會出現 `<Execute>`，代表我們此時可以執行這個流程。點擊 `<Execute>` 跳出執行選項，繼續點選 `<Execute>` 開始執行。

![](png/kestra-execute-flow.png)

4. Flow 開始執行時就會出現這個 flow 的甘特圖，標示出這個流程的順序及耗時。

|Gannt| Log|
|--|--|
|![](png/kestra-gannt.png)|![](png/kestra-log.png)|

在 log 中可以看到 Flow 執行時的紀錄與相關輸出。這邊出現的 「Hello World! 🚀」就是我們在第 2 步所設置的 task:

```yaml
tasks:
  - id: hello
    type: io.kestra.plugin.core.log.Log
    message: Hello World! 🚀
```

## 2.2.3 ETL Pipelines with Postgres in Kestra
[![](https://img.shields.io/youtube/views/OkfLX28Ecjg?style=social)](https://www.youtube.com/watch?v=OkfLX28Ecjg)
[![Static Badge](https://img.shields.io/badge/back_to_top-8A2BE2)](#table-of-content)

https://kestra.io/docs/installation/docker-compose#networking-in-docker-compose

* staging truncate trick
* md5 key trick
* runif vs. flow.if 


## 2.2.4 Manage Scheduling and Backfills with Postgres in Kestra



## 2.2.5 Orchestrate dbt Models with Postgres in Kestra
[![](https://img.shields.io/youtube/views/ZLp2N6p2JjE?style=social)](https://www.youtube.com/watch?v=ZLp2N6p2JjE)
[![Static Badge](https://img.shields.io/badge/back_to_top-8A2BE2)](#table-of-content)
ZLp2N6p2JjE


