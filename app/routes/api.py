from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import shutil

app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------------
# Mock Data for Testing
# -------------------------

mock_categories = [
    {"id": "1", "levelData": "Category 1"},
    {"id": "2", "levelData": "Category 2"},
]

mock_subcategories = [
    {"id": "101", "parentId": "1", "levelData": "Subcategory 1A"},
    {"id": "102", "parentId": "1", "levelData": "Subcategory 1B"},
    {"id": "201", "parentId": "2", "levelData": "Subcategory 2A"},
]


mock_services = [
    {
        "id": str(uuid.uuid4()),
        "categoryId": "1",
        "subCategoryId": "101",
        "version": "1.0",
        "service": "SEO Optimization",
        "serviceList": [
            {"id": "1", "labelNo": 1, "labelName": "Site Audit", "labelDetails": "Analyze website performance"},
            {"id": "2", "labelNo": 2, "labelName": "Keyword Research", "labelDetails": "Find high-performing keywords"},
            {"id": "3", "labelNo": 3, "labelName": "On-Page SEO", "labelDetails": "Optimize page titles and meta tags"},
        ]
    },
    {
        "id": str(uuid.uuid4()),
        "categoryId": "1",
        "subCategoryId": "102",
        "version": "2.0",
        "service": "Social Media Management",
        "serviceList": [
            {"id": "1", "labelNo": 1, "labelName": "Content Calendar", "labelDetails": "Plan social media posts"},
            {"id": "2", "labelNo": 2, "labelName": "Engagement", "labelDetails": "Respond to comments & messages"},
            {"id": "3", "labelNo": 3, "labelName": "Analytics", "labelDetails": "Monitor performance metrics"},
        ]
    },
    {
        "id": str(uuid.uuid4()),
        "categoryId": "2",
        "subCategoryId": "201",
        "version": "1.5",
        "service": "Graphic Design",
        "serviceList": [
            {"id": "1", "labelNo": 1, "labelName": "Logo Design", "labelDetails": "Create a unique brand logo"},
            {"id": "2", "labelNo": 2, "labelName": "Brochure Design", "labelDetails": "Design marketing materials"},
            {"id": "3", "labelNo": 3, "labelName": "Brand Kit", "labelDetails": "Develop color palette & typography"},
        ]
    },
    {
        "id": str(uuid.uuid4()),
        "categoryId": "2",
        "subCategoryId": "201",
        "version": "2.0",
        "service": "Video Editing",
        "serviceList": [
            {"id": "1", "labelNo": 1, "labelName": "Footage Cutting", "labelDetails": "Trim unnecessary parts"},
            {"id": "2", "labelNo": 2, "labelName": "Color Correction", "labelDetails": "Enhance visual quality"},
            {"id": "3", "labelNo": 3, "labelName": "Sound Mixing", "labelDetails": "Balance audio levels"},
        ]
    },
    {
        "id": str(uuid.uuid4()),
        "categoryId": "1",
        "subCategoryId": "101",
        "version": "3.0",
        "service": "Email Marketing",
        "serviceList": [
            {"id": "1", "labelNo": 1, "labelName": "Newsletter Creation", "labelDetails": "Design engaging emails"},
            {"id": "2", "labelNo": 2, "labelName": "Audience Segmentation", "labelDetails": "Target the right customers"},
            {"id": "3", "labelNo": 3, "labelName": "A/B Testing", "labelDetails": "Optimize email performance"},
        ]
    }
]




# -------------------------
# GET API Endpoints
# -------------------------

@router.get("/categories")
async def get_categories():
    """Fetch all service categories"""
    return {"data": mock_categories}

@router.get("/subcategories/{parent_id}")
async def get_subcategories(parent_id: str):
    """Fetch subcategories by category ID"""
    subcategories = [s for s in mock_subcategories if s["parentId"] == parent_id]
    return {"data": subcategories}

@router.get("/services")
async def get_services():
    """Fetch all services"""
    return {"data": mock_services}

@router.get("/services/{service_id}")
async def get_service_by_id(service_id: str):
    """Fetch a single service by ID"""
    service = next((s for s in mock_services if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"data": service}

# -------------------------
# POST API Endpoints
# -------------------------

class ServiceStep(BaseModel):
    id: str
    labelNo: int
    labelName: str
    labelDetails: str

class ServiceModel(BaseModel):
    categoryId: str
    subCategoryId: str
    version: str
    service: str
    serviceList: List[ServiceStep]

@router.post("/services")
async def add_service(service: ServiceModel):
    """Create a new service"""
    new_service = service.dict()
    new_service["id"] = str(uuid.uuid4())  # Assign a unique ID
    mock_services.append(new_service)
    return {"message": "Service created successfully", "data": new_service}

# -------------------------
# PUT API Endpoints
# -------------------------

@router.put("/services/{service_id}")
async def update_service(service_id: str, service: ServiceModel):
    """Update an existing service"""
    global mock_services
    for i, existing_service in enumerate(mock_services):
        if existing_service["id"] == service_id:
            mock_services[i] = service.dict()
            mock_services[i]["id"] = service_id  # Preserve the original ID
            return {"message": "Service updated successfully", "data": mock_services[i]}
    raise HTTPException(status_code=404, detail="Service not found")

# -------------------------
# DELETE API Endpoints
# -------------------------

@router.delete("/services/{service_id}")
async def delete_service(service_id: str):
    """Delete a service"""
    global mock_services
    mock_services = [s for s in mock_services if s["id"] != service_id]
    return {"message": "Service deleted successfully"}

# -------------------------
# File Upload API
# -------------------------

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file"""
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File uploaded successfully", "filename": file.filename}

# -------------------------
# OAuth2 Authentication (Token Placeholder)
# -------------------------

@router.get("/auth/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Mock authentication endpoint"""
    return {"message": "Authenticated", "token": token}

# -------------------------
# Register the Router
# -------------------------

app.include_router(router, prefix="/api/v1")
