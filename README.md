# ustc-wakeup
将USTC教务系统中的课程表导出为 WakeUp课程表 app
的备份文件（*.wakeup_schedule），该备份文件可以方便地[导入到WakeUp课程表app中](https://support.qq.com/products/97617/faqs/59884?)

## 运行环境
- python 3
- 需要PIL（用来处理统一身份认证的验证码）
### 安装PIL
```bash
pip install -v pillow=="9.0.1"
```

## 使用
1. 运行 main.py，按提示操作
2. 导出的文件保存在 main.py 的同级目录下
3. 课程的颜色可通过修改color.py自定义


