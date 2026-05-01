const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

const mockData = {
  customers: [
    { id: 1, name: '张先生', phone: '13812345678', industry: '互联网', tag: ['重要客户'], follow_time: '2024-01-15', business_count: 5, remark: 'VIP客户' },
    { id: 2, name: '李女士', phone: '13987654321', industry: '金融', tag: ['新客户'], follow_time: '2024-02-20', business_count: 2, remark: '' },
    { id: 3, name: '王总', phone: '13711112222', industry: '制造业', tag: ['长期合作'], follow_time: '2024-01-10', business_count: 10, remark: '重点维护' },
    { id: 4, name: '赵先生', phone: '13633334444', industry: '教育', tag: ['潜在客户'], follow_time: '2024-03-01', business_count: 1, remark: '需要跟进' }
  ],
  business: [
    { id: 1, customer_id: 1, name: '年度合作项目', amount: 500000, stage: '谈判中', probability: 60, follow_time: '2024-03-10', remark: '' },
    { id: 2, customer_id: 2, name: '季度服务合同', amount: 80000, stage: '已签约', probability: 100, follow_time: '2024-02-25', remark: '已完成' },
    { id: 3, customer_id: 3, name: '设备采购项目', amount: 2000000, stage: '需求分析', probability: 30, follow_time: '2024-03-05', remark: '大型项目' }
  ],
  contracts: [
    { id: 1, customer_id: 2, business_id: 2, name: 'Q1服务合同', amount: 80000, sign_date: '2024-02-25', start_date: '2024-03-01', end_date: '2024-06-30', status: '执行中' },
    { id: 2, customer_id: 1, name: '框架协议', amount: 1000000, sign_date: '2024-01-15', start_date: '2024-01-15', end_date: '2024-12-31', status: '执行中' }
  ],
  users: [
    { id: 1, username: 'admin', password: '123456', name: '管理员', phone: '13812345678', email: 'admin@crm.com', role: 'admin' },
    { id: 2, username: 'sales', password: '123456', name: '销售经理', phone: '13987654321', email: 'sales@crm.com', role: 'sales' }
  ],
  approvals: [
    { id: 1, type: 'contract', target_id: 1, status: 'approved', apply_time: '2024-02-20', approve_time: '2024-02-22', remark: '' },
    { id: 2, type: 'business', target_id: 3, status: 'pending', apply_time: '2024-03-08', approve_time: '', remark: '等待审批' }
  ]
};

function isValidPhone(phone) {
  if (!phone) return false;
  const phoneRegex = /^1[3-9]\d{9}$/;
  return phoneRegex.test(phone);
}

function isValidEmail(email) {
  if (!email) return false;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

app.post('/api/users/login', (req, res) => {
  const { username, password } = req.body;
  
  if (!username || !password) {
    return res.status(400).json({ message: '用户名和密码不能为空' });
  }
  
  if (username.length < 4 || username.length > 50) {
    return res.status(400).json({ message: '用户名长度必须在4-50个字符之间' });
  }
  
  if (password.length < 6 || password.length > 32) {
    return res.status(400).json({ message: '密码长度必须在6-32个字符之间' });
  }
  
  const user = mockData.users.find(u => u.username === username && u.password === password);
  
  if (user) {
    const { password, ...userInfo } = user;
    res.json({ message: '登录成功', user: userInfo });
  } else {
    res.status(401).json({ message: '用户名或密码错误' });
  }
});

app.get('/api/users/info', (req, res) => {
  const userId = parseInt(req.query.id);
  const user = mockData.users.find(u => u.id === userId);
  
  if (user) {
    const { password, ...userInfo } = user;
    res.json(userInfo);
  } else {
    res.status(404).json({ message: '用户不存在' });
  }
});

app.put('/api/users/update', (req, res) => {
  const { id, name, phone, email } = req.body;
  
  if (!name || name.trim() === '') {
    return res.status(400).json({ message: '姓名不能为空' });
  }
  
  if (phone && !isValidPhone(phone)) {
    return res.status(400).json({ message: '手机号格式不正确' });
  }
  
  if (email && !isValidEmail(email)) {
    return res.status(400).json({ message: '邮箱格式不正确' });
  }
  
  const userIndex = mockData.users.findIndex(u => u.id === id);
  
  if (userIndex === -1) {
    return res.status(404).json({ message: '用户不存在' });
  }
  
  mockData.users[userIndex] = { ...mockData.users[userIndex], name, phone, email };
  const { password, ...updatedUser } = mockData.users[userIndex];
  
  res.json({ message: '更新成功', user: updatedUser });
});

app.get('/api/customers', (req, res) => {
  res.json(mockData.customers);
});

app.post('/api/customers', (req, res) => {
  const { name, phone, industry, tag, remark } = req.body;
  
  if (!name || name.trim() === '') {
    return res.status(400).json({ message: '客户名称不能为空' });
  }
  
  if (name.trim().length < 4) {
    return res.status(400).json({ message: '客户名称不能少于4个字符' });
  }
  
  if (name.length > 50) {
    return res.status(400).json({ message: '客户名称不能超过50个字符' });
  }
  
  if (!phone || phone.trim() === '') {
    return res.status(400).json({ message: '联系电话不能为空' });
  }
  
  if (!isValidPhone(phone)) {
    return res.status(400).json({ message: '联系电话格式不正确（需为11位手机号）' });
  }
  
  if (!industry || industry.trim() === '') {
    return res.status(400).json({ message: '所属行业不能为空' });
  }
  
  const newCustomer = {
    id: mockData.customers.length + 1,
    name: name.trim(),
    phone: phone.trim(),
    industry: industry.trim(),
    tag: tag || [],
    follow_time: new Date().toISOString().split('T')[0],
    business_count: 0,
    remark: remark || ''
  };
  
  mockData.customers.push(newCustomer);
  res.status(201).json({ message: '新增客户成功', customer: newCustomer });
});

app.get('/api/customers/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const customer = mockData.customers.find(c => c.id === id);
  
  if (customer) {
    res.json(customer);
  } else {
    res.status(404).json({ message: '客户不存在' });
  }
});

