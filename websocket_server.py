#!/usr/bin/env python3
"""
BioBD Enhanced V4+V5 - WebSocket Server
整合 V4 完整界面 + V5 真实数据 (1492资产)
Port: 8765
"""
import asyncio
import websockets
import json
import random
import logging
from datetime import datetime
from data_pipeline import DataPipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global state
connected_clients = set()
pipeline = DataPipeline()
assets_cache = []

# Field mapping: V5 -> V4 Interface
V5_TO_V4_MAPPING = {
    "asset_id": "id",
    "asset_name": "target",  # Display as target name
    "company": "company",
    "phase": "phase",
    "indications": "indication",
    "country": "region",
    "targets": "target",
    "mechanism": "mechanism",
    "data_quality": "data_quality",
    "priority": "priority",
    "location": "location",
    "funding": "funding"
}

# Phase standardization mapping
PHASE_MAPPING = {
    # Approved variants
    "Approved": "Approved",
    "Approved (2025)": "Approved",
    "Approved (2024)": "Approved",
    "Approved (2024-10)": "Approved",
    "Approved (2024-09)": "Approved",
    "Approved (2024-02)": "Approved",
    "Approved (April 2025)": "Approved",
    "Approved (US)": "Approved",
    "Approved (EU)": "Approved",
    "Approved (EU conditional)": "Approved",
    "Approved (FDA 2024)": "Approved",
    "Approved (FDA June 2025)": "Approved",
    "Approved (FDA/EC 2025)": "Approved",
    "Approved (FDA/EMA 2024-2025)": "Approved",
    "Approved (FDA 2022, China NMPA 2025, UK MHRA 2025)": "Approved",
    "Approved (UC 2024)": "Approved",
    "Approved (UC)": "Approved",
    "Approved (Vyvgart Hytrulo)": "Approved",
    "获批上市": "Approved",
    "Approved/Phase 3": "Approved",
    "Approved/Phase 3 extension": "Approved",
    "Approved/Phase 2 extension": "Approved",
    "Phase 3/Approved": "Approved",
    "Phase II/Approved": "Approved",
    "Phase 2/Approved": "Approved",
    "Phase 3/Approved (CN)": "Approved",
    "Phase 3/Approved (JP)": "Approved",
    "Phase III/Approved": "Approved",
    "已批准(美国 2025-09)": "Approved",
    "已批准(欧盟 2025-04)": "Approved",
    "已批准(美国 2024-09)": "Approved",
    "已批准(美国 2024-04)": "Approved",
    "已批准(美国 2025-03)": "Approved",
    "已批准(美国/欧盟 2025)": "Approved",
    "已批准(美国 2025-04)": "Approved",
    "已批准(美国 2026-03)": "Approved",
    "已批准(中国NMPA 2026-01)": "Approved",
    "已批准(中国NMPA 2026-02)": "Approved",
    "sBLA已提交(FDA)": "Approved",
    "sBLA审评中": "Approved",
    "Marketed (Japan)": "Approved",
    "Marketed (EU)": "Approved",
    "获批上市(日本)": "Approved",
    
    # Phase 3 variants
    "Phase 3": "Phase III",
    "Phase III": "Phase III",
    "Phase 3 (ongoing)": "Phase III",
    "Phase 3 (PIP)": "Phase III",
    "Phase 3 (NDA准备)": "Phase III",
    "Phase 3 (NDA 2026)": "Phase III",
    "Phase 3 (AD)": "Phase III",
    "Phase 3 (银屑病)": "Phase III",
    "Phase 3 (UC)": "Phase III",
    "Phase 3 (SLE获批)": "Phase III",
    "Phase 3 (CLL)": "Phase III",
    "Phase 3 AFFIRM研究阳性": "Phase III",
    "Phase 3 UP-AA研究阳性": "Phase III",
    "Phase 3阳性结果": "Phase III",
    "Phase 3进行中": "Phase III",
    "Phase 3 MAJESTY研究阳性": "Phase III",
    "Phase 3 POSTERITY研究": "Phase III",
    "Phase 3 ALLEGORY研究": "Phase III",
    "Phase 3 CANOVA研究": "Phase III",
    "Phase 3 VERONA研究完成": "Phase III",
    "Phase 3b TOGETHER-PsO研究阳性": "Phase III",
    "Phase 3 BRAVE-AA-PEDS研究完成": "Phase III",
    "Phase 3 (re-initiated)": "Phase III",
    "Phase 3/regulatory": "Phase III",
    "Phase 3/NDA": "Phase III",
    "Phase 3 (VALOR trial completed, FDA filing expected early 2026)": "Phase III",
    "Phase 3 (NCT06455449)": "Phase III",
    "Phase 3 (DAISY trial NCT05925803)": "Phase III",
    "Phase 3 (completed)": "Phase III",
    "Phase 3 (VALOR)": "Phase III",
    "Phase 3 (LIMIT-JIA)": "Phase III",
    "Phase 3 (Vivacity)": "Phase III",
    "Phase 3 (NCT06799000 ongoing)": "Phase III",
    "Phase 3 (CUV105 trial ongoing)": "Phase III",
    "Phase 3 (FENtrepid)": "Phase III",
    "Phase 3 (ARISE)": "Phase III",
    "Phase 3 (CUV105)": "Phase III",
    "Phase 3 (TRANQUILLO)": "Phase III",
    "Phase 3 (BE HEARD)": "Phase III",
    "Phase 3 (HARP)": "Phase III",
    "Phase 3 (PsO/PsA) / Phase 2 (IBD)": "Phase III",
    "Phase 3 (ITP) / Phase 1b (IgAN)": "Phase III",
    "Phase 3 (FENtrepid vs Ocrelizumab in PPMS)": "Phase III",
    "Phase 3 (topline data expected end of 2026)": "Phase III",
    "Phase 3 (REMODEL-2 ongoing)": "Phase III",
    "Phase 3 (NCT04524273)": "Phase III",
    "Phase 3 (HERCULES successful; FDA priority review March 2025)": "Phase III",
    "Phase 3 (PEGASUS completed)": "Phase III",
    "Phase 3/临床": "Phase III",
    
    # Phase 2 variants
    "Phase 2": "Phase II",
    "Phase II": "Phase II",
    "Phase IIb": "Phase II",
    "Phase IIa": "Phase II",
    "Phase 2 (SPRING trial completed, Phase 3 planned)": "Phase II",
    "Phase 2 (7项适应症)": "Phase II",
    "Phase 2 (2025年3月启动)": "Phase II",
    "Phase 2 (TRITON)": "Phase II",
    "Phase 2 (MaGic)": "Phase II",
    "Phase 2 (CEDAR)": "Phase II",
    "Phase 2 (LOTUS)": "Phase II",
    "Phase 2 (terminated)": "Phase II",
    "Phase 2 (已终止)": "Phase II",
    "Phase 2 (ELMWOOD trial completed)": "Phase II",
    "Phase 2 (Ver-A-T1D trial)": "Phase II",
    "Phase 2 (NCT05284175)": "Phase II",
    "Phase 2 (NCT05356858)": "Phase II",
    "Phase 2 (NCT06655896)": "Phase II",
    "Phase 2 (open-label prospective trial)": "Phase II",
    "Phase 2 (ChiCTR2200061599 completed)": "Phase II",
    "Phase 2 (MAS indication)": "Phase II",
    "Phase 2 (proof-of-concept completed)": "Phase II",
    "Phase 2 (ADHERE trial completed)": "Phase II",
    "Phase 2 (NCT04338581 completed May 2025)": "Phase II",
    "Phase II(自免扩展)": "Phase II",
    "Phase 2/3": "Phase II",
    "Phase 2/3 (discontinued in some indications)": "Phase II",
    "Phase 2/3 (ALKIVIA)": "Phase II",
    "Phase 2/3 (AMBER)": "Phase II",
    "Phase 2/3 (VITALIZE and MOBILIZE trials)": "Phase II",
    "Phase 2/3 (VISIONARY-MS)": "Phase II",
    "Phase 2/3 (BALLAD)": "Phase II",
    "Phase 2/3 (DAWN trial NCT05403138)": "Phase II",
    "Phase 2/3 (ALKIVIA trial fully enrolled)": "Phase II",
    "Phase 2/3 (BELIEVE completed, PEGASUS completed)": "Phase II",
    "Phase 2/Case series": "Phase II",
    "Phase 2a (PORTOLA)": "Phase II",
    "Phase 2a (PORTOLA NCT05569759 completed)": "Phase II",
    "Phase 2a (NCT04338581 completed May 2025)": "Phase II",
    "Phase 2b (VISTAS trial enrolled, topline Q2 2026)": "Phase II",
    "Phase 2b (planned)": "Phase II",
    "Phase 2b/3": "Phase II",
    "Phase 2b/3 (TRANSFORM)": "Phase II",
    "Phase 2/IIT": "Phase II",
    
    # Phase 1 variants
    "Phase 1": "Phase I",
    "Phase I": "Phase I",
    "Phase 1/2": "Phase I",
    "Phase 1/2a": "Phase I",
    "Phase 1/2 (IIT)": "Phase I",
    "Phase 1/2 (2024)": "Phase II",
    "Phase 1/2 (Soon)": "Phase I",
    "Phase 1/2 (HELIOS)": "Phase I",
    "Phase 1/2 (returned)": "Phase I",
    "Phase 1 (Soon)": "Phase I",
    "Phase 1 (IIT)": "Phase I",
    "Phase 1 (planned)": "Phase I",
    "Phase 1 (SAD/MAD completed)": "Phase I",
    "Phase 1 (SLE)": "Phase I",
    "Phase 1 (Breakfree-1)": "Phase I",
    "Phase 1 (Autoimmune)": "Phase I",
    "Phase 1 (GLEAM trial)": "Phase I",
    "Phase 1 (GLEAM trial NCT06294236)": "Phase I",
    "Phase 1 (NCT04752371)": "Phase I",
    "Phase 1b/2a": "Phase I",
    "Phase 1b/2": "Phase I",
    "Phase 1a/b": "Phase I",
    "Phase 1a/1b": "Phase I",
    "Phase 1 (IIT)": "Phase I",
    "Phase Ib/II": "Phase I",
    "IND申请中": "Phase I",
    "IND申请": "Phase I",
    "IND Approved": "Phase I",
    "IND submitted": "Phase I",
    "IND 2026": "Phase I",
    "IND 2025": "Phase I",
    "获批临床": "Phase I",
    
    # Preclinical variants
    "Preclinical": "Preclinical",
    "Discovery/Preclinical": "Preclinical",
    "Preclinical/IND-enabling": "Preclinical",
    "Preclinical/IND Enabling": "Preclinical",
    "Preclinical/Clinical": "Preclinical",
    "Preclinical/Phase 1": "Preclinical",
    "Preclinical/IIT": "Preclinical",
    "Preclinical/IND": "Preclinical",
    "Preclinical扩展": "Preclinical",
    "Preclinical扩展": "Preclinical",
    "Animal Model Validation": "Preclinical",
    "IND-enabling": "Preclinical",
    "Lead Optimization": "Preclinical",
    "Drug Discovery": "Preclinical",
    "Feasibility Clinical Exploration": "Preclinical",
    "临床前": "Preclinical",
    
    # Platform/Other
    "技术平台": "Platform",
    "Platform": "Platform",
    "IIT": "Preclinical",
    "Clinical": "Phase II",
    "临床阶段": "Phase II",
    "临床": "Phase II",
    "Prospective observational (2024 publication)": "Phase II",
    "Case series/reports": "Preclinical",
    "Clinical experience/case series": "Preclinical",
    "Investigational in pediatrics": "Phase II",
    "N/A": "N/A",
    "开发中": "Preclinical",
    "Research": "Preclinical",
    "全球": "Global",
    "Global": "Global",
    "已终止": "Discontinued",
    "Discontinued": "Discontinued",
    "获批上市(后撤市)": "Discontinued"
}

