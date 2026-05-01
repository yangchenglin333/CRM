const { Sequelize } = require('sequelize');

// 数据库连接配置
const sequelize = new Sequelize('crm_system', 'root', '', {
  host: 'localhost',
  port: 3306,
  dialect: 'mysql',
  logging: console.log,
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  }
});

// 测试连接
sequelize.authenticate()
  .then(() => {
    console.log('Database connection has been established successfully.');
  })
  .catch((error) => {
    console.error('Unable to connect to the database:', error);
  });

module.exports = sequelize;
