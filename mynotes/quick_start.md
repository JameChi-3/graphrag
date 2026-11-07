# 快速开始任务

## 执行索引任务

执行命令
```shell
graphrag index
```

==**初次实验一定需要 将索引的文档吗一定是 文本量很少的,  这个过程非常消耗 tokens**==

## 存在问题记录

```log
(graphrag) PS D:\workspace\source\graphrag> graphrag.exe  index  
Starting pipeline with workflows: load_input_documents, create_base_text_units, create_final_documents, extract_graph, finalize_graph, extract_covariates, create_communities, create_final_text_units, create_community_reports, generate_text_embeddings
Starting workflow: load_input_documents

Workflow complete: load_input_documents
Starting workflow: create_base_text_units
  1 / 1 ............................................................................................
Workflow complete: create_base_text_units
Starting workflow: create_final_documents

Workflow complete: create_final_documents
Starting workflow: extract_graph
  9 / 9 ............................................................................................
Workflow complete: extract_graph
Starting workflow: finalize_graph

Workflow complete: finalize_graph
Starting workflow: extract_covariates

Workflow complete: extract_covariates
Starting workflow: create_communities

Workflow complete: create_communities
Starting workflow: create_final_text_units

Workflow complete: create_final_text_units
Starting workflow: create_community_reports
Pipeline error: 'community'.........................................................................
Pipeline complete
```

==🔴在 community  这里发生了失败==
