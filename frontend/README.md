# 高校就业服务平台 - 前端

基于 Vue 3 + Vite + Element Plus + Tailwind CSS 的高校就业服务平台前端项目。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5
- **UI 组件库**: Element Plus
- **样式**: Tailwind CSS + SCSS
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP 客户端**: Axios
- **图表**: ECharts 5

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 接口封装
│   ├── layouts/           # 布局组件
│   │   ├── StudentLayout.vue
│   │   ├── CompanyLayout.vue
│   │   └── AdminLayout.vue
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia 状态管理
│   ├── styles/           # 全局样式
│   ├── views/            # 页面组件
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── student/      # 学生端页面
│   │   ├── company/      # 企业端页面
│   │   └── admin/        # 管理端页面
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

项目将在 http://localhost:3000 启动。

### 构建生产版本

```bash
npm run build
```

### 代码检查

```bash
npm run lint
```

## 页面路由

### 公共页面
- `/login` - 登录页
- `/register` - 注册页

### 学生端
- `/student/home` - 首页
- `/student/jobs` - 岗位搜索
- `/student/jobs/:id` - 岗位详情
- `/student/resume` - 我的简历
- `/student/applications` - 我的投递
- `/student/favorites` - 我的收藏
- `/student/career-talks` - 宣讲会
- `/student/messages` - 消息中心
- `/student/settings` - 账号设置

### 企业端
- `/company/dashboard` - 工作台
- `/company/jobs` - 岗位管理
- `/company/resumes` - 人才库
- `/company/talks` - 宣讲会管理
- `/company/analytics` - 数据分析
- `/company/settings` - 企业设置

### 管理端
- `/admin/dashboard` - 数据大屏
- `/admin/students` - 学生管理
- `/admin/companies` - 企业管理
- `/admin/jobs` - 岗位审核
- `/admin/activities` - 活动管理
- `/admin/statistics` - 统计分析
- `/admin/settings` - 系统设置

## 环境变量

创建 `.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## API 代理

开发环境下，Vite 会将 `/api` 请求代理到后端服务器。

配置见 `vite.config.js`。

## License

MIT