app.put('/api/customers/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { name, phone, industry, tag, remark } = req.body;
  
  const customerIndex = mockData.customers.findIndex(c => c.id === id);
  
  if (customerIndex === -1) {
    return res.status(404).json({ message: '客户不存在' });
  }
  
  if (name) {
    if (name.trim() === '') {
      return res.status(400).json({ message: '客户名称不能为空' });
    }
    if (name.length > 50) {
      return res.status(400).json({ message: '客户名称不能超过50个字符' });
    }
  }
  
  if (phone && !isValidPhone(phone)) {
    return res.status(400).json({ message: '联系电话格式不正确' });
  }
  
  mockData.customers[customerIndex] = { ...mockData.customers[customerIndex], ...req.body };
  res.json({ message: '更新成功', customer: mockData.customers[customerIndex] });
});

app.delete('/api/customers/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const customerIndex = mockData.customers.findIndex(c => c.id === id);
  
  if (customerIndex === -1) {
    return res.status(404).json({ message: '客户不存在' });
  }
  
  mockData.customers.splice(customerIndex, 1);
  res.json({ message: '删除成功' });
});

app.get('/api/business', (req, res) => {
  res.json(mockData.business);
});

app.post('/api/business', (req, res) => {
  const { customer_id, name, amount, stage, probability } = req.body;
  
  if (!name || name.trim() === '') {
    return res.status(400).json({ message: '商机名称不能为空' });
  }
  
  if (!customer_id) {
    return res.status(400).json({ message: '客户ID不能为空' });
  }
  
  const customerExists = mockData.customers.some(c => c.id === customer_id);
  if (!customerExists) {
    return res.status(400).json({ message: '客户不存在' });
  }
  
  if (!amount || amount <= 0) {
    return res.status(400).json({ message: '金额必须大于0' });
  }
  
  const newBusiness = {
    id: mockData.business.length + 1,
    customer_id,
    name: name.trim(),
    amount,
    stage: stage || '需求分析',
    probability: probability || 0,
    follow_time: new Date().toISOString().split('T')[0],
    remark: ''
  };
  
  mockData.business.push(newBusiness);
  
  const customerIndex = mockData.customers.findIndex(c => c.id === customer_id);
  if (customerIndex !== -1) {
    mockData.customers[customerIndex].business_count++;
  }
  
  res.status(201).json({ message: '新增商机成功', business: newBusiness });
});

app.get('/api/business/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const business = mockData.business.find(b => b.id === id);
  
  if (business) {
    res.json(business);
  } else {
    res.status(404).json({ message: '商机不存在' });
  }
});

