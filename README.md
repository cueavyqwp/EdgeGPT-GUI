<div align="center">

  # Edge GPT - GUI

<p align="center">
  为 <a href="https://github.com/acheong08/EdgeGPT">EdgeGPT</a> 写的 GUI
</p>

<p align="center">
    <a href="https://www.python.org">
        <img alt="Python version" src="https://img.shields.io/badge/python-3.8+-blue">
    </a>
    <a href="https://opensource.org/license/gpl-3-0/">
        <img alt="license" src="https://img.shields.io/badge/license-GPL3.0-blue">
    </a>
    <a href="https://github.com/cueavy/EdgeGPT-GUI">
        <img alt="Github stars" src="https://img.shields.io/github/stars/cueavy/EdgeGPT-GUI?color=blue">
    </a>
    <a href="https://github.com/cueavy/EdgeGPT-GUI">
        <img alt="Github issues" src="https://img.shields.io/github/issues/cueavy/EdgeGPT-GUI?color=blue">
    </a>
</p>

</div>

---

## 准备

### 要求

- python 3.8+
- ~~通过 [候补名单](http://bing.com/chat)~~(bing现已开启公测)
- ~~网络代理 具体见 [#178](https://github.com/acheong08/EdgeGPT/issues/178)~~(貌似现在不需要了)

<details>

<summary>

#### ~~获取Cookie文件~~

</summary>

- 安装 cookie editor 扩展 [ [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) | [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) | [Edge](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlf) ]
- 访问 `bing.com`
- 点击插件图标
- 点击最右边的 `Export` -> `Export as JSON` 按钮 (cookie将会保存到你的剪切板里)
- 把你的cookie内容从剪切板中粘贴到 `cookies.json` 文件里

</details>

### 安装模块

<details>

<summary>

#### Linux

</summary>

安装`tkinter` `sudo apt install python3-tk`

安装`pip` `sudo apt install python3-pip`

</details>

<details>

<summary>

</summary>

- 按理来说运行程序时会自动下载缺失模块
- 当然 你也可以输入 `pip install -r ./requirements.txt` 来主动安装

</details>

## 运行

直接运行 `python ./EdgeGPT-GUI.py` 或 `python3 ./EdgeGPT-GUI.py`

## 说明

请注意`EdgeGPT`的版本应为`requirements.txt`中所要求的版本 见 [#505](https://github.com/acheong08/EdgeGPT/issues/505)

按 `F9` 进行发送

按 `F12` 来开启新话题

对话会以 `Markdown` 文件的形式进行储存

默认保存在`chat_logs`文件夹下

日志将会保存在`logs`文件夹下

<details>

<summary>

</summary>

>~~因代理的问题 所以可能会暂停更新~~

>~~项目已寄 欢迎烧纸~~

</details>

## 其它

如果喜欢本项目的话 就点一下`Star`吧

[![Star History Chart](https://api.star-history.com/svg?repos=cueavy/EdgeGPT-GUI&type=Date)](https://star-history.com/#cueavy/EdgeGPT-GUI&Date)
