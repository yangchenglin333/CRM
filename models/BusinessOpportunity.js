const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');
const Customer = require('./Customer');

const BusinessOpportunity = sequelize.define('BusinessOpportunity', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  name: {
    type: DataTypes.STRING(200),
    allowNull: false
  },
  customer_id: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: Customer,
      key: 'id'
    }
  },
  amount: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false
  },
  status: {
    type: DataTypes.STRING(20),
    allowNull: false
  },
  expected_date: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  follow_person: {
    type: DataTypes.STRING(50),
    allowNull: false
  }
}, {
  tableName: 'business_opportunities',
  timestamps: true,
  createdAt: 'created_at',
  updatedAt: 'updated_at'
});

// 关联关系
BusinessOpportunity.belongsTo(Customer, { foreignKey: 'customer_id' });
Customer.hasMany(BusinessOpportunity, { foreignKey: 'customer_id' });

module.exports = BusinessOpportunity;
