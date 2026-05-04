const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');
const Contract = require('./Contract');
const BusinessOpportunity = require('./BusinessOpportunity');

const Approval = sequelize.define('Approval', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  type: {
    type: DataTypes.STRING(50),
    allowNull: false
  },
  title: {
    type: DataTypes.STRING(200),
    allowNull: false
  },
  applicant: {
    type: DataTypes.STRING(50),
    allowNull: false
  },
  apply_time: {
    type: DataTypes.DATE,
    allowNull: false
  },
  status: {
    type: DataTypes.STRING(20),
    defaultValue: '待审批'
  },
  related_contract_id: {
    type: DataTypes.INTEGER,
    references: {
      model: Contract,
      key: 'id'
    }
  },
  related_business_id: {
    type: DataTypes.INTEGER,
    references: {
      model: BusinessOpportunity,
      key: 'id'
    }
  }
}, {
  tableName: 'approvals',
  timestamps: true,
  createdAt: 'created_at',
  updatedAt: 'updated_at'
});

// 关联关系
Approval.belongsTo(Contract, { foreignKey: 'related_contract_id' });
Approval.belongsTo(BusinessOpportunity, { foreignKey: 'related_business_id' });

module.exports = Approval;
