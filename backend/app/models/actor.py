from app import db
from app.models.base import BaseModel

class ThreatActor(BaseModel):
    """MITRE ATT&CK Threat Actor (Intrusion Set)"""
    __tablename__ = 'threat_actors'
    
    actor_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    aliases = db.Column(db.JSON)  # List of aliases
    description = db.Column(db.Text)
    first_seen = db.Column(db.String(50))  # Date or year
    last_seen = db.Column(db.String(50))
    motivation = db.Column(db.String(200))
    origin = db.Column(db.String(200))
    targets = db.Column(db.JSON)  # List of target industries/regions
    tools_used = db.Column(db.JSON)  # List of tool names
    url = db.Column(db.String(500))
    version = db.Column(db.String(20))
    
    # Relationships
    techniques = db.relationship('ActorTechnique', back_populates='actor', lazy='dynamic')
    software = db.relationship('ActorSoftware', back_populates='actor', lazy='dynamic')
    
    def __repr__(self):
        return f'<ThreatActor {self.actor_id}: {self.name}>'
    
    def to_dict(self):
        data = super().to_dict()
        data['technique_count'] = self.techniques.count()
        data['software_count'] = self.software.count()
        return data

class ActorTechnique(BaseModel):
    """Association between ThreatActor and Technique"""
    __tablename__ = 'actor_techniques'
    
    actor_id = db.Column(db.String(50), db.ForeignKey('threat_actors.actor_id'), nullable=False)
    technique_id = db.Column(db.String(20), db.ForeignKey('techniques.technique_id'), nullable=False)
    usage_description = db.Column(db.Text)  # How the actor uses this technique
    
    # Relationships
    actor = db.relationship('ThreatActor', back_populates='techniques')
    technique = db.relationship('Technique')
    
    __table_args__ = (
        db.UniqueConstraint('actor_id', 'technique_id', name='unique_actor_technique'),
    )
    
    def __repr__(self):
        return f'<ActorTechnique {self.actor_id} - {self.technique_id}>'
    
    def to_dict(self):
        data = super().to_dict()
        if self.technique:
            data['technique_name'] = self.technique.name
            data['tactic_id'] = self.technique.tactic_id
        return data

class ActorSoftware(BaseModel):
    """Association between ThreatActor and Software"""
    __tablename__ = 'actor_software'
    
    actor_id = db.Column(db.String(50), db.ForeignKey('threat_actors.actor_id'), nullable=False)
    software_id = db.Column(db.String(20), db.ForeignKey('software.software_id'), nullable=False)
    usage_description = db.Column(db.Text)
    
    # Relationships
    actor = db.relationship('ThreatActor', back_populates='software')
    software_obj = db.relationship('Software')
    
    __table_args__ = (
        db.UniqueConstraint('actor_id', 'software_id', name='unique_actor_software'),
    )
    
    def __repr__(self):
        return f'<ActorSoftware {self.actor_id} - {self.software_id}>'
    
    def to_dict(self):
        data = super().to_dict()
        if self.software_obj:
            data['software_name'] = self.software_obj.name
            data['software_type'] = self.software_obj.type
        return data
