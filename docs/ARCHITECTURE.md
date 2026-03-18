# BioBD Platform Architecture

## Overview

BioBD Platform is a real-time biotech asset dashboard with AI scoring capabilities.

## System Architecture

```
┌─────────────────┐     WebSocket      ┌─────────────────┐
│   Frontend      │ ◄─────────────────► │  WebSocket      │
│   (index.html)  │                     │  Server         │
└─────────────────┘                     └────────┬────────┘
                                                  │
                                                  │ File I/O
                                                  ▼
                                         ┌─────────────────┐
                                         │  Assets Data    │
                                         │  (JSON/CSV)     │
                                         └─────────────────┘
                                                  │
                                                  │ Calculate
                                                  ▼
                                         ┌─────────────────┐
                                         │  AI Scoring     │
                                         │  Engine         │
                                         └─────────────────┘
```

## Components

### 1. WebSocket Server (`src/websocket_server.py`)
- **Port**: 8765
- **Protocol**: WebSocket
- **Features**:
  - Multi-client support
  - Real-time updates (3s interval)
  - Search and filter API
  - AI score broadcasting

### 2. AI Scoring Engine (`src/ai_scoring.py`)
Scoring dimensions:
- Innovation (25%)
- Clinical Progress (20%)
- Market Potential (20%)
- Company Strength (15%)
- Competitive Landscape (20%)

### 3. Frontend Dashboard (`frontend/index.html`)
- Dark theme with glassmorphism
- Real-time asset cards
- Interactive filters
- Statistics panel

### 4. Data Layer (`data/`)
- Master database: 1,492 assets
- Standardized schema
- CSV export support

## Data Flow

1. Server loads assets from JSON
2. AI scores calculated on startup
3. Clients connect via WebSocket
4. Server broadcasts updates every 3s
5. Clients receive and display data

## Performance

- Asset capacity: 1,492+
- Update frequency: 3 seconds
- Simultaneous clients: Unlimited
- Average latency: <100ms (local)
