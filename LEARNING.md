# 📚 What I Learned - Detailed Notes

This document contains my detailed learning notes from building this project.

## Table of Contents
- [AWS Services](#aws-services)
- [Networking Concepts](#networking-concepts)
- [Linux & Server Management](#linux--server-management)
- [Git & Version Control](#git--version-control)
- [Debugging Skills](#debugging-skills)
- [Key Takeaways](#key-takeaways)

---

## AWS Services

### Amazon EC2 (Elastic Compute Cloud)

**What I Learned:**
- EC2 is a virtual server in the cloud
- You pay only for what you use (per-second billing)
- Can SSH into it like a regular Linux server
- Instance types: t2.micro (1 vCPU, 1GB RAM) - free tier eligible

**Steps I Performed:**
1. Launched EC2 instance with Amazon Linux 2
2. Created key pair for SSH access
3. Configured security groups
4. Connected via MobaXterm
5. Installed Python, Flask, Git
6. Ran Flask application

**Key Commands:**
```bash
# Connect to EC2
ssh -i my-key.pem ec2-user@54.123.456.789

# Check instance metadata
curl http://169.254.169.254/latest/meta-data/

# Monitor resources
top
df -h
free -m
```

**Mistakes I Made:**
- ❌ Forgot to allow port 5000 in security group initially
- ❌ Tried to SSH without proper key permissions (chmod 400)
- ❌ Didn't know about screen/tmux for persistent sessions

---

### Amazon S3 (Simple Storage Service)

**What I Learned:**
- S3 stores objects (files) in buckets
- Can host static websites directly
- Need to make bucket public for website hosting
- Bucket names must be globally unique

**Configuration Steps:**
1. Created bucket: `student-app-frontend-kshitij`
2. Enabled static website hosting
3. Set index document to `index.html`
4. Added bucket policy for public read access
5. Uploaded `index.html`

**Bucket Policy I Used:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::student-app-frontend-kshitij/*"
    }
  ]
}
```

**Website Endpoint Format:**
```
http://bucket-name.s3-website-region.amazonaws.com
```

---

### Application Load Balancer (ALB)

**What I Learned:**
- ALB distributes traffic across multiple targets
- Can do health checks to know if target is healthy
- Provides a single DNS endpoint for your application
- Costs ~$16/month (expensive for learning!)

**Components:**
1. **Load Balancer**: The main ALB resource
2. **Listener**: Checks for connection requests (HTTP on port 80)
3. **Target Group**: Group of EC2 instances
4. **Health Check**: Periodically checks if targets are responding

**Health Check Configuration:**
- Path: `/students`
- Interval: 30 seconds
- Timeout: 5 seconds
- Healthy threshold: 2 consecutive successes
- Unhealthy threshold: 2 consecutive failures

**Why My Target Was Unhealthy:**
Security group wasn't allowing ALB to reach EC2 on port 5000!

---

### Security Groups

**What I Learned:**
- Security groups = Virtual firewalls
- Control inbound and outbound traffic
- **Stateful**: If you allow inbound, response is automatically allowed outbound
- Can reference other security groups

**My Configuration:**

**EC2 Security Group:**
```
Inbound:
- Type: SSH, Port: 22, Source: MY_IP
- Type: Custom TCP, Port: 5000, Source: ALB_SECURITY_GROUP

Outbound:
- All traffic (default)
```

**ALB Security Group:**
```
Inbound:
- Type: HTTP, Port: 80, Source: 0.0.0.0/0 (anywhere)

Outbound:
- All traffic
```

**Key Concept**: Security groups can reference each other!
- Instead of ALB's IP, use ALB's security group ID
- More maintainable (if ALB IP changes, rule still works)

---

## Networking Concepts

### CORS (Cross-Origin Resource Sharing)

**The Problem:**
```
Frontend: http://bucket.s3-website.com
Backend:  http://alb-dns.amazonaws.com

These are DIFFERENT ORIGINS!
Browser blocks requests by default for security.
```

**What is an Origin?**
Origin = Protocol + Domain + Port
- `http://example.com` ≠ `https://example.com` (different protocol)
- `http://example.com` ≠ `http://api.example.com` (different domain)
- `http://example.com:80` ≠ `http://example.com:3000` (different port)

**The Solution:**
Backend must send CORS headers:
```python
from flask_cors import CORS
CORS(app)
```

This tells browser: "It's okay for requests from other origins"

**Real-World Analogy:**
- You're in Building A (Frontend)
- Need to access Building B (Backend)
- Building B guard (Browser) stops you
- Building B owner (Backend) gives permission note (CORS headers)
- Now guard lets you through

---

### Absolute vs Relative URLs

**My Bug:**
```javascript
// ❌ WRONG - Missing http://
fetch("alb-dns.com/students")
```

**What Happened:**
Browser thought it was a relative URL:
```
Current page: http://bucket.s3-website.com/
Tried to fetch: http://bucket.s3-website.com/alb-dns.com/students
Result: 404 Not Found
```

**The Fix:**
```javascript
// ✅ CORRECT
fetch("http://alb-dns.com/students")
```

**Rule**: For cross-origin requests, ALWAYS use full URL with protocol!

---

### HTTP Methods

**GET /students**
- Purpose: Retrieve data
- No request body
- Safe & Idempotent (can call multiple times)

**POST /students**
- Purpose: Create new data
- Has request body (JSON)
- Not idempotent (calling twice creates two records)

**Request Example:**
```javascript
fetch("http://alb-dns.com/students", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    name: "John",
    marks: 85
  })
})
```

---

## Linux & Server Management

### SSH (Secure Shell)

**What I Learned:**
- SSH = Secure remote access to servers
- Uses public-key cryptography
- Default port: 22

**First Time Setup:**
```bash
# 1. Download .pem key from AWS
# 2. Set correct permissions
chmod 400 my-key.pem

# 3. Connect
ssh -i my-key.pem ec2-user@54.123.456.789
```

**Useful SSH Commands:**
```bash
# Copy file TO server
scp -i my-key.pem file.txt ec2-user@ip:/home/ec2-user/

# Copy file FROM server
scp -i my-key.pem ec2-user@ip:/path/file.txt ./

# Keep connection alive
ssh -i my-key.pem -o ServerAliveInterval=60 ec2-user@ip
```

---

### Linux Commands I Used

**System Management:**
```bash
# Update packages
sudo yum update -y

# Install software
sudo yum install python3 -y

# Check running processes
ps aux | grep python

# Kill process
kill -9 PID

# Check disk usage
df -h

# Check memory
free -m

# Check CPU/Memory in real-time
top
htop  # (better, need to install)
```

**File Operations:**
```bash
# Navigate
cd /path/to/directory
pwd
ls -la

# Create/Delete
mkdir my-folder
rm -rf my-folder

# Edit files
vim file.txt
nano file.txt  # (easier for beginners)

# File permissions
chmod 755 script.sh  # rwxr-xr-x
chmod 644 file.txt   # rw-r--r--
```

**Networking:**
```bash
# Check if port is listening
netstat -tulpn | grep 5000

# Test endpoint
curl http://localhost:5000/students

# Check DNS
nslookup google.com

# Test connectivity
ping google.com
```

---

### Python Virtual Environments

**Why Use venv?**
- Isolates project dependencies
- Prevents conflicts between projects
- Easy to replicate exact environment

**Steps:**
```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Now in venv (notice (venv) in prompt)
(venv) [ec2-user@ip ~]$

# Install packages
pip install flask flask-cors

# Save dependencies
pip freeze > requirements.txt

# Deactivate
deactivate
```

**What's in requirements.txt:**
```
Flask==3.0.0
Flask-Cors==4.0.0
click==8.1.7
...
```

---

### Running Apps Persistently

**Problem**: When I close SSH, Flask stops!

**Solutions:**

**Option 1: nohup**
```bash
nohup python3 app.py &
# Runs in background, output to nohup.out
```

**Option 2: screen (Better)**
```bash
# Start screen session
screen -S flask-app

# Run app
python3 app.py

# Detach: Ctrl+A, then D
# App keeps running!

# Reattach later
screen -r flask-app
```

**Option 3: systemd (Production)**
```bash
# Create service file
sudo nano /etc/systemd/system/flask-app.service

# Enable and start
sudo systemctl enable flask-app
sudo systemctl start flask-app
```

---

## Git & Version Control

### Basic Git Workflow
```bash
# Clone repository
git clone https://github.com/username/repo.git

# Check status
git status

# Stage changes
git add .
git add specific-file.txt

# Commit
git commit -m "Descriptive message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

### .gitignore

**What to ignore:**
```
# Python
__pycache__/
*.pyc
venv/
*.egg-info/

# Environment
.env
*.pem
*.key

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

**Why?**
- Don't commit sensitive data (keys, passwords)
- Don't commit generated files (__pycache__)
- Don't commit large binaries
- Keep repo clean!

---

## Debugging Skills

### Systematic Debugging Approach

**My Process for "Target Unhealthy" Issue:**

1. **Define the problem**
   - ALB showing target as unhealthy
   - Can't access application through ALB

2. **Check each layer systematically**
   
   **Layer 1: Application**
```bash
   # Is Flask running?
   ps aux | grep python
   ✓ Yes, running
   
   # Is it responding?
   curl localhost:5000/students
   ✓ Yes, returns JSON
```
   
   **Layer 2: EC2 Level**
```bash
   # Is port 5000 listening?
   netstat -tulpn | grep 5000
   ✓ Yes, listening
```
   
   **Layer 3: Security Groups**
```bash
   # Does EC2 SG allow port 5000?
   Check AWS Console...
   ✗ NO! Only allows port 22
```
   
   **FOUND THE PROBLEM!**

3. **Fix and verify**
   - Add inbound rule: Port 5000 from ALB SG
   - Wait 30 seconds
   - ✓ Target becomes healthy!

---

### Using Browser DevTools

**Network Tab:**
- Shows all HTTP requests
- Can see request/response headers
- Shows status codes (200, 404, 500)
- Shows response time

**Console Tab:**
- Shows JavaScript errors
- My CORS error showed here
- My URL typo error showed here

**Key Errors I Saw:**

**CORS Error:**
```
Access to fetch at 'http://alb-dns.com/students' from origin 
'http://s3-bucket.com' has been blocked by CORS policy
```

**JSON Parse Error (from URL typo):**