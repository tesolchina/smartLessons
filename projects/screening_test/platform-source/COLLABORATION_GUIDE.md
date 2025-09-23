# 阿里云Codeup协作开发指南

## 🔄 **像GitHub一样的开发协作流程**

阿里云Codeup支持完整的Git协作功能，包括分支管理、合并请求（类似GitHub的Pull Request）和代码评审。

## 📋 **标准协作工作流程**

### **第一步：创建功能分支**
```bash
# 在前端项目中
cd ExamPlatform-FE
git checkout main
git pull origin main
git checkout -b feature/fix-listening-audio-issue

# 在后端项目中
cd ExamPlatform-BE
git checkout main
git pull origin main
git checkout -b feature/fix-listening-api
```

### **第二步：进行代码修改**
```bash
# 编辑文件
code src/pages/ListeningTest.vue

# 查看修改
git diff

# 暂存修改
git add .

# 提交修改
git commit -m "修复听力测试音频数量不匹配问题

- 更新音频文件计数逻辑
- 修复问题映射关系
- 参考会议记录21-09-25的问题描述"
```

### **第三步：推送分支**
```bash
# 推送新分支到远程仓库
git push origin feature/fix-listening-audio-issue
```

### **第四步：创建合并请求（Pull Request）**

#### **方法A：通过阿里云Codeup网页界面**
1. **访问项目页面：**
   - 前端：`https://codeup.aliyun.com/68601427323b2da0bd601e0e/ExamPlatform-FE`
   - 后端：`https://codeup.aliyun.com/68601427323b2da0bd601e0e/ExamPlatform-BE`

2. **创建合并请求：**
   - 点击 **"合并请求"** 或 **"Merge Request"**
   - 点击 **"新建合并请求"**
   - 选择源分支：`feature/fix-listening-audio-issue`
   - 选择目标分支：`main`

3. **填写合并请求信息：**
   ```markdown
   ## 修复听力测试音频问题
   
   ### 问题描述
   根据9月21日会议记录，发现以下问题：
   - 音频数量与说明不匹配（说明提到2个音频，实际只有1个）
   - 问题与音频段落的映射关系不清晰
   
   ### 解决方案
   - [ ] 修复音频计数逻辑
   - [ ] 更新UI显示正确的音频数量
   - [ ] 改进问题映射机制
   
   ### 测试
   - [ ] 本地测试通过
   - [ ] 与后端API联调正常
   
   ### 相关文件
   - `src/pages/ListeningTest.vue`
   - `src/components/AudioPlayer.vue`
   
   ### 会议记录参考
   参考：`meeting_notes/meeting-summary-921-testplatform.md`
   ```

#### **方法B：通过命令行（如果支持）**
```bash
# 某些Git工具支持命令行创建MR
git push origin feature/fix-listening-audio-issue -o merge_request.create
```

## 👥 **通知开发者的方法**

### **1. 合并请求自动通知**
- 创建合并请求时，系统会自动通知项目成员
- 可以指定特定的审查者（Reviewer）

### **2. @提及功能**
在合并请求描述或评论中使用：
```markdown
@hermitriver 请审查这个修复听力测试的合并请求
@developer-username 这个修改解决了会议中提到的音频问题
```

### **3. 邮件通知**
阿里云Codeup会发送邮件通知到：
- 项目成员
- 合并请求的审查者
- 关注该项目的用户

### **4. 项目协作设置**
```bash
# 查看项目成员
git remote -v
# 显示：origin  https://codeup.aliyun.com/68601427323b2da0bd601e0e/ExamPlatform-FE.git
```

## 🔧 **合并请求最佳实践**

### **合并请求标题格式**
```
[类型] 简短描述

例如：
[修复] 听力测试音频数量不匹配问题
[功能] 添加写作测试阅读材料显示
[优化] 口语测试字体大小和自动停止功能
```

### **合并请求描述模板**
```markdown
## 变更类型
- [ ] 缺陷修复
- [ ] 新功能
- [ ] 性能优化
- [ ] 代码重构
- [ ] 文档更新

## 问题描述
[描述要解决的问题]

## 解决方案
[描述如何解决问题]

## 测试检查
- [ ] 本地测试通过
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] UI/UX验证完成

## 相关Issue/会议记录
- 会议记录：meeting_notes/meeting-summary-921-testplatform.md
- 相关问题：[链接到具体问题]

## 截图/录屏
[如果是UI修改，提供前后对比图]
```

## 📝 **代码评审流程**

### **作为提交者**
1. **创建详细的合并请求**
2. **响应评审意见**
3. **根据反馈修改代码**
4. **推送更新到同一分支**

### **作为评审者**
1. **审查代码变更**
2. **测试功能**
3. **提供建设性反馈**
4. **批准或请求修改**

## 🚀 **实际操作示例**

### **修复听力测试问题的完整流程**

```bash
# 1. 创建分支
cd ExamPlatform-FE
git checkout -b fix/listening-audio-count

# 2. 找到相关文件
find src -name "*listening*" -type f
find src -name "*audio*" -type f

# 3. 修改代码
code src/pages/ExamListening.vue  # 假设的文件名

# 4. 测试修改
npm run dev:test

# 5. 提交代码
git add src/pages/ExamListening.vue
git commit -m "修复听力测试音频数量显示问题

根据9月21日会议记录：
- 修复音频数量从2个改为1个的显示问题
- 更新相关的UI文案
- 确保与实际音频文件数量一致

解决了会议中提到的'音频数量不匹配'问题"

# 6. 推送分支
git push origin fix/listening-audio-count

# 7. 在网页界面创建合并请求
```

## 📞 **联系开发者的其他方式**

### **项目作者信息**
根据`package.json`，项目作者是：
- **作者：** hermitriver
- **邮箱：** hermitriver@hotmail.com

### **直接联系方式**
1. **通过阿里云Codeup私信**
2. **项目Issue功能**
3. **邮件联系**
4. **如果是团队项目，通过团队沟通工具**

## 🎯 **建议的沟通策略**

### **首次联系模板**
```
主题：关于ExamPlatform听力测试问题的修复建议

你好！

我是[你的姓名]，最近在测试ExamPlatform时发现了一些问题，并根据会议记录做了一些修复。

发现的主要问题：
1. 听力测试音频数量显示不匹配
2. 写作部分阅读材料无法访问
3. 口语部分字体太小且自动停止功能不工作

我已经分析了代码并准备了一些修复方案。是否可以通过合并请求的方式提交这些修复？

期待你的回复！

最佳祝愿，
[你的姓名]
```

**总结：阿里云Codeup完全支持GitHub式的协作流程！你可以创建分支、提交代码、发起合并请求，并通过@提及、邮件等方式通知开发者。** 🚀