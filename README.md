# ustc-wakeup

将USTC教务系统中的课程表导出为 WakeUp课程表 app 的备份文件（*.wakeup_schedule），
该备份文件可以方便地[导入到WakeUp课程表app中](https://support.qq.com/products/97617/faqs/59884?)。

## Features

- 自带正确的时间表
- 不同的课程有不同的颜色
- 正确的时间段、授课老师，和上课地点

## Usage

### ArchLinux

1. 安装 AUR 中的 [ustcwakeup-git](https://aur.archlinux.org/packages/ustcwakeup-git) 包
2. 

```bash
$ ustcwakeup
```

### Linux

```bash
git clone https://github.com/littzhch/ustc-wakeup.git
cd ustc-wakeup
pip install -r requirements.txt
python3 main.py
```

### Windows

1. [下载](https://www.python.org/downloads/windows/)安装 Python3
2. 从 github 下载源码并解压缩。如果已安装 git，也可以使用命令 `git clone https://github.com/littzhch/ustc-wakeup.git`
3. 安装依赖库：

```powershell
pip install -r requirements.txt
```
4. 运行：
```powershell
python main.py
```

## License

This project is licensed under [GLWTPL](./LICENSE)
