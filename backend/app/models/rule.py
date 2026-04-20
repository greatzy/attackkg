from app import db
from app.models.base import BaseModel

class DetectionRule(BaseModel):
    """Threat Detection Rule"""
    __tablename__ = 'detection_rules'
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    rule_type = db.Column(db.String(50), nullable=False)  # signature, behavior, correlation
    content = db.Column(db.Text, nullable=False)  # Rule content (Sigma, YARA, etc.)
    language = db.Column(db.String(50))  # sigma, yara, snort, etc.
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(20), default='draft')  # draft, active, inactive, deprecated
    platform = db.Column(db.String(100))  # Windows, Linux, macOS, etc.
    data_source = db.Column(db.String(200))
    false_positives = db.Column(db.Text)
    references = db.Column(db.JSON)
    tags = db.Column(db.JSON)
    author = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    version = db.Column(db.Integer, default=1)
    
    # Relationships
    techniques = db.relationship('RuleTechnique', back_populates='rule', lazy='dynamic')
    creator = db.relationship('User', backref='created_rules')
    
    def __repr__(self):
        return f'<DetectionRule {self.id}: {self.name}>'
    
    def to_dict(self):
        data = super().to_dict()
        data['technique_count'] = self.techniques.count()
        data['creator_name'] = self.creator.username if self.creator else None
        return data

class RuleTechnique(BaseModel):
    """Association between DetectionRule and Technique"""
    __tablename__ = 'rule_techniques'
    
    rule_id = db.Column(db.Integer, db.ForeignKey('detection_rules.id'), nullable=False)
    technique_id = db.Column(db.String(20), db.ForeignKey('techniques.technique_id'), nullable=False)
    coverage_level = db.Column(db.String(20))  # full, partial, related
    notes = db.Column(db.Text)
    
    # Relationships
    rule = db.relationship('DetectionRule', back_populates='techniques')
    technique = db.relationship('Technique')
    
    __table_args__ = (
        db.UniqueConstraint('rule_id', 'technique_id', name='unique_rule_technique'),
    )
    
    def __repr__(self):
        return f'<RuleTechnique rule:{self.rule_id} - {self.technique_id}>'
    
    def to_dict(self):
        data = super().to_dict()
        if self.technique:
            data['technique_name'] = self.technique.name
            data['tactic_id'] = self.technique.tactic_id
        return data
