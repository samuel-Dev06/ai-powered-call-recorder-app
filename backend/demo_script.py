#!/usr/bin/env python3
"""
Demo script for AI Call Summarization Backend
This script demonstrates the key features of the system
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
import os

BASE_URL = "http://localhost:8000"

async def demo_api_calls():
    """Demonstrate the main API functionality"""
    async with aiohttp.ClientSession() as session:
        print("🚀 AI Call Summarization Backend Demo")
        print("=" * 50)
        
        # 1. Health Check
        print("\n1. Checking system health...")
        async with session.get(f"{BASE_URL}/health") as response:
            health_data = await response.json()
            print(f"   Status: {health_data.get('status', 'unknown')}")
            for service, status in health_data.get('services', {}).items():
                status_icon = "✅" if status else "❌"
                print(f"   {status_icon} {service}: {'OK' if status else 'NOT AVAILABLE'}")
        
        # 2. Start a call session
        print("\n2. Starting a new call session...")
        session_id = f"demo-session-{int(time.time())}"
        start_payload = {
            "session_id": session_id,
            "metadata": {
                "agent_id": "agent-001",
                "customer_id": "customer-123",
                "call_type": "support"
            }
        }
        
        async with session.post(f"{BASE_URL}/api/calls/start", json=start_payload) as response:
            start_data = await response.json()
            print(f"   ✅ Call started: {start_data.get('message')}")
            print(f"   📞 Session ID: {session_id}")
            call_id = start_data.get('call_id')
        
        # 3. Simulate some delay (in real scenario, audio would be uploaded here)
        print("\n3. Simulating call activity...")
        print("   📱 (In a real scenario, audio would be uploaded here)")
        print("   ⏳ Waiting for processing...")
        await asyncio.sleep(2)
        
        # 4. Get call history
        print("\n4. Checking call history...")
        async with session.get(f"{BASE_URL}/api/calls/history?limit=5") as response:
            history_data = await response.json()
            print(f"   📋 Found {len(history_data.get('calls', []))} recent calls")
            
        # 5. End the call
        print("\n5. Ending the call session...")
        end_payload = {"generate_summary": True}
        async with session.post(f"{BASE_URL}/api/calls/{session_id}/end", json=end_payload) as response:
            end_data = await response.json()
            print(f"   ✅ Call ended: {end_data.get('message')}")
        
        # 6. Get analytics dashboard
        print("\n6. Checking analytics dashboard...")
        async with session.get(f"{BASE_URL}/api/analytics/dashboard") as response:
            analytics_data = await response.json()
            metrics = analytics_data.get('metrics', {})
            print(f"   📊 Total calls: {metrics.get('total_calls', 0)}")
            print(f"   ⏱️  Average duration: {metrics.get('avg_duration', 0):.1f}s")
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Next steps:")
        print("   • Upload audio files using POST /api/calls/{session_id}/audio")
        print("   • Connect via WebSocket for real-time updates")
        print("   • Check the full API documentation at http://localhost:8000/docs")

def print_sample_curl_commands():
    """Print sample curl commands for testing"""
    print("\n🔧 Sample API Commands:")
    print("=" * 30)
    
    session_id = "test-session-123"
    
    commands = [
        ("Health Check", f'curl {BASE_URL}/health'),
        ("Start Call", f'''curl -X POST "{BASE_URL}/api/calls/start" \\
  -H "Content-Type: application/json" \\
  -d '{{"session_id": "{session_id}", "metadata": {{"demo": true}}}}\''''),
        ("Get History", f'curl "{BASE_URL}/api/calls/history?limit=10"'),
        ("End Call", f'''curl -X POST "{BASE_URL}/api/calls/{session_id}/end" \\
  -H "Content-Type: application/json" \\
  -d '{{"generate_summary": true}}\'')
    ]
    
    for name, command in commands:
        print(f"\n{name}:")
        print(f"  {command}")

async def main():
    """Main demo function"""
    print("Starting AI Call Summarization Demo...")
    print("Make sure the backend is running on http://localhost:8000")
    
    try:
        await demo_api_calls()
    except aiohttp.ClientConnectorError:
        print("❌ Could not connect to the backend server.")
        print("   Please make sure the server is running:")
        print("   python -m uvicorn app.main:app --reload")
        print("   or")
        print("   docker-compose up")
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
    
    print_sample_curl_commands()

if __name__ == "__main__":
    asyncio.run(main())
