# Order Management System - Architecture Diagram

## System Architecture

```mermaid
flowchart TD
    Client[Client Layer<br/>Swagger UI, Postman,<br/>Frontend Applications]
    
    MainApp[FastAPI Application<br/>app/main.py<br/>- App Configuration<br/>- CORS Middleware<br/>- Router Registration]
    
    APILayer["API Layer<br/>app/api/v1/<br/>- orders.py - 3 endpoints<br/>- products.py - 4 endpoints<br/>- users.py - 3 endpoints<br/>- Request Validation<br/>- Error Handling<br/>- Swagger Documentation"]
    
    ServiceLayer[Service Layer<br/>app/services/<br/>- order_service.py<br/>- product_service.py<br/>- user_service.py<br/>- Business Logic<br/>- Validation Rules]
    
    RepoLayer[Repository Layer<br/>app/repositories/<br/>- base.py<br/>- order_repository.py<br/>- product_repository.py<br/>- user_repository.py<br/>- SQL Queries<br/>- Aggregations]
    
    ModelLayer["Model Layer<br/>app/models/<br/>- user.py<br/>- product.py<br/>- order.py<br/>- order_item.py<br/>- Relationships: User, Product<br/>- Constraints<br/>- Timestamps: created_at, updated_at"]
    
    Database[("PostgreSQL Database<br/>Schema: tony<br/>- users<br/>- products<br/>- orders with updated_at<br/>- order_items")]
    
    Client -->|HTTP/REST API| MainApp
    MainApp --> APILayer
    APILayer -->|Service Calls| ServiceLayer
    ServiceLayer -->|Repository Calls| RepoLayer
    RepoLayer -->|SQLAlchemy ORM| ModelLayer
    ModelLayer -->|Database Connection| Database
    
    style Client fill:#1e3a5f,stroke:#4a90e2,stroke-width:2px,color:#e8f4fd
    style MainApp fill:#3d2817,stroke:#d4a574,stroke-width:2px,color:#f5e6d3
    style APILayer fill:#4a1e3a,stroke:#e294d4,stroke-width:2px,color:#f5d4e8
    style ServiceLayer fill:#1e4a1e,stroke:#74d474,stroke-width:2px,color:#d4f5d4
    style RepoLayer fill:#3a1e4a,stroke:#b474d4,stroke-width:2px,color:#e8d4f5
    style ModelLayer fill:#4a1e1e,stroke:#d47474,stroke-width:2px,color:#f5d4d4
    style Database fill:#1e1e4a,stroke:#7474d4,stroke-width:2px,color:#d4d4f5
```

## Component Responsibilities

### API Layer
- **Purpose**: HTTP request/response handling
- **Responsibilities**:
  - Route requests to appropriate handlers
  - Validate input using Pydantic schemas
  - Handle HTTP status codes and error responses
  - Format responses

### Service Layer
- **Purpose**: Business logic and orchestration
- **Responsibilities**:
  - Implement business rules
  - Coordinate between repositories
  - Validate business constraints
  - Handle transactions

### Repository Layer
- **Purpose**: Data access abstraction
- **Responsibilities**:
  - Execute database queries
  - Implement filtering and aggregation
  - Manage database sessions
  - Optimize queries

### Model Layer
- **Purpose**: Database entity mapping
- **Responsibilities**:
  - Define table structures
  - Define relationships
  - Enforce constraints
  - Provide ORM mappings

## Data Flow

```mermaid
flowchart LR
    subgraph Request["Request Flow"]
        direction LR
        R1[Client] --> R2[API Endpoint] --> R3[Service] --> R4[Repository] --> R5[Model] --> R6[Database]
    end
    
    subgraph Response["Response Flow"]
        direction LR
        P1[Database] --> P2[Model] --> P3[Repository] --> P4[Service] --> P5[Pydantic Schema] --> P6[API] --> P7[Client]
    end
    
    subgraph Error["Error Flow"]
        direction LR
        E1[Any Layer] --> E2[Exception] --> E3[Service/API] --> E4[HTTP Error Response] --> E5[Client]
    end
    
    style Request fill:#1e3a1e,stroke:#74d474,stroke-width:2px,color:#d4f5d4
    style Response fill:#1e1e3a,stroke:#7474d4,stroke-width:2px,color:#d4d4f5
    style Error fill:#3a1e1e,stroke:#d47474,stroke-width:2px,color:#f5d4d4
```

