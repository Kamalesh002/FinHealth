# Company Management Testing Documentation

## Overview
This document details the testing performed on Company Management features for the SME Financial Health Platform.

---

## Test Environment
- **Backend:** FastAPI + SQLAlchemy
- **Database:** PostgreSQL
- **Authentication:** JWT (required for all endpoints)

---

## ✅ Core Functionality Tests

### 1. Create Company Profile
| Test Case | Endpoint | Expected | Result |
|-----------|----------|----------|--------|
| Create company with valid data | `POST /api/upload/company` | 200 + company object | ✅ PASS |
| Company has unique ID | Response body | Auto-incremented ID | ✅ PASS |
| Industry stored correctly | Response body | Matches input | ✅ PASS |

**Test Request:**
```json
POST /api/upload/company
{
  "name": "Test Company A",
  "industry": "Manufacturing"
}
```

**Test Response:**
```json
{
  "id": 2,
  "name": "Test Company A",
  "industry": "Manufacturing",
  "created_at": "2026-02-05T05:33:28.139405"
}
```

---

### 2. Create Multiple Companies
| Test Case | Expected | Result |
|-----------|----------|--------|
| Create Company A (Manufacturing) | ID assigned | ✅ PASS (ID: 2) |
| Create Company B (Retail) | Different ID | ✅ PASS (ID: 3) |

---

### 3. List/Switch Companies
| Test Case | Endpoint | Expected | Result |
|-----------|----------|----------|--------|
| Get all user companies | `GET /api/upload/companies` | Array of companies | ✅ PASS |
| Each company has unique ID | Response | Different IDs | ✅ PASS |
| User isolation | Response | Only user's companies | ✅ PASS |

**Sample Response:**
```json
[
  {"id": 2, "name": "Test Company A", "industry": "Manufacturing"},
  {"id": 3, "name": "Test Company B", "industry": "Retail"}
]
```

---

### 4. Company-Specific Data Storage
| Test Case | Expected | Result |
|-----------|----------|--------|
| Upload file to Company A | Stored with company_id=2 | ✅ PASS |
| Upload file to Company B | Stored with company_id=3 | ✅ PASS |
| Data isolated per company | Each company sees own data | ✅ PASS |

---

### 5. Analysis Per Company
| Test Case | Expected | Result |
|-----------|----------|--------|
| Health score for Company A | Manufacturing benchmarks | ✅ PASS |
| Health score for Company B | Retail benchmarks | ✅ PASS |
| Different industries = Different analysis | Industry-specific weights | ✅ PASS |

---

## ⚠️ Edge Case Tests

### 1. No Company Selected (Invalid ID)
```
GET /api/analysis/health-score/999
```
| Expected | Actual | Result |
|----------|--------|--------|
| 404 Not Found | 404 | ✅ PASS |

---

### 2. Duplicate Company Name
```
POST /api/upload/company
{"name": "Test Company A", "industry": "Services"}
```
| Expected | Actual | Result |
|----------|--------|--------|
| 400 Bad Request | 400 | ✅ PASS |

**Error Response:**
```json
{"detail": "Company with name 'Test Company A' already exists"}
```

---

### 3. Deleting a Company
```
DELETE /api/upload/company/4
```
| Expected | Actual | Result |
|----------|--------|--------|
| 200 + success message | 200 | ✅ PASS |

**Success Response:**
```json
{"message": "Company 'Test Company A' and all associated data deleted successfully"}
```

**Features:**
- ✅ Verifies ownership before deletion
- ✅ Cascade deletes financial data
- ✅ Cascade deletes health scores
- ✅ Returns 404 for non-existent company

---

## Summary Table

| Feature | Status | Notes |
|---------|--------|-------|
| Create company profile | ✅ PASS | Returns ID, industry |
| Multiple companies per user | ✅ PASS | Each has unique ID |
| List user's companies | ✅ PASS | Returns array |
| Company data isolation | ✅ PASS | Each company separate |
| Analysis per company | ✅ PASS | Industry-specific |
| Invalid company ID | ✅ PASS | Returns 404 |
| Duplicate company name | ✅ PASS | Returns 400 |
| Delete company | ✅ PASS | Cascade deletion |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload/company` | Create new company |
| `GET` | `/api/upload/companies` | List user's companies |
| `GET` | `/api/upload/company/{id}` | Get specific company |
| `DELETE` | `/api/upload/company/{id}` | Delete company + cascade |
| `GET` | `/api/upload/pending/{company_id}` | Get pending validations |
| `POST` | `/api/upload/file/{company_id}` | Upload financial file |

---

## How to Run Tests

```powershell
# Login to get token
$body = @{username="user@test.com"; password="Password123"}
$login = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" -Method POST -Body $body
$token = $login.access_token
$headers = @{Authorization="Bearer $token"}

# Create company
Invoke-RestMethod -Uri "http://localhost:8000/api/upload/company" `
  -Method POST -Headers $headers -ContentType "application/json" `
  -Body '{"name": "My Company", "industry": "Manufacturing"}'

# List companies
Invoke-RestMethod -Uri "http://localhost:8000/api/upload/companies" `
  -Method GET -Headers $headers

# Test invalid company
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/analysis/health-score/999" `
      -Method GET -Headers $headers
} catch {
    Write-Host "Expected 404: $($_.Exception.Response.StatusCode.value__)"
}
```

---

## Recommendations for Future Enhancement

1. **Add duplicate name validation** - Prevent same company name per user
2. **Implement company deletion** - Add DELETE endpoint with cascade
3. **Add company update** - Allow editing company name/industry
4. **Add company archive** - Soft delete instead of hard delete

---

*Last verified: February 2026*
