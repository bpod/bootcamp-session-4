"""
Slalom Capabilities Management System API

A FastAPI application that enables Slalom consultants to register their
capabilities and manage consulting expertise across the organization.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from database import get_db, init_db
from models import Capability, Consultant, Certification, Industry, SkillLevel

app = FastAPI(title="Slalom Capabilities Management API",
              description="API for managing consulting capabilities and consultant expertise")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database and seed with initial data if empty."""
    init_db()
    seed_initial_data()


def seed_initial_data():
    """Seed the database with initial capability data if it's empty."""
    db = next(get_db())
    try:
        # Check if data already exists
        existing_capabilities = db.query(Capability).first()
        if existing_capabilities:
            return  # Data already exists, no need to seed
        
        # Create skill levels
        skill_levels = ["Emerging", "Proficient", "Advanced", "Expert"]
        skill_level_objs = []
        for level in skill_levels:
            sl = SkillLevel(name=level)
            db.add(sl)
            skill_level_objs.append(sl)
        db.commit()
        
        # Initial capabilities data
        initial_capabilities = [
            {
                "name": "Cloud Architecture",
                "description": "Design and implement scalable cloud solutions using AWS, Azure, and GCP",
                "practice_area": "Technology",
                "capacity": 40,
                "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
                "industries": ["Healthcare", "Financial Services", "Retail"],
                "consultants": ["alice.smith@slalom.com", "bob.johnson@slalom.com"]
            },
            {
                "name": "Data Analytics",
                "description": "Advanced data analysis, visualization, and machine learning solutions",
                "practice_area": "Technology",
                "capacity": 35,
                "certifications": ["Tableau Desktop Specialist", "Power BI Expert", "Google Analytics"],
                "industries": ["Retail", "Healthcare", "Manufacturing"],
                "consultants": ["emma.davis@slalom.com", "sophia.wilson@slalom.com"]
            },
            {
                "name": "DevOps Engineering",
                "description": "CI/CD pipeline design, infrastructure automation, and containerization",
                "practice_area": "Technology",
                "capacity": 30,
                "certifications": ["Docker Certified Associate", "Kubernetes Admin", "Jenkins Certified"],
                "industries": ["Technology", "Financial Services"],
                "consultants": ["john.brown@slalom.com", "olivia.taylor@slalom.com"]
            },
            {
                "name": "Digital Strategy",
                "description": "Digital transformation planning and strategic technology roadmaps",
                "practice_area": "Strategy",
                "capacity": 25,
                "certifications": ["Digital Transformation Certificate", "Agile Certified Practitioner"],
                "industries": ["Healthcare", "Financial Services", "Government"],
                "consultants": ["liam.anderson@slalom.com", "noah.martinez@slalom.com"]
            },
            {
                "name": "Change Management",
                "description": "Organizational change leadership and adoption strategies",
                "practice_area": "Operations",
                "capacity": 20,
                "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
                "industries": ["Healthcare", "Manufacturing", "Government"],
                "consultants": ["ava.garcia@slalom.com", "mia.rodriguez@slalom.com"]
            },
            {
                "name": "UX/UI Design",
                "description": "User experience design and digital product innovation",
                "practice_area": "Technology",
                "capacity": 30,
                "certifications": ["Adobe Certified Expert", "Google UX Design Certificate"],
                "industries": ["Retail", "Healthcare", "Technology"],
                "consultants": ["amelia.lee@slalom.com", "harper.white@slalom.com"]
            },
            {
                "name": "Cybersecurity",
                "description": "Information security strategy, risk assessment, and compliance",
                "practice_area": "Technology",
                "capacity": 25,
                "certifications": ["CISSP", "CISM", "CompTIA Security+"],
                "industries": ["Financial Services", "Healthcare", "Government"],
                "consultants": ["ella.clark@slalom.com", "scarlett.lewis@slalom.com"]
            },
            {
                "name": "Business Intelligence",
                "description": "Enterprise reporting, data warehousing, and business analytics",
                "practice_area": "Technology",
                "capacity": 35,
                "certifications": ["Microsoft BI Certification", "Qlik Sense Certified"],
                "industries": ["Retail", "Manufacturing", "Financial Services"],
                "consultants": ["james.walker@slalom.com", "benjamin.hall@slalom.com"]
            },
            {
                "name": "Agile Coaching",
                "description": "Agile transformation and team coaching for scaled delivery",
                "practice_area": "Operations",
                "capacity": 20,
                "certifications": ["Certified Scrum Master", "SAFe Agilist", "ICAgile Certified"],
                "industries": ["Technology", "Financial Services", "Healthcare"],
                "consultants": ["charlotte.young@slalom.com", "henry.king@slalom.com"]
            }
        ]
        
        # Pre-create all unique certifications, industries, and consultants to avoid duplicates
        all_certs = set()
        all_industries = set()
        all_consultants = set()
        
        for cap_data in initial_capabilities:
            all_certs.update(cap_data["certifications"])
            all_industries.update(cap_data["industries"])
            all_consultants.update(cap_data["consultants"])
        
        # Create certification objects
        cert_map = {}
        for cert_name in all_certs:
            cert = Certification(name=cert_name)
            db.add(cert)
            cert_map[cert_name] = cert
        
        # Create industry objects
        industry_map = {}
        for ind_name in all_industries:
            industry = Industry(name=ind_name)
            db.add(industry)
            industry_map[ind_name] = industry
        
        # Create consultant objects
        consultant_map = {}
        for email in all_consultants:
            consultant = Consultant(email=email)
            db.add(consultant)
            consultant_map[email] = consultant
        
        db.commit()
        
        # Create capabilities with related data
        for cap_data in initial_capabilities:
            capability = Capability(
                name=cap_data["name"],
                description=cap_data["description"],
                practice_area=cap_data["practice_area"],
                capacity=cap_data["capacity"]
            )
            
            # Add skill levels
            capability.skill_levels.extend(skill_level_objs)
            
            # Add certifications
            for cert_name in cap_data["certifications"]:
                capability.certifications.append(cert_map[cert_name])
            
            # Add industries
            for ind_name in cap_data["industries"]:
                capability.industries.append(industry_map[ind_name])
            
            # Add consultants
            for email in cap_data["consultants"]:
                capability.consultants.append(consultant_map[email])
            
            db.add(capability)
        
        db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/capabilities")
