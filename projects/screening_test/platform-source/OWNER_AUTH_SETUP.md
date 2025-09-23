# 阿里云Codeup项目所有者认证设置指南

## 🎯 **你是项目所有者！**

账号名：`hkbuscreeningtest`
这意味着你有完全的管理权限，只需要正确配置认证即可。

## 🔧 **认证配置步骤**

### **方法1：HTTPS认证（推荐）**

#### **第一步：获取个人访问令牌**
1. **登录阿里云Codeup：**
   ```
   https://codeup.aliyun.com/
   ```

2. **进入个人设置：**
   - 点击右上角头像
   - 选择"个人设置"或"Settings"
   - 进入"访问令牌"或"Access Tokens"

3. **创建新的访问令牌：**
   - 点击"新建访问令牌"
   - 名称：`ExamPlatform开发`
   - 权限：选择 `api`, `read_repository`, `write_repository`
   - 到期时间：根据需要设置
   - 点击"创建"

4. **复制令牌：**
   - ⚠️ **重要：** 令牌只显示一次，务必保存！

#### **第二步：配置Git认证**
```bash
# 清除现有认证缓存
git config --global --unset credential.helper
git config --global credential.helper store

# 设置用户信息
git config --global user.name "hkbuscreeningtest"
git config --global user.email "你的邮箱"

# 更新远程URL（包含用户名）
git remote set-url origin https://hkbuscreeningtest@codeup.aliyun.com/68601427323b2da0bd601e0e/ExamPlatform-FE.git
```

#### **第三步：首次推送**
```bash
git push origin test/owner-access-check
```
系统会提示输入：
- **Username:** hkbuscreeningtest
- **Password:** [刚才创建的访问令牌]

### **方法2：SSH密钥认证（更安全）**

#### **第一步：生成SSH密钥**
```bash
# 生成新的SSH密钥
ssh-keygen -t rsa -b 4096 -C "hkbuscreeningtest@codeup.aliyun.com"

# 添加到SSH代理
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# 复制公钥
cat ~/.ssh/id_rsa.pub
```

#### **第二步：在Codeup中添加SSH密钥**
1. **登录Codeup控制台**
2. **进入"个人设置" → "SSH密钥"**
3. **点击"添加SSH密钥"**
4. **粘贴公钥内容**
5. **保存**

#### **第三步：更新Git远程URL为SSH**
```bash
git remote set-url origin git@codeup.aliyun.com:68601427323b2da0bd601e0e/ExamPlatform-FE.git
```

## 🚀 **立即行动步骤**

### **现在需要做的：**

1. **访问Codeup控制台：**
   ```
   https://codeup.aliyun.com/
   ```

2. **使用你的账号登录：** `hkbuscreeningtest`

3. **获取访问令牌或设置SSH密钥**

4. **回来继续配置Git**

## 📝 **同时为后端项目配置**

记住，你也需要为后端项目设置相同的认证：
```bash
cd ../ExamPlatform-BE
git remote set-url origin https://hkbuscreeningtest@codeup.aliyun.com/68601427323b2da0bd601e0e/ExamPlatform-BE.git
```

## 🎯 **配置完成后你就可以：**

1. **✅ 直接推送代码到主分支**
2. **✅ 创建和管理分支**
3. **✅ 审查和合并代码**
4. **✅ 管理项目设置**
5. **✅ 添加其他协作者**

## 📞 **如果遇到问题：**

1. **检查账号状态** - 确保 `hkbuscreeningtest` 账号激活
2. **检查项目权限** - 作为所有者应该有完全权限
3. **检查网络** - 确保能访问阿里云服务

## ⏰ **下一步**

**请先去阿里云Codeup控制台获取访问令牌，然后回来我们继续配置！**

访问地址：https://codeup.aliyun.com/

获取令牌后，运行：
```bash
git push origin test/owner-access-check
```
输入用户名和令牌即可！