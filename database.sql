-- 数据库表结构设计

-- 创建数据库
CREATE DATABASE IF NOT EXISTS crm_system;
USE crm_system;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    phone VARCHAR(20) COMMENT '电话',
    email VARCHAR(100) COMMENT '邮箱',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT='用户表';

-- 客户表
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '客户ID',
    name VARCHAR(100) NOT NULL COMMENT '客户名称',
    phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    industry VARCHAR(50) COMMENT '行业',
    tag JSON COMMENT '标签',
    follow_time DATETIME COMMENT '跟进时间',
    business_count INT DEFAULT 0 COMMENT '商机数量',
    remark TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT='客户表';

-- 商机表
CREATE TABLE IF NOT EXISTS business_opportunities (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '商机ID',
    name VARCHAR(200) NOT NULL COMMENT '商机名称',
    customer_id INT NOT NULL COMMENT '客户ID',
    amount DECIMAL(10, 2) NOT NULL COMMENT '金额',
    status VARCHAR(20) NOT NULL COMMENT '状态',
    expected_date DATE NOT NULL COMMENT '预计成交日期',
    follow_person VARCHAR(50) NOT NULL COMMENT '跟进人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
) COMMENT='商机表';

-- 合同表
CREATE TABLE IF NOT EXISTS contracts (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '合同ID',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '合同编号',
    name VARCHAR(200) NOT NULL COMMENT '合同名称',
    customer_id INT NOT NULL COMMENT '客户ID',
    amount DECIMAL(10, 2) NOT NULL COMMENT '金额',
    sign_date DATE NOT NULL COMMENT '签约日期',
    status VARCHAR(20) NOT NULL COMMENT '状态',
    applicant VARCHAR(50) NOT NULL COMMENT '申请人',
    apply_time DATETIME NOT NULL COMMENT '申请时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
) COMMENT='合同表';

-- 跟进记录表
CREATE TABLE IF NOT EXISTS follow_records (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '跟进记录ID',
    customer_id INT NOT NULL COMMENT '客户ID',
    customer_name VARCHAR(100) NOT NULL COMMENT '客户名称',
    business_id INT COMMENT '商机ID',
    business_name VARCHAR(200) COMMENT '商机名称',
    contract_id INT COMMENT '合同ID',
    follow_type VARCHAR(50) NOT NULL COMMENT '跟进方式',
    content TEXT NOT NULL COMMENT '跟进内容',
    follow_result VARCHAR(50) COMMENT '跟进结果',
    next_action VARCHAR(200) COMMENT '下一步行动',
    follow_time DATETIME NOT NULL COMMENT '跟进时间',
    follow_person VARCHAR(50) NOT NULL COMMENT '跟进人',
    next_time DATE COMMENT '下次跟进时间',
    create_todo BOOLEAN DEFAULT FALSE COMMENT '是否创建待办',
    todo_id INT COMMENT '待办ID',
    todo_completed BOOLEAN DEFAULT FALSE COMMENT '待办是否完成',
    attachments JSON COMMENT '附件',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (business_id) REFERENCES business_opportunities(id) ON DELETE SET NULL,
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE SET NULL
) COMMENT='跟进记录表';

-- 待办任务表
CREATE TABLE IF NOT EXISTS todo_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '待办任务ID',
    title VARCHAR(200) NOT NULL COMMENT '任务标题',
    due_date DATE NOT NULL COMMENT '截止日期',
    assignee VARCHAR(50) NOT NULL COMMENT '负责人',
    related_follow_id INT COMMENT '关联跟进记录ID',
    related_customer_id INT COMMENT '关联客户ID',
    related_business_id INT COMMENT '关联商机ID',
    completed BOOLEAN DEFAULT FALSE COMMENT '是否完成',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (related_follow_id) REFERENCES follow_records(id) ON DELETE SET NULL,
    FOREIGN KEY (related_customer_id) REFERENCES customers(id) ON DELETE SET NULL,
    FOREIGN KEY (related_business_id) REFERENCES business_opportunities(id) ON DELETE SET NULL
) COMMENT='待办任务表';

