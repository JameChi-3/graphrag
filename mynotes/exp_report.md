# 实验记录

## 测试文本

将下面的文本放到工程的根目录下的 `input/book.txt`

```txt
A 和 B 今天早上一起出去玩
B 和 C 今天晚上一起吃饭
A 和 C 是同事
```

## 执行测试

运行命令
```shell
graphrag index
```

## extract_graph

执行代码在:
[graph_extractor.py](../packages/graphrag/graphrag/index/operations/extract_graph/graph_extractor.py)的`GraphExtractor`类

我们这里记录 extract_graph 的流程
核心代码函数 `_process_document`

**记录日志**：

[extract_graph log](./details/indexing-engine.extract_graph.1.log)

对应的代码在[extract_graph.py](../packages/graphrag/graphrag/index/workflows/extract_graph.py)

### 调用阶段1: 提取关系图

在[extract_graph.py](../packages/graphrag/graphrag/index/workflows/extract_graph.py)里面调用的代码段如下

```python
extracted_entities, extracted_relationships = await extractor(
    text_units=text_units,
    callbacks=callbacks,
    text_column="text",
    id_column="id",
    model=extraction_model,
    prompt=extraction_prompt,
    entity_types=entity_types,
    max_gleanings=max_gleanings,
    num_threads=extraction_num_threads,
    async_type=extraction_async_type,
)
```

实施处理是在代码[graph_extractor.py里的GraphExtractor类](../packages/graphrag/graphrag/index/operations/extract_graph/graph_extractor.py)

#### 初次开始提取

[prompt template](../prompts/extract_graph.txt)

从上述的prompt上面看到了两个格式化选项:

| 内容 | 说明 |
| ---- | ----- |
| entity_types | 需要提取的实体类型  |
| input_text | 输入的待提取的文本内容 |

**输出的答案**:

```txt
("entity"<|>A<|>PERSON<|>A is a person who went out with B this morning and is a colleague of C)
##
("entity"<|>B<|>PERSON<|>B is a person who went out with A this morning and had dinner with C tonight)
##
("entity"<|>C<|>PERSON<|>C is a person who had dinner with B tonight and is a colleague of A)
##
("relationship"<|>A<|>B<|>A and B went out together this morning<|>5)
##
("relationship"<|>B<|>C<|>B and C had dinner together tonight<|>5)
##
("relationship"<|>A<|>C<|>A and C are colleagues<|>8)
<|COMPLETE|>
```

#### 继续进行补充的审核，补全输出

这时候在就会追加 prompt, 起到了 verify and reflect 的作用 

```python
CONTINUE_PROMPT = "MANY entities and relationships were missed in the last extraction. Remember to ONLY emit entities that match any of the previously extracted types. Add them below using the same format:\n"
```

#### 判断是否需要继续进行提取

追加Promt继续进行提取


```python
LOOP_PROMPT = "It appears some entities and relationships may have still been missed. Answer Y if there are still entities or relationships that need to be added, or N if there are none. Please answer with a single letter Y or N.\n"
```

输出Y表示继续，N表示不要继续

### 调用阶段2：对 对 entities 和 relationships 进行合并

在[extract_graph.py](..\packages\graphrag\graphrag\index\operations\extract_graph\extract_graph.py)中的`extract_graph`函数中调用表示合并

```python
entities = _merge_entities(entity_dfs)
relationships = _merge_relationships(relationship_dfs)
relationships = filter_orphan_relationships(relationships, entities)
```

### 调用阶段3: 对提取图进行总结

在[extract_graph.py](../packages/graphrag/graphrag/index/workflows/extract_graph.py)里面调用的代码段如下

```python
entities, relationships = await get_summarized_entities_relationships(
    extracted_entities=extracted_entities,
    extracted_relationships=extracted_relationships,
    callbacks=callbacks,
    model=summarization_model,
    max_summary_length=max_summary_length,
    max_input_tokens=max_input_tokens,
    summarization_prompt=summarization_prompt,
    num_threads=summarization_num_threads,
)
```

具体实施代码在[description_summary_extractor.py的SummarizeExtractor类](../packages/graphrag/graphrag/index/operations/summarize_descriptions/description_summary_extractor.py)


如果单个 entity 或 relationships 存在多个 description, 就需要调用 summary

