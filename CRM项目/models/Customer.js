const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Customer = sequelize.define('Customer', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  name: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  phone: {
    type: DataTypes.STRING(20),
    allowNull: false
  },
  industry: {
    type: DataTypes.STRING(50)
  },
  tag: {
    type: DataTypes.JSON
  },
  follow_time: {
    type: DataTypes.DATE
  },
  business_count: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  },
  remark: {
    type: DataTypes.TEXT
  }
}, {
  tableName: 'customers',
  timestamps: true,
  createdAt: 'created_at',
  updatedAt: 'updated_at'
});

module.exports = Customer;
