# Collaborative Checklist App

A minimalist, containerized web application for creating and sharing checklists. Built with Flask and MySQL, this app allows users to create checklists and share them via secure URLs without requiring authentication.

## Features

- 🎯 **Simple & Clean Interface**: Minimalist design with Bootstrap for a responsive experience
- 🔗 **Shareable Links**: Each checklist gets a unique, secure URL
- ✏️ **Real-time Collaboration**: Multiple users can edit the same checklist simultaneously
- ✅ **Core Functionality**:
  - Create checklists with custom titles
  - Add, remove, and toggle checklist items
  - Edit checklist titles
  - Reset all items to unchecked state
  - Copy checklist link to clipboard
  - Health check endpoint at `/health` to verify database connectivity
- 🔒 **Security**:
  - Input sanitization to prevent XSS
  - Secure random URLs for checklists
  - No public listing of checklists
  - No authentication required

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: Bootstrap 5, JavaScript
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd checklist
   ```

2. Create a `.env` file with the following variables:
   ```env
   MYSQL_USER=checklist_user
   MYSQL_PASSWORD=your_secure_password
   MYSQL_DATABASE=checklist_db
   MYSQL_ROOT_PASSWORD=your_secure_root_password
   # Optional: required for /trending page
   VULN_API_KEY=your_circl_api_key
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
   The application will automatically create the required database tables on startup.

4. Access the application at `http://localhost:5000`

### Optional: Trending Vulnerabilities

To display trending vulnerability information from [vulnerability.circl.lu](https://vulnerability.circl.lu), set the environment variable `VULN_API_KEY` with your API key. A new page is available at `/trending` showing the data fetched from the API.

## Usage

1. **Creating a Checklist**:
   - Visit the homepage
   - Enter a title for your checklist
   - Click "Create Checklist"

2. **Managing Checklist Items**:
   - Add new items using the input field
   - Check/uncheck items by clicking the checkbox
   - Delete items using the trash icon (appears on hover)
   - Edit the checklist title by clicking on it

3. **Sharing**:
   - Click the "Copy Link" button to copy the checklist URL
   - Share the URL with others
   - Anyone with the link can view and edit the checklist

4. **Resetting**:
   - Click "Reset All" to uncheck all items
   - Confirm the action in the popup dialog

## Development

### Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-container setup
└── templates/           # HTML templates
    ├── index.html       # Landing page
    └── checklist.html   # Checklist view/edit page
```

### Database Schema

These tables are created automatically when the Flask app starts.

```sql
CREATE TABLE checklists (
    id VARCHAR(32) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE checklist_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    checklist_id VARCHAR(32) NOT NULL,
    content TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (checklist_id) REFERENCES checklists(id) ON DELETE CASCADE
);
```

## Security Considerations

- The application uses secure random URLs for checklists
- All user input is sanitized to prevent XSS attacks
- No authentication system means anyone with the URL can edit
- Database credentials are managed through environment variables
- HTTPS should be configured in production using a reverse proxy

## Production Deployment

For production deployment:

1. Use a reverse proxy (nginx/Caddy) for HTTPS
2. Set strong passwords in the `.env` file
3. Configure proper backup strategies for the MySQL database
4. Consider using Docker secrets instead of `.env` file
5. Set appropriate resource limits in docker-compose.yml

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 