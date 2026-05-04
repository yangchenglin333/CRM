const User = require('../models/User');

// 登录
const login = async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // 查找用户
    const user = await User.findOne({ where: { username } });
    
    if (!user) {
      return res.status(401).json({ message: '账号或密码错误' });
    }
    
    // 简单验证密码（实际项目中应该使用加密）
    if (user.password !== password) {
      return res.status(401).json({ message: '账号或密码错误' });
    }
    
    // 返回用户信息
    res.status(200).json({
      message: '登录成功',
      user: {
        id: user.id,
        username: user.username,
        name: user.name,
        phone: user.phone,
        email: user.email
      }
    });
  } catch (error) {
    console.error('登录错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 获取用户信息
const getUserInfo = async (req, res) => {
  try {
    // 这里应该从请求中获取用户ID（实际项目中使用JWT）
    const userId = 1; // 暂时使用默认管理员ID
    
    const user = await User.findByPk(userId);
    
    if (!user) {
      return res.status(404).json({ message: '用户不存在' });
    }
    
    res.status(200).json({
      id: user.id,
      username: user.username,
      name: user.name,
      phone: user.phone,
      email: user.email
    });
  } catch (error) {
    console.error('获取用户信息错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

// 更新用户信息
const updateUserInfo = async (req, res) => {
  try {
    // 这里应该从请求中获取用户ID（实际项目中使用JWT）
    const userId = 1; // 暂时使用默认管理员ID
    const { name, phone, email } = req.body;
    
    const user = await User.findByPk(userId);
    
    if (!user) {
      return res.status(404).json({ message: '用户不存在' });
    }
    
    // 更新用户信息
    await user.update({ name, phone, email });
    
    res.status(200).json({
      message: '更新成功',
      user: {
        id: user.id,
        username: user.username,
        name: user.name,
        phone: user.phone,
        email: user.email
      }
    });
  } catch (error) {
    console.error('更新用户信息错误:', error);
    res.status(500).json({ message: '服务器错误' });
  }
};

module.exports = {
  login,
  getUserInfo,
  updateUserInfo
};
