### 如何安裝 Docker

- 在開啟或關閉 Windows 功能 (Turn Windows features on or off) 中勾選以下項目
  - 容器 (Container)
  - Hyper-V
- 在 Docker 官網下載安裝程式並執行

### 如何順利執行 [hello-world](https://hub.docker.com/_/hello-world) Docker 映像

1. 在一個具系統管理員身分 (Administrator) 的終端中執行位於`Docker`目錄下的 `.\Docker\resources dockerd.exe`
2. 在**另一個**具系統管理員身分的終端中運行 `docker run hwllo-world`

如果成功執行，你將會看到以下的說明文字：

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (windows-amd64, nanoserver-1809)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run a Windows Server container with:
 PS C:\> docker run -it mcr.microsoft.com/windows/servercore:1809 powershell

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

### 如何順利執行 Python Docker 映像

在 Windows 環境下，是沒有辦法成功執行以下指令的：

```shell
 docker run -it --entrypoint=bash python:3.9
```

第一個問題，因為官方並沒有提供在 Windows 環境下的 Docker 映像，所以本機端Docker無法找到相容於目前作業系統的映像檔。
![](../png/docker-python3.9.png)

第二個問題，是 Windows 系統上無法選擇 bash 作為進入點(entrypoint)，因為 bash 是專屬於 Linux OS 的 shell。

```
docker: Error response from daemon: container
d4a7657d822e33c928fc5f80f8cf0e3340d719bfa522ca97b6cc287e87ee4c4b encountered
an error during hcs::System::CreateProcess: bash: failure in a Windows system
call: The system cannot find the file specified. (0x2)
```

> [!TIP]
> 解決方法是，我們選擇支援 Windows 系統的 Python 3.12，並把 bash 替換為 Windows 的 powershell 即可。
>
> ```shell
> docker run -it --entrypoint=popwershell  python:3.12
> ```

### 如何順利執行 test:pandas 映像

同樣地，在 Windows 中我們把起始點的Python 版本改為 3.12

```Dockerfile
FROM python:3.12

RUN pip install pandas
```

#### Build

不要忘記最後的 `.` (使用當前目錄下的 Dockerfile)

```shell
docker build -t test:pandas .
```

#### Run

加入`-i`，使得映像檔運行時可以接受鍵盤(標準輸入)訊號

```shell
docker run -i -t test:pandas
```