# Region standardization mapping
REGION_MAPPING = {
    "China": "中国",
    "United States": "美国",
    "美国": "美国",
    "Europe": "欧洲",
    "欧洲": "欧洲",
    "Japan": "日本",
    "日本": "日本",
    "Japan/UK": "日本",
    "Japan/Global": "日本",
    "全球": "全球",
    "Global": "全球",
    "India": "印度",
    "Israel": "以色列",
    "Australia": "澳大利亚",
    "Australia/USA": "美国",
    "South Korea": "韩国",
    "Korea": "韩国",
    "Germany": "德国",
    "Germany/Switzerland": "德国",
    "Sweden/Germany": "德国",
    "Singapore": "新加坡",
    "Taiwan": "台湾",
    "UK": "英国",
    "United Kingdom": "英国",
    "Belgium": "比利时",
    "Switzerland": "瑞士",
    "Austria": "奥地利",
    "France": "法国",
    "Ireland": "爱尔兰",
    "Denmark": "丹麦",
    "Netherlands": "荷兰",
    "Netherlands/Denmark": "荷兰",
    "Italy": "意大利",
    "Canada": "加拿大",
    "China/USA": "中国",
    "USA/China": "美国",
    "Global (Australia, US, China)": "全球",
    "International": "国际",
    "N/A": "未知"
}