-- 审批表
CREATE TABLE IF NOT EXISTS approvals (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '审批ID',
    type VARCHAR(50) NOT NULL COMMENT '审批类型',
    title VARCHAR(200) NOT NULL COMMENT '审批标题',
    applicant VARCHAR(50) NOT NULL COMMENT '申请人',
    apply_time DATETIME NOT NULL COMMENT '申请时间',
    status VARCHAR(20) DEFAULT '待审批' COMMENT '状态',
    related_contract_id INT COMMENT '关联合同ID',
    related_business_id INT COMMENT '关联商机ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (related_contract_id) REFERENCES contracts(id) ON DELETE SET NULL,
    FOREIGN KEY (related_business_id) REFERENCES business_opportunities(id) ON DELETE SET NULL
) COMMENT='审批表';

-- 插入默认管理员用户
INSERT INTO users (username, password, name, phone, email) VALUES 
('admin', '123456', '管理员', '13812345678', 'admin@crm.com');

-- 插入测试数据
INSERT INTO customers (name, phone, industry, tag, follow_time, business_count, remark) VALUES
('张三', '13812345678', '互联网', '["意向客户", "高价值客户"]', '2025-05-19 14:30:00', 1, '该客户是互联网行业的企业负责人。'),
('李四', '13987654321', '制造业', '["老客户"]', '2025-05-18 10:00:00', 2, '长期合作的制造企业。'),
('王五', '13712348765', '金融', '["潜在客户"]', '2025-05-17 16:00:00', 0, ''),
('赵六', '13687651234', '教育', '["意向客户"]', '2025-05-16 09:00:00', 1, ''),
('钱七', '13543218765', '医疗', '["潜在客户", "高价值客户"]', '2025-05-15 11:30:00', 0, '');

INSERT INTO business_opportunities (name, customer_id, amount, status, expected_date, follow_person) VALUES
('标准版软件采购', 1, 6800.00, '报价中', '2025-05-25', '销售小李'),
('企业安全方案', 2, 12000.00, '初步接触', '2025-06-10', '销售小张'),
('云服务年框', 1, 50000.00, '谈判中', '2025-05-30', '销售小李'),
('培训课程采购', 3, 8000.00, '需求确认', '2025-06-05', '销售小张'),
('设备维保续费', 2, 15000.00, '赢单', '2025-05-20', '销售小李');

INSERT INTO contracts (code, name, customer_id, amount, sign_date, status, applicant, apply_time) VALUES
('HT202505001', '标准版软件采购合同', 1, 6800.00, '2025-05-19', '待审批', '销售小李', '2025-05-19 10:30:00');

INSERT INTO follow_records (customer_id, customer_name, business_id, business_name, contract_id, follow_type, content, follow_result, next_action, follow_time, follow_person, next_time, create_todo, todo_id, todo_completed, attachments) VALUES
(1, '张三', 1, '标准版软件采购', NULL, '微信沟通', '确认产品需求', '意向高', '制作报价单', '2025-05-19 14:30:00', '销售小李', '2025-05-20', true, 1, false, '[]');

INSERT INTO todo_tasks (title, due_date, assignee, related_follow_id, related_customer_id, related_business_id, completed) VALUES
('2025-05-21 前向张三提交报价单', '2025-05-21', '销售小李', 1, 1, 1, false);

INSERT INTO approvals (type, title, applicant, apply_time, status, related_contract_id, related_business_id) VALUES
('合同审批', '合同审批-张三（云安全）', '销售小郑', '2023-09-18 09:00:00', '待审批', NULL, NULL),
('商机审批', '商机审批-王五（企业版采购）', '销售小张', '2023-09-18 10:00:00', '待审批', NULL, NULL);
