import time
import uuid


class RunTracker:
    def __init__(self, domain: str):
        self.run_id = str(uuid.uuid4())
        self.domain = domain
        self.started_at = time.time()

    def finish(self, status: str) -> dict:
        return {
            "run_id": self.run_id,
            "domain": self.domain,
            "status": status,
            "duration_seconds": round(
                time.time() - self.started_at,
                2,
            ),
        }
