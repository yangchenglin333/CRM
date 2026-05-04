const express = require('express');
const router = express.Router();
const businessController = require('../controllers/businessController');

// 获取商机列表
router.get('/', businessController.getBusinessList);

// 获取商机详情
router.get('/:id', businessController.getBusinessDetail);

// 新增商机
router.post('/', businessController.addBusiness);

// 更新商机
router.put('/:id', businessController.updateBusiness);

// 删除商机
router.delete('/:id', businessController.deleteBusiness);

module.exports = router;
