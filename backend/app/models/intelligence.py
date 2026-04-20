from app import db
from app.models.base import BaseModel

class ThreatIntelligence(BaseModel):
    """Threat Intelligence data"""
    __tablename__ = 'threat_intelligence'
    
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    source = db.Column(db.String(200))  # Source of intelligence
    source_type = db.Column(db.String(50))  # open_source, commercial, internal
    threat_type = db.Column(db.String(100))  # malware, apt, vulnerability, etc.
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    confidence = db.Column(db.String(20), default='medium')  # low, medium, high
    status = db.Column(db.String(20), default='active')  # active, expired, false_positive
    
    # ATT&CK mapping
    technique_ids = db.Column(db.JSON)  # List of technique IDs
    actor_ids = db.Column(db.JSON)  # List of actor IDs
    software_ids = db.Column(db.JSON)  # List of software IDs
    
    # IoCs
    iocs = db.Column(db.JSON)  # List of IoCs (IPs, domains, hashes, etc.)
    
    # Timeline
    first_seen = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime)
    published_at = db.Column(db.DateTime)
    
    # Risk assessment
    risk_score = db.Column(db.Float)  # 0-100
    risk_factors = db.Column(db.JSON)  # Risk factor breakdown
    
    # References
    references = db.Column(db.JSON)  # List of reference URLs
    raw_data = db.Column(db.JSON)  # Raw intelligence data
    
    # Tags
    tags = db.Column(db.JSON)
    
    # Created by
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', backref='intelligence_items')
    
    def __repr__(self):
        return f'<ThreatIntelligence {self.id}: {self.title}>'
    
    def to_dict(self):
        data = super().to_dict()
        data['creator_name'] = self.creator.username if self.creator else None
        return data
    
    def calculate_risk_score(self):
        """Calculate risk score based on various factors"""
        score = 0
        
        # Severity weight
        severity_weights = {'low': 20, 'medium': 40, 'high': 70, 'critical': 100}
        score += severity_weights.get(self.severity, 40) * 0.4
        
        # Confidence weight
        confidence_weights = {'low': 20, 'medium': 50, 'high': 100}
        score += confidence_weights.get(self.confidence, 50) * 0.2
        
        # Technique count weight
        technique_count = len(self.technique_ids) if self.technique_ids else 0
        score += min(technique_count * 5, 30) * 0.2
        
        # Actor association weight
        actor_count = len(self.actor_ids) if self.actor_ids else 0
        score += min(actor_count * 10, 20) * 0.2
        
        self.risk_score = round(score, 2)
        return self.risk_score