def load_v5_assets():
    """Load and transform V5 assets to V4 format"""
    global assets_cache
    
    try:
        with open('assets_v5_master.json', 'r', encoding='utf-8') as f:
            v5_assets = json.load(f)
        
        logger.info(f"Loaded {len(v5_assets)} assets from V5 data")
        
        transformed_assets = []
        for v5_asset in v5_assets:
            # Map fields from V5 to V4 format
            asset = {
                "id": v5_asset.get("asset_id", "UNKNOWN"),
                "name": v5_asset.get("asset_name", ""),
                "target": v5_asset.get("targets") or v5_asset.get("asset_name", ""),
                "indication": _get_primary_indication(v5_asset.get("indications", [])),
                "phase": _standardize_phase(v5_asset.get("phase", "N/A")),
                "region": _standardize_region(v5_asset.get("country", "N/A")),
                "company": v5_asset.get("company", "Unknown"),
                "mechanism": v5_asset.get("mechanism", "N/A"),
                "location": v5_asset.get("location", ""),
                "funding": v5_asset.get("funding", ""),
                "priority": v5_asset.get("priority", "P2"),
                "data_quality": int(v5_asset.get("data_quality", 0.8) * 100),
                "last_updated": datetime.now().isoformat(),
            }
            
            # Calculate AI score
            asset = pipeline.enrich_asset(asset)
            transformed_assets.append(asset)
        
        assets_cache = transformed_assets
        logger.info(f"Transformed {len(transformed_assets)} assets")
        return transformed_assets
        
    except Exception as e:
        logger.error(f"Error loading assets: {e}")
        return []

