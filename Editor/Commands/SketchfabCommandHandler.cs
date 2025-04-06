using UnityEngine;
using UnityEditor;
using Newtonsoft.Json.Linq;
using System;

namespace UnityMCP.Editor.Commands
{
    /// <summary>
    /// 处理 Sketchfab 相关的命令
    /// </summary>
    public static class SketchfabCommandHandler
    {
        /// <summary>
        /// 从 Sketchfab 搜索并下载模型
        /// </summary>
        /// <param name="params">包含搜索参数的对象</param>
        /// <returns>操作结果</returns>
        public static object ImportSketchfabModel(JObject @params)
        {
            try
            {
                // 提取参数
                string keyword = (string)@params["keyword"] ?? throw new Exception("Parameter 'keyword' is required.");
                
                // 创建默认的边界框
                Bounds targetBounds = new Bounds(Vector3.zero, Vector3.one * 2);
                
                // 如果提供了边界框参数
                if (@params["bounds"] != null)
                {
                    JObject boundsObj = (JObject)@params["bounds"];
                    Vector3 center = new Vector3(
                        (float)boundsObj["centerX"], 
                        (float)boundsObj["centerY"], 
                        (float)boundsObj["centerZ"]
                    );
                    Vector3 size = new Vector3(
                        (float)boundsObj["sizeX"], 
                        (float)boundsObj["sizeY"], 
                        (float)boundsObj["sizeZ"]
                    );
                    targetBounds = new Bounds(center, size);
                }

                // 查找场景中已有的 SketchfabManager，如果没有则创建一个
                SketchfabManager manager = UnityEngine.Object.FindObjectOfType<SketchfabManager>();

                manager.searchKeyword = keyword;
                manager.targetBounds = targetBounds;
                
                // 调用 SearchModels 方法
                manager.SearchModels(keyword, targetBounds);
                
                return new {
                    message = $"正在从 Sketchfab 搜索并下载关键词为 '{keyword}' 的模型",
                    status = "searching"
                };
            }
            catch (Exception ex)
            {
                Debug.LogError($"导入 Sketchfab 模型失败: {ex.Message}\n{ex.StackTrace}");
                return new {
                    message = $"导入 Sketchfab 模型失败: {ex.Message}",
                    error = ex.Message,
                    status = "error"
                };
            }
        }
    }
}