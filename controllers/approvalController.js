const { Op } = require('sequelize');
const Approval = require('../models/Approval');
const Contract = require('../models/Contract');

// 获取审批列表
const getApprovalList = async (req, res) => {
  try {
    const { page = 1, pageSize = 10, status = '', type = '' } = req.query;
    
    // 构建查询条件
    const where = {};
    if (status) {
      where.status = status;
    }
    if (type) {
      where.type = type;
    }
    
    // 查询审批列表
    const { count, rows } = await Approval.findAndCountAll({
      where,
      limit: parseInt(pageSize),
      offset: (parseInt(page) - 1) * parseInt(pageSize),
      order: [['apply_time', 'DESC']]
    });
    
    res.status(200).json({
      total: count,
      list: rows,
      page: parseInt(page),
      pageSize: parseInt(pageSize)
    });
  } catch (error) {
    console.error('获取审批列表错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 获取审批详情
const getApprovalDetail = async (req, res) => {
  try {
    const { id } = req.params;
    
    const approval = await Approval.findByPk(id, {
      include: [{
        model: Contract,
        attributes: ['code', 'name', 'amount']
      }]
    });
    
    if (!approval) {
      return res.status(404).json({ message: '审批不存在' });
    }
    
    res.status(200).json(approval);
  } catch (error) {
    console.error('获取审批详情错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 新增审批
const addApproval = async (req, res) => {
  try {
    const { type, title, applicant, apply_time, related_contract_id, related_business_id } = req.body;
    
    // 验证必填字段
    if (!type || !title || !applicant || !apply_time) {
      return res.status(400).json({ message: '请填写所有必填字段' });
    }
    
    // 创建审批
    const approval = await Approval.create({
      type,
      title,
      applicant,
      apply_time,
      status: '待审批',
      related_contract_id,
      related_business_id
    });
    
    res.status(201).json({
      message: '新增审批成功',
      approval
    });
  } catch (error) {
    console.error('新增审批错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 更新审批
const updateApproval = async (req, res) => {
  try {
    const { id } = req.params;
    const { type, title, applicant, apply_time, status, related_contract_id, related_business_id } = req.body;
    
    const approval = await Approval.findByPk(id);
    
    if (!approval) {
      return res.status(404).json({ message: '审批不存在' });
    }
    
    // 更新审批
    await approval.update({
      type,
      title,
      applicant,
      apply_time,
      status,
      related_contract_id,
      related_business_id
    });
    
    res.status(200).json({
      message: '更新审批成功',
      approval
    });
  } catch (error) {
    console.error('更新审批错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 删除审批
const deleteApproval = async (req, res) => {
  try {
    const { id } = req.params;
    
    const approval = await Approval.findByPk(id);
    
    if (!approval) {
      return res.status(404).json({ message: '审批不存在' });
    }
    
    // 删除审批
    await approval.destroy();
    
    res.status(200).json({ message: '删除审批成功' });
  } catch (error) {
    console.error('删除审批错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 审批通过
const approvalPass = async (req, res) => {
  try {
    const { id } = req.params;
    
    const approval = await Approval.findByPk(id);
    
    if (!approval) {
      return res.status(404).json({ message: '审批不存在' });
    }
    
    // 更新审批状态为已通过
    await approval.update({ status: '已通过' });
    
    // 如果是合同审批，更新合同状态
    if (approval.related_contract_id) {
      await Contract.update(
        { status: '已通过' },
        { where: { id: approval.related_contract_id } }
      );
    }
    
    res.status(200).json({
      message: '审批通过成功',
      approval
    });
  } catch (error) {
    console.error('审批通过错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 审批拒绝
const approvalReject = async (req, res) => {
  try {
    const { id } = req.params;
    
    const approval = await Approval.findByPk(id);
    
    if (!approval) {
      return res.status(404).json({ message: '审批不存在' });
    }
    
    // 更新审批状态为已拒绝
    await approval.update({ status: '已拒绝' });
    
    // 如果是合同审批，更新合同状态
    if (approval.related_contract_id) {
      await Contract.update(
        { status: '已拒绝' },
        { where: { id: approval.related_contract_id } }
      );
    }
    
    res.status(200).json({
      message: '审批拒绝成功',
      approval
    });
  } catch (error) {
    console.error('审批拒绝错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

module.exports = {
  getApprovalList,
  getApprovalDetail,
  addApproval,
  updateApproval,
  deleteApproval,
  approvalPass,
  approvalReject
};
