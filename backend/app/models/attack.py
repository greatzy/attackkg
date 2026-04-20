from app import db
from app.models.base import BaseModel

class Tactic(BaseModel):
    """MITRE ATT&CK Tactic"""
    __tablename__ = 'tactics'
    
    tactic_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    short_name = db.Column(db.String(100))
    url = db.Column(db.String(500))
    version = db.Column(db.String(20))
    
    # Relationships
    techniques = db.relationship('Technique', back_populates='tactic', lazy='dynamic')
    
    def __repr__(self):
        return f'<Tactic {self.tactic_id}: {self.name}>'
    
    def to_dict(self, include_counts=True):
        data = super().to_dict()
        if include_counts:
            data['technique_count'] = self.techniques.count()
        return data

class Technique(BaseModel):
    """MITRE ATT&CK Technique"""
    __tablename__ = 'techniques'
    
    technique_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    tactic_id = db.Column(db.String(20), db.ForeignKey('tactics.tactic_id'), index=True)
    platforms = db.Column(db.JSON)  # List of platforms
    permissions_required = db.Column(db.JSON)  # List of permissions
    data_sources = db.Column(db.JSON)  # List of data sources
    defense_bypassed = db.Column(db.JSON)
    detection = db.Column(db.Text)
    url = db.Column(db.String(500))
    version = db.Column(db.String(20))
    is_subtechnique = db.Column(db.Boolean, default=False, index=True)
    
    # Relationships
    subtechniques = db.relationship('SubTechnique', backref='parent_technique', lazy='dynamic')
    mitigations = db.relationship('Mitigation', secondary='technique_mitigations', back_populates='techniques')
    tactic = db.relationship('Tactic', back_populates='techniques')
    
    def __repr__(self):
        return f'<Technique {self.technique_id}: {self.name}>'
    
    def to_dict(self, include_counts=True):
        data = super().to_dict()
        if include_counts:
            data['subtechnique_count'] = self.subtechniques.count()
        data['tactic_name'] = self.tactic.name if self.tactic else None
        return data

class SubTechnique(BaseModel):
    """MITRE ATT&CK Sub-technique"""
    __tablename__ = 'subtechniques'
    
    subtechnique_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technique_id = db.Column(db.String(20), db.ForeignKey('techniques.technique_id'))
    platforms = db.Column(db.JSON)
    permissions_required = db.Column(db.JSON)
    data_sources = db.Column(db.JSON)
    defense_bypassed = db.Column(db.JSON)
    detection = db.Column(db.Text)
    url = db.Column(db.String(500))
    version = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<SubTechnique {self.subtechnique_id}: {self.name}>'
    
    def to_dict(self):
        data = super().to_dict()
        data['parent_technique_name'] = self.parent_technique.name if self.parent_technique else None
        return data

class Mitigation(BaseModel):
    """MITRE ATT&CK Mitigation"""
    __tablename__ = 'mitigations'
    
    mitigation_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500))
    version = db.Column(db.String(20))
    
    # Relationship
    techniques = db.relationship('Technique', secondary='technique_mitigations', back_populates='mitigations')
    
    def __repr__(self):
        return f'<Mitigation {self.mitigation_id}: {self.name}>'

# Association table for Technique-Mitigation many-to-many relationship
technique_mitigations = db.Table('technique_mitigations',
    db.Column('technique_id', db.String(20), db.ForeignKey('techniques.technique_id'), primary_key=True),
    db.Column('mitigation_id', db.String(20), db.ForeignKey('mitigations.mitigation_id'), primary_key=True)
)

class Software(BaseModel):
    """MITRE ATT&CK Software (Malware/Tools)"""
    __tablename__ = 'software'
    
    software_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))  # malware or tool
    description = db.Column(db.Text)
    platforms = db.Column(db.JSON)
    aliases = db.Column(db.JSON)
    url = db.Column(db.String(500))
    version = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<Software {self.software_id}: {self.name}>'
