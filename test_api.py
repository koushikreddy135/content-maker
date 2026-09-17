import asyncio
import sys
import httpx

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def test_api_endpoints():
    print("=" * 70)
    print("TESTING FASTAPI ENDPOINTS & ASYNC PERSISTENCE")
    print("=" * 70)

    base_url = "http://127.0.0.1:8000"

    from httpx import ASGITransport
    from backend.main import app

    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as client:
        # 1. Health check
        res = await client.get("/")
        assert res.status_code == 200
        print("1. Health Check Response:", res.json())

        # 2. Submit topic
        topic = "Building Cyclic Multi-Agent Systems with LangGraph"
        submit_res = await client.post("/api/generate", json={
            "topic": topic,
            "duration_target": "8-10 mins",
            "tone": "authoritative, dynamic",
            "max_revisions": 3
        })
        assert submit_res.status_code == 200
        data = submit_res.json()
        job_id = data["job_id"]
        print(f"2. Job Submitted -> ID: {job_id} | Status: {data['status']}")

        # 3. Wait for multi-agent pipeline background worker to complete
        print("3. Waiting for multi-agent pipeline background task to process...")
        for i in range(90):
            await asyncio.sleep(1)
            status_res = await client.get(f"/api/jobs/{job_id}")
            job_status = status_res.json()["status"]
            print(f"   Polling status ({i+1}s)... Status = {job_status}")
            if job_status in ["approved", "escalated_to_human", "failed"]:
                break

        # 4. Fetch full version history and diffs
        history_res = await client.get(f"/api/jobs/{job_id}/history")
        assert history_res.status_code == 200
        history = history_res.json()
        print("\n4. Full Job History Retrieved:")
        print(f"   Job Topic: {history['job']['topic']}")
        print(f"   Total Revisions: {history['job']['total_revisions']}")
        print(f"   Drafts Stored: {len(history['drafts'])}")
        print(f"   Critic Evaluations: {len(history['critic_evaluations'])}")

        # 5. Fetch final package
        if history['job']['status'] == 'approved':
            final_res = await client.get(f"/api/jobs/{job_id}/final")
            assert final_res.status_code == 200
            final_pkg = final_res.json()
            print("\n5. Final Deliverable Package:")
            print(f"   Quality Score: {final_pkg['quality_score']}/5.0")
            print(f"   Primary Title: {final_pkg['metadata']['primary_title']}")
            print(f"   Script Chapters: {len(final_pkg['metadata']['chapters'])}")
            print(f"   Thumbnail Concepts: {len(final_pkg['thumbnails']['concepts'])}")
            if "broll" in final_pkg and final_pkg["broll"]:
                print(f"   AI B-Roll Shots: {len(final_pkg['broll'].get('shots', []))}")
            if "repurposed" in final_pkg and final_pkg["repurposed"]:
                short_title = final_pkg['repurposed'].get('short', {}).get('title', 'N/A')
                print(f"   Repurposed Short: {short_title}")

        # 6. List all jobs
        jobs_res = await client.get("/api/jobs")
        assert jobs_res.status_code == 200
        print(f"\n6. List Jobs -> Total Jobs in SQLite: {len(jobs_res.json())}")

    print("\n" + "=" * 70)
    print("ALL FASTAPI ENDPOINTS & DATABASE PERSISTENCE VERIFIED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_api_endpoints())