def _get_primary_indication(indications):
    """Get primary indication from list"""
    if not indications:
        return "Unknown"
    if isinstance(indications, list):
        return indications[0]
    return str(indications)

def _standardize_phase(phase):
    """Standardize phase names"""
    return PHASE_MAPPING.get(phase, phase)

def _standardize_region(country):
    """Standardize region/country names"""
    return REGION_MAPPING.get(country, country)

def get_stats(assets):
    """Calculate statistics"""
    if not assets:
        return {}
    
    scores = [a.get("ai_score", 0) for a in assets]
    phases = {}
    regions = {}
    
    for asset in assets:
        phase = asset.get("phase", "Unknown")
        phases[phase] = phases.get(phase, 0) + 1
        region = asset.get("region", "Unknown")
        regions[region] = regions.get(region, 0) + 1
    
    return {
        "total_assets": len(assets),
        "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "high_priority": sum(1 for a in assets if a.get("priority") in ["High", "P0", "P1"]),
        "phase_distribution": phases,
        "region_distribution": regions,
        "timestamp": datetime.now().isoformat()
    }

def filter_assets(assets, filters):
    """Filter assets based on criteria"""
    filtered = assets
    
    if filters.get("phase"):
        filtered = [a for a in filtered if a.get("phase") == filters["phase"]]
    
    if filters.get("region"):
        filtered = [a for a in filtered if a.get("region") == filters["region"]]
    
    if filters.get("priority"):
        priority_map = {"High": ["High", "P0"], "Medium": ["Medium", "P1"], "Low": ["Low", "P2"]}
        valid_priorities = priority_map.get(filters["priority"], [filters["priority"]])
        filtered = [a for a in filtered if a.get("priority") in valid_priorities]
    
    if filters.get("search"):
        query = filters["search"].lower()
        filtered = [a for a in filtered if 
                    query in a.get("target", "").lower() or
                    query in a.get("indication", "").lower() or
                    query in a.get("company", "").lower() or
                    query in a.get("id", "").lower()]
    
    return filtered

