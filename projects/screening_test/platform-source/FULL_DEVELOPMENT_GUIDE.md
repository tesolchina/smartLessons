# 完整的前后端开发环境设置指南

## 🎉 **项目发现总结**

我们成功找到了完整的前后端项目：

### **后端项目 (ExamPlatform-BE)**
- **技术栈：** FastAPI + Python
- **数据库：** PostgreSQL
- **Git仓库：** `https://codeup.aliyun.com/68601427323b2da0bd601e0e/ExamPlatform-BE.git`
- **本地路径：** `platform-source/ExamPlatform-BE/`

### **前端项目 (ExamPlatform-FE)**
- **技术栈：** Vue 3 + Quasar + TypeScript
- **构建工具：** Vite
- **Git仓库：** `https://codeup.aliyun.com/68601427323b2da0bd601e0e/ExamPlatform-FE.git`
- **本地路径：** `platform-source/ExamPlatform-FE/`

## 🚀 **完整开发环境设置**

### **前端开发环境设置**

#### **第一步：安装Node.js依赖**
```bash
cd /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/screening_test/platform-source/ExamPlatform-FE

# 安装依赖
npm install

# 或者使用yarn
yarn install
```

#### **第二步：启动开发服务器**
```bash
# 开发模式
npm run dev

# 测试环境模式
npm run dev:test
```

#### **第三步：构建生产版本**
```bash
# 生产构建
npm run build

# 测试环境构建
npm run build:test
```

### **后端开发环境设置**

#### **第一步：Python环境**
```bash
cd /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/screening_test/platform-source/ExamPlatform-BE

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### **第二步：配置环境变量**
```bash
# 复制测试环境配置
cp .env.test .env.local

# 编辑配置
code .env.local
```

#### **第三步：启动后端服务**
```bash
# 开发模式
fastapi dev app/main.py

# 生产模式
fastapi run app/main.py --host 0.0.0.0 --port 8000
```

## 📁 **项目结构概览**

### **前端结构 (ExamPlatform-FE)**
```
ExamPlatform-FE/
├── src/
│   ├── components/      # Vue组件
│   ├── pages/          # 页面组件
│   ├── layouts/        # 布局组件
│   ├── router/         # 路由配置
│   ├── stores/         # Pinia状态管理
│   ├── i18n/          # 国际化配置
│   ├── util/          # 工具函数
│   └── App.vue        # 根组件
├── public/            # 静态资源
├── package.json       # npm配置
├── quasar.config.ts   # Quasar配置
└── index.html        # HTML入口
```

### **后端结构 (ExamPlatform-BE)**
```
ExamPlatform-BE/
├── app/
│   ├── main.py         # FastAPI应用入口
│   ├── ui/             # API路由
│   │   ├── examinee/   # 考生API
│   │   └── proctor/    # 监考API
│   ├── data/           # 数据处理
│   └── util/           # 工具函数
├── deploy/             # 部署配置
├── requirements.txt    # Python依赖
└── .env.*             # 环境配置
```

## 🔧 **开发工作流程**

### **前端开发流程**
```bash
# 1. 拉取最新代码
cd ExamPlatform-FE
git pull origin main

# 2. 创建功能分支
git checkout -b feature/fix-audio-issues

# 3. 启动开发服务器
npm run dev:test

# 4. 开发和测试
# （在浏览器中访问 http://localhost:9000）

# 5. 提交代码
git add .
git commit -m "修复音频播放问题"
git push origin feature/fix-audio-issues
```

### **后端开发流程**
```bash
# 1. 拉取最新代码
cd ExamPlatform-BE
git pull origin main

# 2. 创建功能分支
git checkout -b feature/fix-listening-section

# 3. 启动开发服务器
source venv/bin/activate
fastapi dev app/main.py

# 4. 开发和测试
# （API文档：http://localhost:8000/docs）

# 5. 提交代码
git add .
git commit -m "修复听力部分问题"
git push origin feature/fix-listening-section
```

## 🌐 **前后端联调**

### **本地开发环境**
1. **后端：** `http://localhost:8000`
2. **前端：** `http://localhost:9000`
3. **API文档：** `http://localhost:8000/docs`

### **配置前端API地址**
在前端的环境配置文件中设置后端API地址：
```bash
# .env.dev 或 .env.local
VITE_API_BASE_URL=http://localhost:8000
```

## 🚀 **部署到服务器**

### **后端部署**
```bash
# SSH到服务器
ssh root@120.79.244.157

# 更新后端代码
cd /app/ExamPlatform-BE
git pull origin main

# 重启服务
./exam-platform.sh
```

### **前端部署**
前端需要找到在服务器上的部署位置（可能在另一个ECS实例或CDN）

## 📋 **VS Code工作区设置**

### **创建多项目工作区**
```bash
# 在项目根目录创建工作区文件
cd /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/screening_test/platform-source

# 创建VS Code工作区
code examplatform.code-workspace
```

工作区配置：
```json
{
    "folders": [
        {
            "name": "Frontend",
            "path": "./ExamPlatform-FE"
        },
        {
            "name": "Backend", 
            "path": "./ExamPlatform-BE"
        }
    ],
    "settings": {
        "typescript.preferences.includePackageJsonAutoImports": "auto"
    }
}
```

## 🎯 **根据会议记录的问题修复**

现在你可以开始修复会议中发现的问题：

### **听力部分问题：**
- 音频数量不匹配（前端问题）
- 问题映射不清晰（后端API问题）

### **写作部分问题：**
- 阅读材料无法访问（前端路由问题）
- 音频时长过长（前端UI问题）

### **口语部分问题：**
- 字体大小太小（前端CSS问题）
- 自动停止功能不工作（前端JavaScript问题）

**现在你拥有了完整的前后端开发环境！可以开始修复这些问题了！** 🎉