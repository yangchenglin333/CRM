#!/bin/bash
# CRM项目启动脚本

CRM_PATH="/Users/admin/Desktop/test-management-platform 2/CRM项目"
cd "$CRM_PATH"

# 启动后端服务
npm start &
BACKEND_PID=$!

echo "CRM服务已启动"
echo "前端页面: http://localhost:3000/CRM.html"
echo "Swagger文档: http://localhost:3000/swagger.html"
echo "后端API: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待退出
wait $BACKEND_PID