async def broadcast(message):
    """Broadcast message to all connected clients"""
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )

async def data_stream():
    """Continuously stream data updates"""
    while True:
        await asyncio.sleep(5)  # Update every 5 seconds
        
        if assets_cache and connected_clients:
            # Update random assets
            for asset in random.sample(assets_cache, min(5, len(assets_cache))):
                # Simulate small score variations
                variation = random.uniform(-0.05, 0.05)
                asset["ai_score"] = round(min(10.0, max(5.0, asset["ai_score"] + variation)), 1)
                asset["last_updated"] = datetime.now().isoformat()
                
                update = {
                    "type": "asset_update",
                    "data": asset
                }
                await broadcast(json.dumps(update))
            
            # Send stats update
            stats = {
                "type": "stats_update",
                "data": get_stats(assets_cache)
            }
            await broadcast(json.dumps(stats))

async def handler(websocket, path):
    """Handle WebSocket connections"""
    client_id = id(websocket)
    connected_clients.add(websocket)
    logger.info(f"Client {client_id} connected. Total clients: {len(connected_clients)}")
    
    try:
        # Load assets if not already loaded
        global assets_cache
        if not assets_cache:
            assets_cache = load_v5_assets()
        
        # Send initial data
        init_message = json.dumps({
            "type": "init",
            "data": {
                "assets": assets_cache,
                "metadata": {
                    "version": "BioBD_Enhanced_V4V5_v1.0",
                    "total": len(assets_cache),
                    "timestamp": datetime.now().isoformat(),
                    "source": "V5 Real Data (1492 assets)"
                },
                "stats": get_stats(assets_cache)
            }
        })
        await websocket.send(init_message)
        
        # Keep connection alive and handle client messages
        async for message in websocket:
            try:
                msg = json.loads(message)
                action = msg.get("action")
                
                if action == "filter":
                    filters = msg.get("filters", {})
                    filtered = filter_assets(assets_cache, filters)
                    response = json.dumps({
                        "type": "filter_result",
                        "data": {
                            "filters_applied": filters,
                            "count": len(filtered),
                            "assets": filtered[:100]  # Limit to first 100
                        }
                    })
                    await websocket.send(response)
                    
                elif action == "search":
                    query = msg.get("query", "")
                    filters = {"search": query}
                    results = filter_assets(assets_cache, filters)
                    response = json.dumps({
                        "type": "search_result",
                        "data": {
                            "query": query,
                            "count": len(results),
                            "assets": results[:50]
                        }
                    })
                    await websocket.send(response)
                    
                elif action == "get_stats":
                    response = json.dumps({
                        "type": "stats_result",
                        "data": get_stats(assets_cache)
                    })
                    await websocket.send(response)
                    
                elif action == "ping":
                    await websocket.send(json.dumps({"type": "pong"}))
                    
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"type": "error", "message": "Invalid JSON"}))
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client {client_id} disconnected")
    finally:
        connected_clients.discard(websocket)
        logger.info(f"Client {client_id} removed. Total clients: {len(connected_clients)}")

async def main():
    """Start WebSocket server"""
    logger.info("=" * 50)
    logger.info("BioBD Enhanced V4+V5 WebSocket Server")
    logger.info("Port: 8765")
    logger.info("=" * 50)
    
    # Pre-load assets
    global assets_cache
    assets_cache = load_v5_assets()
    
    # Start data stream
    asyncio.create_task(data_stream())
    
    # Start server
    async with websockets.serve(handler, "0.0.0.0", 8765):
        logger.info("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown")
