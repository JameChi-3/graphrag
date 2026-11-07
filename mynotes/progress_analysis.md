# 过程分析

## index 的 workflow

### **index 代码解析**

graphrag index 的执行流程

standard模式的流程

从代码[factory.py](../packages/graphrag/graphrag/index/workflows/factory.py)中可以看到这些流程
```python
_standard_workflows = [
    "create_base_text_units",
    "create_final_documents",
    "extract_graph",
    "finalize_graph",
    "extract_covariates",
    "create_communities",
    "create_final_text_units",
    "create_community_reports",
    "generate_text_embeddings",

]

PipelineFactory.register_pipeline(
    IndexingMethod.Standard, ["load_input_documents", *_standard_workflows]
)
```

查看从名称到对应代码的映射 从代码[\_\_init__.py](../packages/graphrag/graphrag/index/workflows/__init__.py) 

```python
# register all of our built-in workflows at once

PipelineFactory.register_all({  # noqa: RUF067
    "load_input_documents": run_load_input_documents,
    "load_update_documents": run_load_update_documents,
    "create_base_text_units": run_create_base_text_units,
    "create_communities": run_create_communities,
    "create_community_reports_text": run_create_community_reports_text,
    "create_community_reports": run_create_community_reports,
    "extract_covariates": run_extract_covariates,
    "create_final_documents": run_create_final_documents,
    "create_final_text_units": run_create_final_text_units,
    "extract_graph_nlp": run_extract_graph_nlp,
    "extract_graph": run_extract_graph,
    "finalize_graph": run_finalize_graph,
    "generate_text_embeddings": run_generate_text_embeddings,
    "prune_graph": run_prune_graph,
    "update_final_documents": run_update_final_documents,
    "update_text_embeddings": run_update_text_embeddings,
    "update_community_reports": run_update_community_reports,
    "update_entities_relationships": run_update_entities_relationships,
    "update_communities": run_update_communities,
    "update_covariates": run_update_covariates,
    "update_text_units": run_update_text_units,
    "update_clean_state": run_update_clean_state,
})
```

### 提取图结构

对应的注册步骤是
`"extract_graph`

### 
