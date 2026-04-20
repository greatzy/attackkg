from app import db
from app.models.base import BaseModel

class Report(BaseModel):
    """Security Report"""
    __tablename__ = 'reports'
    
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(50), nullable=False)  # attack_path, technique_detail, threat_assessment, custom
    format = db.Column(db.String(20), default='pdf')  # pdf, word, excel, html
    status = db.Column(db.String(20), default='generating')  # generating, completed, failed
    
    # Report content
    content = db.Column(db.Text)  # HTML or markdown content
    file_path = db.Column(db.String(500))  # Path to generated file
    file_size = db.Column(db.Integer)  # File size in bytes
    
    # Report parameters
    parameters = db.Column(db.JSON)  # Report generation parameters
    
    # ATT&CK data references
    technique_ids = db.Column(db.JSON)
    actor_ids = db.Column(db.JSON)
    tactic_ids = db.Column(db.JSON)
    
    # Statistics
    page_count = db.Column(db.Integer)
    generation_time = db.Column(db.Integer)  # Generation time in seconds
    
    # Created by
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', backref='reports')
    
    def __repr__(self):
        return f'<Report {self.id}: {self.title}>'
    
    def to_dict(self):
        data = super().to_dict()
        data['creator_name'] = self.creator.username if self.creator else None
        data['download_url'] = f'/api/v1/reports/{self.id}/download' if self.status == 'completed' else None
        return data
