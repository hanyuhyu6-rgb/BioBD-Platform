# BioBD Platform

🚀 **BioBD Platform** - Real-time Biotech Asset Dashboard with AI Scoring

基于标准化 V5 数据库（1492资产），整合 V4 的 AI 评分功能和 V5 的平台功能，打造可实时追踪生物医药资产动态的现代化平台。

## ✨ Features

- **实时数据更新**: WebSocket 连接，3秒间隔自动刷新
- **AI 智能评分**: 多维度评分算法，自动计算资产潜力
- **多客户端支持**: 支持多个客户端同时连接
- **搜索与筛选**: 按阶段、地区、优先级筛选资产
- **响应式界面**: 现代化深色主题，支持移动端
- **1492 真实资产**: 完整的生物医药资产数据库

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/BioBD-Platform.git
cd BioBD-Platform

# Install dependencies
pip install -r requirements.txt

# Start the server
./start.sh
```

### Access the Dashboard

打开浏览器访问: `http://localhost:8765` (前端)  
WebSocket 连接: `ws://localhost:8765`

## 📁 Project Structure

```
BioBD-Platform/
├── README.md                    # 项目介绍
├── LICENSE                      # MIT License
├── start.sh                     # 启动脚本
├── requirements.txt             # Python 依赖
├── docs/                        # 文档
│   ├── API.md                  # API 文档
│   ├── ARCHITECTURE.md         # 架构文档
│   └── DEPLOYMENT.md           # 部署指南
├── data/                        # 数据文件
│   ├── assets_master.json      # 主数据库 (1492资产)
│   ├── assets_master.csv       # CSV导出
│   └── schema.json             # 数据Schema
├── src/                         # 源代码
│   ├── websocket_server.py     # WebSocket服务器
│   ├── data_pipeline.py        # AI评分引擎
│   ├── ai_scoring.py           # AI评分算法
│   └── utils.py                # 工具函数
├── frontend/                    # 前端代码
│   ├── index.html              # Dashboard
│   └── static/                 # 静态资源
├── config/                      # 配置文件
│   ├── default.yaml            # 默认配置
│   └── production.yaml         # 生产配置
└── tests/                       # 测试
    ├── test_server.py
    └── test_scoring.py
```

## 🔌 API

### WebSocket Messages

#### Client → Server

```json
// 搜索资产
{"action": "search", "query": "恒瑞"}

// 筛选资产
{"action": "filter", "filters": {"phase": "Phase III", "priority": "High"}}

// 获取统计
{"action": "get_stats"}

// 心跳检测
{"action": "ping"}
```

#### Server → Client

```json
// 初始数据
{
  "type": "init",
  "data": {
    "assets": [...],
    "metadata": {"version": "BioBD_Platform_V1.0", "total": 1492}
  }
}

// 资产更新
{
  "type": "asset_update",
  "data": {"id": "CN-HR-001", "ai_score": 8.7, "trend": "↑"}
}

// 统计更新
{
  "type": "stats_update",
  "data": {"total_assets": 1492, "avg_score": 7.82, "high_priority": 156}
}
```

## 🤖 AI Scoring

AI 评分基于以下维度：

| 维度 | 权重 | 说明 |
|------|------|------|
| Innovation | 25% | 靶点创新性、技术先进性 |
| Clinical Progress | 20% | 临床进展阶段 |
| Market Potential | 20% | 市场潜力、适应症规模 |
| Company Strength | 15% | 公司实力、资源背景 |
| Competitive Landscape | 20% | 竞争格局、差异化程度 |

## 🛠️ Development

### Run Tests

```bash
python -m pytest tests/
```

### Generate CSV Export

```bash
python src/utils.py
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- BioBD V4: AI 评分功能
- BioBD V5: 标准化数据平台
