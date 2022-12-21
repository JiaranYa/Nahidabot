# 如何安装虚空

## 环境配置

环境： python3.9+ 

### 安装python 

[python下载链接](https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe) - 64位

### 安装git

[git下载链接](https://github.com/git-for-windows/git/releases/download/v2.39.0.windows.1/Git-2.39.0-64-bit.exe)

win10系统新版本也可以用winget工具

    winget install --id Git.Git -e --source winget

### 安装纳西妲

1. 使用github Desktop 
   
    推荐新手，比较容易

2. git clone
   
        git clone --depth=1 https://github.com/JiaranYa/Nahidabot.git

    
**后续步骤均在 ./Nahidabot 文件夹下开启powershell 执行**

Tips: 按Tab键会自动补全文件

3. 创建虚拟环境（可以跳过）

        python -m venv ./venv
        
        ./venv/Script/Activate.ps1

4. 安装依赖

        pip install -r requirement.txt

5. 启动

        nb run

### 安装 go-cqhttp

下载对应版本：[Releases](https://github.com/Mrs4s/go-cqhttp/releases/tag/v1.0.0-rc3)

放入 go-cqhttp 文件夹下，运行，首次运行选择3.反向Websocket通信后关闭

    



