from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.review import review

def test_flags_sod_and_stale():
    res = review(ROOT / "data" / "entitlements.csv")
    issues = {i for d in res["decisions"] for i in d["issues"]}
    assert "sod_conflict" in issues
    assert "stale_account" in issues

if __name__ == "__main__":
    test_flags_sod_and_stale(); print("smoke_ok")
