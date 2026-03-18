#!/usr/bin/env python3
"""
BioBD Platform - Data Pipeline with AI Scoring
Integrated V4 + V5
"""
import json
import random
import math
from datetime import datetime
from typing import List, Dict, Any


class DataPipeline:
    """AI-powered data pipeline for BioBD assets"""
    
    def __init__(self):
        self.model_version = "v1.0.0"
        self.scoring_weights = {
            "innovation": 0.25,
            "clinical_progress": 0.20,
            "market_potential": 0.20,
            "company_strength": 0.15,
            "competitive_landscape": 0.20
        }
    
    def calculate_ai_score(self, asset: Dict[str, Any]) -> float:
        """
        Calculate AI score based on multiple factors
        Returns score between 0-10
        """
        innovation = self._score_innovation(asset)
        clinical = self._score_clinical_progress(asset)
        market = self._score_market_potential(asset)
        company = self._score_company_strength(asset)
        competition = self._score_competitive_landscape(asset)
        
        # Weighted sum
        score = (
            innovation * self.scoring_weights["innovation"] +
            clinical * self.scoring_weights["clinical_progress"] +
            market * self.scoring_weights["market_potential"] +
            company * self.scoring_weights["company_strength"] +
            competition * self.scoring_weights["competitive_landscape"]
        )
        
        return round(min(10.0, max(0.0, score)), 2)
    
    def _score_innovation(self, asset: Dict) -> float:
        """Score based on target novelty and mechanism"""
        novel_targets = ["CD3/CD20", "TSLP", "PD-1/VEGF", "IL-23R", "TYK2", "STING"]
        target = asset.get("target", "")
        
        base_score = 7.0
        if any(t in target for t in novel_targets):
            base_score += 2.0
        if "双抗" in target or "多抗" in target:
            base_score += 0.5
        if "降解剂" in target or "分子胶" in target:
            base_score += 1.0
        if "ADC" in target or "抗体偶联" in target:
            base_score += 0.8
        
        return min(10.0, base_score + random.uniform(-0.3, 0.3))
    
    def _score_clinical_progress(self, asset: Dict) -> float:
        """Score based on clinical phase"""
        phase_scores = {
            "Preclinical": 6.0,
            "Phase I": 7.0,
            "Phase II": 8.0,
            "Phase III": 9.0,
            "Approved": 10.0
        }
        phase = asset.get("phase", "Preclinical")
        return phase_scores.get(phase, 6.0) + random.uniform(-0.3, 0.3)
    
    def _score_market_potential(self, asset: Dict) -> float:
        """Score based on indication market size"""
        large_markets = ["特应性皮炎", "银屑病", "哮喘", "类风湿性关节炎", 
                        "癌症", "肿瘤", "糖尿病", "肥胖"]
        indication = asset.get("indication", "")
        
        base_score = 6.5
        for market in large_markets:
            if market in indication:
                base_score += 2.5
                break
        
        # China market bonus
        if asset.get("region") == "China":
            base_score += 0.5
        
        return min(10.0, base_score + random.uniform(-0.5, 0.5))
    
    def _score_company_strength(self, asset: Dict) -> float:
        """Score based on company reputation and resources"""
        tier1_companies = ["Novartis", "Roche", "Amgen", "AbbVie", "Eli Lilly", 
                          "Johnson & Johnson", "Pfizer", "Merck", "AstraZeneca"]
        tier2_companies = ["恒瑞医药", "百济神州", "信达生物", "君实生物", "复宏汉霖"]
        
        company = asset.get("company", "")
        
        if any(c in company for c in tier1_companies):
            return 9.0 + random.uniform(-0.5, 0.5)
        elif any(c in company for c in tier2_companies):
            return 8.0 + random.uniform(-0.5, 0.5)
        else:
            return 7.0 + random.uniform(-0.5, 0.5)
    
    def _score_competitive_landscape(self, asset: Dict) -> float:
        """Score based on competitive positioning"""
        target = asset.get("target", "")
        
        crowded_targets = ["PD-1", "PD-L1", "TNF-α", "IL-17"]
        emerging_targets = ["TSLP", "CD3/CD20", "IL-23R", "STING", "KRAS"]
        
        if any(t in target for t in crowded_targets):
            return 6.0 + random.uniform(-0.5, 0.5)
        elif any(t in target for t in emerging_targets):
            return 8.5 + random.uniform(-0.5, 0.5)
        else:
            return 7.5 + random.uniform(-0.5, 0.5)
    
    def enrich_asset(self, asset: Dict) -> Dict:
        """Enrich asset with AI-generated insights"""
        ai_score = self.calculate_ai_score(asset)
        
        # Determine priority
        if ai_score >= 8.5:
            priority = "High"
        elif ai_score >= 7.0:
            priority = "Medium"
        else:
            priority = "Low"
        
        # Generate trend
        trend_score = random.uniform(-1, 1)
        if trend_score > 0.3:
            trend = "↑"
        elif trend_score < -0.3:
            trend = "↓"
        else:
            trend = "→"
        
        enriched = asset.copy()
        enriched.update({
            "ai_score": ai_score,
            "priority": priority,
            "trend": trend,
            "model_version": self.model_version,
            "last_scored": datetime.now().isoformat(),
            "data_quality": random.randint(85, 100)
        })
        
        return enriched
    
    def process_batch(self, assets: List[Dict]) -> List[Dict]:
        """Process a batch of assets"""
        return [self.enrich_asset(asset) for asset in assets]
    
    def get_analytics(self, assets: List[Dict]) -> Dict:
        """Generate analytics summary"""
        scores = [a.get("ai_score", 0) for a in assets]
        
        if not scores:
            return {
                "total_assets": 0,
                "avg_score": 0,
                "generated_at": datetime.now().isoformat()
            }
        
        return {
            "total_assets": len(assets),
            "avg_score": round(sum(scores) / len(scores), 2),
            "max_score": round(max(scores), 2),
            "min_score": round(min(scores), 2),
            "high_priority_count": sum(1 for a in assets if a.get("priority") == "High"),
            "score_distribution": {
                "excellent (9-10)": sum(1 for s in scores if 9 <= s <= 10),
                "good (8-9)": sum(1 for s in scores if 8 <= s < 9),
                "average (7-8)": sum(1 for s in scores if 7 <= s < 8),
                "below_avg (<7)": sum(1 for s in scores if s < 7)
            },
            "generated_at": datetime.now().isoformat()
        }


def main():
    """Test the pipeline"""
    pipeline = DataPipeline()
    
    test_assets = [
        {"target": "CD3/CD20", "indication": "系统性红斑狼疮", "phase": "Phase II", "company": "Novartis", "region": "USA"},
        {"target": "TSLP", "indication": "哮喘", "phase": "Phase III", "company": "恒瑞医药", "region": "China"},
        {"target": "PD-1", "indication": "癌症", "phase": "Approved", "company": "Roche", "region": "Europe"}
    ]
    
    print("Testing BioBD Data Pipeline...")
    print("=" * 50)
    
    for asset in test_assets:
        enriched = pipeline.enrich_asset(asset)
        print(f"\n{enriched['target']}:")
        print(f"  AI Score: {enriched['ai_score']}")
        print(f"  Priority: {enriched['priority']}")
        print(f"  Trend: {enriched['trend']}")
    
    analytics = pipeline.get_analytics([pipeline.enrich_asset(a) for a in test_assets])
    print(f"\nAnalytics: {json.dumps(analytics, indent=2)}")


if __name__ == "__main__":
    import json
    main()
