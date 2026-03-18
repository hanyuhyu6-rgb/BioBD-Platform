# BioBD Platform Deployment Guide

## Local Deployment

### Requirements
- Python 3.8+
- pip
- Modern web browser

### Steps

1. Clone repository
```bash
git clone https://github.com/yourusername/BioBD-Platform.git
cd BioBD-Platform
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Start server
```bash
./start.sh
```

4. Open dashboard
```bash
# Linux
xdg-open frontend/index.html

# macOS
open frontend/index.html

# Windows
start frontend/index.html
```

## Server Deployment

### Using systemd (Linux)

1. Create service file
```bash
sudo nano /etc/systemd/system/biobd.service
```

2. Add configuration
```ini
[Unit]
Description=BioBD Platform
After=network.target

[Service]
Type=simple
User=biobd
WorkingDirectory=/opt/BioBD-Platform
ExecStart=/usr/bin/python3 src/websocket_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start
```bash
sudo systemctl enable biobd
sudo systemctl start biobd
```

### Using Docker

1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8765

CMD ["python3", "src/websocket_server.py"]
```

2. Build and run
```bash
docker build -t biobd-platform .
docker run -p 8765:8765 biobd-platform
```

### Using Docker Compose

```yaml
version: '3'
services:
  biobd:
    build: .
    ports:
      - "8765:8765"
    volumes:
      - ./data:/app/data
    restart: always
```

```bash
docker-compose up -d
```

## Configuration

### Default Config (`config/default.yaml`)
```yaml
server:
  host: "0.0.0.0"
  port: 8765
  update_interval: 3

ai_scoring:
  enabled: true
  update_frequency: 300

data:
  source: "data/assets_master.json"
  auto_reload: true
```

### Production Config (`config/production.yaml`)
```yaml
server:
  host: "0.0.0.0"
  port: 8765
  update_interval: 5

logging:
  level: "INFO"
  file: "logs/biobd.log"
```

## Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name biobd.example.com;

    location /ws {
        proxy_pass http://localhost:8765;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        root /var/www/biobd/frontend;
        index index.html;
    }
}
```

## Troubleshooting

### Port 8765 in use
```bash
sudo lsof -ti:8765 | xargs sudo kill -9
```

### Permission denied
```bash
chmod +x start.sh
```

### WebSocket connection failed
- Check firewall settings
- Verify server is running: `curl http://localhost:8765`
- Check logs: `tail -f logs/biobd.log`
