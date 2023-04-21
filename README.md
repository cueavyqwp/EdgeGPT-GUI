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
    <a href="https://github.com/cueavyqwp/EdgeGPT-GUI">
        <img alt="Github stars" src="https://img.shields.io/github/stars/cueavyqwp/EdgeGPT-GUI?color=blue">
    </a>
    <a href="https://github.com/cueavyqwp/EdgeGPT-GUI">
        <img alt="Github issues" src="https://img.shields.io/github/issues/cueavyqwp/EdgeGPT-GUI?color=blue">
    </a>

</p>

</div>

---

## 准备

### 要求

- python 3.8+
- 通过 [候补名单](http://bing.com/chat)
- ~~网络代理 具体见 [#178](https://github.com/acheong08/EdgeGPT/issues/178)~~(貌似现在不需要了)

### 获取Cookie文件

- 安装 cookie editor 扩展 [ [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) | [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) | [Edge](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlf) ]
- 访问 `bing.com`
- 点击插件图标
- 点击最右边的 `Export` -> `Export as JSON` 按钮 (cookie将会保存到你的剪切板里)
- 把你的cookie内容从剪切板中粘贴到 `cookies.json` 文件里

### 安装模块

- 按理来说运行程序时会自动下载缺失模块
- 当然 你也可以输入 `pip install -r ./requirements.txt` 来主动安装

## 运行

直接运行 `python ./EdgeGPT-GUI.py` 或 `python3 ./EdgeGPT-GUI.py`

## 说明

按 `F9` 进行发送

按 `F12` 来开启新话题

对话会以 `Markdown` 文件的形式进行储存

默认保存在`./logs`文件夹下

>~~因代理的问题 所以可能会暂停更新~~

>~~项目已寄 欢迎烧纸~~

项目正常更新

## 反馈

目前界面可能有些问题

欢迎来到`Issues`提交问题 或 到`Pull requests`提交合并请求

如果喜欢本项目的话 就点一下`Star`吧