def get_capabilities(db: Session = Depends(get_db)):
    """Get all capabilities with their associated data."""
    capabilities = db.query(Capability).all()
    
    result = {}
    for cap in capabilities:
        result[cap.name] = {
            "description": cap.description,
            "practice_area": cap.practice_area,
            "skill_levels": [sl.name for sl in cap.skill_levels],
            "certifications": [cert.name for cert in cap.certifications],
            "industry_verticals": [ind.name for ind in cap.industries],
            "capacity": cap.capacity,
            "consultants": [cons.email for cons in cap.consultants]
        }
    
    return result


@app.post("/capabilities/{capability_name}/register")
def register_for_capability(capability_name: str, email: str, db: Session = Depends(get_db)):
    """Register a consultant for a capability"""
    # Find capability
    capability = db.query(Capability).filter(Capability.name == capability_name).first()
    if not capability:
        raise HTTPException(status_code=404, detail="Capability not found")
    
    # Find or create consultant
    consultant = db.query(Consultant).filter(Consultant.email == email).first()
    if not consultant:
        consultant = Consultant(email=email)
        db.add(consultant)
    
    # Check if already registered
    if consultant in capability.consultants:
        raise HTTPException(
            status_code=400,
            detail="Consultant is already registered for this capability"
        )
    
    # Add consultant to capability
    capability.consultants.append(consultant)
    db.commit()
    
    return {"message": f"Registered {email} for {capability_name}"}


@app.delete("/capabilities/{capability_name}/unregister")
def unregister_from_capability(capability_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a consultant from a capability"""
    # Find capability
    capability = db.query(Capability).filter(Capability.name == capability_name).first()
    if not capability:
        raise HTTPException(status_code=404, detail="Capability not found")
    
    # Find consultant
    consultant = db.query(Consultant).filter(Consultant.email == email).first()
    if not consultant or consultant not in capability.consultants:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability"
        )
    
    # Remove consultant from capability
    capability.consultants.remove(consultant)
    db.commit()
    
    return {"message": f"Unregistered {email} from {capability_name}"}

