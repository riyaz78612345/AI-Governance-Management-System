from database.connection import SessionLocal
from database.models import AIModel, RiskAssessment


def get_dashboard_metrics():
    session = SessionLocal()

    total_models = session.query(AIModel).count()

    high_risk = (
        session.query(RiskAssessment)
        .filter(RiskAssessment.level == "High")
        .count()
    )

    medium_risk = (
        session.query(RiskAssessment)
        .filter(RiskAssessment.level == "Medium")
        .count()
    )

    low_risk = (
        session.query(RiskAssessment)
        .filter(RiskAssessment.level == "Low")
        .count()
    )

    recent_models = (
        session.query(AIModel)
        .order_by(AIModel.id.desc())
        .limit(5)
        .all()
    )

    recent_assessments = (
        session.query(RiskAssessment)
        .order_by(RiskAssessment.id.desc())
        .limit(5)
        .all()
    )

    session.close()

    return {
    "total_models": total_models,
    "high_risk": high_risk,
    "medium_risk": medium_risk,
    "low_risk": low_risk,
    "total_assessments": high_risk + medium_risk + low_risk,
    "recent_models": recent_models,
    "recent_assessments": recent_assessments,
}