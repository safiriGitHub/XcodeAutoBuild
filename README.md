#XcodeAutoBuild

##介绍
工作中，特别是所做项目进入测试阶段，肯定会经常打 Ad-hoc 包给测试人员进行测试，但是我们肯定不想每次进行打包的时候都要进行一些工程的设置修改，以及一系列的 next 按钮点击操作，现在就让这些操作都交给脚本化吧!

1. 脚本化中使用如下的命令打包:

    `xcodebuild -project name.xcodeproj -target targetname -configuration Release -sdk iphoneos `

    `xcodebuild -workspace name.xcworkspace -scheme schemename -configuration Release -sdk iphoneos`

2. 然后使用 xcrun 生成 ipa 文件:
    `xcrun -sdk iphoneos -v PackageApplication ./build/Release-iphoneos/$(target|scheme).app"`

3. 清除 build 过程中产生的中间文件
4. 结合蒲公英分发平台，将 ipa 文件上传至蒲公英分发平台，同时在终端会打印上传结果以及上传应用后该应用的 URL。蒲公英分发平台能够方便地将 ipa 文件尽快分发到测试人员，该平台有开放 API，可避免人工上传。

##autobuild.py （xcodebuild和xcrun自动化打包）：
一、
```
Usage: autobuild.py [options]

Options:
-h, --help            show this help message and exit
-w name.xcworkspace, --workspace=name.xcworkspace
Build the workspace name.xcworkspace.
-p name.xcodeproj, --project=name.xcodeproj
Build the project name.xcodeproj.
-s schemename, --scheme=schemename
Build the scheme specified by schemename. Required if
building a workspace.
-t targetname, --target=targetname
Build the target specified by targetname. Required if
building a project.
-o output_filename, --output=output_filename
specify output filename
```
二、

在脚本顶部，有几个全局变量，根据自己的项目情况修改。
```
CODE_SIGN_IDENTITY = "iPhone Distribution: companyname (9xxxxxxx9A)"
PROVISIONING_PROFILE = "xxxxx-xxxx-xxx-xxxx-xxxxxxxxx"
CONFIGURATION = "Release"
SDK = "iphoneos"

USER_KEY = "15d6xxxxxxxxxxxxxxxxxx"
API_KEY = "efxxxxxxxxxxxxxxxxxxxx"
```
其中，`CODE_SIGN_IDENTITY` 为开发者证书标识，可以在 钥匙串访问 ->证书 -> 选中证书右键弹出菜单 -> 显示简介 -> 常用名称 获取，类似 `iPhone Distribution: Company name Co. Ltd (xxxxxxxx9A)`, 包括括号内的内容。

`PROVISIONING_PROFILE`: 这个是 mobileprovision 文件的 identifier，获取方式：

Xcode -> Preferences -> 选中申请开发者证书的 Apple ID -> 选中开发者证书 -> View Details… -> 根据 Provisioning Profiles 的名字选中打包所需的 mobileprovision 文件 -> 右键菜单 -> Show in Finder -> 找到该文件后，除了该文件后缀名的字符串就是 `PROVISIONING_PROFILE` 字段的内容。
`USER_KEY`, `API_KEY`: 是蒲公英开放 API 的密钥。

如果Xcode中不配置证书，则设置为空字符串：`CODE_SIGN_IDENTITY=''，PROVISIONING_PROFILE=''`，就自动不使用指定证书打包。

**注意**

- -o命令是文件路径不是单纯的文件名 `help="specify output filePath+filename"`
- 使用过程中出现了错误 ：
File "autobuild.py", line 6, in <module>
import requests
ImportError: No module named requests

这里requests是Python中给人用的http工具包。我通过`sudo easy_install pip`安装了pip,然后`sudo pip install requests`安装成功 ;运行过程中又出现了编码错误`ascii codec can't decode byte 0xe8 in position 0:ordinal not in range(128)` ，通过添加一下三行代码解决的：
`import sys`

`reload(sys)`

`sys.setdefaultencoding('utf-8')`



##举个栗子
`$ python autobuild.py -w EPayment.xcworkspace -s Epayment -o ~/Desktop/123.ipa`
Upload Success...

进入蒲公英看到了自己刚才上传的应用，以后每个应用放一个修改后唯一的`autobuild.py` 文件，测试，发布，就用它啦。。。

***

##autobuild_archive.py（生成 .xcarchive 再导出 .ipa 的自动打包脚本）

我的python脚本[autobuild_archive.py](https://github.com/safiriGitHub/XcodeAutoBuild)

**脚本的使用：**
在脚本顶部，有几个全局变量，根据自己的项目情况修改。
```
CONFIGURATION = "Release"

# configuration for pgyer
PGYER_UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
USER_KEY = "599xxxxxxxxxxxxxxxxxx74"
API_KEY = "39xxxxxxxxxxxxxxxxxxxxa3"
```
相关打包证书在Xcode中配置。

**举个栗子**
`python autobuild_archive.py -p xcodeAutoBuild.xcodeproj -s xcodeAutoBuild -o ~/Desktop/1232.ipa`


###详细介绍见[xcodebuild自动打包+脚本使用](http://www.jianshu.com/p/2d1c6fdc88f2)