## Layer Interaction

```mermaid
flowchart TD
    subgraph External["External"]
        Client[API Clients]
        Swagger[Swagger UI]
        Postman[Postman]
    end
    
    subgraph Application["Application Layers"]
        API[API Layer<br/>FastAPI Endpoints]
        Service[Service Layer<br/>Business Logic]
        Repo[Repository Layer<br/>Data Access]
        Model[Model Layer<br/>ORM Models]
    end
    
    subgraph Data["Data Layer"]
        DB[(PostgreSQL)]
    end
    
    Client --> API
    Swagger --> API
    Postman --> API
    
    API -->|Validates & Routes| Service
    Service -->|Business Rules| Repo
    Repo -->|Query Builder| Model
    Model -->|ORM Mapping| DB
    
    DB -->|Results| Model
    Model -->|Data| Repo
    Repo -->|Entities| Service
    Service -->|DTOs| API
    API -->|JSON Response| Client
    
    style External fill:#1e3a5f,stroke:#4a90e2,stroke-width:2px,color:#e8f4fd
    style Application fill:#3d2817,stroke:#d4a574,stroke-width:2px,color:#f5e6d3
    style Data fill:#1e1e4a,stroke:#7474d4,stroke-width:2px,color:#d4d4f5
```

## Key Design Patterns

1. **Layered Architecture**: Separation of concerns across layers
2. **Repository Pattern**: Abstraction of data access
3. **Dependency Injection**: FastAPI's dependency system
4. **Schema Validation**: Pydantic for request/response validation
5. **ORM Mapping**: SQLAlchemy for database operations

## Request Processing Pipeline

```mermaid
flowchart TD
    Start([HTTP Request]) --> Validate{Validate<br/>Pydantic Schema}
    Validate -->|Invalid| Error1[400 Bad Request]
    Validate -->|Valid| Route{Route to<br/>Endpoint}
    Route --> Service[Service Layer<br/>Business Logic]
    Service --> ValidateBiz{Business<br/>Validation}
    ValidateBiz -->|Invalid| Error2[400/404/409]
    ValidateBiz -->|Valid| Repo[Repository<br/>Data Access]
    Repo --> DB[(Database)]
    DB -->|Success| Response[200/201 Response]
    DB -->|Error| Error3[500 Error]
    Response --> End([JSON Response])
    Error1 --> End
    Error2 --> End
    Error3 --> End
    
    style Start fill:#1e4a1e,stroke:#74d474,stroke-width:2px,color:#d4f5d4
    style End fill:#1e4a1e,stroke:#74d474,stroke-width:2px,color:#d4f5d4
    style Validate fill:#3a3a1e,stroke:#d4d474,stroke-width:2px,color:#f5f5d4
    style Service fill:#4a1e3a,stroke:#d474b4,stroke-width:2px,color:#f5d4e8
    style Repo fill:#1e3a4a,stroke:#74b4d4,stroke-width:2px,color:#d4e8f5
    style DB fill:#3a1e1e,stroke:#d47474,stroke-width:2px,color:#f5d4d4
    style Error1 fill:#3a1e1e,stroke:#d47474,stroke-width:2px,color:#f5d4d4
    style Error2 fill:#3a1e1e,stroke:#d47474,stroke-width:2px,color:#f5d4d4
    style Error3 fill:#3a1e1e,stroke:#d47474,stroke-width:2px,color:#f5d4d4
    style Response fill:#1e3a1e,stroke:#74d474,stroke-width:2px,color:#d4f5d4
```
