# Backend
Django后端

## 目录结构

```
Backend/
├── manage.py           # Django管理脚本
├── package.json        # Node依赖（如有前端构建需求）
├── package-lock.json
├── myapp/              # 核心应用
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py       # 数据模型定义
│   ├── tests.py
│   ├── views.py        # 视图与API接口
│   └── migrations/     # 数据库迁移文件
│       ├── __init__.py
│       ├── 0001_initial.py
│       ├── 0002_articles_usermanager_avatar_usermanager_introduction_and_more.py
│       └── 0003_usermanager_nickname_usermanager_work.py
├── team/               # 项目配置
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py     # 全局配置
│   ├── urls.py         # 路由配置
│   └── wsgi.py
├── template/           # 前端模板目录（如有）
└── ...                 # 其他如虚拟环境、node_modules等
```

---

## 主要模块说明

### 1. 启动与管理
- **manage.py**  
  Django项目的管理脚本，用于启动开发服务器、数据库迁移等。

### 2. 项目配置（team/）
- **settings.py**  
  包含数据库、应用、静态文件、跨域等全局配置。
- **urls.py**  
  配置后端API路由，接口统一以`/api/`或`/my/`开头。

### 3. 应用模块（myapp/）
- **models.py**  
  定义主要数据模型：
  - `UserManager`：用户信息（用户名、昵称、密码、邮箱、头像、简介、权限等）
  - `Articles`：文章（标题、内容、作者、时间、封面、标签、阅读/点赞/评论数等）
- **views.py**  
  实现主要API接口，包括注册、登录、头像上传、密码修改等。
- **migrations/**  
  数据库迁移文件，记录模型变更。

### 4. 依赖管理
- **package.json**  
  Node依赖（如有前端构建需求，可忽略）。
- Python依赖通过`requirements.txt`或虚拟环境管理（建议补充requirements.txt）。

---

## 数据模型示例

- **UserManager**
  | 字段         | 类型    | 说明         |
  | ------------ | ------- | ------------ |
  | username     | Char    | 用户名       |
  | nickname     | Char    | 昵称         |
  | password     | Char    | 密码         |
  | email        | Char    | 邮箱         |
  | work         | Char    | 工作/身份    |
  | signature    | Char    | 个性签名     |
  | avatar       | Char    | 头像URL      |
  | introduction | Char    | 个人简介     |
  | photo        | Char    | 精选照片     |
  | permission   | Integer | 权限等级     |

- **Articles**
  | 字段     | 类型    | 说明     |
  | -------- | ------- | -------- |
  | title    | Char    | 标题     |
  | content  | Char    | 内容     |
  | author   | Char    | 作者     |
  | time     | Char    | 时间     |
  | cover    | Char    | 封面图片 |
  | tag      | Char    | 标签     |
  | read     | Integer | 阅读量   |
  | like     | Integer | 点赞量   |
  | comment  | Integer | 评论量   |

---

## 主要API接口

- `POST   /api/register/`      用户注册
- `POST   /api/login/`         用户登录
- `PATCH  /my/update/avatar`   修改用户头像
- `PATCH  /my/update/pwd`      修改用户密码

接口均返回JSON格式数据，具体字段见`views.py`实现。

---

## 启动方式

1. 安装依赖（建议使用虚拟环境）
   ```bash
   pip install django pymysql python-dotenv oss2
   ```
   如有`requirements.txt`，可直接：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置数据库
   - 默认使用MySQL，配置见`team/settings.py`，请根据实际情况修改数据库名、用户、密码。

3. 运行数据库迁移
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. 启动开发服务器
   ```bash
   python manage.py runserver
   ```

5. 访问API
   - 默认地址：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 其他说明
- 跨域已通过`django-cors-headers`配置，前后端可分离开发。
- 推荐补充`requirements.txt`以便团队协作。

