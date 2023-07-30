# ustc-wakeup
将USTC教务系统中的课程表导出为 WakeUp课程表 app
的备份文件（*.wakeup_schedule），该备份文件可以方便地[导入到WakeUp课程表app中](https://support.qq.com/products/97617/faqs/59884?)

## 使用（Linux）
```bash
git clone https://github.com/littzhch/ustc-wakeup.git
cd ustc-wakeup
pip install -r requirements.txt
python3 main.py
```
- 导出的文件保存在 main.py 的同级目录下
- 课程的颜色可通过修改 color.py 自定义


