from __future__ import annotations
import csv
from pathlib import Path

SOD = [{"Finance.Pay", "Audit.Approve"}]

def review(path: Path) -> dict:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    decisions = []
    for r in rows:
        roles = {x.strip() for x in (r.get("roles") or "").split(";") if x.strip()}
        days = int(r.get("last_sign_in_days") or 0)
        issues = []
        decision = "keep"
        if days >= 90:
            issues.append("stale_account")
            decision = "disable_candidate"
        if "Admin.Global" in roles:
            issues.append("standing_global_admin")
            decision = "review_required"
        for pair in SOD:
            if pair.issubset(roles):
                issues.append("sod_conflict")
                decision = "revoke_or_split"
        if len(roles) >= 3:
            issues.append("role_creep")
            decision = "review_required" if decision == "keep" else decision
        decisions.append({
            "upn": r.get("upn"),
            "department": r.get("department"),
            "roles": sorted(roles),
            "last_sign_in_days": days,
            "issues": issues,
            "decision": decision,
        })
    return {
        "identity_count": len(decisions),
        "action_needed": sum(1 for d in decisions if d["decision"] != "keep"),
        "decisions": decisions,
    }
