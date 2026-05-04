const { Op } = require('sequelize');
const Contract = require('../models/Contract');
const Customer = require('../models/Customer');
const Approval = require('../models/Approval');

// 获取合同列表
const getContractList = async (req, res) => {
  try {
    const { page = 1, pageSize = 10, search = '', status = '' } = req.query;
    
    // 构建查询条件
    const where = {};
    if (search) {
      where[Op.or] = [
        { code: { [Op.like]: `%${search}%` } },
        { name: { [Op.like]: `%${search}%` } }
      ];
    }
    if (status) {
      where.status = status;
    }
    
    // 查询合同列表
    const { count, rows } = await Contract.findAndCountAll({
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
    console.error('获取合同列表错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 获取合同详情
const getContractDetail = async (req, res) => {
  try {
    const { id } = req.params;
    
    const contract = await Contract.findByPk(id, {
      include: [{
        model: Customer,
        attributes: ['name', 'phone']
      }]
    });
    
    if (!contract) {
      return res.status(404).json({ message: '合同不存在' });
    }
    
    res.status(200).json(contract);
  } catch (error) {
    console.error('获取合同详情错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 新增合同
const addContract = async (req, res) => {
  try {
    const { code, name, customer_id, amount, sign_date, status, applicant, apply_time } = req.body;
    
    // 验证必填字段
    if (!code || !name || !customer_id || !amount || !sign_date || !status || !applicant || !apply_time) {
      return res.status(400).json({ message: '请填写所有必填字段' });
    }
    
    // 验证客户是否存在
    const customer = await Customer.findByPk(customer_id);
    if (!customer) {
      return res.status(404).json({ message: '客户不存在' });
    }
    
    // 创建合同
    const contract = await Contract.create({
      code,
      name,
      customer_id,
      amount,
      sign_date,
      status,
      applicant,
      apply_time
    });
    
    res.status(201).json({
      message: '新增合同成功',
      contract
    });
  } catch (error) {
    console.error('新增合同错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 更新合同
const updateContract = async (req, res) => {
  try {
    const { id } = req.params;
    const { code, name, customer_id, amount, sign_date, status, applicant, apply_time } = req.body;
    
    const contract = await Contract.findByPk(id);
    
    if (!contract) {
      return res.status(404).json({ message: '合同不存在' });
    }
    
    // 验证客户是否存在
    if (customer_id) {
      const customer = await Customer.findByPk(customer_id);
      if (!customer) {
        return res.status(404).json({ message: '客户不存在' });
      }
    }
    
    // 更新合同信息
    await contract.update({
      code,
      name,
      customer_id,
      amount,
      sign_date,
      status,
      applicant,
      apply_time
    });
    
    res.status(200).json({
      message: '更新合同成功',
      contract
    });
  } catch (error) {
    console.error('更新合同错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 删除合同
const deleteContract = async (req, res) => {
  try {
    const { id } = req.params;
    
    const contract = await Contract.findByPk(id);
    
    if (!contract) {
      return res.status(404).json({ message: '合同不存在' });
    }
    
    // 删除合同
    await contract.destroy();
    
    res.status(200).json({ message: '删除合同成功' });
  } catch (error) {
    console.error('删除合同错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 提交合同审批
const submitContractApproval = async (req, res) => {
  try {
    const { id } = req.params;
    
    const contract = await Contract.findByPk(id);
    
    if (!contract) {
      return res.status(404).json({ message: '合同不存在' });
    }
    
    // 更新合同状态为待审批
    await contract.update({ status: '待审批' });
    
    // 创建审批记录
    const approval = await Approval.create({
      type: '合同审批',
      title: `合同审批-${contract.name}`,
      applicant: contract.applicant,
      apply_time: new Date(),
      status: '待审批',
      related_contract_id: contract.id
    });
    
    res.status(200).json({
      message: '提交审批成功',
      approval
    });
  } catch (error) {
    console.error('提交合同审批错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

module.exports = {
  getContractList,
  getContractDetail,
  addContract,
  updateContract,
  deleteContract,
  submitContractApproval
};
