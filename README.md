# EduSphere API

EduSphere is a robust backend API for connecting students globally with research and internship opportunities. Built with FastAPI and PostgreSQL, it provides a secure and scalable platform for students and universities to interact.

## 🚀 Features

- **User Authentication & Security**

  - JWT-based authentication
  - Role-based access control (Student/University)
  - Secure password hashing
  - OAuth 2.0 support

- **Profile Management**

  - Student profiles with education details and skills
  - University profiles with institutional information
  - Profile picture upload with S3 integration

- **Opportunity Management**

  - Create and manage research/internship opportunities
  - Advanced search with multiple filters
  - Pagination support
  - AI-powered recommendations using OpenAI

- **Application System**
  - Submit and track applications
  - Application status management
  - Review system for universities

## 🛠 Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with OAuth 2.0
- **Storage**: AWS S3 (profile pictures)
- **AI Integration**: OpenAI API
- **Containerization**: Docker

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL
- AWS Account (for S3)
- OpenAI API Key

## 🔧 Configuration

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/edusphere.git
   cd edusphere
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/edusphere
   JWT_SECRET_KEY=your-secret-key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   OPENAI_API_KEY=your-openai-api-key
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   AWS_BUCKET_NAME=your-bucket-name
   AWS_REGION=your-region
   ```

## 🚀 Running the Application

### Local Development

1. Start the application:

   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Deployment

1. Build the Docker image:

   ```bash
   docker build -t edusphere .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env edusphere
   ```

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/v1/auth/register`: Register new user (student/university)
- `POST /api/v1/auth/login`: Login and get access token

### Profile Endpoints

- `POST /api/v1/profiles/student`: Create student profile
- `PUT /api/v1/profiles/student`: Update student profile
- `POST /api/v1/profiles/university`: Create university profile
- `PUT /api/v1/profiles/university`: Update university profile
- `POST /api/v1/profiles/upload-picture`: Upload profile picture

### Opportunity Endpoints

- `POST /api/v1/opportunities`: Create new opportunity
- `PUT /api/v1/opportunities/{opportunity_id}`: Update opportunity
- `GET /api/v1/opportunities/search`: Search opportunities with filters
- `GET /api/v1/opportunities/recommendations`: Get AI-powered recommendations

### Application Endpoints

- `POST /api/v1/opportunities/apply/{opportunity_id}`: Submit application
- `PUT /api/v1/opportunities/applications/{application_id}`: Update application status

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Role-based access control
- Input validation using Pydantic
- CORS middleware configuration
- Rate limiting (TODO)
- SQL injection protection via SQLAlchemy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
