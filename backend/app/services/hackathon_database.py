"""
CallGist - Zimbabwe Call Center Hackathon Database Service
Unified database operations for single "calls" collection
"""

import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os

from app.models.hackathon_models import (
    CallRecord, CallSearchRequest, APIUsageStats,
    CallCategory, SentimentType, Priority, ResolutionStatus, CallStatus
)

logger = logging.getLogger(__name__)


class HackathonDatabaseManager:
    """
    Unified database manager for CallGist hackathon
    Single 'calls' collection with all insights and metadata
    """
    
    def __init__(self):
        self.mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        self.database_name = os.getenv("DATABASE_NAME", "callgist_hackathon")
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(self.mongodb_url)
            self.db = self.client[self.database_name]
            
            # Create indexes for optimization
            await self._create_indexes()
            logger.info(f"Connected to MongoDB: {self.database_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """Create indexes for the calls collection"""
        try:
            # Primary indexes
            await self.db.calls.create_index("call_id", unique=True)
            await self.db.calls.create_index("upload_timestamp")
            await self.db.calls.create_index("status")
            
            # Search and filter indexes
            await self.db.calls.create_index("category")
            await self.db.calls.create_index("sentiment")
            await self.db.calls.create_index("priority")
            await self.db.calls.create_index("resolution_status")
            await self.db.calls.create_index("tags")
            
            # Compound indexes for complex queries
            await self.db.calls.create_index([
                ("category", 1),
                ("sentiment", 1),
                ("upload_timestamp", -1)
            ])
            
            # Text search index
            await self.db.calls.create_index([
                ("transcript", "text"),
                ("summary", "text"),
                ("customer_requests", "text")
            ])
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    async def _ensure_connected(self):
        """Ensure database connection is established"""
        if self.db is None:
            await self.connect()
    
    async def create_call_record(self, call_record: CallRecord) -> str:
        """Create a new call record"""
        try:
            await self._ensure_connected()
            # Prepare data for insertion
            call_data = call_record.model_dump(by_alias=True, exclude_none=True)
            
            # Remove _id if None to let MongoDB auto-generate
            if '_id' in call_data and call_data['_id'] is None:
                del call_data['_id']
            
            result = await self.db.calls.insert_one(call_data)
            logger.info(f"Created call record: {call_record.call_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error creating call record: {e}")
            raise
    
    async def get_call_record(self, call_id: str) -> Optional[CallRecord]:
        """Get call record by call_id"""
        try:
            await self._ensure_connected()
            doc = await self.db.calls.find_one({"call_id": call_id})
            if doc:
                # Convert ObjectId to string for Pydantic compatibility
                if "_id" in doc and doc["_id"]:
                    doc["_id"] = str(doc["_id"])
                return CallRecord(**doc)
            return None
            
        except Exception as e:
            logger.error(f"Error getting call record {call_id}: {e}")
            return None
    
    async def update_call_record(self, call_id: str, updates: Dict[str, Any]) -> bool:
        """Update call record with new data"""
        try:
            await self._ensure_connected()
            result = await self.db.calls.update_one(
                {"call_id": call_id},
                {"$set": updates}
            )
            
            if result.modified_count > 0:
                logger.info(f"Updated call record: {call_id}")
                return True
            else:
                logger.warning(f"No updates made to call record: {call_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating call record {call_id}: {e}")
            return False
    
    async def search_call_records(
        self, 
        search_request: CallSearchRequest
    ) -> Tuple[List[CallRecord], int]:
        """Search and filter call records with pagination"""
        try:
            # Build MongoDB query
            query = {}
            
            # Category filter
            if search_request.category:
                query["category"] = search_request.category
            
            # Sentiment filter
            if search_request.sentiment:
                query["sentiment"] = search_request.sentiment
            
            # Priority filter
            if search_request.priority:
                query["priority"] = search_request.priority
            
            # Resolution status filter
            if search_request.resolution_status:
                query["resolution_status"] = search_request.resolution_status
            
            # Date range filter
            if search_request.date_from or search_request.date_to:
                date_query = {}
                if search_request.date_from:
                    date_query["$gte"] = search_request.date_from
                if search_request.date_to:
                    date_query["$lte"] = search_request.date_to
                query["upload_timestamp"] = date_query
            
            # Tags filter
            if search_request.tags:
                query["tags"] = {"$in": search_request.tags}
            
            # Text search
            if search_request.search_text:
                query["$text"] = {"$search": search_request.search_text}
            
            # Only show completed calls for search results
            query["status"] = CallStatus.COMPLETED
            
            # Get total count
            total = await self.db.calls.count_documents(query)
            
            # Get paginated results
            skip = (search_request.page - 1) * search_request.per_page
            cursor = self.db.calls.find(query).sort("upload_timestamp", -1).skip(skip).limit(search_request.per_page)
            
            docs = await cursor.to_list(length=None)
            
            # Convert to CallRecord objects
            call_records = []
            for doc in docs:
                if "_id" in doc and doc["_id"]:
                    doc["_id"] = str(doc["_id"])
                call_records.append(CallRecord(**doc))
            
            return call_records, total
            
        except Exception as e:
            logger.error(f"Error searching call records: {e}")
            return [], 0
    
    async def get_dashboard_analytics(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get analytics for dashboard"""
        try:
            # Aggregation pipeline for dashboard metrics
            pipeline = [
                {
                    "$match": {
                        "upload_timestamp": {"$gte": start_date, "$lte": end_date},
                        "status": CallStatus.COMPLETED
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total_calls": {"$sum": 1},
                        "category_breakdown": {
                            "$push": "$category"
                        },
                        "sentiment_breakdown": {
                            "$push": "$sentiment"
                        },
                        "priority_breakdown": {
                            "$push": "$priority"
                        },
                        "resolution_breakdown": {
                            "$push": "$resolution_status"
                        },
                        "follow_up_required_count": {
                            "$sum": {"$cond": [{"$eq": ["$follow_up_required", True]}, 1, 0]}
                        },
                        "avg_processing_time": {
                            "$avg": {
                                "$subtract": ["$processed_at", "$upload_timestamp"]
                            }
                        }
                    }
                }
            ]
            
            result = await self.db.calls.aggregate(pipeline).to_list(length=1)
            
            if not result:
                return {"total_calls": 0}
            
            data = result[0]
            
            # Process category breakdown
            category_counts = {}
            for category in data.get("category_breakdown", []):
                if category:
                    category_counts[category] = category_counts.get(category, 0) + 1
            
            # Process sentiment breakdown
            sentiment_counts = {}
            for sentiment in data.get("sentiment_breakdown", []):
                if sentiment:
                    sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            # Process priority breakdown
            priority_counts = {}
            for priority in data.get("priority_breakdown", []):
                if priority:
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            # Process resolution breakdown
            resolution_counts = {}
            for resolution in data.get("resolution_breakdown", []):
                if resolution:
                    resolution_counts[resolution] = resolution_counts.get(resolution, 0) + 1
            
            # Calculate resolution rate
            total_calls = data.get("total_calls", 0)
            resolved_calls = resolution_counts.get("resolved", 0)
            resolution_rate = (resolved_calls / total_calls * 100) if total_calls > 0 else 0
            
            # Calculate follow-up rate
            follow_up_rate = (data.get("follow_up_required_count", 0) / total_calls * 100) if total_calls > 0 else 0
            
            return {
                "total_calls": total_calls,
                "category_breakdown": category_counts,
                "sentiment_breakdown": sentiment_counts,
                "priority_breakdown": priority_counts,
                "resolution_breakdown": resolution_counts,
                "resolution_rate": round(resolution_rate, 2),
                "follow_up_rate": round(follow_up_rate, 2),
                "avg_processing_time_ms": data.get("avg_processing_time", 0),
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard analytics: {e}")
            return {"total_calls": 0, "error": str(e)}
    
    async def get_api_usage_stats(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> APIUsageStats:
        """Get API usage statistics for monetization"""
        try:
            # Basic stats query
            total_calls = await self.db.calls.count_documents({
                "upload_timestamp": {"$gte": start_date, "$lte": end_date}
            })
            
            # Category breakdown
            category_pipeline = [
                {
                    "$match": {
                        "upload_timestamp": {"$gte": start_date, "$lte": end_date},
                        "status": CallStatus.COMPLETED
                    }
                },
                {
                    "$group": {
                        "_id": "$category",
                        "count": {"$sum": 1}
                    }
                }
            ]
            
            category_results = await self.db.calls.aggregate(category_pipeline).to_list(length=None)
            calls_by_category = {
                result["_id"]: result["count"] 
                for result in category_results 
                if result["_id"]
            }
            
            # Sentiment breakdown
            sentiment_pipeline = [
                {
                    "$match": {
                        "upload_timestamp": {"$gte": start_date, "$lte": end_date},
                        "status": CallStatus.COMPLETED
                    }
                },
                {
                    "$group": {
                        "_id": "$sentiment",
                        "count": {"$sum": 1}
                    }
                }
            ]
            
            sentiment_results = await self.db.calls.aggregate(sentiment_pipeline).to_list(length=None)
            calls_by_sentiment = {
                result["_id"]: result["count"] 
                for result in sentiment_results 
                if result["_id"]
            }
            
            # Success rate calculation
            completed_calls = await self.db.calls.count_documents({
                "upload_timestamp": {"$gte": start_date, "$lte": end_date},
                "status": CallStatus.COMPLETED
            })
            
            success_rate = (completed_calls / total_calls * 100) if total_calls > 0 else 0
            
            # Average processing time
            avg_time_pipeline = [
                {
                    "$match": {
                        "upload_timestamp": {"$gte": start_date, "$lte": end_date},
                        "status": CallStatus.COMPLETED,
                        "processed_at": {"$exists": True}
                    }
                },
                {
                    "$project": {
                        "processing_time": {
                            "$subtract": ["$processed_at", "$upload_timestamp"]
                        }
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "avg_time": {"$avg": "$processing_time"}
                    }
                }
            ]
            
            time_results = await self.db.calls.aggregate(avg_time_pipeline).to_list(length=1)
            avg_processing_time = time_results[0]["avg_time"] / 1000 if time_results else 0  # Convert to seconds
            
            return APIUsageStats(
                total_calls_processed=total_calls,
                calls_by_category=calls_by_category,
                calls_by_sentiment=calls_by_sentiment,
                average_processing_time=avg_processing_time,
                success_rate=round(success_rate, 2),
                date_range={
                    "start": start_date,
                    "end": end_date
                }
            )
            
        except Exception as e:
            logger.error(f"Error getting API usage stats: {e}")
            # Return empty stats on error
            return APIUsageStats(
                total_calls_processed=0,
                calls_by_category={},
                calls_by_sentiment={},
                average_processing_time=0.0,
                success_rate=0.0,
                date_range={"start": start_date, "end": end_date}
            )
    
    async def health_check(self) -> bool:
        """Check database connection health"""
        try:
            await self.client.admin.command('ping')
            return True
        except Exception:
            return False
