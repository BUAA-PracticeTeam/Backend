# 实践队项目前端（Vue 3）

## 目录结构

```
src/
├── api/           # 封装所有后端接口请求
│   ├── article.js
│   └── user.js
├── assets/        # 静态资源（图片、样式等）
│   ├── base.css
│   ├── main.css
│   ├── logo.png
│   ├── css/
│   │   └── global.css
│   └── img/
│       ├── aboutBG.png
│       ├── LoginBG.jpg
│       └── mountain.png
├── components/    # 全局/局部可复用组件
│   ├── FooterBar.vue
│   ├── HelloWorld.vue
│   ├── NavBar.vue
│   ├── PageContainer.vue
│   ├── SelfEntry.vue
│   └── icons/
│       ├── IconCommunity.vue
│       ├── IconDocumentation.vue
│       ├── IconEcosystem.vue
│       ├── IconSupport.vue
│       └── IconTooling.vue
├── main.js        # 入口文件，初始化Vue应用
├── App.vue        # 根组件，布局主结构
├── router/        # 路由配置
│   └── index.js
├── stores/        # 状态管理（Pinia）
│   ├── index.js
│   └── modules/
│       ├── counter.js
│       └── user.js
├── utils/         # 工具函数
│   ├── format.js
│   └── request.js
└── views/         # 页面视图
    ├── About.vue
    ├── AuthPage.vue
    ├── Forum.vue
    ├── Gallery.vue
    ├── Login.vue
    ├── PersonalCenter.vue
    ├── Register.vue
    ├── Team.vue
    ├── article/
    │   ├── ArticleEdit.vue
    │   └── ArticleManage.vue
    └── user/
        ├── UserAvatar.vue
        ├── UserPassword.vue
        └── UserProfile.vue
```

---

## 主要模块说明

### 1. 入口与主结构

- **main.js**  
  初始化 Vue 应用，集成 Element Plus、Pinia（含持久化插件）、全局样式和路由。

- **App.vue**  
  根组件，包含导航栏（NavBar）、页面内容（router-view）和底部栏（FooterBar）。

### 2. 路由（router/）

- **index.js**  
  配置所有页面路由，包括主页面、登录注册、个人中心（含子路由：文章管理、用户信息、头像、密码等）。

### 3. 状态管理（stores/）

- **index.js**  
  Pinia 状态管理入口，注册持久化插件，导出用户和计数器模块。

- **modules/user.js**  
  用户信息的状态管理，支持持久化，包含用户信息的获取、设置、清空等方法。

- **modules/counter.js**  
  简单的计数器状态管理模块，演示 Pinia 用法。

### 4. API 封装（api/）

- **user.js**  
  用户相关接口（注册、登录、信息更新、头像、密码等）。

- **article.js**  
  文章相关接口（列表、详情、发布、编辑、删除等）。

### 5. 工具函数（utils/）

- **request.js**  
  基于 axios 的请求封装，统一基础地址、超时、响应拦截等。

- **format.js**  
  时间格式化工具，基于 dayjs。

### 6. 静态资源（assets/）

- **img/**  
  存放页面用到的图片资源。

- **css/**  
  存放全局和模块化 CSS 文件。

- **logo.png**  
  项目 logo。

### 7. 组件（components/）

- **NavBar.vue**  
  全局导航栏。

- **FooterBar.vue**  
  全局底部栏。

- **PageContainer.vue**  
  页面容器组件。

- **SelfEntry.vue**  
  个人入口组件。

- **icons/**  
  项目用到的 SVG 图标组件。

### 8. 页面视图（views/）

- **About.vue**  
  团队介绍页面。

- **Team.vue**  
  队员介绍页面，展示团队成员信息。

- **Gallery.vue**  
  活动相册页面。

- **Forum.vue**  
  论坛页面。

- **Login.vue / Register.vue / AuthPage.vue**  
  用户登录、注册、认证页面。

- **PersonalCenter.vue**  
  个人中心页面，包含用户信息、头像、密码等子页面。

- **article/**  
  文章管理与编辑页面。

- **user/**  
  用户信息、头像、密码管理页面。

---

## 技术栈

- **Vue 3** + **Composition API**
- **Element Plus** UI 框架
- **Pinia** 状态管理
- **Vue Router** 路由管理
- **Axios** 请求库
- **animate.css**、**font-awesome** 图标与动画

---

## 启动方式

1. 安装依赖

   ```bash
   pnpm install
   # 或 npm install
   ```

2. 启动开发服务器

   ```bash
   pnpm dev
   # 或 npm run dev
   ```

3. 访问  
   浏览器打开 [http://localhost:5173](http://localhost:5173)

---

## 其他说明

- 所有 API 地址默认指向 `http://127.0.0.1:8000`，如需更改请修改 `src/utils/request.js`。
- 个人中心、文章管理等页面需要登录后访问。
- 静态资源和样式可根据实际需求扩展。
