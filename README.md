#ustc-wakeup
将USTC教务系统中的课程表导出为 WakeUp课程表 app
的备份文件（*.wakeup_schedule），该备份文件可以方便地导入app中。

## 使用说明
1. 在浏览器（以PC端的 Microsoft Edge 为例）中，登录[综合教务系统](https://jw.ustc.edu.cn)
2. 在左上角的菜单中右键点击”我的课表“，点击”在新标签页中打开链接“
3. 出现课表界面后，按F12打开开发人员工具
4. 在开发人员工具最上方的标签页栏中选择”网络“
5. 刷新网页或者选择不同的学期，使网页重新加载
6. 在开发人员工具下方的网络活动列表中查找名称以”?weekIndex=“结尾的项，并点击
7. 在右侧弹出的界面中，找到”请求URL”一项，在浏览器中访问该项给出的链接
8. 按ctrl+S保存该网页为本地文件
9. 运行 main.py
10. 输入上述文件的路径，导出的文件保存在 main.py 的同级目录下
- 该文件可[导入到WakeUp课程表app](https://support.qq.com/products/97617/faqs/59884?)

## 注意
- 不支持夏季学期导入
- 课程的颜色请在app中自己设置
- 若一门课有多个老师，只保存第一个
- 未经过充分测试，不保证导出的结果正确无误
