# **E-commerce Microservices Platform**

## **Project Overview**
This project is a microservices-based e-commerce platform designed to manage user accounts, product inventories, sales transactions, and product reviews. It is developed using Flask for service creation, Docker for containerization, and additional tools for scalability, security, and performance optimization.

---

## **Features**
### **1. Customers Service**
- User registration and authentication.
- Wallet management with balance tracking.
- Role-based access control for admin and users.

### **2. Inventory Service**
- Adding, updating, and managing product details.
- Stock tracking for inventory items.

### **3. Sales Service**
- Processing customer purchases.
- Logging transaction history with timestamps.

### **4. Reviews Service**
- Managing product reviews.
- CRUD operations for reviews by authenticated users.

---

## **Architecture**
### **1. Services**
- **Customers Service**
- **Inventory Service**
- **Sales Service**
- **Reviews Service**

### **2. Database Design**
- **Customers Table**: Manages user data.
- **Inventory Table**: Stores product details.
- **Sales Table**: Links customers to inventory items for purchases.
- **Reviews Table**: Links customers to product reviews.

### **3. Inter-Service Communication**
- Asynchronous messaging via **RabbitMQ**.
- Health-check APIs for monitoring.

---

## **Technologies Used**
- **Backend Framework**: Flask
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Containerization**: Docker, Docker Compose
- **Caching**: Redis
- **Messaging**: RabbitMQ
- **Monitoring**: Prometheus, Grafana
- **Code Documentation**: Sphinx
- **Testing**: Pytest

---

## **Setup and Installation**
### **1. Prerequisites**
- Docker and Docker Compose installed.
- Python 3.10 or later.
- Redis and RabbitMQ installed or Dockerized.

### **2. Clone Repository**
```bash
git clone <repository-url>
cd ecommerce-microservices-platform
