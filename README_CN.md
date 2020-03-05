# SZPT-Course

一个用于查询深职院课程的简单 Python 包。

## 如何使用

如下所示。

### 安装

* 从 0.0.1 版本开始，该模块将上传到 pypi，你也可以直接使用 pip 进行安装。

```bash
pip install SZPT-Course
```

#### 手动安装

1. 打开 [Release 页面](https://github.com/HsOjo/SZPT-Course/releases)，找到最新版本的安装文件。

2. （可选）通过浏览器下载到本机，然后使用 **pip** 执行以下命令，进行安装。

```bash
pip install SZPT-Course-0.0.1-py3-none-any.whl
```

* 当然，你也可以直接复制安装包的下载链接，使用 **pip** 进行在线安装。（执行以下命令）

```bash
# 注意，这里的链接为 0.0.1 版本，请自行替换成最新版本。
pip install https://github.com/HsOjo/SZPT-Course/releases/download/0.0.1/SZPT-Course-0.0.1-py3-none-any.whl
```

### 实例代码

```python3
from szpt_course import Course

c = Course('<Course System Host>')
print(c.current_stu_year)
print(c.current_date)
print(c.current_week)
print(c.current_day)
cs = c.query('<Your Number>')
for i in cs:
    if i.week == c.current_week:
        print(i, i.day == c.current_day)

```
