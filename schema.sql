-- LifeConnect Database Schema
-- Run this in MySQL Workbench

CREATE DATABASE IF NOT EXISTS lifeconnect;
USE lifeconnect;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    phone       VARCHAR(15),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Donors Table
CREATE TABLE IF NOT EXISTS donors (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    blood_group  ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    city         VARCHAR(100) NOT NULL,
    state        VARCHAR(100) NOT NULL,
    age          INT NOT NULL,
    gender       ENUM('Male','Female','Other') NOT NULL,
    last_donated DATE,
    is_available TINYINT(1) DEFAULT 1,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Blood Requests Table
CREATE TABLE IF NOT EXISTS blood_requests (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    blood_group  ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    units_needed INT NOT NULL DEFAULT 1,
    hospital     VARCHAR(200) NOT NULL,
    city         VARCHAR(100) NOT NULL,
    state        VARCHAR(100) NOT NULL,
    urgency      ENUM('Normal','Urgent','Critical') DEFAULT 'Normal',
    notes        TEXT,
    status       ENUM('open','fulfilled','cancelled') DEFAULT 'open',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Sample Data (optional)
INSERT INTO users (name, email, password, phone) VALUES
('Admin User', 'admin@lifeconnect.com', 'pbkdf2:sha256:placeholder', '9876543210');
