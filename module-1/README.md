### Table of Content
* [Ingesting NY Taxi Data to Postgres](#122---ingesting-ny-taxi-data-to-postgres)
* [Connecting pgAdmin and Postgres](#123---connecting-pgadmin-and-postgres)
* [Dockerizing the Ingestion Script](#124---dockerizing-the-ingestion-script)
* [Running Postgres and pgAdmin with Docker-Compose](#125---running-postgres-and-pgadmin-with-docker-compose)
* [SQL Resfresher](#126---sql-resfresher)

## 1.2.1 - Introduction to Docker
我採用的設定，是透過 wsl 操作 Windows 系統中的 Docker。在開始前，記得啟動 Docker Desktop。

如果想要在 Windows 系統下直接運行 Docker 的話，可以參考此篇 [筆記](./how-to-run-docker-in-primitive-windows.mdhow-to)。

> [!WARNING]
> 遺憾的是，因為後續的章節會透過 Docker 運行 PostgresQL 和 PostgresQL 的圖形使用者介面(GUI) - pgadmin，而二者皆僅提供 Linux 的映像檔 (image)，所以無法在 Windows 系統下跟著課程內容實作。

## 1.2.2 - Ingesting NY Taxi Data to Postgres
[![](https://img.shields.io/youtube/views/2JM-ziJt0WI?style=social)](https://www.youtube.com/watch?v=2JM-ziJt0WI) 
![Static Badge](https://img.shields.io/badge/back_to_the_top-8A2BE2)

> 在這個單元，我們將會透過 Docker 創建能夠運行 [Postgres Database 的容器](https://hub.docker.com/r/library/postgres)，並將 [NY Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) 的資料加入 Postgres Database 之中。

### Step 1. Postgres Database From Docker
在 WSL 中，有些步驟跟 Alexey 示範的有些不同。我們首先得在 Docker 中掛載一個 Volume:
```docker
docker volume create --name dtc_postgres_volume_local -d local
```
接著運行容器
```docker
docker run -it  \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v dtc_postgres_volume_local:/var/lib/postgresql/data   \
    -p 5432:5432 \
    postgres:13
```

最後測試一下可不可以利用 `pgcli` 跟資料庫後端互動，我們先安裝以下 Python 套件
```shell
pip install pgcli psycopg_binary
```
接著在 shell 裡面執行
```shell
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
### Step 2. NY Taxi Data
因為目前 [NY Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) 資料的公開格式已經改成 `.parquet`，所以我將原本`.csv`的操作流程，針對`.parquet`做了些許調整。首先，我們先 `pip install` 以下的 Python 套件：
```
pip install pandas sqlalchemy pyarrow psycopg2_binary
```
並到這個[網站](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)下載 2021 年的 Yellow Taxi Trip Records。或者透過命令工具下載資料：
```
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
```
接著開啟 jupyter notebook 執行 [upload-data.ipynb]()，你可以直接複製這個檔案並使用它。
注意：我完成這個步驟的時候，將資料和 `upload-data.ipynb` 放置於同一個目錄下。
如果你沒有將資料放在同一個目錄之下，那麼你將需要按照檔案路徑修改 `ipynb` 中的 `pd.read_parquet(<your-data-path>)` 來讀取對應位置的資料。


## 1.2.3 - Connecting pgAdmin and Postgres
[![](https://img.shields.io/youtube/views/hCAIVe9N0ow?style=social)](https://www.youtube.com/watch?v=hCAIVe9N0ow)
[![Static Badge](https://img.shields.io/badge/back_to_the_top-8A2BE2)](#table-of-content)

> 在這個小節中，我們開始使用一個為 Postgres 設計的 GUI -- [pgAdmin](https://www.pgadmin.org/download/pgadmin-4-windows/)
來查詢 Postgres 資料庫。

### Step 1. Start using pdAdmin
進入 [pgAdmin](https://www.pgadmin.org/download/pgadmin-4-windows/) 的網站後，點選 Container 就可以看到 pdAdmin 在 DockerHub 的首頁。

我們執行下面的 Docker 指令來運行 pgAdmin 的容器：
```docker
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
```
> [!NOTE]
> 在這個步驟我們便可以關閉 pgcli 了。二者本質上而言，都同樣是跟資料庫溝通的介面程式，因此我們擇一即可。

成功下載 Docker image 並運行容器後，我們接著開啟瀏覽器，在網址列輸入`http://localhost:8080/`
順利的話，我們可以在瀏覽器中看到以下的登入頁面。使用剛才運行容器的環境變數 (EMAIL = admin@admin.com, PASSWORD=root)
可以登入控制介面。

|    pgAdmin登入頁面     | pgAdmin 控制介面  |
| :--------------------: | :---------------: |
| ![](./png/pgadmin.png) | ![](./png/pg.png) |

> [!CAUTION]
> 然而，在這邊 "Add New Server" 輸入 localhost 和對應的 port 居然沒辦法連上 Postgres 資料庫伺服器！

> [!TIP]
> 因為 Postgres 和 pdAdmin 分別在互不連通的容器裡運行，所以我們需要透過 **網路 (network)** 連接二個容器，

### Step 2. Setup Docker network
這邊我們要解決 Step 1 留下的問題。首先輸入以下指令在 Docker 中新增一個網路 `pg-network`
```docker
docker network create pg-network
```
接著運行 postgres 的容器，並在指令中加入剛剛新增的網路和容器的名稱。
```docker
docker run -it  \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v dtc_postgres_volume_local:/var/lib/postgresql/data   \
    -p 5432:5432 \
    --network pg-network \
    --name pg-database \
    postgres:13
```

> [!NOTE]  
> **`docker run image`其實是新增一個容器。**<br>
> 在影片中 Alexey 用了想要幫容器取名為 pg-database 但是沒有成功，因為他自己先前運行 (run) 容器已經用掉這個名稱了，如果在這個步驟停下來，隔天重跑一次的朋友可能也會遇到同樣的問題。

> [!TIP]
> 你可以利用 `docker container prune` 將先前新增的容器刪除後再重來。或者透過 `docker start pg-database` 重新啟用容器。

然後，運行 pgadmin 的容器，並在指令中加入剛剛新增的網路和容器的名稱。
```docker
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pg-admin\
    dpage/pgadmin4
```
> [!TIP]
> 可以透過 `Ctrl+P` `Ctrl+Q` 返回 shell，將 docker 容器保留在背景運行。

### Step 3. Connect Dastabase to GUI
最後在 "Add New Server" 中的 `Gerneral >  Name` 輸入 "Docker localhost"，`Connection` 輸入以下資訊
- `Host Name/address`: pd-database
- `Port`: 5432
- `Maintainence database`: postgres
- `Username`: root
- `Password`: root

如此便完成了容器間的通訊，順利在 pgAdmin 中接入資料庫。
|   Settings - General   |   Settings - Connection   |
| :--------------------: | :-----------------------: |
| ![](./png/general.png) | ![](./png/connection.png) |

<br>

## 1.2.4 - Dockerizing the Ingestion Script
[![](https://img.shields.io/youtube/views/B1WwATwf-vY?style=social)](https://www.youtube.com/watch?v=B1WwATwf-vY)
[![Static Badge](https://img.shields.io/badge/back_to_the_top-8A2BE2)](#table-of-content)

> 在這個小節，我們學習如何將 1.2.2 的 Data ingestion 也加入 Docker 中。
> 透過資料導入的步驟也納入容器中，為我們建置環境提供更多自動化的選擇。


*PS: Alexey 在影片中先做出 `ingest_data.py` 並測試後，才放進 Docker。我在這邊的筆記中，將影片內的步驟簡化成線性的流程便於閱讀，實際上你還是可以跟著影片、測試每個環節的半成品來熟悉操作。*

### Step 0. 移除資料
* 為了測試，我們需要移除先前放入資料庫的資料。你可以在 pgAdmin 中 `Servers > Docker localhost > Databases > ny_taxi > Schemas > public > Tables > yellow_taxi_data` 右鍵點擊、選擇 `Query tool`，並輸入以下查詢移除資料。
```sql
DROP TABLE yellow_taxi_data;
```

* 或者你可以刪除 Volume，直接重新建一組空白的環境。

```shell
docker volume create --name dtc_postgres_volume_local -d local

docker run -it  \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v dtc_postgres_volume_local:/var/lib/postgresql/data   \
    -p 5432:5432 \
    --network pg-network \
    --name pg-database \
    postgres:13

docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pg-admin\
    dpage/pgadmin4
```

### Step 1. 製作 CLI 工具 - `ingest_data.py`
我們可以利用 `jupyter nbconvert` 將 `ipynb` 轉換為 `py` 檔
```shell
jupyter nbconvert --to=script upload-data.ipynb
```
將不需要的程式碼刪除後，我們加入 `argparse` 使我們的 python script 可以輕鬆地接受命令列參數。調整後的 python script 大致如下：
* 利用 `argparse` 解析以下使用者透過輸入的資訊
    * Username
    * Password
    * Host
    * Port
    * Database name
    * Table name
    * URL for the CSV (parquet) file 
* 從上述的 URL 下載資料
* 剩餘的參數用於連接 Postgres database 並將資料匯入資料庫中，程式碼如下所示
```python
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
```
最後完成的 python script 可以參考這個檔案：[ingest_data.py]()

### Step 2. 製作 Dockerfile
我們能以先前的 Dockerfile 為基礎去修改，得到用於 `ingest_data.py` 的 Dockerfile：
```dockerfile
FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2_binary pyarrow

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
```

### Step 3. 運行容器
到這邊已經大致完成，我們先 `build` 製作出 image
```shell
docker build -t taxi_ingest:v001 .
```
再 `run` 產生並運行 docker 容器。
```shell
URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

<br>

## 1.2.5 - Running Postgres and pgAdmin with Docker-Compose
[![](https://img.shields.io/youtube/views/hKI6PkPhpa0?style=social)](https://www.youtube.com/watch?v=hKI6PkPhpa0)
[![Static Badge](https://img.shields.io/badge/back_to_the_top-8A2BE2)](#table-of-content)

>  在這個小節中，我們學習使用 Docker Compose，一次啟動所有與服務相關的程序。

### Step 1. Create `docker-compose.yaml`

新增一個 `docker-compose.yaml` 檔案，並把前面所使用的容器設定都放進去。

值得注意的是，我們在先前掛載 (mount) 的
Docker Volume `dtc_postgres_volume_local` 也需要在這個檔案中的 `volume` 底下列出，並加入屬性 `external: true`
代表已經創建的容器空間，沒有這個屬性的話，Docker 就會當成一個 docker-compose 的內部命名，並在啟動的時候另外建立
一個毫不相干的 Volume 供這組服務使用。
```yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - dtc_postgres_volume_local:/var/lib/postgresql/data
    ports:
      - 5432:5432
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - 8080:80

volumes:
  dtc_postgres_volume_local:
    external: true
```

### Step 2. Start and stop services
接著在 shell 中輸入以下指令，一次為所有服務建立並開啟容器。
```shell
docker compose up
```
或者加入選項 `-d` 在背景運行服務。
```shell
docker compose up -d
```
在 shell 中輸入以下指令，可以關閉所有服務並刪除容器。
```shell
docker compose down
```

> [!TIP]
> 可以發現一件事：**使用 docker-compose 後，我們不需要設定網路了！**
> 根據 [Docker Docs](https://docs.docker.com/compose/how-tos/networking/)，我們不需要手動地將容器透過網路串聯， docker-compose 預設便建立一個網路，並把所有使用到的容器加入其中。<br><br>
> "By default Compose sets up a single network for your app. Each container for a service joins the default network and is both reachable by other containers on that network, and discoverable by the service's name."

> [!NOTE]
> `docker-compose` or `docker compose`? <br><br>
> 在影片中 Alexey 用了 `docker-compose`， 然而這是 Compose V1 的指令，它獨立於 Docker 被開發出來，並在 2023 年 7 月宣布停止所有更新。 `docker compose`則是 Compose V2，它被整合進 Docker 作為 Docker 服務的一部分。因此，使用`docker compose` 會是更好的選擇。 可以參考：[Migrate to Compose V2](https://docs.docker.com/compose/releases/migrate/)<br><br> <img src="https://docs.docker.com/compose/images/v1-versus-v2.png" width="500" align="center" />

<br>

## 1.2.6 - SQL Resfresher
[![](https://img.shields.io/youtube/views/QEcps_iskgg?style=social)](https://www.youtube.com/watch?v=QEcps_iskgg)
[![Static Badge](https://img.shields.io/badge/back_to_the_top-8A2BE2)](#table-of-content)

### Step 1. Docker-compose the whole service
在 Youtube 影片中，Alexey 已經預先在 jupyter notebook 中將 zone 這個資料表放進去了。我在這邊採用了一個不同的方法：把前面的 `ingest_data.py` 和他對應的 Dockerfile 稍作調整後，加入 `docker-compose.yaml` 中。

> [!TIP]
> 值得一提的是，`ingest_data` 必須要在 `pgdatabase` 開啟之後才可以導入資料，因此我們要在`ingest_data`底下加入 `depend_on`、`pgdatabase` 底下加入 `healthcheck` 來確保服務的運行順序。具體細節可以參考這個小節的 [docker-compose.yaml](1.2.6%20-%20SQL%20Refresher/docker-compose.yaml)。

### Step 2. SQL queries
```sql
SELECT
    *
FROM
    trips
LIMIT 100;
```
TBD


## 1.3.1 Terraform Primer
[![](https://img.shields.io/youtube/views/s2bOYDCKl_M?style=social)](https://www.youtube.com/watch?v=s2bOYDCKl_M)
[![Static Badge](https://img.shields.io/badge/back_to_the_top-8A2BE2)](#table-of-content)

> 在這個小節，我們將會初步認識 [Terraform](https://www.terraform.io/)。

![](https://www.terraform.io/_next/static/media/terraform-community_on-light.cda79e7c.svg)

> [!NOTE]
> HashiCorp Terraform 是一個 Infrastructure as code 工具，讓你在的配置文件中定義雲端和本地資源。我們能利用這些配置文件可以進行版本控制、重複使用和共享雲端或本地資源的設定。如此，你便可以使用一致的工作流程，來配置和管理整個基礎設施的生命週期。

### Infrastructure as code
> [!TIP]
> 簡單來說，寫好 Terraform 腳本，接著跑程式碼，就可以讓 Terraform 自動幫你開好機器。我們不再需要到 Web 介面上去手動設定雲端資源。

### Terraform is not ...
* Terraform 不管理和更新基礎設施上的程式碼 (Does not manage and update code on infrastructure)
  * Terraform 負責基礎設施的配置，但不會處理運行在基礎設施上的應用程式
  * 例如：你透過 Terrafrom 開啟了一台 AWS 伺服器，它無法幫你在這台伺服器上安裝 Node.js，也無法部署你的網站代碼。
* Terraform 無法更改不可變的資源 (Does not give you the ability to change immutable resources)
  * 某些資源一旦創建就不能修改，需要銷毀並重新創建
  * 例如：你建了一個在 North America 的 AWS S3 Bucket，你沒辦法單純透過設定更動存儲位置到 Asia Pacific，只能移除重建一個 Bucket。
* Terraform 不用於管理未在 Terraform 文件中定義的資源 (Not used to manage resources not defined in your terraform files)
  * 只能管理在 Terraform 配置文件中明確定義的資源，對於外部創建的資源則無法管理
  * 例如：在使用 Terraform 之前手動部署的雲端資源，無法透過 Terraform 刪除。


## 1.3.2 Terraform Basics
[![](https://img.shields.io/youtube/views/Y2ux7gq3Z0o?style=social)](https://www.youtube.com/watch?v=Y2ux7gq3Z0o)
[![Static Badge](https://img.shields.io/badge/back_to_the_top-8A2BE2)](#table-of-content)

> 在這個小節，我們將會學習基本的 Terraform 流程


### Step 0. Create a Service Account

1. 在 Google Cloud 中新增一個專案 (Project) 名稱為 `terraform-demo`
2. 點選左上角開啟選單，點選 `IAM & Admin > Service Account`，進入頁面後點擊 `+ CREATE SERVICE ACCOUNT`，開起新增畫面。
3. 在 `Service account details > Service account name` 輸入 terraform-runner，接著 `create and continue`
4. 在 `Grant this service account access to project`中，依序加入 `Cloud Storage > Storage Admin` 和 `BigQuery > BigQuery Admin` 二個角色 (Role)，完成後回到 Service Account 那個畫面。
5. 點選 terraform-runner，開啟選單後點選 `Manage key`，接著 `Add key > Create new key > JSON`，然後把這個 json 個式的私鑰下載到工作目錄(影片中是`terrademo`)下的 `keys` 資料夾取名為 `my-creds.json`。


### Step 1. Create Terraform Script
建立一個檔案 `./main.tf`，並在 [Example Usage - Life cycle settings for storage bucket objects](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket#example-usage---life-cycle-settings-for-storage-bucket-objects) 複製建立雲端空間的程式片段。完成後的 `main.tf` 如下所示。

```terraform
// The terraform block contains Terraform settings
// including the required providers Terraform will use to provision your infrastructure.

terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.7.0"
    }
  }
}

// The provider block configures the specified provider

provider "google" {
  project     = "terraform-demo-439216"
  region      = "us-central1"
  credentials = "./keys/my-creds.json"
}

// Use resource blocks to define components of your infrastructure.

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-demo-439216-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }   
  }
}
```

### Step 2. Run Terraform Script
1. 我們首先初始化專案， Terrafrom 會根據你 `main.tf` 的服務商安裝對應所需的擴充，並產生一個 lock file `.terraform.lock.hcl` 來記錄服務商的版本。
```shell
terraform init 
```
初始化之餘，有另外 (可選的) 二件事可以幫助我們檢查我們的的配置文件：
* 驗證 (validate) 我們的配置是否合格（沒有語法錯誤、沒有相互衝突的設定）
```
terraform validate
```
* 或者整理我們配置文件的格式 (format)
```
terraform fmt
```

2. 接著使用 `plan` 產生部署計畫，這時候畫面上會顯示計畫的具體細節：
```
terraform plan
```
3. 最後使用 `apply` 執行計畫，Terraform 將會執行剛剛 `plan` 的設定，為我們建立一個 google storage bucket
```shell
terraform apply
```
![](./png/terraform-apply-1.png)

4. 如果不需要資源了，我們可以利用 `destroy` 刪除雲端資源
```shell
terraform destroy
```
![](./png/terraform-destroy-1.png) 

## 1.3.3 - Terraform Variables
