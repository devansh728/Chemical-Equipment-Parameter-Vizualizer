# API Documentation

### Authentication Endpoints

#### POST `/api/signup/`
Register new user account.

**Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response** (201 Created):
```json
{
  "user": {
    "id": 1,
    "username": "string",
    "email": "string"
  },
  "tokens": {
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
  }
}
```

#### POST `/api/token/`
Authenticate user and obtain tokens.

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

#### POST `/api/token/refresh/`
Refresh access token.

**Request Body**:
```json
{
  "refresh": "jwt_refresh_token"
}
```

**Response** (200 OK):
```json
{
  "access": "new_jwt_access_token"
}
```

### Dataset Endpoints

#### POST `/api/upload/`
Upload CSV file for analysis.

**Headers**: `Authorization: Bearer {access_token}`  
**Content-Type**: `multipart/form-data`

**Request Body**:
- `file`: CSV file

**Response** (202 Accepted):
```json
{
  "message": "File uploaded successfully. Processing started.",
  "dataset_id": 1,
  "status": "PROCESSING"
}
```

#### GET `/api/history/`
List recent datasets (last 5).

**Headers**: `Authorization: Bearer {access_token}`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "filename": "equipment_data.csv",
    "uploaded_at": "2025-11-23T14:30:00Z",
    "status": "COMPLETED",
    "total_records": 100,
    "profiling_complete": true,
    "analysis_complete": true,
    "ai_complete": true
  }
]
```

#### GET `/api/dataset/{id}/`
Get detailed dataset information.

**Headers**: `Authorization: Bearer {access_token}`

**Response** (200 OK):
```json
{
  "id": 1,
  "filename": "equipment_data.csv",
  "uploaded_at": "2025-11-23T14:30:00Z",
  "status": "COMPLETED",
  "summary": { ... },
  "enhanced_summary": { ... },
  "column_profile": { ... },
  "ai_suggestions": { ... },
  "ai_insights": { ... },
  "correlation_matrix": { ... },
  "outliers": { ... },
  "data": [ ... ],
  "profiling_complete": true,
  "analysis_complete": true,
  "ai_complete": true
}
```

#### GET `/api/dataset/{id}/stats/`
Get calculated statistics for dashboard cards.

**Headers**: `Authorization: Bearer {access_token}`

**Response** (200 OK):
```json
{
  "total_records": 100,
  "avg_pressure": 245.8,
  "avg_temperature": 350.2,
  "avg_flowrate": 120.5
}
```

#### GET `/api/dataset/{id}/correlation/`
Get correlation matrix data.

**Headers**: `Authorization: Bearer {access_token}`

**Response** (200 OK):
```json
{
  "correlation_matrix": [[1.0, 0.85, ...], ...],
  "column_names": ["Temperature", "Pressure", "Flowrate"],
  "strong_correlations": [
    {
      "param1": "Temperature",
      "param2": "Pressure",
      "coefficient": 0.92
    }
  ]
}
```

#### GET `/api/dataset/{id}/optimize/`
Get optimization recommendations.

**Headers**: `Authorization: Bearer {access_token}`

**Response** (200 OK):
```json
{
  "recommendations": [
    {
      "category": "Efficiency",
      "suggestion": "...",
      "impact": "High",
      "priority": 1
    }
  ],
  "summary": "..."
}
```

#### POST `/api/dataset/{id}/explain-outlier/`
Get AI explanation for specific outlier.

**Headers**: `Authorization: Bearer {access_token}`

**Request Body**:
```json
{
  "equipment_name": "HE-101",
  "equipment_type": "Heat Exchanger",
  "parameter": "Temperature",
  "value": 450.5,
  "expected_range": [200, 400]
}
```

**Response** (200 OK):
```json
{
  "explanation": "AI-generated explanation...",
  "outlier": { ... }
}
```

#### GET `/api/dataset/{id}/report/`
Download PDF report.

**Headers**: `Authorization: Bearer {access_token}`

**Response** (200 OK):
- Content-Type: `application/pdf`
- PDF file download

### WebSocket Endpoint

#### `/ws/analysis/`
Real-time analysis progress updates.

**Connection**: `ws://localhost:8000/ws/analysis/?token={access_token}`

**Messages Received**:
```json
{
  "status": "profiling_complete",
  "dataset_id": 1,
  "message": "Phase 1/3: Column profiling complete"
}
```

**Status Types**:
- `profiling_complete`: Phase 1 done
- `analysis_complete`: Phase 2 done
- `COMPLETED`: Phase 3 done (all phases complete)
- `FAILED`: Error occurred

---