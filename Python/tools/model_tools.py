import logging
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
        bounds: Optional[Dict[str, float]] = None
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
            params: Dict[str, Any] = {
                "keyword": keyword,
            }
            
            # 添加可选参数
            if bounds:
                params["bounds"] = bounds
            
            # 发送命令到 Unity
            connection = get_unity_connection()
            response = connection.send_command("IMPORT_SKETCHFAB_MODEL", params)
            
            if response and response.get("success", False):
                return response.get("message", "is searching model...")
            else:
                error_msg = response.get("message", "unknown error")
                return f"import sketch fab model error: {error_msg}"
                
        except Exception as e:
            logger.error(f"Sketchfab 模型导入错误: {str(e)}")
            return f"导入过程中发生错误: {str(e)}"