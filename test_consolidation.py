#!/usr/bin/env python3
"""
Test script to verify name consolidation functionality.
"""

import sys
import logging
from ranking import RankingProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_name_consolidation():
    """Test the name consolidation feature."""
    print("🧪 Testing Name Consolidation Feature")
    print("=" * 50)
    
    # Create test data with duplicate names using ~ suffix
    test_data = {
        "code": 200,
        "success": True,
        "players": [
            {"playername": "Borsti1", "votes": 25},
            {"playername": "Borsti1~1", "votes": 12},
            {"playername": "Borsti1~2", "votes": 10},
            {"playername": "Betty", "votes": 20},
            {"playername": "Betty~mobile", "votes": 14},
            {"playername": "KistenKai007", "votes": 31},
            {"playername": "Player4", "votes": 18},
            {"playername": "Player4~phone", "votes": 7},
            {"playername": "Player4~tablet", "votes": 5},
            {"playername": "SinglePlayer", "votes": 15},
        ]
    }
    
    print("📊 Original API Data:")
    for player in test_data["players"]:
        print(f"  {player['playername']}: {player['votes']} votes")
    
    print("\n🔄 Processing with consolidation...")
    
    # Test the consolidation
    processor = RankingProcessor()
    consolidated_rankings = processor.process_rankings(test_data, max_count=10)
    
    print("\n📈 Consolidated Rankings:")
    for player in consolidated_rankings:
        print(f"  #{player['rank']}. {player['playername']}: {player['votes']} votes")
    
    print("\n✅ Expected Results:")
    print("  - Borsti1: 47 votes (25 + 12 + 10)")
    print("  - Betty: 34 votes (20 + 14)")
    print("  - KistenKai007: 31 votes (unchanged)")
    print("  - Player4: 30 votes (18 + 7 + 5)")
    print("  - SinglePlayer: 15 votes (unchanged)")
    
    # Verify the consolidation worked correctly
    expected_results = {
        "Borsti1": 47,
        "Betty": 34, 
        "KistenKai007": 31,
        "Player4": 30,
        "SinglePlayer": 15
    }
    
    print("\n🔍 Verification:")
    all_correct = True
    for player in consolidated_rankings:
        name = player['playername']
        votes = player['votes']
        expected = expected_results.get(name, 0)
        
        if votes == expected:
            print(f"  ✅ {name}: {votes} votes (correct)")
        else:
            print(f"  ❌ {name}: {votes} votes (expected {expected})")
            all_correct = False
    
    if all_correct:
        print("\n🎉 All consolidations are correct!")
    else:
        print("\n❌ Some consolidations failed!")

if __name__ == "__main__":
    test_name_consolidation()