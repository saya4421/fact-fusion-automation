#!/usr/bin/env python3
"""
Trends Integration Module - Connect Viral-Faceless TrendsScraper to Batch Generator

This module provides Python wrapper for the Google Trends scraper service.
"""

import requests
import os
from typing import List, Optional
from loguru import logger

# TrendsScraper service URL (from Docker or local)
TRENDSCRAPER_URL = os.getenv(
    "TRENDSCRAPER_URL",
    "http://localhost:3000"  # Default for local testing
)


class TrendsScraperClient:
    """Client for Google Trends Scraper service."""
    
    def __init__(self, base_url: str = TRENDSCRAPER_URL):
        self.base_url = base_url.rstrip('/')
    
    def get_trending_topics(
        self,
        geo: str = "US",
        limit: int = 10,
        category: int = 0
    ) -> List[dict]:
        """
        Fetch trending topics from Google Trends.
        
        Args:
            geo: Geographic region (US, ID, GB, etc.)
            limit: Max number of topics to return
            category: Google Trends category ID (0 = all)
            
        Returns:
            List of trending topics with metadata
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/google-trends/trending",
                params={
                    "geo": geo,
                    "limit": limit,
                    "category": category
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("trends", [])
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to fetch trends: {e}")
            return []
    
    def search_trends(
        self,
        keyword: str,
        geo: str = "US",
        time_range: str = "now 7-d"
    ) -> dict:
        """
        Search Google Trends for specific keyword.
        
        Args:
            keyword: Search term
            geo: Geographic region
            time_range: Time range (now 1-h, now 7-d, now 1-m, etc.)
            
        Returns:
            Trend data with interest over time, related queries, etc.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/google-trends/search",
                params={
                    "keyword": keyword,
                    "geo": geo,
                    "time": time_range
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to search trends: {e}")
            return {}


# Singleton client instance
_trends_client = None


def get_trends_client() -> TrendsScraperClient:
    """Get singleton TrendsScraper client."""
    global _trends_client
    if _trends_client is None:
        _trends_client = TrendsScraperClient()
    return _trends_client


def get_trending_topics(
    limit: int = 10,
    geo: str = "ID"  # Default to Indonesia
) -> List[str]:
    """
    Convenience function to get trending topics.
    
    Args:
        limit: Number of topics
        geo: Geographic region (ID = Indonesia)
        
    Returns:
        List of topic titles (strings)
    """
    client = get_trends_client()
    trends = client.get_trending_topics(geo=geo, limit=limit)
    
    # Extract just the titles
    topics = []
    for trend in trends:
        title = trend.get("title") or trend.get("topic", "")
        if title:
            topics.append(title)
    
    return topics


def search_keyword(keyword: str, geo: str = "ID") -> dict:
    """
    Convenience function to search trends for keyword.
    
    Args:
        keyword: Search term
        geo: Geographic region
        
    Returns:
        Trend data dict
    """
    client = get_trends_client()
    return client.search_trends(keyword=keyword, geo=geo)


if __name__ == "__main__":
    # Test
    print("Testing TrendsScraper integration...")
    print(f"Service URL: {TRENDSCRAPER_URL}")
    
    topics = get_trending_topics(limit=5, geo="ID")
    print(f"\n📈 Trending topics in Indonesia:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    if not topics:
        print("\n⚠️  No trends returned. Make sure TrendsScraper service is running:")
        print("   docker-compose up -d trendscraper")