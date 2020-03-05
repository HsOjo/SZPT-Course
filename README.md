# SZPT-Course

A simple Course query Python package for SZPT.

## How to use

As shown below.

### Installation

* Starting from version 0.0.1, the module will be uploaded to pypi. You can also install it directly using pip.

```bash
pip install SZPT-Course
```

#### Manual Installation

1. Open the [release page](https://github.com/HsOjo/SZPT-Course/releases) to find the latest version of the installation file.

2. (Optional) download to this machine through browser, and then use **pip** to execute the following command to install.

```bash
pip install SZPT-Course-0.0.1-py3-none-any.whl
```

* Of course, you can also directly copy the download link of the installation package and use **pip** for online installation. (execute the following command)

```bash
# Note: that the link here is version 0.0.1, please replace it with the latest version.
pip install https://github.com/HsOjo/SZPT-Course/releases/download/0.0.1/SZPT-Course-0.0.1-py3-none-any.whl
```

### Example code

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
