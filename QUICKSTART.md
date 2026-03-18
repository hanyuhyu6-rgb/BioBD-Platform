# BioBD Platform - 快速启动指南

## 🚀 最快方案: Gitpod 一键运行

点击以下链接，在浏览器中直接运行完整功能：

👉 **[在 Gitpod 中打开](https://gitpod.io/#https://github.com/hanyuhyu6-rgb/BioBD-Platform/tree/enhanced)**

运行后：
1. 在终端执行 `./start.sh`
2. 点击右侧弹出的 "Open Browser" 按钮
3. 即可访问 Dashboard

---

## 💻 本地运行

### 要求
- Python 3.8+
- pip

### 步骤

```bash
# 1. 克隆仓库
git clone -b enhanced https://github.com/hanyuhyu6-rgb/BioBD-Platform.git
cd BioBD-Platform

# 2. 安装依赖
pip install websockets pyyaml

# 3. 启动服务器
./start.sh

# 4. 打开 Dashboard
# Linux:   xdg-open index.html
# macOS:   open index.html
# Windows: start index.html
```

---

## 🔗 访问地址

启动后：
- **Dashboard**: 直接打开 `index.html`
- **WebSocket API**: `ws://localhost:8765`

---

## 📊 数据说明

- **总资产**: 1492 个
- **更新频率**: 3 秒
- **中国资产**: 297 (19.9%)
- **Preclinical**: ~733

---

## 🌐 公网访问 (如需)

如果需要公网访问，可以使用：

### Cloudflare 隧道
```bash
cloudflared tunnel --url http://localhost:8765
```

### ngrok
```bash
ngrok http 8765
```

---

## 📁 项目结构

```
BioBD-Platform/
├── index.html          # Dashboard 前端
├── websocket_server.py # WebSocket 服务器
├── data_pipeline.py    # AI 评分引擎
├── assets_v5_master.json # 1492 资产数据
└── start.sh            # 启动脚本
```

---

**GitHub 仓库**: https://github.com/hanyuhyu6-rgb/BioBD-Platform
