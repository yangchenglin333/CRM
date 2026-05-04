const { Op, Sequelize } = require('sequelize');
const BusinessOpportunity = require('../models/BusinessOpportunity');
const Customer = require('../models/Customer');
const sequelize = require('../config/database');

// 获取商机列表
const getBusinessList = async (req, res) => {
  try {
    const { page = 1, pageSize = 10, search = '', status = '' } = req.query;
    
    // 构建查询条件
    const where = {};
    if (search) {
      where[Op.or] = [
        { name: { [Op.like]: `%${search}%` } }
      ];
    }
    if (status) {
      where.status = status;
    }
    
    // 查询商机列表
    const { count, rows } = await BusinessOpportunity.findAndCountAll({
      where,
      include: [{
        model: Customer,
        attributes: ['name']
      }],
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
    console.error('获取商机列表错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 获取商机详情
const getBusinessDetail = async (req, res) => {
  try {
    const { id } = req.params;
    
    const business = await BusinessOpportunity.findByPk(id, {
      include: [{
        model: Customer,
        attributes: ['name', 'phone']
      }]
    });
    
    if (!business) {
      return res.status(404).json({ message: '商机不存在' });
    }
    
    res.status(200).json(business);
  } catch (error) {
    console.error('获取商机详情错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 新增商机
const addBusiness = async (req, res) => {
  try {
    const { name, customer_id, amount, status, expected_date, follow_person } = req.body;
    
    // 验证必填字段
    if (!name || !customer_id || !amount || !status || !expected_date || !follow_person) {
      return res.status(400).json({ message: '请填写所有必填字段' });
    }
    
    // 验证客户是否存在
    const customer = await Customer.findByPk(customer_id);
    if (!customer) {
      return res.status(404).json({ message: '客户不存在' });
    }
    
    // 创建商机
    const business = await BusinessOpportunity.create({
      name,
      customer_id,
      amount,
      status,
      expected_date,
      follow_person
    });
    
    // 更新客户的商机数量
    await Customer.update(
      { business_count: sequelize.literal('business_count + 1') },
      { where: { id: customer_id } }
    );
    
    res.status(201).json({
      message: '新增商机成功',
      business
    });
  } catch (error) {
    console.error('新增商机错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 更新商机
const updateBusiness = async (req, res) => {
  try {
    const { id } = req.params;
    const { name, customer_id, amount, status, expected_date, follow_person } = req.body;
    
    const business = await BusinessOpportunity.findByPk(id);
    
    if (!business) {
      return res.status(404).json({ message: '商机不存在' });
    }
    
    // 验证客户是否存在
    if (customer_id) {
      const customer = await Customer.findByPk(customer_id);
      if (!customer) {
        return res.status(404).json({ message: '客户不存在' });
      }
      
      // 如果客户发生变化，更新两个客户的商机数量
      if (business.customer_id !== customer_id) {
        await Customer.update(
          { business_count: sequelize.literal('business_count - 1') },
          { where: { id: business.customer_id } }
        );
        await Customer.update(
          { business_count: sequelize.literal('business_count + 1') },
          { where: { id: customer_id } }
        );
      }
    }
    
    // 更新商机信息
    await business.update({
      name,
      customer_id,
      amount,
      status,
      expected_date,
      follow_person
    });
    
    res.status(200).json({
      message: '更新商机成功',
      business
    });
  } catch (error) {
    console.error('更新商机错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 删除商机
const deleteBusiness = async (req, res) => {
  try {
    const { id } = req.params;
    
    const business = await BusinessOpportunity.findByPk(id);
    
    if (!business) {
      return res.status(404).json({ message: '商机不存在' });
    }
    
    const customerId = business.customer_id;
    
    // 删除商机
    await business.destroy();
    
    // 更新客户的商机数量
    await Customer.update(
      { business_count: sequelize.literal('business_count - 1') },
      { where: { id: customerId } }
    );
    
    res.status(200).json({ message: '删除商机成功' });
  } catch (error) {
    console.error('删除商机错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

module.exports = {
  getBusinessList,
  getBusinessDetail,
  addBusiness,
  updateBusiness,
  deleteBusiness
};
