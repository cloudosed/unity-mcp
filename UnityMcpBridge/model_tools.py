import logging
import time
from mcp.server.fastmcp import Context
from typing import Dict, Optional, Any
from unity_connection import get_unity_connection

# 配置日志
logger = logging.getLogger("UnityMCP")

def register_model_tools(mcp):
    """Register all model-related tools with MCP."""
    
    @mcp.tool()
    def import_sketchfab_model(
        ctx: Context,
        keyword: str,
        bounds: Dict[str, float],
        max_retries: int = 10  # 最多尝试20次，约30秒
    ) -> str:
        """ search and import models from Sketchfab into Unity.
        
        Args:
            ctx: MCP context
            keyword: keywords for searching models (e.g., "car", "tree")
            bounds: parameters for bounding box (optional), e.g., {"centerX": -10, "centerY": 10, "centerZ": 0, "sizeX": 1, "sizeY": 1, "sizeZ": 1}
            
        Returns:
            str: 操作结果信息
        """
        try:
            # 构建参数
            if not bounds:
                raise ValueError("参数 'bounds' 是必须的，不能为 None 或空值。")
            
            # 构建参数
            params: Dict[str, Any] = {
                "keyword": keyword,
                "bounds": bounds,
            }
            
            # 发送命令到 Unity
            connection = get_unity_connection()
            response = connection.send_command("IMPORT_SKETCHFAB_MODEL", params)
            
            if not response or not response.get("success", False):
                error_msg = response.get("message", "unknown error") if response else "没有收到响应"
                return f"import sketch fab model error: {error_msg}"
            
            # 获取请求的任务ID
            task_id = response.get("taskId")
            if not task_id:
                return "模型导入已启动，但无法追踪进度（未返回任务ID）"
                
            # 每3秒检查一次模型创建状态
            retries = 0
            while retries < max_retries:
                time.sleep(3)  # 等待3秒
                
                # 检查模型创建状态
                check_params = {"taskId": task_id}
                status_response = connection.send_command("CHECK_SKETCHFAB_IMPORT_STATUS", check_params)
                
                if status_response and status_response.get("success", False):
                    if status_response.get("completed", False):
                        model_info = status_response.get("modelInfo", {})
                        return f"模型导入成功! 模型名称: {model_info.get('name', '未知')}"
                    else:
                        # 继续检查
                        progress = status_response.get("progress", 0)
                        logger.info(f"模型导入进度: {progress}%")
                
                retries += 1
            
            return "模型导入已启动，但未在预期时间内完成。请在Unity中检查导入状态。"
                
        except Exception as e:
            logger.error(f"Sketchfab 模型导入错误: {str(e)}")
            return f"导入过程中发生错误: {str(e)}"