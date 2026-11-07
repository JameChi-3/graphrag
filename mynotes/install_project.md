# 开始步骤 

## **clone code**
```shell
git clone https://github.com/microsoft/graphrag.git
```

## **init env**

```shell
uv venv --python 3.12
uv sync
cd .\packages\graphrag\ 
uv sync
```

## **初始化配置文件**

```shell
graphrag init
```

## **修改配置文件**

```yaml
completion_models:
  default_completion_model:
    model_provider: deepseek
    api_base: https://api.deepseek.com
    # auth_type: api_key
    # api_key: ${GRAPHRAG_API_KEY}
    model: deepseek-flash
    auth_method: api_key # or azure_managed_identity
    api_key: ${GRAPHRAG_API_KEY} # set this in the generated .env file, or remove if managed identity
    retry:
      type: exponential_backoff

  
embedding_models:
  default_embedding_model:
    model_provider: ollama
    model: embeddinggemma-2:440m
    auth_method: api_key
    api_key: as
    retry:
      type: exponential_backoff
```

