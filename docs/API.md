# BioBD Platform API Documentation

## WebSocket API

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => console.log('Connected to BioBD Platform');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
ws.onclose = () => console.log('Disconnected');
```

### Client → Server Messages

#### 1. Search Assets
```json
{
  "action": "search",
  "query": "恒瑞医药"
}
```

#### 2. Filter Assets
```json
{
  "action": "filter",
  "filters": {
    "phase": "Phase III",
    "country": "China",
    "priority": "High"
  }
}
```

#### 3. Get Statistics
```json
{
  "action": "get_stats"
}
```

#### 4. Heartbeat
```json
{
  "action": "ping"
}
```

### Server → Client Messages

#### Initial Data
```json
{
  "type": "init",
  "data": {
    "assets": [...],
    "metadata": {
      "version": "BioBD_Platform_V1.0",
      "total": 1492,
      "timestamp": "2026-03-18T09:00:00Z"
    }
  }
}
```

#### Asset Updates
```json
{
  "type": "asset_update",
  "data": {
    "asset_id": "CN-HR-001",
    "ai_score": 8.7,
    "score_change": 0.3,
    "trend": "↑"
  }
}
```

#### Statistics Update
```json
{
  "type": "stats_update",
  "data": {
    "total_assets": 1492,
    "avg_score": 7.82,
    "high_priority": 156,
    "preclinical": 331,
    "phase1": 139,
    "phase2": 109,
    "phase3": 116,
    "approved": 50
  }
}
```

#### Error Response
```json
{
  "type": "error",
  "message": "Invalid action"
}
```
