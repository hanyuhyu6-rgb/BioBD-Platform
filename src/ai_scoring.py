#!/usr/bin/env python3
"""
BioBD Platform - AI Scoring Module
Advanced scoring algorithms for biotech assets
"""
import math
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class PriorityLevel(Enum):
    P0 = "P0"  # Critical
    P1 = "P1"  # High
    P2 = "P2"  # Medium
    P3 = "P3"  # Low


class ClinicalPhase(Enum):
    PRECLINICAL = "Preclinical"
    PHASE_I = "Phase I"
    PHASE_II = "Phase II"
    PHASE_III = "Phase III"
    APPROVED = "Approved"


@dataclass
class ScoringFactors:
    """Factors contributing to AI score"""
    innovation: float      # 0-10
    clinical_progress: float  # 0-10
    market_potential: float   # 0-10
    company_strength: float   # 0-10
    competitive_landscape: float  # 0-10
    
    def to_dict(self) -> Dict:
        return {
            "innovation": round(self.innovation, 2),
            "clinical_progress": round(self.clinical_progress, 2),
            "market_potential": round(self.market_potential, 2),
            "company_strength": round(self.company_strength, 2),
            "competitive_landscape": round(self.competitive_landscape, 2)
        }


class AIScoringEngine:
    """Advanced AI scoring engine for biotech assets"""
    
    # Weight configuration
    DEFAULT_WEIGHTS = {
        "innovation": 0.25,
        "clinical_progress": 0.20,
        "market_potential": 0.20,
        "company_strength": 0.15,
        "competitive_landscape": 0.20
    }
    
    # Novel targets with high innovation potential
    NOVEL_TARGETS = [
        "CD3/CD20", "TSLP", "PD-1/VEGF", "IL-23R", "TYK2", 
        "STING", "KRAS", "CLDN18.2", "TROP2", "HER3"
    ]
    
    # Large market indications
    LARGE_MARKETS = [
        "特应性皮炎", "银屑病", "哮喘", "类风湿性关节炎",
        "癌症", "肿瘤", "糖尿病", "肥胖", "心血管疾病",
        "阿尔茨海默病", "帕金森病"
    ]
    
    # Crowded targets (lower competitive score)
    CROWDED_TARGETS = ["PD-1", "PD-L1", "TNF-α", "IL-17", "VEGF"]
    
    # Emerging targets (higher competitive score)
    EMERGING_TARGETS = ["TSLP", "CD3/CD20", "IL-23R", "STING", "KRAS"]
    
    # Tier 1 companies
    TIER1_COMPANIES = [
        "Novartis", "Roche", "Amgen", "AbbVie", "Eli Lilly",
        "Johnson & Johnson", "Pfizer", "Merck", "AstraZeneca", "Sanofi"
    ]
    
    # Tier 2 companies (strong Chinese biotech)
    TIER2_COMPANIES = [
        "恒瑞医药", "百济神州", "信达生物", "君实生物", 
        "复宏汉霖", "荣昌生物", "康方生物"
    ]
    
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
    
    def calculate_score(self, asset: Dict) -> Tuple[float, ScoringFactors]:
        """
        Calculate comprehensive AI score
        Returns: (total_score, factors)
        """
        factors = ScoringFactors(
            innovation=self._score_innovation(asset),
            clinical_progress=self._score_clinical_progress(asset),
            market_potential=self._score_market_potential(asset),
            company_strength=self._score_company_strength(asset),
            competitive_landscape=self._score_competitive_landscape(asset)
        )
        
        # Weighted sum
        total = (
            factors.innovation * self.weights["innovation"] +
            factors.clinical_progress * self.weights["clinical_progress"] +
            factors.market_potential * self.weights["market_potential"] +
            factors.company_strength * self.weights["company_strength"] +
            factors.competitive_landscape * self.weights["competitive_landscape"]
        )
        
        # Normalize to 0-10
        score = round(min(10.0, max(0.0, total)), 2)
        
        return score, factors
    
    def _score_innovation(self, asset: Dict) -> float:
        """Score target/mechanism innovation (0-10)"""
        target = asset.get("targets", "") or asset.get("target", "")
        mechanism = asset.get("mechanism", "")
        
        base_score = 6.0
        
        # Novel target bonus
        if any(t in target for t in self.NOVEL_TARGETS):
            base_score += 2.0
        
        # Advanced modality bonus
        if "双抗" in target or "多抗" in target or "Bispecific" in target:
            base_score += 0.8
        if "ADC" in target or "抗体偶联" in target:
            base_score += 0.8
        if "降解剂" in target or "分子胶" in target or "PROTAC" in target:
            base_score += 1.2
        if "CAR-T" in target or "CAR-T" in mechanism:
            base_score += 0.5
        if "siRNA" in target or "ASO" in target:
            base_score += 0.8
        
        # Add small randomness for variety
        return min(10.0, base_score + random.uniform(-0.2, 0.2))
    
    def _score_clinical_progress(self, asset: Dict) -> float:
        """Score clinical development progress (0-10)"""
        phase = asset.get("phase", "Preclinical")
        
        phase_scores = {
            "Preclinical": 6.0,
            "Phase 1": 7.0,
            "Phase I": 7.0,
            "Phase 2": 8.0,
            "Phase II": 8.0,
            "Phase 3": 9.0,
            "Phase III": 9.0,
            "Approved": 10.0
        }
        
        base_score = phase_scores.get(phase, 6.0)
        return base_score + random.uniform(-0.3, 0.3)
    
    def _score_market_potential(self, asset: Dict) -> float:
        """Score market potential (0-10)"""
        indications = asset.get("indications", [])
        if isinstance(indications, str):
            indications = [indications]
        
        indication_str = " ".join(indications) if indications else ""
        region = asset.get("country", "") or asset.get("region", "")
        
        base_score = 6.5
        
        # Large market bonus
        for market in self.LARGE_MARKETS:
            if market in indication_str:
                base_score += 2.0
                break
        
        # China market bonus (large growing market)
        if region in ["China", "中国"]:
            base_score += 0.5
        
        return min(10.0, base_score + random.uniform(-0.4, 0.4))
    
    def _score_company_strength(self, asset: Dict) -> float:
        """Score company strength (0-10)"""
        company = asset.get("company", "Unknown")
        funding = asset.get("funding", "")
        
        # Tier 1 MNCs
        if any(c in company for c in self.TIER1_COMPANIES):
            return 9.0 + random.uniform(-0.3, 0.3)
        
        # Tier 2 strong biotech
        if any(c in company for c in self.TIER2_COMPANIES):
            return 8.0 + random.uniform(-0.3, 0.3)
        
        # Funding-based scoring
        if "上市公司" in funding or "Public" in funding:
            base_score = 7.5
        elif "风投" in funding or "VC" in funding:
            base_score = 7.0
        else:
            base_score = 6.5
        
        return base_score + random.uniform(-0.4, 0.4)
    
    def _score_competitive_landscape(self, asset: Dict) -> float:
        """Score competitive positioning (0-10)"""
        target = asset.get("targets", "") or asset.get("target", "")
        
        # Check crowded targets (high competition = lower score)
        if any(t in target for t in self.CROWDED_TARGETS):
            return 6.0 + random.uniform(-0.3, 0.3)
        
        # Check emerging targets (low competition = higher score)
        if any(t in target for t in self.EMERGING_TARGETS):
            return 8.5 + random.uniform(-0.3, 0.3)
        
        # Moderate competition
        return 7.5 + random.uniform(-0.4, 0.4)
    
    def get_priority(self, score: float) -> str:
        """Determine priority level from score"""
        if score >= 8.5:
            return "High"
        elif score >= 7.0:
            return "Medium"
        else:
            return "Low"
    
    def get_trend(self, score: float, priority: str) -> str:
        """Determine trend direction"""
        if priority == "High" and score >= 8.5:
            return "↑"
        elif priority == "Low" and score < 7.0:
            return "↓"
        return "→"


