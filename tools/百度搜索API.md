



百度搜索（BaiduSearch）是一项利用百度搜索引擎查找相关信息的组件，它会直接输出用户的搜索内容。当前组件已升级，可支持API调用或在工作流Agent中使用。

认证鉴权

调用此工具需使用百度千帆 API Key 鉴权，请前往创建或获取

```plaintext
Authorization: Bearer <YOUR_API_Key>
```

## 在线调试

百度智能云千帆提供了 [API在线调试平台 ](https://console.bce.baidu.com/support/?u=bce-head#/api?product=QIANFAN\&project=%E5%8D%83%E5%B8%86AppBuilder\&parent=%E7%BB%84%E4%BB%B6)，平台集成了快速检索、查看开发文档、查看在线调用的请求内容和返回结果、复制和下载示例代码等功能，帮助开发者快速调试接口。

## 接口定义

| URL           | /v2/ai\_search/web\_search         |
| ------------- | ---------------------------------- |
| Method        | POST                               |
| Content-Type  | application/json                   |
| Authorization | 请求签名(Bearer \<AppBuilder API Key>) |

### 请求结构

```plaintext
POST /v2/ai_search/web_search HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <AppBuilder API Key>
Content-Type: application/json
{
  "messages": [
    {
      "content": "北京有哪些旅游景区",
      "role": "user"
    }
  ],
  "search_source": "baidu_search_v2",
  "resource_type_filter": [{"type": "web","top_k": 20}],
  "search_filter": {
    "match": {
      "site": [
        "www.weather.com.cn"
      ]
    }
  },
  "search_recency_filter": "year"
}
```

## 请求参数

### header参数

除公共头域外，无其它特殊头域。

### body参数

| **参数名称**                | **数据类型**               | **是否必须** | **描述**                                                                                                                                                                                                                                                                                                                 |
| ----------------------- | ---------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| messages                | array\<Message>        | 是        | 搜索输入；&#xA;array的长度需要是奇数, role必须是user-assistant-user交替，以user开始以user结束;在百度搜索时，仅支持单轮输入，若传入多轮输入，则以用户传入最后的content为输入查询。                                                                                                                                                                                                     |
| edition                 | string                 | 否        | 搜索版本。默认为standard。&#xA;可选值：&#xA;standard：完整版本。&#xA;lite：标准版本，对召回规模和精排条数简化后的版本，时延表现更好，效果略弱于完整版。                                                                                                                                                                                                                          |
| search\_source          | string                 | 否        | 使用的搜索引擎版本；&#xA;固定值：baidu\_search\_v2                                                                                                                                                                                                                                                                                   |
| resource\_type\_filter  | array\<SearchResource> | 否        | 支持设置网页、视频、图片、阿拉丁搜索模态，网页top\_k最大取值为50，视频top\_k最大为10，图片top\_k最大为30，阿拉丁top\_k最大为5，默认值为：&#xA;\[{"type": "web","top\_k": 20},{"type": "video","top\_k": 0},{"type": "image","top\_k": 0},{"type": "aladdin","top\_k": 0}]&#xA;使用阿拉丁时注意：&#xA;1\. 阿拉丁不支持站点、时效过滤。&#xA;2\. 建议搭配网页模态使用，增加搜索返回数量。&#xA;3\. 阿拉丁的返回参数为beta版本，后续可能变更。 |
| search\_filter          | SearchFilter           | 否        | 根据SearchFilter下的子条件做检索过滤，使用方式参考 SearchFilter表详情 。                                                                                                                                                                                                                                                                      |
| block\_websites         | array\<string>         | 否        | 需要屏蔽的站点列表。过滤站点列表中属于该站点与该站点下子站点的搜索结果，为保证最终返回的结果数量，可能会引起时延的增长。&#xA;示例：\["tieba.baidu.com"]                                                                                                                                                                                                                               |
| search\_recency\_filter | string                 | 否        | 根据网页发布时间进行筛选。枚举值:&#xA;week:最近7天&#xA;month：最近30天&#xA;semiyear：最近180天&#xA;year：最近365天                                                                                                                                                                                                                                    |

**Message对象**

| **参数名称** | **数据类型** | **是否必须** | **描述**                                                                                                 |
| -------- | -------- | -------- | ------------------------------------------------------------------------------------------------------ |
| role     | string   | 是        | 角色设定，可选值：&#xA;user：用户&#xA;assistant：模型                                                                 |
| content  | string   | 是        | content为文本时, 对应对话内容，即用户的query问题。说明：&#xA;1.不能为空。&#xA;2.多轮对话中，用户最后一次输入content不能为空字符，如空格、"\n"、“\r”、“\f”等。 |

**SearchResource对象**

| **参数名称** | **数据类型** | **是否必须** | **描述**                                                           |
| -------- | -------- | -------- | ---------------------------------------------------------------- |
| type     | string   | 是        | 搜索资源类型。可选值：&#xA;web：网页&#xA;video：视频&#xA;image：图片&#xA;aladdin：阿拉丁 |
| top\_k   | int      | 是        | 指定模态最大返回个数。                                                      |

**SearchFilter**

| **参数名称**     | **数据类型**       | **是否必须** | **描述**                                                                              |
| ------------ | -------------- | -------- | ----------------------------------------------------------------------------------- |
| match        | object         | 否        | 条件查询。                                                                               |
| + site       | array\<string> | 否        | 支持设置指定站点的搜索条件，即仅在设置的站点中进行内容搜索。目前支持设置20个站点。示例：\["tieba.baidu.com"]                   |
| range        | object         | 否        | 范围查询，参考 范围查询(range) 详情。                                                             |
| + page\_time | object         | 否        | 假设下述的now时间是2024-07-16。                                                              |
| ++ gte       | string         | 否        | 时间查询参数，大于或等于。"now-1w/d"，2024-07-16前一周、向下做舍入，即大于2024-07-09 00:00:00，包含2024-07-09完整天。 |
| ++ gt        | string         | 否        | 时间查询参数，大于。"now-1w/d"，2024-07-16前一周、向上做舍入，即大于2024-07-09 23:59:59，不包含2024-07-09完整天。   |
| ++ lte       | string         | 否        | 时间查询参数，小于或等于。"now-1w/d"，2024-07-16前一周、向上做舍入，即小于2024-07-09 23:59:59，包含2024-07-09完整天。 |
| ++ lt        | string         | 否        | 时间查询参数，小于。"now-1w/d"，2024-07-16前一周、向下做舍入，即小于2024-07-09 00:00:00，不包含2024-07-09完整天。   |

**范围查询(range)**

可以用于数值型、日期型的字段。语法格式如下：

```plaintext
"range": {
     "{field}": {
          "gte": "{lowerBound}",
          "gt": "{lowerBound}",
          "lte": "{upperBound}",
          "lt": "{upperBound}"
       }
  }
```

**实体(field)**

pageTime：发布时间的实体名，表示针对pageTime做范围查询。此处pageTime对应响应数据中的page\_time字段。 **网页发布时间的筛选功能只适用于可利用与可展现库，其他结果如视频等不召回。**

**查询范围(lowerBound\upperBound)**

支持的时间单位：y（年）、M（月）、w（周）、d（日）。目前提供如下固定套餐，其他值非法。其中，"now"表示当前时间，在now后可以添加数学表达式：“-1w”表示减1周；“-1M”表示减1月；“-1y”表示减1年；“/d”表示归一化到当前天的起始\结束时间。

```plaintext
- now/d
- now-1w/d：一周
- now-2w/d：两周
- now-1M/d：一个月
- now-3M/d：三个月
- now-6M/d：六个月
- now-1y/d：一年
```

**参数限制说明**

1. lte使用注意：range范围会参与检索系统的cache key计算，lte在做向上归一舍入后，由于cache可能导致结果时效性落后于match指定的lte值。

2. 起始(lowerBound)和截止（upperBound）时间必需同时存在，否则该功能不生效。

3. gte和gt只传其中一个即可，都传只生效gt；lte和lt只传其中一个即可，都传只生效lt。

**示例**

查询当天前7天(不含当天)发布的网页结果：

```plaintext
"query": {
    "filter": { 
         "range": {
             "page_time": {
                 "gte": "now-1w/d"
                 "lt": "now/d"
              }
         }
     }
}
```

## 响应头域

除公共头域外，无其它特殊头域。

## 响应参数

| **参数名称**    | **数据类型**          | **描述**                     |
| ----------- | ----------------- | -------------------------- |
| request\_id | string            | 请求ID。                      |
| code        | string            | 错误码，当发生异常时返回。              |
| message     | string            | 错误消息，当发生异常时返回。             |
| references  | array\<Reference> | 模型回答详情列表，参考Reference对象表详情。 |

**Reference对象**

| **参数名称**         | **数据类型**      | **描述**                                                                |
| ---------------- | ------------- | --------------------------------------------------------------------- |
| icon             | string        | 网站图标地址。                                                               |
| id               | int           | 引用编号1、2、3。                                                            |
| title            | string        | 网页标题。                                                                 |
| url              | string        | 网页地址。                                                                 |
| web\_anchor      | string        | 网站锚文本或网站标题。                                                           |
| website          | string        | 站点名称。                                                                 |
| content          | string        | 网页内容，显示2000字以内的相关信息原文片段                                               |
| rerank\_score    | float         | 原文片段相关性评分（仅type值为web、video、image时存在），取值范围\[0,1]，数值越大越相关               |
| authority\_score | float         | 网页权威性评分（仅type值为web时存在），取值范围\[0,1]，数值越大越权威                             |
| date             | string        | 网页日期。                                                                 |
| type             | string        | 检索资源类型。返回值：&#xA;web:网页&#xA;video:视频内容&#xA;image：图片&#xA;aladdin：阿拉丁    |
| image            | ImageDetail   | 图片详情。                                                                 |
| video            | VideoDetail   | 视频详情。                                                                 |
| is\_aladdin      | boolean       | 是否为阿拉丁内容。                                                             |
| aladdin          | Object        | 阿拉丁详细内容， [参考文档 ](https://cloud.baidu.com/doc/AppBuilder/s/xmewx15yi)。 |
| web\_extensions  | WebExtensions | 网页相关图片                                                                |

**Reference.ImageDetail对象**

| **参数名称** | **数据类型** | **描述** |
| -------- | -------- | ------ |
| url      | string   | 图片链接。  |
| height   | string   | 图片高度。  |
| width    | string   | 图片宽度。  |

**Reference.VideoDetail对象**

| **参数名称**   | **数据类型** | **描述**        |
| ---------- | -------- | ------------- |
| url        | string   | 视频链接。         |
| height     | string   | 视频高度。         |
| width      | string   | 视频宽度。         |
| size       | string   | 视频大小，单位Bytes。 |
| duration   | string   | 视频长度，单位秒。     |
| hover\_pic | string   | 视频封面图。        |

**Reference.WebExtensions**

| **参数名称**           | **数据类型**      | **描述** |
| ------------------ | ------------- | ------ |
| images             | array\<Image> | 网页相关图片 |
| +images\[0].url    | string        | 图片链接   |
| +images\[0].height | string        | 图片高度   |
| +images\[0].width  | string        | 图片宽度   |

## 请求curl 示例

```plaintext
 curl --location 'https://qianfan.baidubce.com/v2/ai_search/web_search' \
--header 'X-Appbuilder-Authorization: Bearer <AppBuilder API Key>' \
--header 'Content-Type: application/json' \
--data '{
  "messages": [
    {
      "content": "河北各个城市最近的天气",
      "role": "user"
    }
  ],
  "search_source": "baidu_search_v2",
  "resource_type_filter": [{"type": "web","top_k": 10}],
  "search_filter": {
    "match": {
      "site": [
        "www.weather.com.cn"
      ]
    }
  },
  "search_recency_filter": "year"
}'
```

## 正确响应示例

```plaintext
{
    "references": [
        {
            "content": "河北天气预报,及时准确发布中央气象台天气信息,便捷查询河北今日天气\u0004,河北周末天气,河北一周天气预报,河北蓝天预报,河北天气预报,河北40日天气预报,还\u0005提供河北的生活指数、健康指数、交通...",
            "date": "2025-04-27 18:02:00",
            "icon": null,
            "id": 1,
            "image": null,
            "title": "【河北天气】河北天气预报,蓝天,蓝天预报,雾霾,雾霾...",
            "type": "web",
            "url": "https://www.weather.com.cn/html/weather/101031600.shtml",
            "video": null,
            "web_anchor": "【河北天气】河北天气预报,蓝天,蓝天预报,雾霾,雾霾..."
        },
        {
            "content": "保定天气预报,及时准确发布中央气象台天气信息,便捷查询保定今日天气,保定周末天气,保定一周天气预报,保定蓝天预报,保定天气预报,保定40日天气预报,还提供保定的生活指数、健康指数、交通...",
            "date": "2025-05-20 11:58:00",
            "icon": null,
            "id": 2,
            "image": null,
            "title": "保定天气预报,保定7天天气预报,保定15天天气预报,保定...",
            "type": "web",
            "url": "https://www.weather.com.cn/weather/101090201.shtml",
            "video": null,
            "web_anchor": "保定天气预报,保定7天天气预报,保定15天天气预报,保定..."
        },
        {
            "content": "河北省气象台2025年05月23日11时发布天气预报: 今天下午到夜间,保定西部、石家庄西部、邢台西部阴有小雨或零星小雨转晴,其他地区阴转晴。最高气温,张家口、承德北部、保定西北部13～17...",
            "date": "2025-05-23 00:00:00",
            "icon": null,
            "id": 3,
            "image": null,
            "title": "今天西部部分地区仍有降水 其它地区阴转晴-河北首页...",
            "type": "web",
            "url": "http://hebei.weather.com.cn/tqxs/4190923_m.shtml",
            "video": null,
            "web_anchor": "今天西部部分地区仍有降水 其它地区阴转晴-河北首页..."
        },
        {
            "content": "河北省气象台2025年05月22日05时发布天气预报 今天白天,保定、廊坊及以北地区阴有小雨或阵雨,其中张家口、保定西北部有中到大雨;其他地区多云转阴有小雨或阵雨,其中邯郸大部有中雨。...",
            "date": "2025-05-22 09:07:22",
            "icon": null,
            "id": 4,
            "image": null,
            "title": "今天白天到夜间,我省大部分地区有降水-河北首页-中国...",
            "type": "web",
            "url": "http://hebei.weather.com.cn/tqxs/4189523_m.shtml",
            "video": null,
            "web_anchor": "今天白天到夜间,我省大部分地区有降水-河北首页-中国..."
        }
    ],
    "request_id": "ca749cb1-26db-4ff6-9735-f7b472d59003"
}
```

## 错误响应示例

```plaintext
{
    "requestId": "00000000-0000-0000-0000-000000000000",
    "code": 216003,
    "message": "Authentication error: ( [Code: InvalidHTTPAuthHeader; Message: Fail to parse apikey authorization; RequestId: ea6ffeca-a136-401b-ba30-61c910c02ead] )"
}
```

## 错误码

| 错误码 | 描述                                                                     |
| --- | ---------------------------------------------------------------------- |
| 400 | 客户端请求参数错误。                                                             |
| 500 | 服务端执行错误。                                                               |
| 501 | 调用模型服务超时。                                                              |
| 502 | 模型流式输出超时。                                                              |
| 其它  | 详见 [模型返回错误码 ](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/tlmyncueh)。 |