app.put('/api/business/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { customer_id, name, amount, stage, probability } = req.body;
  
  const businessIndex = mockData.business.findIndex(b => b.id === id);
  
  if (businessIndex === -1) {
    return res.status(404).json({ message: '商机不存在' });
  }
  
  if (name && name.trim() === '') {
    return res.status(400).json({ message: '商机名称不能为空' });
  }
  
  if (customer_id) {
    const customerExists = mockData.customers.some(c => c.id === customer_id);
    if (!customerExists) {
      return res.status(400).json({ message: '客户不存在' });
    }
  }
  
  if (amount && amount <= 0) {
    return res.status(400).json({ message: '金额必须大于0' });
  }
  
  mockData.business[businessIndex] = { ...mockData.business[businessIndex], ...req.body };
  res.json({ message: '更新成功', business: mockData.business[businessIndex] });
});

app.delete('/api/business/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const businessIndex = mockData.business.findIndex(b => b.id === id);
  
  if (businessIndex === -1) {
    return res.status(404).json({ message: '商机不存在' });
  }
  
  const business = mockData.business[businessIndex];
  const customerIndex = mockData.customers.findIndex(c => c.id === business.customer_id);
  if (customerIndex !== -1 && mockData.customers[customerIndex].business_count > 0) {
    mockData.customers[customerIndex].business_count--;
  }
  
  mockData.business.splice(businessIndex, 1);
  res.json({ message: '删除成功' });
});

app.get('/api/contracts', (req, res) => {
  res.json(mockData.contracts);
});

app.post('/api/contracts', (req, res) => {
  const { customer_id, business_id, name, amount, sign_date, start_date, end_date } = req.body;
  
  if (!name || name.trim() === '') {
    return res.status(400).json({ message: '合同名称不能为空' });
  }
  
  if (!customer_id) {
    return res.status(400).json({ message: '客户ID不能为空' });
  }
  
  const customerExists = mockData.customers.some(c => c.id === customer_id);
  if (!customerExists) {
    return res.status(400).json({ message: '客户不存在' });
  }
  
  if (!amount || amount <= 0) {
    return res.status(400).json({ message: '金额必须大于0' });
  }
  
  const newContract = {
    id: mockData.contracts.length + 1,
    customer_id,
    business_id: business_id || null,
    name: name.trim(),
    amount,
    sign_date: sign_date || new Date().toISOString().split('T')[0],
    start_date: start_date || new Date().toISOString().split('T')[0],
    end_date: end_date || new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    status: '待审批'
  };
  
  mockData.contracts.push(newContract);
  res.status(201).json({ message: '新增合同成功', contract: newContract });
});

app.get('/api/approvals', (req, res) => {
  res.json(mockData.approvals);
});

app.post('/api/approvals', (req, res) => {
  const { type, target_id } = req.body;
  
  if (!type || !['contract', 'business'].includes(type)) {
    return res.status(400).json({ message: '审批类型无效' });
  }
  
  if (!target_id) {
    return res.status(400).json({ message: '目标ID不能为空' });
  }
  
  const newApproval = {
    id: mockData.approvals.length + 1,
    type,
    target_id,
    status: 'pending',
    apply_time: new Date().toISOString().split('T')[0],
    approve_time: '',
    remark: ''
  };
  
  mockData.approvals.push(newApproval);
  res.status(201).json({ message: '提交审批成功', approval: newApproval });
});

app.put('/api/approvals/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { status, remark } = req.body;
  
  const approvalIndex = mockData.approvals.findIndex(a => a.id === id);
  
  if (approvalIndex === -1) {
    return res.status(404).json({ message: '审批记录不存在' });
  }
  
  if (!status || !['approved', 'rejected', 'pending'].includes(status)) {
    return res.status(400).json({ message: '状态无效' });
  }
  
  mockData.approvals[approvalIndex] = {
    ...mockData.approvals[approvalIndex],
    status,
    remark: remark || '',
    approve_time: status !== 'pending' ? new Date().toISOString().split('T')[0] : ''
  };
  
  if (status === 'approved' && mockData.approvals[approvalIndex].type === 'contract') {
    const contractIndex = mockData.contracts.findIndex(c => c.id === mockData.approvals[approvalIndex].target_id);
    if (contractIndex !== -1) {
      mockData.contracts[contractIndex].status = '执行中';
    }
  }
  
  res.json({ message: '审批成功', approval: mockData.approvals[approvalIndex] });
});

app.listen(port, () => {
  console.log(`CRM系统运行在 http://localhost:${port}`);
});
