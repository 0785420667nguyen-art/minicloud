CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL UNIQUE,
    fullname VARCHAR(100) NOT NULL,
    dob DATE,
    major VARCHAR(50)
);

INSERT INTO students (student_id, fullname, dob, major) VALUES 
('SV001', 'Nguyen Van An', '2003-01-15', 'Mang may tinh'),
('SV002', 'Tran Thi Binh', '2003-05-20', 'An toan thong tin'),
('SV003', 'Le Van Cuong', '2003-09-10', 'Cong nghe phan mem');