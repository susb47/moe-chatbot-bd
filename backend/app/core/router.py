import re
from typing import Dict, Any

class QueryRouter:
    # Bengali and English trigger patterns
    ACTION_KEYWORDS = [
        "portal", "website", "link", "contact", "office", "form", "apply", "helpline",
        "পোর্টাল", "ওয়েবসাইট", "লিঙ্ক", "যোগাযোগ", "অফিস", "ফরম", "আবেদন", "হেল্পলাইন"
    ]
    
    STATS_KEYWORDS = [
        "statistic", "population", "rate", "count", "total", "percentage", "banbeis", "apss", "bbs",
        "পরিসংখ্যান", "অনুপাত", "হার", "সংখ্যা", "মোট", "ব্যানবেইস"
    ]

    PORTAL_REGISTRY = {
        "admission": "https://gpadmission.gov.bd",
        "board": "https://dhakaeducationboard.gov.bd",
        "nctb": "https://nctb.gov.bd",
        "moe": "https://moedu.gov.bd",
        "dshe": "https://dshe.gov.bd",
        "dpe": "https://dpe.gov.bd"
    }

    @classmethod
    def classify_intent(cls, query: str) -> Dict[str, Any]:
        q_lower = query.lower()

        # Check for guided actions
        for kw in cls.ACTION_KEYWORDS:
            if kw in q_lower:
                # Find matching portal if specified
                target_url = cls.PORTAL_REGISTRY["moe"]
                for key in cls.PORTAL_REGISTRY:
                    if key in q_lower:
                        target_url = cls.PORTAL_REGISTRY[key]
                        break
                return {
                    "tier": "guided_action",
                    "action_url": target_url,
                    "confidence": 0.95
                }

        # Check for statistical queries
        for kw in cls.STATS_KEYWORDS:
            if kw in q_lower:
                return {
                    "tier": "statistics_lookup",
                    "source": "BANBEIS/BBS",
                    "confidence": 0.90
                }

        # Default fallback to Knowledge Base / Policy RAG
        return {
            "tier": "policy_kb",
            "confidence": 0.85
        }