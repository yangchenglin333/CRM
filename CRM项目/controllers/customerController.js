const { Op } = require('sequelize');
const Customer = require('../models/Customer');
const BusinessOpportunity = require('../models/BusinessOpportunity');

// 获取客户列表
const getCustomerList = async (req, res) => {
  try {
    const { page = 1, pageSize = 10, search = '', industry = '', tag = '' } = req.query;
    
    // 构建查询条件
    const where = {};
    if (search) {
      where[Op.or] = [
        { name: { [Op.like]: `%${search}%` } },
        { phone: { [Op.like]: `%${search}%` } }
      ];
    }
    if (industry) {
      where.industry = industry;
    }
    if (tag) {
      // 这里需要根据实际情况实现标签查询
    }
    
    // 查询客户列表
    const { count, rows } = await Customer.findAndCountAll({
      where,
      limit: parseInt(pageSize),
      offset: (parseInt(page) - 1) * parseInt(pageSize),
      order: [['created_at', 'DESC']]
    });
    
    res.status(200).json({
      total: count,
      list: rows,
      page: parseInt(page),
      pageSize: parseInt(pageSize)
    });
  } catch (error) {
    console.error('获取客户列表错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 获取客户详情
const getCustomerDetail = async (req, res) => {
  try {
    const { id } = req.params;
    
    const customer = await Customer.findByPk(id);
    
    if (!customer) {
      return res.status(404).json({ message: '客户不存在' });
    }
    
    res.status(200).json(customer);
  } catch (error) {
    console.error('获取客户详情错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 新增客户
const addCustomer = async (req, res) => {
  try {
    const { name, phone, industry, tag, remark } = req.body;
    
    // 验证必填字段
    if (!name || !phone) {
      return res.status(400).json({ message: '客户姓名和电话不能为空' });
    }
    
    // 创建客户
    const customer = await Customer.create({
      name,
      phone,
      industry,
      tag,
      remark
    });
    
    res.status(201).json({
      message: '新增客户成功',
      customer
    });
  } catch (error) {
    console.error('新增客户错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 更新客户
const updateCustomer = async (req, res) => {
  try {
    const { id } = req.params;
    const { name, phone, industry, tag, remark } = req.body;
    
    const customer = await Customer.findByPk(id);
    
    if (!customer) {
      return res.status(404).json({ message: '客户不存在' });
    }
    
    // 更新客户信息
    await customer.update({
      name,
      phone,
      industry,
      tag,
      remark
    });
    
    res.status(200).json({
      message: '更新客户成功',
      customer
    });
  } catch (error) {
    console.error('更新客户错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 删除客户
const deleteCustomer = async (req, res) => {
  try {
    const { id } = req.params;
    
    const customer = await Customer.findByPk(id);
    
    if (!customer) {
      return res.status(404).json({ message: '客户不存在' });
    }
    
    // 删除客户
    await customer.destroy();
    
    res.status(200).json({ message: '删除客户成功' });
  } catch (error) {
    console.error('删除客户错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

module.exports = {
  getCustomerList,
  getCustomerDetail,
  addCustomer,
  updateCustomer,
  deleteCustomer
};
