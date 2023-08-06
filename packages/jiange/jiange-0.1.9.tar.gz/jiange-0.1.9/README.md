# Python Packaging

[[GitLab]](https://gitlab.leihuo.netease.com/zhanglinjian1/jiange) [[pypi-jiange]](https://pypi.org/project/jiange/)

```bash
pip install jiange
```

## 开发流程

1.开发功能

```bash
# 创建环境
mkvirtualenv jiange -p /usr/bin/python3
# 测试功能
xxx
```

2.打包测试

```bash
# 创建环境
mkvirtualenv test -p /usr/bin/python3
cd /Users/zhanglinjian1/Documents/project/jiange
workon test
# 安装本包（修改后也可实时生效）
pip install -e .
```

3.上传至 pypi

```bash
# 注册 & 生成 source distribution
python setup.py sdist
# 上传至 pypi
twine upload dist/*
```

## 版本管理

1. 在 setup.py & project/version.json 中设置新的版本【upload 无法覆盖，故每次必须新建版本】
2. ```bash
   # 保存最新代码至 master 分支 & 保存最新代码至新建分支 & 上传安装包至 pypi
   sh build.sh update
   ```