def batch_score(assets: List[Dict], engine: AIScoringEngine = None) -> List[Dict]:
    """Score a batch of assets"""
    if engine is None:
        engine = AIScoringEngine()
    
    results = []
    for asset in assets:
        score, factors = engine.calculate_score(asset)
        enriched = asset.copy()
        enriched.update({
            "ai_score": score,
            "ai_factors": factors.to_dict(),
            "priority": engine.get_priority(score),
            "trend": engine.get_trend(score, engine.get_priority(score))
        })
        results.append(enriched)
    
    return results


def main():
    """Test the AI scoring engine"""
    engine = AIScoringEngine()
    
    test_assets = [
        {
            "asset_id": "TEST-001",
            "asset_name": "Test Asset 1",
            "targets": "TSLP",
            "indications": ["哮喘"],
            "phase": "Phase III",
            "company": "恒瑞医药",
            "country": "China"
        },
        {
            "asset_id": "TEST-002",
            "asset_name": "Test Asset 2",
            "targets": "CD3/CD20",
            "indications": ["系统性红斑狼疮"],
            "phase": "Phase II",
            "company": "Roche",
            "country": "Switzerland"
        },
        {
            "asset_id": "TEST-003",
            "asset_name": "Test Asset 3",
            "targets": "PD-1",
            "indications": ["癌症"],
            "phase": "Approved",
            "company": "某小公司",
            "country": "China"
        }
    ]
    
    print("BioBD AI Scoring Engine Test")
    print("=" * 60)
    
    for asset in test_assets:
        score, factors = engine.calculate_score(asset)
        priority = engine.get_priority(score)
        trend = engine.get_trend(score, priority)
        
        print(f"\n{asset['asset_name']} ({asset['targets']}):")
        print(f"  AI Score: {score}")
        print(f"  Priority: {priority}")
        print(f"  Trend: {trend}")
        print(f"  Factors: {factors.to_dict()}")


if __name__ == "__main__":
    main()
