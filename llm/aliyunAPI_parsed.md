> 模型介绍、选型建议和使用方法请参考[文本生成模型概述](https://help.aliyun.com/zh/model-studio/text-generation)。

可通过 OpenAI 兼容或 DashScope 协议调用通义千问 API。

## OpenAI 兼容

北京地域

新加坡地域

金融云

__

__

SDK 调用配置的`base_url`：`https://dashscope.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

SDK 调用配置的`base_url`：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`

SDK 调用配置的`base_url`：`https://dashscope-finance.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope-finance.aliyuncs.com/compatible-mode/v1/chat/completions`

> 您需要先[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过OpenAI SDK进行调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

### 请求体

|  POST /chat/completions 调试

### OpenAI 兼容接口在线调试

× 中国大陆（北京）  国际（新加坡）  POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions API Key Bearer Token [获取中国大陆（北京）地域 API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 请求体 默认 深度思考 图像输入 工具调用 结构化输出 { "model": "qwen-plus", "messages": [ { "role": "system", "content": "You are a helpful assistant." }, { "role": "user", "content": "你是谁？" } ] } 发送请求  清空响应  响应结果 原始响应 解析内容 文本输入流式输出图像输入视频输入工具调用联网搜索异步调用文档理解 --- PythonJavaNode.jsGoC#（HTTP）PHP（HTTP）curl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ]
)
print(completion.model_dump_json())
```
  ---
```java
// 该代码 OpenAI SDK 版本为 2.6.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .addUserMessage("你是谁")
                .model("qwen-plus")
                .build();

        try {
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            System.out.println(chatCompletion);
        } catch (Exception e) {
            System.err.println("Error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",  //此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "你是谁？" }
        ],
    });
    console.log(JSON.stringify(completion))
}

main();
```
  ---
```go
package main

import (
	"context"
	"os"

	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"
)

func main() {
	client := openai.NewClient(
		option.WithAPIKey(os.Getenv("DASHSCOPE_API_KEY")),
		option.WithBaseURL("https://dashscope.aliyuncs.com/compatible-mode/v1"),
	)
	chatCompletion, err := client.Chat.Completions.New(
		context.TODO(), openai.ChatCompletionNewParams{
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.UserMessage("你是谁"),
			},
			Model: "qwen-plus",
		},
	)

	if err != nil {
		panic(err.Error())
	}

	println(chatCompletion.Choices[0].Message.Content)
}
```
  ---
```csharp
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
            return;
        }

        // 设置请求 URL 和内容
        string url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
        // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        string jsonContent = @"{
            ""model"": ""qwen-plus"",
            ""messages"": [
                {
                    ""role"": ""system"",
                    ""content"": ""You are a helpful assistant.""
                },
                {
                    ""role"": ""user"",
                    ""content"": ""你是谁？""
                }
            ]
        }";

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```
  ---
```php
<?php
// 设置请求的URL
$url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
// 若没有配置环境变量，请用百炼API Key将下行替换为：$apiKey = "sk-xxx";
$apiKey = getenv('DASHSCOPE_API_KEY');
// 设置请求头
$headers = [
    'Authorization: Bearer '.$apiKey,
    'Content-Type: application/json'
];
// 设置请求体
$data = [
    // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    "model" => "qwen-plus",
    "messages" => [
        [
            "role" => "system",
            "content" => "You are a helpful assistant."
        ],
        [
            "role" => "user",
            "content" => "你是谁？"
        ]
    ]
];
// 初始化cURL会话
$ch = curl_init();
// 设置cURL选项
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
// 执行cURL会话
$response = curl_exec($ch);
// 检查是否有错误发生
if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
}
// 关闭cURL资源
curl_close($ch);
// 输出响应结果
echo $response;
?>
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ]
}'
```


> 相关文档：[流式输出](https://help.aliyun.com/zh/model-studio/stream)。

PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '你是谁？'}],
    stream=True,
    stream_options={"include_usage": True}
    )
for chunk in completion:
    print(chunk.model_dump_json())
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus", // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你是谁？"}
        ],
        stream: true,
        stream_options: {include_usage: true}
    });
    for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
    }
}

main();
```
  ---
```curl
curl --location "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream":true,
    "stream_options": {
        "include_usage": true
    }
}'
```


> 相关文档：[视觉理解](https://help.aliyun.com/zh/model-studio/vision)。

PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-vl-plus",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{"role": "user","content": [
            {"type": "image_url",
             "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}},
            {"type": "text", "text": "这是什么"},
            ]}]
    )
print(completion.model_dump_json())
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen-vl-max", // 此处以qwen-vl-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [{role: "user",content: [
            { type: "image_url",image_url: {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}},
            { type: "text", text: "这是什么？" },
        ]}]
    });
    console.log(JSON.stringify(response));
}

main();
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen-vl-plus",
  "messages": [{
      "role": "user",
      "content": [
       {"type": "image_url","image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}},
       {"type": "text","text": "这是什么"}
       ]}]
}'
```


> 以下示例展示了如何将图片列表作为视频输入。如需使用视频文件等其他方式，请参阅“[视觉理解](https://help.aliyun.com/zh/model-studio/vision#80dbf6ca8fh6s)。

PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen-vl-max-latest",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "video",
                "video": [
                    "https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                    "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                    "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                    "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"]
            },
            {
                "type": "text",
                "text": "描述这个视频的具体过程"
            }]}]
)
print(completion.model_dump_json())
```
  ---
```nodejs
// 确保之前在 package.json 中指定了 "type": "module"
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        // 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model: "qwen-vl-max-latest",
        messages: [{
            role: "user",
            content: [
                {
                    type: "video",
                    video: [
                        "https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"
                    ]
                },
                {
                    type: "text",
                    text: "描述这个视频的具体过程"
                }
        ]}]
    });
    console.log(JSON.stringify(response));
}

main();
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen-vl-max-latest",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "video",
                    "video": [
                        "https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"
                    ]
                },
                {
                    "type": "text",
                    "text": "描述这个视频的具体过程"
                }
            ]
        }
    ]
}'
```


> 相关文档：[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)

PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # 因为获取当前时间无需输入参数，因此parameters为空字典
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    # 查询天气时需要提供位置，因此参数设置为location
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
messages = [{"role": "user", "content": "杭州天气怎么样"}]
completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    tools=tools
)

print(completion.model_dump_json())
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

const messages = [{"role": "user", "content": "杭州天气怎么样"}];
const tools = [
// 工具1 获取当前时刻的时间
{
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "当你想知道现在的时间时非常有用。",
        // 因为获取当前时间无需输入参数，因此parameters为空
        "parameters": {}
    }
},
// 工具2 获取指定城市的天气
{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "当你想查询指定城市的天气时非常有用。",
        "parameters": {
            "type": "object",
            "properties": {
                // 查询天气时需要提供位置，因此参数设置为location
                "location": {
                    "type": "string",
                    "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                }
            },
            "required": ["location"]
        }
    }
}
];

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen-plus", // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: messages,
        tools: tools,
    });
    console.log(JSON.stringify(response));
}

main();
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "杭州天气怎么样"
        }
    ],
    "tools": [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location":{
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
  ]
}'
```
  PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '中国队在巴黎奥运会获得了多少枚金牌'}],
    extra_body={
        "enable_search": True
    }
    )
print(completion.model_dump_json())
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus", //此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "中国队在巴黎奥运会获得了多少枚金牌" }
        ],
        enable_search:true
    });
    console.log(JSON.stringify(completion))
}

main();
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "中国队在巴黎奥运会获得了多少枚金牌"
        }
    ],
    "enable_search": true
}'
```
  ---
```python
import os
import asyncio
from openai import AsyncOpenAI
import platform

client = AsyncOpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

async def main():
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": "你是谁"}],
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    )
    print(response.model_dump_json())

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
```


> 当前仅qwen-long模型支持对文档进行分析，详细用法请参见[长上下文（Qwen-Long）](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)。

PythonJavaNode.jscurl --- ---
```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
file_object = client.files.create(file=Path("百炼系列手机产品介绍.docx"), purpose="file-extract")
completion = client.chat.completions.create(
    model="qwen-long",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': f'fileid://{file_object.id}'},
        {'role': 'user', 'content': '这篇文章讲了什么？'}
    ]
)
print(completion.model_dump_json())
```
  ---
```java
// 建议OpenAI SDK的版本 >= 0.32.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.files.FileCreateParams;
import com.openai.models.files.FileObject;
import com.openai.models.files.FilePurpose;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        // 设置文件路径
        Path filePath = Paths.get("百炼系列手机产品介绍.docx");
        // 创建文件上传参数
        FileCreateParams fileParams = FileCreateParams.builder()
                .file(filePath)
                .purpose(FilePurpose.of("file-extract"))
                .build();

        // 上传文件
        FileObject fileObject = client.files().create(fileParams);
        String fileId = fileObject.id();

        // 创建聊天请求
        ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
                .addSystemMessage("fileid://" + fileId)
                .addUserMessage("这篇文章讲了什么？")
                .model("qwen-long")
                .build();

        // 发送请求并获取响应
        ChatCompletion chatCompletion = client.chat().completions().create(chatParams);

        // 打印响应结果
        System.out.println(chatCompletion);
    }
}
```
  ---
```nodejs
import fs from "fs";
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function getFileID() {
    const fileObject = await openai.files.create({
        file: fs.createReadStream("百炼系列手机产品介绍.docx"),
        purpose: "file-extract"
    });
    return fileObject.id;
}

async function main() {
    const fileID = await getFileID();
    const completion = await openai.chat.completions.create({
        model: "qwen-long",  //模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: "system", content: `fileid://${fileID}`},
            { role: "user", content: "这篇文章讲了什么？" }
        ],
    });
    console.log(JSON.stringify(completion))
}

main();
```
  ---
```curl
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-long",
    "messages": [
        {"role": "system","content": "You are a helpful assistant."},
        {"role": "system","content": "fileid://file-fe-xxx"},
        {"role": "user","content": "这篇文章讲了什么？"}
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    }
}'
```

---|---
**model**` _string_` __**（必选）** 模型名称。支持的模型：Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math。

> Qwen-Audio不支持OpenAI兼容协议，仅支持DashScope协议。

**具体模型名称和计费，请参见**[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。
**messages**` _array_` __**（必选）** 传递给大模型的上下文，按对话顺序排列。 **消息类型** __ System Message****`_object_` __ （可选）系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在`messages`数组的第一位。

> QwQ 模型不建议设置 System Message，QVQ 模型设置 System Message不会生效。

**属性** __ **content**` _string_` __**（必选）** 系统指令，用于明确模型的角色、行为规范、回答风格和任务约束等。**role**` _string_` __**（必选）** 系统消息的角色，固定为`system`。 User Message****`_object_` __**（必选）** 用户消息，用于向模型传递问题、指令或上下文等。 **属性** __ **content**` _string 或 array_`**（必选）** 消息内容。若输入只有文本，则为 string 类型；若输入包含图像等多模态数据，或启用显式缓存，则为 array 类型。 **使用多模态模型或启用显式缓存时的属性** __ **type**` _string_` __**（必选）** 可选值：

  * `text`输入文本时需设为`text`。
  * `image_url`输入图片时需设为`image_url`。
  * `input_audio`输入音频时需设为`input_audio`。
  * `video`输入图片列表形式的视频时需设为`video`。
  * `video_url`输入视频文件时需设为`video_url`。

> Qwen-VL仅部分模型可输入视频文件，详情参见[视频理解（Qwen-VL）](https://help.aliyun.com/zh/model-studio/vision#80dbf6ca8fh6s)；QVQ与Qwen-Omni 模型支持直接传入视频文件。

**text**` _string_` __ 输入的文本。当`type`为`text`时，是必选参数。 **image_url**` _object_` 输入的图片信息。当`type`为`image_url`时是必选参数。 **属性** __ **url** `_string_`**（必选）** 图片的 URL或 Base64 Data URL。传入本地文件请参考[视觉理解](https://help.aliyun.com/zh/model-studio/vision#647c6397db430)。 **input_audio**` _object_` 输入的音频信息。当`type`为`input_audio`时是必选参数。 **属性** __ **data** `_string_`**（必选）** 音频的 URL 或Base64 Data URL。传入本地文件请参见：[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。**format**` _string_`**（必选）** 输入音频的格式，如`mp3`、`wav`等。 **video**` _array_` __ 输入的**图片列表形式的视频信息** 。当`type`为`video`时是必选参数。使用方法请参见：[视频理解（Qwen-VL）](https://help.aliyun.com/zh/model-studio/vision#80dbf6ca8fh6s)、[视频理解（QVQ）](https://help.aliyun.com/zh/model-studio/visual-reasoning#e6df293d5565g)或[视频理解（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni#0f4360d63a8nk)。示例值： ---
```json
[
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
]
```
  **video_url**` _object_` __ 输入的视频文件信息。当`type`为`video_url`时是必选参数。Qwen-VL 只可理解视频文件的视觉信息，Qwen-Omni 可理解视频文件中的视觉与音频信息。 **属性** __ **url** `_string_`**（必选）** 视频文件的公网 URL 或 Base64 Data URL。输入本地视频文件请参见[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。 **min_pixels**` _integer_` __ （可选）设定输入图像的最小像素阈值。当输入图像或视频帧的像素小于`min_pixels`时，会将其进行放大，直到总像素高于`min_pixels`。

  * 适用模型：QVQ、Qwen-VL
  * 取值范围：如下所示 **min_pixels 取值范围** __
    * `Qwen3-VL`：默认值和最小值均为：`65536`
    * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值和最小值均为4096
    * QVQ 及其他 Qwen2.5-VL 模型：默认值和最小值均为`3136`
  * 示例值：`{"type": "image_url","image_url": {"url":"https://xxxx.jpg"},"min_pixels": 65536}`

**max_pixels**` _integer_` __ （可选）用于设定输入图像或视频帧的最大像素阈值。当输入图像或视频的像素在`[min_pixels, max_pixels]`区间内时，模型会按原图进行识别。当输入图像像素大于`max_pixels`时，会将图像进行缩小，直到总像素低于`max_pixels`。

  * 适用模型：QVQ、Qwen-VL
  * 取值范围：如下所示 **max_pixels 取值范围** __ max_pixels的取值与是否开启`vl_high_resolution_images`参数有关。
    * 当`vl_high_resolution_images`为`False`时：
      * `Qwen3-VL`：默认值为`2621440`，最大值为：`16777216`
      * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值为`1310720`，最大值为：`16777216`
      * `QVQ`及其他`Qwen2.5-VL`模型：默认值为`1003520` ，最大值为`12845056`
    * 当`vl_high_resolution_images`为`True`时：
      * `Qwen3-VL`、`qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：`max_pixels`无效，输入图像的最大像素固定为`16777216`
      * `QVQ`及其他`Qwen2.5-VL`模型：`max_pixels`无效，输入图像的最大像素固定为`12845056`
  * 示例值：`{"type": "image_url","image_url": {"url":"https://xxxx.jpg"},"max_pixels": 8388608}`

**cache_control**` _object_` __ （可选）用于开启显式缓存。相关文档：[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)。 **属性** __ **type** `_string_`**（必选）** 仅支持设定为`ephemeral`。 **role**` _string_` __**（必选）** 用户消息的角色，固定为`user`。 Assistant Message `_object_` __ （可选）模型的回复。通常用于在多轮对话中作为上下文回传给模型。 **属性** __ **content**` _string_` __ （可选）模型回复的文本内容。包含`tool_calls`时，`content`可以为空；否则`content`为必选。**role**` _string_` __**（必选）** 助手消息的角色，固定为`assistant`。**partial**` _boolean_` __ （可选）默认值为`false`是否开启[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)。可选值：

  * true：开启；
  * false：不开启。

**支持的模型** __

  * **通义千问 Max 系列**qwen3-max、qwen3-max-2025-09-23、qwen3-max-preview（非思考模式）、qwen-max、qwen-max-latest、qwen-max-2024-09-19及之后的快照模型
  * **通义千问 Plus 系列（非思考模式）**qwen-plus、qwen-plus-latest、qwen-plus-2024-09-19及之后的快照模型
  * **通义千问 Flash 系列（非思考模式）**qwen-flash、qwen-flash-2025-07-28及之后的快照模型
  * **通义千问 Coder 系列**qwen3-coder-plus、qwen3-coder-flash、qwen3-coder-480b-a35b-instruct、qwen3-coder-30b-a3b-instruct、qwen-coder-plus、qwen-coder-plus-latest、qwen-coder-plus-2024-11-06、qwen-coder-turbo、qwen-coder-turbo-latest、qwen-coder-turbo-2024-09-19、qwen2.5-coder-32b-instruct、qwen2.5-coder-14b-instruct、qwen2.5-coder-7b-instruct、qwen2.5-coder-3b-instruct、qwen2.5-coder-1.5b-instruct、qwen2.5-coder-0.5b-instruct
  * **通义千问 VL 系列**
    * **qwen3-vl-plus 系列（非思考模式）** qwen3-vl-plus、qwen3-vl-plus-2025-09-23及之后的快照模型
    * **qwen3-vl-flash 系列（非思考模式）** qwen3-vl-flash、qwen3-vl-flash-2025-10-15及之后的快照模型
    * **qwen-vl-max 系列** qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2024-08-09及之后的快照模型
    * **qwen-vl-plus 系列** qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2024-08-09及之后的快照模型
  * **通义千问 Turbo 系列（非思考模式）**qwen-turbo、qwen-turbo-latest、qwen-turbo-2024-09-19及之后的快照模型
  * **通义千问开源系列** Qwen3 开源模型（非思考模式）、qwen2.5-72b-instruct、qwen2.5-32b-instruct、qwen2.5-14b-instruct、qwen2.5-7b-instruct、qwen2.5-3b-instruct、qwen2.5-1.5b-instruct、qwen2.5-0.5b-instruct、Qwen3-VL开源模型（非思考模式）
  * **通义千问 Math 系列**qwen-math-plus、qwen-math-plus-latest、qwen-math-plus-0919、qwen-math-turbo、qwen-math-turbo-latest、qwen-math-turbo-0919、qwen2.5-math-72b-instruct、qwen2.5-math-7b-instruct、qwen2.5-math-1.5b-instruct

**tool_calls** `_array_` __ （可选）发起 Function Calling 后，返回的工具与入参信息，包含一个或多个对象。由上一轮模型响应的`tool_calls`字段获得。 **属性** __ **id** `_string_` __**（必选）** 工具响应的ID。**type** `_string_`**（必选）** 工具类型，当前只支持设为`function`。**function** `_object_`**（必选）** 工具与入参信息。 **属性** __ **name** `_string_`**（必选）** 工具名称。**arguments** `_string_`**（必选）** 入参信息，为JSON格式字符串。 **index** `_integer_`**（必选）** 当前工具信息在`tool_calls`数组中的索引。 Tool Message `_object_` __ （可选）工具的输出信息。 **属性** __ **content**` _string_` __**（必选）** 工具函数的输出内容，必须为字符串。若工具返回结构化数据（如JSON），需将其序列化为字符串。**role**` _string_` __**（必选）** 固定为`tool`。**tool_call_id**` _string_` __**（必选）** 发起 Function Calling 后返回的 id，通过completion.choices[0].message.tool_calls[$index].id获取，用于标记 Tool Message 对应的工具。
**stream**` _boolean_` __ （可选） 默认值为 `false`是否以流式输出方式回复。相关文档：[流式输出](https://help.aliyun.com/zh/model-studio/stream)可选值：

  * `false`：模型生成全部内容后一次性返回；
  * `true`：边生成边输出，每生成一部分内容即返回一个数据块（chunk）。需实时逐个读取这些块以拼接完整回复。

推荐设置为`true`，可提升阅读体验并降低超时风险。
**stream_options**` _object_` __ （可选）流式输出的配置项，仅在 `stream` 为 `true` 时生效。 **属性** __ **include_usage**` _boolean_` __ （可选）默认值为`false`是否在响应的**最后一个数据块** 包含Token消耗信息。可选值：

  * `true`：包含；
  * `false`：不包含。

> 流式输出时，Token 消耗信息仅可出现在响应的最后一个数据块。

**modalities**`array` __ （可选）默认值为`["text"]`输出数据的模态，仅适用于 Qwen-Omni 模型。相关文档：[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni)可选值：

  * `["text","audio"]`：输出文本与音频；
  * `["text"]`：仅输出文本。


**audio**` _object_` __ （可选）输出音频的音色与格式，仅适用于 Qwen-Omni 模型，且`modalities`参数需为`["text","audio"]`。相关文档：[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni) **属性** __ **voice**` _string_` **（必选）** 输出音频的音色。请参见[音色列表](https://help.aliyun.com/zh/model-studio/qwen-omni#a447c4fbf5ul0)。**format**` _string_` **（必选）** 输出音频的格式，仅支持设定为`wav`。
**temperature**` _float_` __ （可选） __ 采样温度，控制模型生成文本的多样性。temperature越高，生成的文本更多样，反之，生成的文本更确定。取值范围： [0, 2)temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。更多说明，请参见[文本生成模型概述](https://help.aliyun.com/zh/model-studio/text-generation#ad7b336bec5fw)。 **temperature 默认值** __ Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen-turbo系列（非思考模式）、qwen开源系列、qwen-coder系列、qwq-32b-preview、qwen-doc-turbo、qwen-vl-max-2025-08-13、Qwen3-VL（非思考模式）：0.7；qwen3-max-preview（思考模式）、qwen-long、qwen-omni-turbo系列：1.0；QVQ系列 、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15 : 0.5；其余qwen-vl系列、qwen-omni-turbo系列、qvq-72b-preview：0.01；qwen-math系列：0；Qwen3（思考模式）、Qwen3-Thinking、Qwen3-Omni-Captioner、QwQ 系列：0.6；qwen-plus-character：0.92qwen3-omni-flash系列：0.9Qwen3-VL（思考模式）：0.8

> 不建议修改QVQ模型的默认temperature值 。

**top_p**` _float_` __ （可选）核采样的概率阈值，控制模型生成文本的多样性。top_p越高，生成的文本更多样。反之，生成的文本更确定。取值范围：（0,1.0]temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。更多说明，请参见[文本生成模型概述](https://help.aliyun.com/zh/model-studio/text-generation#ad7b336bec5fw)。 **top_p 默认值** __ Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen-turbo系列（非思考模式）、Qwen 2.5开源系列、qwen-coder系列、qwen-long、qwq-32b-preview、qwen-doc-turbo、qwen-vl-max-2025-08-13、Qwen3-VL（非思考）：0.8；qwen-vl-max-2024-11-19、qwen-vl-max-2024-10-30、qwen-vl-max-2024-08-09、qwen2-vl-72b-instruct、qwen-omni-turbo 系列：0.01；qwen-vl-plus系列、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-04-08、qwen-vl-max-2025-04-02、qwen-vl-max-2025-01-25、qwen-vl-max-2024-12-30、qvq-72b-preview、qwen2-vl-2b-instruct、qwen2-vl-7b-instruct、qwen2.5-vl-3b-instruct、qwen2.5-vl-7b-instruct、qwen2.5-vl-32b-instruct、qwen2.5-vl-72b-instruct、qwen2.5-omni-7b：0.001；QVQ系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15 、qwen2-audio-instruct: 0.5；qwen3-max-preview（思考模式）、qwen-math系列、Qwen3-Omni-Flash系列：1.0；Qwen3（思考模式）、Qwen3-VL（思考模式）、Qwen3-Thinking、QwQ 系列、Qwen3-Omni-Captioner、qwen-plus-character：0.95

> 不建议修改QVQ模型的默认 top_p 值。

**top_k**` _integer_` __ （可选）指定生成过程中用于采样的候选 Token 数量。值越大，输出越随机；值越小，输出越确定。若设为 `null` 或大于 100，则禁用 `top_k` 策略，仅 `top_p` 策略生效。取值必须为大于或等于 0 的整数。 **top_k 默认值** __ QVQ系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15：10；QwQ 系列：40；qwen-math 系列、其余qwen-vl-plus系列、qwen-vl-max-2025-08-13之前的模型、qwen-audio-turbo系列、qwen2.5-omni-7b、qvq-72b-preview：1；Qwen3-Omni-Flash系列：50；其余模型均为20。

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：extra_body={"top_k":xxx}。

> 不建议修改QVQ模型的默认 top_k 值。

**presence_penalty** `_float_` __ （可选）控制模型生成文本时的内容重复度。取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。 **presence_penalty 默认值** __ qwen3-max-preview（思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、qwen3-0.6b/1.7b/4b（思考模式）、QVQ系列、qwen-max、qwen-max-latest、qwen-max-latest、qwen-max-2024-09-19、qwen2.5-vl系列、qwen-vl-max系列、qwen-vl-plus、qwen2-vl-72b-instruct、qwen-vl-plus-2025-01-02、Qwen3-VL（非思考）：1.5；qwen-vl-plus-latest、qwen-vl-plus-2025-08-15、qwen-vl-plus-2025-07-10：1.2qwen-vl-plus-2025-01-25：1.0；qwen3-8b/14b/32b/30b-a3b/235b-a22b（思考模式）、qwen-plus/qwen-plus-latest/2025-04-28（思考模式）、qwen-turbo/qwen-turbo/2025-04-28（思考模式）：0.5；其余均为0.0。 **原理介绍** __ 如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。 **示例** __ 提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。

> 使用qwen-vl-plus-2025-01-25模型进行文字提取时，建议设置presence_penalty为1.5。

> 不建议修改QVQ模型的默认presence_penalty值。

**response_format**` _object_` （可选） 默认值为`{"type": "text"}`返回内容的格式。可选值：

  * `{"type": "text"}`：输出文字回复；
  * `{"type": "json_object"}`：输出标准格式的JSON字符串。
  * `{"type": "json_schema","json_schema": {...} }`：输出指定格式的JSON字符串。

> 相关文档：[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)。

> 若指定为`{"type": "json_object"}`，需在提示词中明确指示模型输出JSON，如：“请按照json格式输出”，否则会报错。

> 支持的模型参见[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)。

**属性** __ **type**` _string_` __**（必选）** 返回内容的格式。可选值：

  * `text`：输出文字回复；
  * `json_object`：输出标准格式的JSON字符串；
  * `json_schema`：输出指定格式的JSON字符串。

**json_schema**` _object_` __ 当 type 为 json_schema 时，该字段为必选，用于定义结构化输出的配置。 **属性** __ **name**` _string_` __**（必选）** Schema 的唯一标识名称。仅支持字母（不区分大小写）、数字、下划线和短横线，最长 64 个字符。**description**` _string_` __ （可选）描述 Schema 的用途，帮助模型理解输出的语义上下文。**schema**` _object_` __ （可选）符合 JSON Schema 标准的对象，定义模型输出的数据结构。

> 构建JSON Schema 方法参加：[JSON Schema](https://json-schema.org/)

**strict**` _boolean_`**** （可选）默认值为`false`控制是否强制模型严格遵守 Schema 的所有约束。

  * **true（推荐）** 模型严格遵循字段类型、必填项、格式等所有约束，确保输出 100% 合规。
  * **false（不推荐）** 模型仅大致遵循 Schema，可能生成不符合规范的输出，导致验证失败。


**max_input_tokens**` _integer_` __ （可选）允许输入的最大 Token 长度。目前仅支持qwen-plus-0728/latest模型。

  * qwen-plus-latest 默认值：129,024

> 后续默认值可能调整至1,000,000。

  * qwen-plus-2025-07-28 默认值：1,000,000

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"max_input_tokens": xxx}`。

**max_tokens**` _integer_` __ （可选）用于限制模型输出的最大 Token 数。若生成内容超过此值，生成将提前停止，且返回的`finish_reason`为`length`。默认值与最大值均为模型的最大输出长度，请参见[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。适用于需控制输出长度的场景，如生成摘要、关键词，或用于降低成本、缩短响应时间。触发 `max_tokens `时，响应的 finish_reason 字段为 `length`。

> `max_tokens`不限制思考模型思维链的长度。

**vl_high_resolution_images**` _boolean_` __ （可选）默认值为`false`是否将输入图像的像素上限提升至 16384 Token 对应的像素值。相关文档：[处理高分辨率图像](https://help.aliyun.com/zh/model-studio/vision#e7e2db755f9h7)。

  * `vl_high_resolution_images：true`，使用固定分辨率策略，忽略 `max_pixels` 设置，超过此分辨率时会将图像总像素缩小至此上限内。 **点击查看各模型像素上限** __ `vl_high_resolution_images`为`True`时，不同模型像素上限不同：
    * `Qwen3-VL系列`、`qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`模型：`16777216`（每`Token`对应`32*32`像素，即`16384*32*32`）
    * `QVQ系列`、其他`Qwen2.5-VL系列`模型：`12845056`（每`Token`对应`28*28`像素，即 `16384*28*28`）
  * `vl_high_resolution_images`为`false`，实际分辨率由 `max_pixels` 与默认上限共同决定，取二者计算结果的最大值。超过此像素上限时会将图像缩小至此上限内。 **点击查看各模型的默认像素上限** __ `vl_high_resolution_images`为`false`时，不同模型默认像素上限不同：
    * `Qwen3-VL系列`：`2621440`(`2560*32*32`，即默认`Token`上限为`2560`)
    * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`模型：`1310720`(`1280*32*32`，即默认`Token`上限为`1280`)
    * `QVQ系列`、其他`Qwen2.5-VL系列`模型：`1003520`(`1280*28*28`，即默认`Token`上限为`1280`)

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：extra_body={"vl_high_resolution_images":xxx}。

**n**` _integer_` __ （可选） 默认值为1生成响应的数量，取值范围是`1-4`。适用于需生成多个候选响应的场景，例如创意写作或广告文案。

> 仅支持 qwen-plus、 [Qwen3（非思考模式）](https://help.aliyun.com/zh/model-studio/deep-thinking#be9890136awsc)、qwen-plus-character 模型。

> 若传入 `tools` 参数， 请将`n` 设为 1。

> 增大 n 会增加输出 Token 的消耗，但不增加输入 Token 消耗。

**enable_thinking** `_boolean_` （可选）使用混合思考（回复前既可思考也可不思考）模型时，是否开启思考模式。适用于 Qwen3 、Qwen3-Omni-Flash、Qwen3-VL模型。相关文档：[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)可选值：

  * `true`：开启

> 开启后，思考内容将通过`reasoning_content`字段返回。

  * `false`：不开启

不同模型的默认值：[支持的模型](https://help.aliyun.com/zh/model-studio/deep-thinking#78286fdc35hlw)

> 通该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"enable_thinking": xxx}`。

**thinking_budget** `_integer_` （可选）思考过程的最大 Token 数。适用于Qwen3-VL、Qwen3 的商业版与开源版模型。相关文档：[限制思考长度](https://help.aliyun.com/zh/model-studio/deep-thinking#e7c0002fe4meu)。默认值为模型最大思维链长度，请参见：[模型列表](https://help.aliyun.com/zh/model-studio/models)

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"thinking_budget": xxx}`。

**enable_code_interpreter** `_boolean_` （可选）默认值为 `false`是否开启代码解释器功能。仅当`model`为`qwen3-max-preview`且`enable_thinking`为`true`时生效。相关文档：[代码解释器](https://help.aliyun.com/zh/model-studio/qwen-code-interpreter)可选值：

  * `true`：开启
  * `false`：不开启

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"enable_code_interpreter": xxx}`。

**seed**` _integer_` __ （可选）随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 `seed` 且其他参数不变，模型将尽可能返回相同结果。取值范围：`[0,231−1]`。 **seed 默认值** __ qwen-vl-plus-2025-01-02、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-04-08、qwen-vl-max-2025-04-02、qwen-vl-max-2024-12-30、qvq-72b-preview、qvq-max系列：3407；qwen-vl-max-2025-01-25、qwen-vl-max-2024-11-19、qwen-vl-max-2024-10-30、qwen-vl-max-2024-08-09、qwen-vl-max-2024-02-01、qwen2-vl-72b-instruct、qwen2-vl-2b-instruct、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2025-05-07、qwen-vl-plus-2025-01-25、qwen-vl-plus-2024-08-09、qwen-vl-plus-2023-12-01：无默认值；其余模型均为1234。
**logprobs** `_boolean_` （可选）默认值为 `false`是否返回输出 Token 的对数概率，可选值：

  * `true`返回
  * `false`不返回

> 思考阶段生成的内容（`reasoning_content`）不会返回对数概率。

**支持的模型** __

  * qwen-plus系列的快照模型（不包含主线模型）
  * qwen-turbo 系列的快照模型（不包含主线模型）
  * Qwen3 开源模型


**top_logprobs** `_integer_` （可选）默认值为0指定在每一步生成时，返回模型最大概率的候选 Token 个数。取值范围：[0,5]仅当 `logprobs` 为 `true` 时生效。
**stop**` _string 或 array_` __ （可选）用于指定停止词。当模型生成的文本中出现`stop` 指定的字符串或`token_id`时，生成将立即终止。可传入敏感词以控制模型的输出。

> stop为数组时，不可将`token_id`和字符串同时作为元素输入，比如不可以指定为`["你好",104307]`。

**tools**` _array_` __ （可选）包含一个或多个工具对象的数组，供模型在 Function Calling 中调用。相关文档：[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)设置 tools 且模型判断需要调用工具时，响应会通过 tool_calls 返回工具信息。 **属性** __ **type**` _string_` __**（必选）** 工具类型，当前仅支持设为`function`。**function**` _object_` __**（必选）** **属性** __ **name**` _string_` __**（必选）** 工具名称。仅允许字母、数字、下划线（`_`）和短划线（`-`），最长 64 个 Token。**description**` _string_` __**（必选）** 工具描述信息，帮助模型判断何时以及如何调用该工具。**parameters**` _object_` __**（必选）** 工具的参数描述，需要是一个合法的JSON Schema。JSON Schema的描述可以见[链接](https://json-schema.org/understanding-json-schema)。若`parameters`参数为空，表示该工具没有入参（如时间查询工具）。
**tool_choice** `_string 或 object_` __ （可选）默认值为 `auto`工具选择策略。若需对某类问题强制指定工具调用方式（例如始终使用某工具或禁用所有工具），可设置此参数。可选值：

  * `auto`大模型自主选择工具策略。
  * `none`若不希望进行工具调用，可设定`tool_choice`参数为`none`；
  * `{"type": "function", "function": {"name": "the_function_to_call"}}`若希望强制调用某个工具，可设定`tool_choice`参数为`{"type": "function", "function": {"name": "the_function_to_call"}}`，其中`the_function_to_call`是指定的工具函数名称。

> 思考模式的模型不支持强制调用某个工具。


**parallel_tool_calls** `_boolean_` （可选）默认值为 `false`是否开启并行工具调用。相关文档：[并行工具调用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#cb6b5c484bt4x)可选值：

  * `true`：开启
  * `false`：不开启


**enable_search** ****`_boolean_` __ （可选）默认值为 `false`是否开启联网搜索。相关文档：[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)可选值：

  * `true`：开启；

> 若开启后未联网搜索，可优化提示词，或设置`search_options`中的`forced_search`参数开启强制搜索。

  * `false`：不开启。

> 启用互联网搜索功能可能会增加 Token 的消耗。

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"enable_search": True}`。

**search_options**` _object_`**** （可选）联网搜索的策略。相关文档：[联网搜索](https://help.aliyun.com/zh/model-studio/web-search) **属性** __ **forced_search** `_boolean_`（可选）默认值为`false`是否强制开启联网搜索，仅当`enable_search`为`true`时生效。可选值：

  * true：强制开启；
  * false：不强制开启，由模型判断是否联网搜索。

**search_strategy** `_string_`（可选）默认值为`turbo`搜索量级策略，仅当`enable_search`为`true`时生效。可选值：

  * `turbo` （默认）: 兼顾响应速度与搜索效果，适用于大多数场景。
  * `max`: 采用更全面的搜索策略，可调用多源搜索引擎，以获取更详尽的搜索结果，但响应时间可能更长。
  * `agent`：可多次调用联网搜索工具与大模型，实现多轮信息检索与内容整合。

> `agent`策略仅适用于 qwen3-max 与 qwen3-max-2025-09-23。

> `agent`策略不可与其他联网搜索策略同时设定。

**enable_search_extension** `_boolean_`（可选）默认值为`false`是否开启垂域搜索，仅当`enable_search`为`true`时生效。可选值：

  * `true`：开启。
  * `false`：不开启。

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"search_options": xxx}`。

|
**X-DashScope-DataInspection**` _string_` （可选）在通义千问 API 的内容安全能力基础上，是否进一步识别输入输出内容的违规信息。取值如下：

  * `'{"input":"cip","output":"cip"}'`：进一步识别；
  * 不设置该参数：不进一步识别。

通过 HTTP 调用时请放入请求头：`-H "X-DashScope-DataInspection: {\"input\": \"cip\", \"output\": \"cip\"}"`；通过 Python SDK 调用时请通过`extra_headers`配置：`extra_headers={'X-DashScope-DataInspection': '{"input":"cip","output":"cip"}'}`。详细使用方法请参见[内容审核](https://help.aliyun.com/zh/model-studio/content-security)。

> 不支持通过 Node.js SDK设置。

> 不适用于 Qwen-VL 系列模型。

|

### chat响应对象（非流式输出）

|  ---
```json
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "我是阿里云开发的一款超大规模语言模型，我叫通义千问。"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 3019,
        "completion_tokens": 104,
        "total_tokens": 3123,
        "prompt_tokens_details": {
            "cached_tokens": 2048
        }
    },
    "created": 1735120033,
    "system_fingerprint": null,
    "model": "qwen-plus",
    "id": "chatcmpl-6ada9ed2-7f33-9de2-8bb0-78bd4035025a"
}
```

---|---
**id**` _string_` 本次调用的唯一标识符。
**choices**` _array_` 模型生成内容的数组。 **属性** __ **finish_reason**` _string_` 模型停止生成的原因。有三种情况：

  * 触发输入参数中的`stop`参数，或自然停止输出时为`stop`；
  * 生成长度过长而结束为`length`；
  * 需要调用工具而结束为`tool_calls`。

**index**` _integer_` 当前对象在`choices`数组中的索引。**logprobs**` _object_` 模型输出的 Token 概率信息。 **属性** __ **content** `_array_` 包含每个 Token 及其对数概率的数组。 **属性** __ **token** `_string_` 当前 Token 的文本。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容（例如表情符号或中文字符）。**logprob** `_float_` 当前 Token 的对数概率。返回值为 `null` 表示概率值极低。**top_logprobs** `_array_` 当前 Token 位置最可能的若干候选 Token，数量与请求参数`top_logprobs`保持一致。每个元素包含： **属性** __ **token** `_string_` 候选 Token 文本。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容（例如表情符号或中文字符）。**logprob** `_float_` 该候选 Token 的对数概率。返回值为 null 表示概率值极低。 **message**` _object_` 模型输出的消息。 **属性** __ **content** `_string_` 模型的回复内容。**reasoning_content** `_string_` 模型的思维链内容。**refusal** `_string_` 该参数当前固定为`null`。**role** `_string_` 消息的角色，固定为`assistant`。**audio** `_object_` 该参数当前固定为`null`。**function_call** （即将废弃）` _object_` 该值固定为`null`，请参考`tool_calls`参数。**tool_calls** `_array_` 在发起 Function Calling后，模型生成的工具与入参信息。 **属性** __ **id** `_string_` 本次工具响应的唯一标识符。**type** `_string_` 工具类型，当前只支持`function`。**function** `_object_` 工具信息。 **属性** __ **name** `_string_` 工具名称。**arguments** `_string_` 入参信息，为JSON格式字符串。

> 由于大模型响应有一定随机性，输出的入参信息可能不符合函数签名。请在调用前校验参数有效性

**index** `_integer_` 当前工具在`tool_calls`数组中的索引。
**created**` _integer_` 请求创建时的 Unix 时间戳（秒）。
**model**` _string_` 本次请求使用的模型。
**object** `_string_` 始终为`chat.completion`。
**service_tier** `_string_` 该参数当前固定为`null`。
**system_fingerprint**` _string_` 该参数当前固定为`null`。
**usage** `_object_` 本次请求的 Token 消耗信息。 **属性** __ **completion_tokens** `_integer_` 模型输出的 Token 数。**prompt_tokens** `_integer_` 输入的 Token 数。**total_tokens** `_integer_` 消耗的总 Token 数，为`prompt_tokens`与`completion_tokens`的总和。**completion_tokens_details** `_object_` 使用[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)时输出Token的细粒度分类。 **属性** __ **audio_tokens** `_integer_` 该参数当前固定为`null`。**reasoning_tokens** `_integer_` 该参数当前固定为`null`。**text_tokens** `_integer_`[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)输出文本的Token数。 **prompt_tokens_details** `_object_` 输入 Token 的细粒度分类。 **属性** __ **audio_tokens** `_integer_` 该参数当前固定为`null`。**cached_tokens** `_integer_` 命中 Cache 的 Token 数。Context Cache 详情请参见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。**text_tokens** `_integer_`[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)输入的文本 Token 数。**image_tokens** `_integer_`[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)输入的图像 Token数。**video_tokens** `_integer_`[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)输入的视频文件或者图像列表 Token 数。**cache_creation** `_object_`[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)创建信息。 **属性** __ **ephemeral_5m_input_tokens** `_integer_` 创建显式缓存的 Token 数。 **cache_creation_input_tokens** `_integer_` 创建显式缓存的 Token 数。**cache_type** `_string_` 使用[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)时，参数值为`ephemeral`，否则该参数不存在。

### chat响应chunk对象（流式输出）

|  ---
```json
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"","function_call":null,"refusal":null,"role":"assistant","tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"我是","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"来自","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"阿里","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"云的超大规模","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"语言模型，我","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"叫通义千","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"问。","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":"stop","index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":{"completion_tokens":17,"prompt_tokens":22,"total_tokens":39,"completion_tokens_details":null,"prompt_tokens_details":{"audio_tokens":null,"cached_tokens":0}}}
```

---|---
**id**` _string_` 本次调用的唯一标识符。每个chunk对象有相同的 id。
**choices**` _array_` 模型生成内容的数组，可包含一个或多个对象。若设置`include_usage`参数为`true`，则`choices`在最后一个chunk中为空数组。 **属性** __ **delta** `_object_` 请求的增量对象。 **属性** __ **content** `_string_` 增量消息内容。**reasoning_content** `_string_` 增量思维链内容。**function_call** `_object_` 该值默认为`null`，请参考`tool_calls`参数。**audio**` _object_` 使用 [Qwen-Omni](https://help.aliyun.com/zh/model-studio/qwen-omni) 模型时生成的回复。 **属性** __ **data** `_string_` 增量的 Base64 音频编码数据。**expires_at** `_integer_` 创建请求时的时间戳。 **refusal** `_object_` 该参数当前固定为`null`。**role** `_string_` 增量消息对象的角色，只在第一个chunk中有值。**tool_calls** `_array_` 在发起 Function Calling后，模型生成的工具与入参信息。 **属性** __ **index** `_integer_` 当前工具在`tool_calls`数组中的索引。**id** `_string_` 本次工具响应的唯一标识符。**function** `_object_` 被调用的工具信息。 **属性** __ **arguments** `_string_` 增量的入参信息，所有chunk的`arguments`拼接后为完整的入参。

> 由于大模型响应有一定随机性，输出的入参信息可能不符合函数签名。请在调用前校验参数有效性。

**name** `_string_` 工具名称，只在第一个chunk中有值。 **type** `_string_` 工具类型，当前只支持`function`。 **finish_reason** `_string_` 模型停止生成的原因。有四种情况：

  * 因触发输入参数中的`stop`参数，或自然停止输出时为`stop`；
  * 生成未结束时为`null`；
  * 生成长度过长而结束为`length`；
  * 需要调用工具而结束为`tool_calls`。

**index** `_integer_` 当前响应在`choices`数组中的索引。当输入参数 n 大于1时，需根据本参数进行不同响应对应的完整内容的拼接。**logprobs**` _object_` 当前对象的概率信息。 **属性** __ **content** `_array_` 带有对数概率信息的 Token 数组。 **属性** __ **token** `_string_` 当前 Token。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。**logprob** `_float_` 当前 Token 的对数概率。返回值为 null 表示概率值极低。**top_logprobs** `_array_` 当前 Token 位置最可能的若干个 Token 及其对数概率，元素个数与入参的`top_logprobs`保持一致。 **属性** __ **token** `_string_` 当前 Token。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。**logprob** `_float_` 当前 Token 的对数概率。返回值为 null 表示概率值极低。
**created**` _integer_` 本次请求被创建时的时间戳。每个chunk有相同的时间戳。
**model**` _string_` 本次请求使用的模型。
**object** `_string_` 始终为`chat.completion.chunk`。
**service_tier** `_string_` 该参数当前固定为`null`。
**system_fingerprint**` _string_` 该参数当前固定为`null`。
**usage** `_object_` 本次请求消耗的Token。只在`include_usage`为`true`时，在最后一个chunk显示。 **属性** __ **completion_tokens** `_integer_` 模型输出的 Token 数。**prompt_tokens** `_integer_` 输入 Token 数。**total_tokens** `_integer_` 总 Token 数，为`prompt_tokens`与`completion_tokens`的总和。**completion_tokens_details** `_object_` 输出 Token 的详细信息。 **属性** __ **audio_tokens**` _integer_`[Qwen-Omni 模型](https://help.aliyun.com/zh/model-studio/qwen-omni)输出的音频 Token 数。**reasoning_tokens** `_integer_` 思考过程 Token 数。**text_tokens**` _integer_` 输出文本 Token 数。 **prompt_tokens_details** `_object_` 输入 Token的细粒度分类。 **属性** __ **audio_tokens** `_integer_` 输入音频的 Token 数。

> 视频文件中的音频 Token 数通过本参数返回。

**text_tokens** `_integer_` 输入文本的 Token 数。**video_tokens** `_integer_` 输入视频（图片列表形式或视频文件）的 Token 数。**image_tokens** `_integer_` 输入图片的 Token 数。**cached_tokens** `_integer_` 命中缓存的 Token 数。Context Cache 详情请参见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。**cache_creation** `_object_`[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)创建信息。 **属性** __ **ephemeral_5m_input_tokens** `_integer_` 创建显式缓存的 Token 数。 **cache_creation_input_tokens** `_integer_` 创建显式缓存的 Token 数。**cache_type** `_string_` 缓存类型，固定为`ephemeral`。

## OpenAI 兼容

北京地域

新加坡地域

金融云

__

__

SDK 调用配置的`base_url`：`https://dashscope.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

SDK 调用配置的`base_url`：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`

SDK 调用配置的`base_url`：`https://dashscope-finance.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://dashscope-finance.aliyuncs.com/compatible-mode/v1/chat/completions`

> 您需要先[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过OpenAI SDK进行调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

### 请求体

|  POST /chat/completions 调试

### OpenAI 兼容接口在线调试

× 中国大陆（北京）  国际（新加坡）  POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions API Key Bearer Token [获取中国大陆（北京）地域 API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 请求体 默认 深度思考 图像输入 工具调用 结构化输出 { "model": "qwen-plus", "messages": [ { "role": "system", "content": "You are a helpful assistant." }, { "role": "user", "content": "你是谁？" } ] } 发送请求  清空响应  响应结果 原始响应 解析内容 文本输入流式输出图像输入视频输入工具调用联网搜索异步调用文档理解 --- PythonJavaNode.jsGoC#（HTTP）PHP（HTTP）curl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ]
)
print(completion.model_dump_json())
```
  ---
```java
// 该代码 OpenAI SDK 版本为 2.6.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .addUserMessage("你是谁")
                .model("qwen-plus")
                .build();

        try {
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            System.out.println(chatCompletion);
        } catch (Exception e) {
            System.err.println("Error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",  //此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "你是谁？" }
        ],
    });
    console.log(JSON.stringify(completion))
}

main();
```
  ---
```go
package main

import (
	"context"
	"os"

	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"
)

func main() {
	client := openai.NewClient(
		option.WithAPIKey(os.Getenv("DASHSCOPE_API_KEY")),
		option.WithBaseURL("https://dashscope.aliyuncs.com/compatible-mode/v1"),
	)
	chatCompletion, err := client.Chat.Completions.New(
		context.TODO(), openai.ChatCompletionNewParams{
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.UserMessage("你是谁"),
			},
			Model: "qwen-plus",
		},
	)

	if err != nil {
		panic(err.Error())
	}

	println(chatCompletion.Choices[0].Message.Content)
}
```
  ---
```csharp
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
            return;
        }

        // 设置请求 URL 和内容
        string url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
        // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        string jsonContent = @"{
            ""model"": ""qwen-plus"",
            ""messages"": [
                {
                    ""role"": ""system"",
                    ""content"": ""You are a helpful assistant.""
                },
                {
                    ""role"": ""user"",
                    ""content"": ""你是谁？""
                }
            ]
        }";

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```
  ---
```php
<?php
// 设置请求的URL
$url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
// 若没有配置环境变量，请用百炼API Key将下行替换为：$apiKey = "sk-xxx";
$apiKey = getenv('DASHSCOPE_API_KEY');
// 设置请求头
$headers = [
    'Authorization: Bearer '.$apiKey,
    'Content-Type: application/json'
];
// 设置请求体
$data = [
    // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    "model" => "qwen-plus",
    "messages" => [
        [
            "role" => "system",
            "content" => "You are a helpful assistant."
        ],
        [
            "role" => "user",
            "content" => "你是谁？"
        ]
    ]
];
// 初始化cURL会话
$ch = curl_init();
// 设置cURL选项
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
// 执行cURL会话
$response = curl_exec($ch);
// 检查是否有错误发生
if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
}
// 关闭cURL资源
curl_close($ch);
// 输出响应结果
echo $response;
?>
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ]
}'
```


> 相关文档：[流式输出](https://help.aliyun.com/zh/model-studio/stream)。

PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '你是谁？'}],
    stream=True,
    stream_options={"include_usage": True}
    )
for chunk in completion:
    print(chunk.model_dump_json())
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus", // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你是谁？"}
        ],
        stream: true,
        stream_options: {include_usage: true}
    });
    for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
    }
}

main();
```
  ---
```curl
curl --location "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream":true,
    "stream_options": {
        "include_usage": true
    }
}'
```


> 相关文档：[视觉理解](https://help.aliyun.com/zh/model-studio/vision)。

PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-vl-plus",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{"role": "user","content": [
            {"type": "image_url",
             "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}},
            {"type": "text", "text": "这是什么"},
            ]}]
    )
print(completion.model_dump_json())
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen-vl-max", // 此处以qwen-vl-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [{role: "user",content: [
            { type: "image_url",image_url: {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}},
            { type: "text", text: "这是什么？" },
        ]}]
    });
    console.log(JSON.stringify(response));
}

main();
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen-vl-plus",
  "messages": [{
      "role": "user",
      "content": [
       {"type": "image_url","image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}},
       {"type": "text","text": "这是什么"}
       ]}]
}'
```


> 以下示例展示了如何将图片列表作为视频输入。如需使用视频文件等其他方式，请参阅“[视觉理解](https://help.aliyun.com/zh/model-studio/vision#80dbf6ca8fh6s)。

PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen-vl-max-latest",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "video",
                "video": [
                    "https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                    "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                    "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                    "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"]
            },
            {
                "type": "text",
                "text": "描述这个视频的具体过程"
            }]}]
)
print(completion.model_dump_json())
```
  ---
```nodejs
// 确保之前在 package.json 中指定了 "type": "module"
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        // 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model: "qwen-vl-max-latest",
        messages: [{
            role: "user",
            content: [
                {
                    type: "video",
                    video: [
                        "https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"
                    ]
                },
                {
                    type: "text",
                    text: "描述这个视频的具体过程"
                }
        ]}]
    });
    console.log(JSON.stringify(response));
}

main();
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen-vl-max-latest",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "video",
                    "video": [
                        "https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"
                    ]
                },
                {
                    "type": "text",
                    "text": "描述这个视频的具体过程"
                }
            ]
        }
    ]
}'
```


> 相关文档：[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)

PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # 因为获取当前时间无需输入参数，因此parameters为空字典
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    # 查询天气时需要提供位置，因此参数设置为location
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
messages = [{"role": "user", "content": "杭州天气怎么样"}]
completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    tools=tools
)

print(completion.model_dump_json())
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

const messages = [{"role": "user", "content": "杭州天气怎么样"}];
const tools = [
// 工具1 获取当前时刻的时间
{
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "当你想知道现在的时间时非常有用。",
        // 因为获取当前时间无需输入参数，因此parameters为空
        "parameters": {}
    }
},
// 工具2 获取指定城市的天气
{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "当你想查询指定城市的天气时非常有用。",
        "parameters": {
            "type": "object",
            "properties": {
                // 查询天气时需要提供位置，因此参数设置为location
                "location": {
                    "type": "string",
                    "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                }
            },
            "required": ["location"]
        }
    }
}
];

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen-plus", // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: messages,
        tools: tools,
    });
    console.log(JSON.stringify(response));
}

main();
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "杭州天气怎么样"
        }
    ],
    "tools": [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location":{
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
  ]
}'
```
  PythonNode.jscurl --- ---
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '中国队在巴黎奥运会获得了多少枚金牌'}],
    extra_body={
        "enable_search": True
    }
    )
print(completion.model_dump_json())
```
  ---
```nodejs
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus", //此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "中国队在巴黎奥运会获得了多少枚金牌" }
        ],
        enable_search:true
    });
    console.log(JSON.stringify(completion))
}

main();
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "中国队在巴黎奥运会获得了多少枚金牌"
        }
    ],
    "enable_search": true
}'
```
  ---
```python
import os
import asyncio
from openai import AsyncOpenAI
import platform

client = AsyncOpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

async def main():
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": "你是谁"}],
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    )
    print(response.model_dump_json())

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
```


> 当前仅qwen-long模型支持对文档进行分析，详细用法请参见[长上下文（Qwen-Long）](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)。

PythonJavaNode.jscurl --- ---
```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
file_object = client.files.create(file=Path("百炼系列手机产品介绍.docx"), purpose="file-extract")
completion = client.chat.completions.create(
    model="qwen-long",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': f'fileid://{file_object.id}'},
        {'role': 'user', 'content': '这篇文章讲了什么？'}
    ]
)
print(completion.model_dump_json())
```
  ---
```java
// 建议OpenAI SDK的版本 >= 0.32.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.files.FileCreateParams;
import com.openai.models.files.FileObject;
import com.openai.models.files.FilePurpose;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        // 设置文件路径
        Path filePath = Paths.get("百炼系列手机产品介绍.docx");
        // 创建文件上传参数
        FileCreateParams fileParams = FileCreateParams.builder()
                .file(filePath)
                .purpose(FilePurpose.of("file-extract"))
                .build();

        // 上传文件
        FileObject fileObject = client.files().create(fileParams);
        String fileId = fileObject.id();

        // 创建聊天请求
        ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
                .addSystemMessage("fileid://" + fileId)
                .addUserMessage("这篇文章讲了什么？")
                .model("qwen-long")
                .build();

        // 发送请求并获取响应
        ChatCompletion chatCompletion = client.chat().completions().create(chatParams);

        // 打印响应结果
        System.out.println(chatCompletion);
    }
}
```
  ---
```nodejs
import fs from "fs";
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function getFileID() {
    const fileObject = await openai.files.create({
        file: fs.createReadStream("百炼系列手机产品介绍.docx"),
        purpose: "file-extract"
    });
    return fileObject.id;
}

async function main() {
    const fileID = await getFileID();
    const completion = await openai.chat.completions.create({
        model: "qwen-long",  //模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: "system", content: `fileid://${fileID}`},
            { role: "user", content: "这篇文章讲了什么？" }
        ],
    });
    console.log(JSON.stringify(completion))
}

main();
```
  ---
```curl
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-long",
    "messages": [
        {"role": "system","content": "You are a helpful assistant."},
        {"role": "system","content": "fileid://file-fe-xxx"},
        {"role": "user","content": "这篇文章讲了什么？"}
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    }
}'
```

---|---
**model**` _string_` __**（必选）** 模型名称。支持的模型：Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math。

> Qwen-Audio不支持OpenAI兼容协议，仅支持DashScope协议。

**具体模型名称和计费，请参见**[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。
**messages**` _array_` __**（必选）** 传递给大模型的上下文，按对话顺序排列。 **消息类型** __ System Message****`_object_` __ （可选）系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在`messages`数组的第一位。

> QwQ 模型不建议设置 System Message，QVQ 模型设置 System Message不会生效。

**属性** __ **content**` _string_` __**（必选）** 系统指令，用于明确模型的角色、行为规范、回答风格和任务约束等。**role**` _string_` __**（必选）** 系统消息的角色，固定为`system`。 User Message****`_object_` __**（必选）** 用户消息，用于向模型传递问题、指令或上下文等。 **属性** __ **content**` _string 或 array_`**（必选）** 消息内容。若输入只有文本，则为 string 类型；若输入包含图像等多模态数据，或启用显式缓存，则为 array 类型。 **使用多模态模型或启用显式缓存时的属性** __ **type**` _string_` __**（必选）** 可选值：

  * `text`输入文本时需设为`text`。
  * `image_url`输入图片时需设为`image_url`。
  * `input_audio`输入音频时需设为`input_audio`。
  * `video`输入图片列表形式的视频时需设为`video`。
  * `video_url`输入视频文件时需设为`video_url`。

> Qwen-VL仅部分模型可输入视频文件，详情参见[视频理解（Qwen-VL）](https://help.aliyun.com/zh/model-studio/vision#80dbf6ca8fh6s)；QVQ与Qwen-Omni 模型支持直接传入视频文件。

**text**` _string_` __ 输入的文本。当`type`为`text`时，是必选参数。 **image_url**` _object_` 输入的图片信息。当`type`为`image_url`时是必选参数。 **属性** __ **url** `_string_`**（必选）** 图片的 URL或 Base64 Data URL。传入本地文件请参考[视觉理解](https://help.aliyun.com/zh/model-studio/vision#647c6397db430)。 **input_audio**` _object_` 输入的音频信息。当`type`为`input_audio`时是必选参数。 **属性** __ **data** `_string_`**（必选）** 音频的 URL 或Base64 Data URL。传入本地文件请参见：[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。**format**` _string_`**（必选）** 输入音频的格式，如`mp3`、`wav`等。 **video**` _array_` __ 输入的**图片列表形式的视频信息** 。当`type`为`video`时是必选参数。使用方法请参见：[视频理解（Qwen-VL）](https://help.aliyun.com/zh/model-studio/vision#80dbf6ca8fh6s)、[视频理解（QVQ）](https://help.aliyun.com/zh/model-studio/visual-reasoning#e6df293d5565g)或[视频理解（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni#0f4360d63a8nk)。示例值： ---
```json
[
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
]
```
  **video_url**` _object_` __ 输入的视频文件信息。当`type`为`video_url`时是必选参数。Qwen-VL 只可理解视频文件的视觉信息，Qwen-Omni 可理解视频文件中的视觉与音频信息。 **属性** __ **url** `_string_`**（必选）** 视频文件的公网 URL 或 Base64 Data URL。输入本地视频文件请参见[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。 **min_pixels**` _integer_` __ （可选）设定输入图像的最小像素阈值。当输入图像或视频帧的像素小于`min_pixels`时，会将其进行放大，直到总像素高于`min_pixels`。

  * 适用模型：QVQ、Qwen-VL
  * 取值范围：如下所示 **min_pixels 取值范围** __
    * `Qwen3-VL`：默认值和最小值均为：`65536`
    * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值和最小值均为4096
    * QVQ 及其他 Qwen2.5-VL 模型：默认值和最小值均为`3136`
  * 示例值：`{"type": "image_url","image_url": {"url":"https://xxxx.jpg"},"min_pixels": 65536}`

**max_pixels**` _integer_` __ （可选）用于设定输入图像或视频帧的最大像素阈值。当输入图像或视频的像素在`[min_pixels, max_pixels]`区间内时，模型会按原图进行识别。当输入图像像素大于`max_pixels`时，会将图像进行缩小，直到总像素低于`max_pixels`。

  * 适用模型：QVQ、Qwen-VL
  * 取值范围：如下所示 **max_pixels 取值范围** __ max_pixels的取值与是否开启`vl_high_resolution_images`参数有关。
    * 当`vl_high_resolution_images`为`False`时：
      * `Qwen3-VL`：默认值为`2621440`，最大值为：`16777216`
      * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值为`1310720`，最大值为：`16777216`
      * `QVQ`及其他`Qwen2.5-VL`模型：默认值为`1003520` ，最大值为`12845056`
    * 当`vl_high_resolution_images`为`True`时：
      * `Qwen3-VL`、`qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：`max_pixels`无效，输入图像的最大像素固定为`16777216`
      * `QVQ`及其他`Qwen2.5-VL`模型：`max_pixels`无效，输入图像的最大像素固定为`12845056`
  * 示例值：`{"type": "image_url","image_url": {"url":"https://xxxx.jpg"},"max_pixels": 8388608}`

**cache_control**` _object_` __ （可选）用于开启显式缓存。相关文档：[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)。 **属性** __ **type** `_string_`**（必选）** 仅支持设定为`ephemeral`。 **role**` _string_` __**（必选）** 用户消息的角色，固定为`user`。 Assistant Message `_object_` __ （可选）模型的回复。通常用于在多轮对话中作为上下文回传给模型。 **属性** __ **content**` _string_` __ （可选）模型回复的文本内容。包含`tool_calls`时，`content`可以为空；否则`content`为必选。**role**` _string_` __**（必选）** 助手消息的角色，固定为`assistant`。**partial**` _boolean_` __ （可选）默认值为`false`是否开启[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)。可选值：

  * true：开启；
  * false：不开启。

**支持的模型** __

  * **通义千问 Max 系列**qwen3-max、qwen3-max-2025-09-23、qwen3-max-preview（非思考模式）、qwen-max、qwen-max-latest、qwen-max-2024-09-19及之后的快照模型
  * **通义千问 Plus 系列（非思考模式）**qwen-plus、qwen-plus-latest、qwen-plus-2024-09-19及之后的快照模型
  * **通义千问 Flash 系列（非思考模式）**qwen-flash、qwen-flash-2025-07-28及之后的快照模型
  * **通义千问 Coder 系列**qwen3-coder-plus、qwen3-coder-flash、qwen3-coder-480b-a35b-instruct、qwen3-coder-30b-a3b-instruct、qwen-coder-plus、qwen-coder-plus-latest、qwen-coder-plus-2024-11-06、qwen-coder-turbo、qwen-coder-turbo-latest、qwen-coder-turbo-2024-09-19、qwen2.5-coder-32b-instruct、qwen2.5-coder-14b-instruct、qwen2.5-coder-7b-instruct、qwen2.5-coder-3b-instruct、qwen2.5-coder-1.5b-instruct、qwen2.5-coder-0.5b-instruct
  * **通义千问 VL 系列**
    * **qwen3-vl-plus 系列（非思考模式）** qwen3-vl-plus、qwen3-vl-plus-2025-09-23及之后的快照模型
    * **qwen3-vl-flash 系列（非思考模式）** qwen3-vl-flash、qwen3-vl-flash-2025-10-15及之后的快照模型
    * **qwen-vl-max 系列** qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2024-08-09及之后的快照模型
    * **qwen-vl-plus 系列** qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2024-08-09及之后的快照模型
  * **通义千问 Turbo 系列（非思考模式）**qwen-turbo、qwen-turbo-latest、qwen-turbo-2024-09-19及之后的快照模型
  * **通义千问开源系列** Qwen3 开源模型（非思考模式）、qwen2.5-72b-instruct、qwen2.5-32b-instruct、qwen2.5-14b-instruct、qwen2.5-7b-instruct、qwen2.5-3b-instruct、qwen2.5-1.5b-instruct、qwen2.5-0.5b-instruct、Qwen3-VL开源模型（非思考模式）
  * **通义千问 Math 系列**qwen-math-plus、qwen-math-plus-latest、qwen-math-plus-0919、qwen-math-turbo、qwen-math-turbo-latest、qwen-math-turbo-0919、qwen2.5-math-72b-instruct、qwen2.5-math-7b-instruct、qwen2.5-math-1.5b-instruct

**tool_calls** `_array_` __ （可选）发起 Function Calling 后，返回的工具与入参信息，包含一个或多个对象。由上一轮模型响应的`tool_calls`字段获得。 **属性** __ **id** `_string_` __**（必选）** 工具响应的ID。**type** `_string_`**（必选）** 工具类型，当前只支持设为`function`。**function** `_object_`**（必选）** 工具与入参信息。 **属性** __ **name** `_string_`**（必选）** 工具名称。**arguments** `_string_`**（必选）** 入参信息，为JSON格式字符串。 **index** `_integer_`**（必选）** 当前工具信息在`tool_calls`数组中的索引。 Tool Message `_object_` __ （可选）工具的输出信息。 **属性** __ **content**` _string_` __**（必选）** 工具函数的输出内容，必须为字符串。若工具返回结构化数据（如JSON），需将其序列化为字符串。**role**` _string_` __**（必选）** 固定为`tool`。**tool_call_id**` _string_` __**（必选）** 发起 Function Calling 后返回的 id，通过completion.choices[0].message.tool_calls[$index].id获取，用于标记 Tool Message 对应的工具。
**stream**` _boolean_` __ （可选） 默认值为 `false`是否以流式输出方式回复。相关文档：[流式输出](https://help.aliyun.com/zh/model-studio/stream)可选值：

  * `false`：模型生成全部内容后一次性返回；
  * `true`：边生成边输出，每生成一部分内容即返回一个数据块（chunk）。需实时逐个读取这些块以拼接完整回复。

推荐设置为`true`，可提升阅读体验并降低超时风险。
**stream_options**` _object_` __ （可选）流式输出的配置项，仅在 `stream` 为 `true` 时生效。 **属性** __ **include_usage**` _boolean_` __ （可选）默认值为`false`是否在响应的**最后一个数据块** 包含Token消耗信息。可选值：

  * `true`：包含；
  * `false`：不包含。

> 流式输出时，Token 消耗信息仅可出现在响应的最后一个数据块。

**modalities**`array` __ （可选）默认值为`["text"]`输出数据的模态，仅适用于 Qwen-Omni 模型。相关文档：[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni)可选值：

  * `["text","audio"]`：输出文本与音频；
  * `["text"]`：仅输出文本。


**audio**` _object_` __ （可选）输出音频的音色与格式，仅适用于 Qwen-Omni 模型，且`modalities`参数需为`["text","audio"]`。相关文档：[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni) **属性** __ **voice**` _string_` **（必选）** 输出音频的音色。请参见[音色列表](https://help.aliyun.com/zh/model-studio/qwen-omni#a447c4fbf5ul0)。**format**` _string_` **（必选）** 输出音频的格式，仅支持设定为`wav`。
**temperature**` _float_` __ （可选） __ 采样温度，控制模型生成文本的多样性。temperature越高，生成的文本更多样，反之，生成的文本更确定。取值范围： [0, 2)temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。更多说明，请参见[文本生成模型概述](https://help.aliyun.com/zh/model-studio/text-generation#ad7b336bec5fw)。 **temperature 默认值** __ Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen-turbo系列（非思考模式）、qwen开源系列、qwen-coder系列、qwq-32b-preview、qwen-doc-turbo、qwen-vl-max-2025-08-13、Qwen3-VL（非思考模式）：0.7；qwen3-max-preview（思考模式）、qwen-long、qwen-omni-turbo系列：1.0；QVQ系列 、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15 : 0.5；其余qwen-vl系列、qwen-omni-turbo系列、qvq-72b-preview：0.01；qwen-math系列：0；Qwen3（思考模式）、Qwen3-Thinking、Qwen3-Omni-Captioner、QwQ 系列：0.6；qwen-plus-character：0.92qwen3-omni-flash系列：0.9Qwen3-VL（思考模式）：0.8

> 不建议修改QVQ模型的默认temperature值 。

**top_p**` _float_` __ （可选）核采样的概率阈值，控制模型生成文本的多样性。top_p越高，生成的文本更多样。反之，生成的文本更确定。取值范围：（0,1.0]temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。更多说明，请参见[文本生成模型概述](https://help.aliyun.com/zh/model-studio/text-generation#ad7b336bec5fw)。 **top_p 默认值** __ Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen-turbo系列（非思考模式）、Qwen 2.5开源系列、qwen-coder系列、qwen-long、qwq-32b-preview、qwen-doc-turbo、qwen-vl-max-2025-08-13、Qwen3-VL（非思考）：0.8；qwen-vl-max-2024-11-19、qwen-vl-max-2024-10-30、qwen-vl-max-2024-08-09、qwen2-vl-72b-instruct、qwen-omni-turbo 系列：0.01；qwen-vl-plus系列、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-04-08、qwen-vl-max-2025-04-02、qwen-vl-max-2025-01-25、qwen-vl-max-2024-12-30、qvq-72b-preview、qwen2-vl-2b-instruct、qwen2-vl-7b-instruct、qwen2.5-vl-3b-instruct、qwen2.5-vl-7b-instruct、qwen2.5-vl-32b-instruct、qwen2.5-vl-72b-instruct、qwen2.5-omni-7b：0.001；QVQ系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15 、qwen2-audio-instruct: 0.5；qwen3-max-preview（思考模式）、qwen-math系列、Qwen3-Omni-Flash系列：1.0；Qwen3（思考模式）、Qwen3-VL（思考模式）、Qwen3-Thinking、QwQ 系列、Qwen3-Omni-Captioner、qwen-plus-character：0.95

> 不建议修改QVQ模型的默认 top_p 值。

**top_k**` _integer_` __ （可选）指定生成过程中用于采样的候选 Token 数量。值越大，输出越随机；值越小，输出越确定。若设为 `null` 或大于 100，则禁用 `top_k` 策略，仅 `top_p` 策略生效。取值必须为大于或等于 0 的整数。 **top_k 默认值** __ QVQ系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15：10；QwQ 系列：40；qwen-math 系列、其余qwen-vl-plus系列、qwen-vl-max-2025-08-13之前的模型、qwen-audio-turbo系列、qwen2.5-omni-7b、qvq-72b-preview：1；Qwen3-Omni-Flash系列：50；其余模型均为20。

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：extra_body={"top_k":xxx}。

> 不建议修改QVQ模型的默认 top_k 值。

**presence_penalty** `_float_` __ （可选）控制模型生成文本时的内容重复度。取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。 **presence_penalty 默认值** __ qwen3-max-preview（思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、qwen3-0.6b/1.7b/4b（思考模式）、QVQ系列、qwen-max、qwen-max-latest、qwen-max-latest、qwen-max-2024-09-19、qwen2.5-vl系列、qwen-vl-max系列、qwen-vl-plus、qwen2-vl-72b-instruct、qwen-vl-plus-2025-01-02、Qwen3-VL（非思考）：1.5；qwen-vl-plus-latest、qwen-vl-plus-2025-08-15、qwen-vl-plus-2025-07-10：1.2qwen-vl-plus-2025-01-25：1.0；qwen3-8b/14b/32b/30b-a3b/235b-a22b（思考模式）、qwen-plus/qwen-plus-latest/2025-04-28（思考模式）、qwen-turbo/qwen-turbo/2025-04-28（思考模式）：0.5；其余均为0.0。 **原理介绍** __ 如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。 **示例** __ 提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。

> 使用qwen-vl-plus-2025-01-25模型进行文字提取时，建议设置presence_penalty为1.5。

> 不建议修改QVQ模型的默认presence_penalty值。

**response_format**` _object_` （可选） 默认值为`{"type": "text"}`返回内容的格式。可选值：

  * `{"type": "text"}`：输出文字回复；
  * `{"type": "json_object"}`：输出标准格式的JSON字符串。
  * `{"type": "json_schema","json_schema": {...} }`：输出指定格式的JSON字符串。

> 相关文档：[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)。

> 若指定为`{"type": "json_object"}`，需在提示词中明确指示模型输出JSON，如：“请按照json格式输出”，否则会报错。

> 支持的模型参见[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)。

**属性** __ **type**` _string_` __**（必选）** 返回内容的格式。可选值：

  * `text`：输出文字回复；
  * `json_object`：输出标准格式的JSON字符串；
  * `json_schema`：输出指定格式的JSON字符串。

**json_schema**` _object_` __ 当 type 为 json_schema 时，该字段为必选，用于定义结构化输出的配置。 **属性** __ **name**` _string_` __**（必选）** Schema 的唯一标识名称。仅支持字母（不区分大小写）、数字、下划线和短横线，最长 64 个字符。**description**` _string_` __ （可选）描述 Schema 的用途，帮助模型理解输出的语义上下文。**schema**` _object_` __ （可选）符合 JSON Schema 标准的对象，定义模型输出的数据结构。

> 构建JSON Schema 方法参加：[JSON Schema](https://json-schema.org/)

**strict**` _boolean_`**** （可选）默认值为`false`控制是否强制模型严格遵守 Schema 的所有约束。

  * **true（推荐）** 模型严格遵循字段类型、必填项、格式等所有约束，确保输出 100% 合规。
  * **false（不推荐）** 模型仅大致遵循 Schema，可能生成不符合规范的输出，导致验证失败。


**max_input_tokens**` _integer_` __ （可选）允许输入的最大 Token 长度。目前仅支持qwen-plus-0728/latest模型。

  * qwen-plus-latest 默认值：129,024

> 后续默认值可能调整至1,000,000。

  * qwen-plus-2025-07-28 默认值：1,000,000

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"max_input_tokens": xxx}`。

**max_tokens**` _integer_` __ （可选）用于限制模型输出的最大 Token 数。若生成内容超过此值，生成将提前停止，且返回的`finish_reason`为`length`。默认值与最大值均为模型的最大输出长度，请参见[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。适用于需控制输出长度的场景，如生成摘要、关键词，或用于降低成本、缩短响应时间。触发 `max_tokens `时，响应的 finish_reason 字段为 `length`。

> `max_tokens`不限制思考模型思维链的长度。

**vl_high_resolution_images**` _boolean_` __ （可选）默认值为`false`是否将输入图像的像素上限提升至 16384 Token 对应的像素值。相关文档：[处理高分辨率图像](https://help.aliyun.com/zh/model-studio/vision#e7e2db755f9h7)。

  * `vl_high_resolution_images：true`，使用固定分辨率策略，忽略 `max_pixels` 设置，超过此分辨率时会将图像总像素缩小至此上限内。 **点击查看各模型像素上限** __ `vl_high_resolution_images`为`True`时，不同模型像素上限不同：
    * `Qwen3-VL系列`、`qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`模型：`16777216`（每`Token`对应`32*32`像素，即`16384*32*32`）
    * `QVQ系列`、其他`Qwen2.5-VL系列`模型：`12845056`（每`Token`对应`28*28`像素，即 `16384*28*28`）
  * `vl_high_resolution_images`为`false`，实际分辨率由 `max_pixels` 与默认上限共同决定，取二者计算结果的最大值。超过此像素上限时会将图像缩小至此上限内。 **点击查看各模型的默认像素上限** __ `vl_high_resolution_images`为`false`时，不同模型默认像素上限不同：
    * `Qwen3-VL系列`：`2621440`(`2560*32*32`，即默认`Token`上限为`2560`)
    * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`模型：`1310720`(`1280*32*32`，即默认`Token`上限为`1280`)
    * `QVQ系列`、其他`Qwen2.5-VL系列`模型：`1003520`(`1280*28*28`，即默认`Token`上限为`1280`)

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：extra_body={"vl_high_resolution_images":xxx}。

**n**` _integer_` __ （可选） 默认值为1生成响应的数量，取值范围是`1-4`。适用于需生成多个候选响应的场景，例如创意写作或广告文案。

> 仅支持 qwen-plus、 [Qwen3（非思考模式）](https://help.aliyun.com/zh/model-studio/deep-thinking#be9890136awsc)、qwen-plus-character 模型。

> 若传入 `tools` 参数， 请将`n` 设为 1。

> 增大 n 会增加输出 Token 的消耗，但不增加输入 Token 消耗。

**enable_thinking** `_boolean_` （可选）使用混合思考（回复前既可思考也可不思考）模型时，是否开启思考模式。适用于 Qwen3 、Qwen3-Omni-Flash、Qwen3-VL模型。相关文档：[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)可选值：

  * `true`：开启

> 开启后，思考内容将通过`reasoning_content`字段返回。

  * `false`：不开启

不同模型的默认值：[支持的模型](https://help.aliyun.com/zh/model-studio/deep-thinking#78286fdc35hlw)

> 通该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"enable_thinking": xxx}`。

**thinking_budget** `_integer_` （可选）思考过程的最大 Token 数。适用于Qwen3-VL、Qwen3 的商业版与开源版模型。相关文档：[限制思考长度](https://help.aliyun.com/zh/model-studio/deep-thinking#e7c0002fe4meu)。默认值为模型最大思维链长度，请参见：[模型列表](https://help.aliyun.com/zh/model-studio/models)

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"thinking_budget": xxx}`。

**enable_code_interpreter** `_boolean_` （可选）默认值为 `false`是否开启代码解释器功能。仅当`model`为`qwen3-max-preview`且`enable_thinking`为`true`时生效。相关文档：[代码解释器](https://help.aliyun.com/zh/model-studio/qwen-code-interpreter)可选值：

  * `true`：开启
  * `false`：不开启

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"enable_code_interpreter": xxx}`。

**seed**` _integer_` __ （可选）随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 `seed` 且其他参数不变，模型将尽可能返回相同结果。取值范围：`[0,231−1]`。 **seed 默认值** __ qwen-vl-plus-2025-01-02、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-04-08、qwen-vl-max-2025-04-02、qwen-vl-max-2024-12-30、qvq-72b-preview、qvq-max系列：3407；qwen-vl-max-2025-01-25、qwen-vl-max-2024-11-19、qwen-vl-max-2024-10-30、qwen-vl-max-2024-08-09、qwen-vl-max-2024-02-01、qwen2-vl-72b-instruct、qwen2-vl-2b-instruct、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2025-05-07、qwen-vl-plus-2025-01-25、qwen-vl-plus-2024-08-09、qwen-vl-plus-2023-12-01：无默认值；其余模型均为1234。
**logprobs** `_boolean_` （可选）默认值为 `false`是否返回输出 Token 的对数概率，可选值：

  * `true`返回
  * `false`不返回

> 思考阶段生成的内容（`reasoning_content`）不会返回对数概率。

**支持的模型** __

  * qwen-plus系列的快照模型（不包含主线模型）
  * qwen-turbo 系列的快照模型（不包含主线模型）
  * Qwen3 开源模型


**top_logprobs** `_integer_` （可选）默认值为0指定在每一步生成时，返回模型最大概率的候选 Token 个数。取值范围：[0,5]仅当 `logprobs` 为 `true` 时生效。
**stop**` _string 或 array_` __ （可选）用于指定停止词。当模型生成的文本中出现`stop` 指定的字符串或`token_id`时，生成将立即终止。可传入敏感词以控制模型的输出。

> stop为数组时，不可将`token_id`和字符串同时作为元素输入，比如不可以指定为`["你好",104307]`。

**tools**` _array_` __ （可选）包含一个或多个工具对象的数组，供模型在 Function Calling 中调用。相关文档：[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)设置 tools 且模型判断需要调用工具时，响应会通过 tool_calls 返回工具信息。 **属性** __ **type**` _string_` __**（必选）** 工具类型，当前仅支持设为`function`。**function**` _object_` __**（必选）** **属性** __ **name**` _string_` __**（必选）** 工具名称。仅允许字母、数字、下划线（`_`）和短划线（`-`），最长 64 个 Token。**description**` _string_` __**（必选）** 工具描述信息，帮助模型判断何时以及如何调用该工具。**parameters**` _object_` __**（必选）** 工具的参数描述，需要是一个合法的JSON Schema。JSON Schema的描述可以见[链接](https://json-schema.org/understanding-json-schema)。若`parameters`参数为空，表示该工具没有入参（如时间查询工具）。
**tool_choice** `_string 或 object_` __ （可选）默认值为 `auto`工具选择策略。若需对某类问题强制指定工具调用方式（例如始终使用某工具或禁用所有工具），可设置此参数。可选值：

  * `auto`大模型自主选择工具策略。
  * `none`若不希望进行工具调用，可设定`tool_choice`参数为`none`；
  * `{"type": "function", "function": {"name": "the_function_to_call"}}`若希望强制调用某个工具，可设定`tool_choice`参数为`{"type": "function", "function": {"name": "the_function_to_call"}}`，其中`the_function_to_call`是指定的工具函数名称。

> 思考模式的模型不支持强制调用某个工具。


**parallel_tool_calls** `_boolean_` （可选）默认值为 `false`是否开启并行工具调用。相关文档：[并行工具调用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#cb6b5c484bt4x)可选值：

  * `true`：开启
  * `false`：不开启


**enable_search** ****`_boolean_` __ （可选）默认值为 `false`是否开启联网搜索。相关文档：[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)可选值：

  * `true`：开启；

> 若开启后未联网搜索，可优化提示词，或设置`search_options`中的`forced_search`参数开启强制搜索。

  * `false`：不开启。

> 启用互联网搜索功能可能会增加 Token 的消耗。

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"enable_search": True}`。

**search_options**` _object_`**** （可选）联网搜索的策略。相关文档：[联网搜索](https://help.aliyun.com/zh/model-studio/web-search) **属性** __ **forced_search** `_boolean_`（可选）默认值为`false`是否强制开启联网搜索，仅当`enable_search`为`true`时生效。可选值：

  * true：强制开启；
  * false：不强制开启，由模型判断是否联网搜索。

**search_strategy** `_string_`（可选）默认值为`turbo`搜索量级策略，仅当`enable_search`为`true`时生效。可选值：

  * `turbo` （默认）: 兼顾响应速度与搜索效果，适用于大多数场景。
  * `max`: 采用更全面的搜索策略，可调用多源搜索引擎，以获取更详尽的搜索结果，但响应时间可能更长。
  * `agent`：可多次调用联网搜索工具与大模型，实现多轮信息检索与内容整合。

> `agent`策略仅适用于 qwen3-max 与 qwen3-max-2025-09-23。

> `agent`策略不可与其他联网搜索策略同时设定。

**enable_search_extension** `_boolean_`（可选）默认值为`false`是否开启垂域搜索，仅当`enable_search`为`true`时生效。可选值：

  * `true`：开启。
  * `false`：不开启。

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra_body** 对象中。配置方式为：`extra_body={"search_options": xxx}`。

|
**X-DashScope-DataInspection**` _string_` （可选）在通义千问 API 的内容安全能力基础上，是否进一步识别输入输出内容的违规信息。取值如下：

  * `'{"input":"cip","output":"cip"}'`：进一步识别；
  * 不设置该参数：不进一步识别。

通过 HTTP 调用时请放入请求头：`-H "X-DashScope-DataInspection: {\"input\": \"cip\", \"output\": \"cip\"}"`；通过 Python SDK 调用时请通过`extra_headers`配置：`extra_headers={'X-DashScope-DataInspection': '{"input":"cip","output":"cip"}'}`。详细使用方法请参见[内容审核](https://help.aliyun.com/zh/model-studio/content-security)。

> 不支持通过 Node.js SDK设置。

> 不适用于 Qwen-VL 系列模型。

|

### chat响应对象（非流式输出）

|  ---
```json
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "我是阿里云开发的一款超大规模语言模型，我叫通义千问。"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 3019,
        "completion_tokens": 104,
        "total_tokens": 3123,
        "prompt_tokens_details": {
            "cached_tokens": 2048
        }
    },
    "created": 1735120033,
    "system_fingerprint": null,
    "model": "qwen-plus",
    "id": "chatcmpl-6ada9ed2-7f33-9de2-8bb0-78bd4035025a"
}
```

---|---
**id**` _string_` 本次调用的唯一标识符。
**choices**` _array_` 模型生成内容的数组。 **属性** __ **finish_reason**` _string_` 模型停止生成的原因。有三种情况：

  * 触发输入参数中的`stop`参数，或自然停止输出时为`stop`；
  * 生成长度过长而结束为`length`；
  * 需要调用工具而结束为`tool_calls`。

**index**` _integer_` 当前对象在`choices`数组中的索引。**logprobs**` _object_` 模型输出的 Token 概率信息。 **属性** __ **content** `_array_` 包含每个 Token 及其对数概率的数组。 **属性** __ **token** `_string_` 当前 Token 的文本。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容（例如表情符号或中文字符）。**logprob** `_float_` 当前 Token 的对数概率。返回值为 `null` 表示概率值极低。**top_logprobs** `_array_` 当前 Token 位置最可能的若干候选 Token，数量与请求参数`top_logprobs`保持一致。每个元素包含： **属性** __ **token** `_string_` 候选 Token 文本。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容（例如表情符号或中文字符）。**logprob** `_float_` 该候选 Token 的对数概率。返回值为 null 表示概率值极低。 **message**` _object_` 模型输出的消息。 **属性** __ **content** `_string_` 模型的回复内容。**reasoning_content** `_string_` 模型的思维链内容。**refusal** `_string_` 该参数当前固定为`null`。**role** `_string_` 消息的角色，固定为`assistant`。**audio** `_object_` 该参数当前固定为`null`。**function_call** （即将废弃）` _object_` 该值固定为`null`，请参考`tool_calls`参数。**tool_calls** `_array_` 在发起 Function Calling后，模型生成的工具与入参信息。 **属性** __ **id** `_string_` 本次工具响应的唯一标识符。**type** `_string_` 工具类型，当前只支持`function`。**function** `_object_` 工具信息。 **属性** __ **name** `_string_` 工具名称。**arguments** `_string_` 入参信息，为JSON格式字符串。

> 由于大模型响应有一定随机性，输出的入参信息可能不符合函数签名。请在调用前校验参数有效性

**index** `_integer_` 当前工具在`tool_calls`数组中的索引。
**created**` _integer_` 请求创建时的 Unix 时间戳（秒）。
**model**` _string_` 本次请求使用的模型。
**object** `_string_` 始终为`chat.completion`。
**service_tier** `_string_` 该参数当前固定为`null`。
**system_fingerprint**` _string_` 该参数当前固定为`null`。
**usage** `_object_` 本次请求的 Token 消耗信息。 **属性** __ **completion_tokens** `_integer_` 模型输出的 Token 数。**prompt_tokens** `_integer_` 输入的 Token 数。**total_tokens** `_integer_` 消耗的总 Token 数，为`prompt_tokens`与`completion_tokens`的总和。**completion_tokens_details** `_object_` 使用[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)时输出Token的细粒度分类。 **属性** __ **audio_tokens** `_integer_` 该参数当前固定为`null`。**reasoning_tokens** `_integer_` 该参数当前固定为`null`。**text_tokens** `_integer_`[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)输出文本的Token数。 **prompt_tokens_details** `_object_` 输入 Token 的细粒度分类。 **属性** __ **audio_tokens** `_integer_` 该参数当前固定为`null`。**cached_tokens** `_integer_` 命中 Cache 的 Token 数。Context Cache 详情请参见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。**text_tokens** `_integer_`[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)输入的文本 Token 数。**image_tokens** `_integer_`[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)输入的图像 Token数。**video_tokens** `_integer_`[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)输入的视频文件或者图像列表 Token 数。**cache_creation** `_object_`[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)创建信息。 **属性** __ **ephemeral_5m_input_tokens** `_integer_` 创建显式缓存的 Token 数。 **cache_creation_input_tokens** `_integer_` 创建显式缓存的 Token 数。**cache_type** `_string_` 使用[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)时，参数值为`ephemeral`，否则该参数不存在。

### chat响应chunk对象（流式输出）

|  ---
```json
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"","function_call":null,"refusal":null,"role":"assistant","tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"我是","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"来自","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"阿里","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"云的超大规模","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"语言模型，我","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"叫通义千","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"问。","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[{"delta":{"content":"","function_call":null,"refusal":null,"role":null,"tool_calls":null},"finish_reason":"stop","index":0,"logprobs":null}],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":null}
{"id":"chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57","choices":[],"created":1735113344,"model":"qwen-plus","object":"chat.completion.chunk","service_tier":null,"system_fingerprint":null,"usage":{"completion_tokens":17,"prompt_tokens":22,"total_tokens":39,"completion_tokens_details":null,"prompt_tokens_details":{"audio_tokens":null,"cached_tokens":0}}}
```

---|---
**id**` _string_` 本次调用的唯一标识符。每个chunk对象有相同的 id。
**choices**` _array_` 模型生成内容的数组，可包含一个或多个对象。若设置`include_usage`参数为`true`，则`choices`在最后一个chunk中为空数组。 **属性** __ **delta** `_object_` 请求的增量对象。 **属性** __ **content** `_string_` 增量消息内容。**reasoning_content** `_string_` 增量思维链内容。**function_call** `_object_` 该值默认为`null`，请参考`tool_calls`参数。**audio**` _object_` 使用 [Qwen-Omni](https://help.aliyun.com/zh/model-studio/qwen-omni) 模型时生成的回复。 **属性** __ **data** `_string_` 增量的 Base64 音频编码数据。**expires_at** `_integer_` 创建请求时的时间戳。 **refusal** `_object_` 该参数当前固定为`null`。**role** `_string_` 增量消息对象的角色，只在第一个chunk中有值。**tool_calls** `_array_` 在发起 Function Calling后，模型生成的工具与入参信息。 **属性** __ **index** `_integer_` 当前工具在`tool_calls`数组中的索引。**id** `_string_` 本次工具响应的唯一标识符。**function** `_object_` 被调用的工具信息。 **属性** __ **arguments** `_string_` 增量的入参信息，所有chunk的`arguments`拼接后为完整的入参。

> 由于大模型响应有一定随机性，输出的入参信息可能不符合函数签名。请在调用前校验参数有效性。

**name** `_string_` 工具名称，只在第一个chunk中有值。 **type** `_string_` 工具类型，当前只支持`function`。 **finish_reason** `_string_` 模型停止生成的原因。有四种情况：

  * 因触发输入参数中的`stop`参数，或自然停止输出时为`stop`；
  * 生成未结束时为`null`；
  * 生成长度过长而结束为`length`；
  * 需要调用工具而结束为`tool_calls`。

**index** `_integer_` 当前响应在`choices`数组中的索引。当输入参数 n 大于1时，需根据本参数进行不同响应对应的完整内容的拼接。**logprobs**` _object_` 当前对象的概率信息。 **属性** __ **content** `_array_` 带有对数概率信息的 Token 数组。 **属性** __ **token** `_string_` 当前 Token。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。**logprob** `_float_` 当前 Token 的对数概率。返回值为 null 表示概率值极低。**top_logprobs** `_array_` 当前 Token 位置最可能的若干个 Token 及其对数概率，元素个数与入参的`top_logprobs`保持一致。 **属性** __ **token** `_string_` 当前 Token。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。**logprob** `_float_` 当前 Token 的对数概率。返回值为 null 表示概率值极低。
**created**` _integer_` 本次请求被创建时的时间戳。每个chunk有相同的时间戳。
**model**` _string_` 本次请求使用的模型。
**object** `_string_` 始终为`chat.completion.chunk`。
**service_tier** `_string_` 该参数当前固定为`null`。
**system_fingerprint**` _string_` 该参数当前固定为`null`。
**usage** `_object_` 本次请求消耗的Token。只在`include_usage`为`true`时，在最后一个chunk显示。 **属性** __ **completion_tokens** `_integer_` 模型输出的 Token 数。**prompt_tokens** `_integer_` 输入 Token 数。**total_tokens** `_integer_` 总 Token 数，为`prompt_tokens`与`completion_tokens`的总和。**completion_tokens_details** `_object_` 输出 Token 的详细信息。 **属性** __ **audio_tokens**` _integer_`[Qwen-Omni 模型](https://help.aliyun.com/zh/model-studio/qwen-omni)输出的音频 Token 数。**reasoning_tokens** `_integer_` 思考过程 Token 数。**text_tokens**` _integer_` 输出文本 Token 数。 **prompt_tokens_details** `_object_` 输入 Token的细粒度分类。 **属性** __ **audio_tokens** `_integer_` 输入音频的 Token 数。

> 视频文件中的音频 Token 数通过本参数返回。

**text_tokens** `_integer_` 输入文本的 Token 数。**video_tokens** `_integer_` 输入视频（图片列表形式或视频文件）的 Token 数。**image_tokens** `_integer_` 输入图片的 Token 数。**cached_tokens** `_integer_` 命中缓存的 Token 数。Context Cache 详情请参见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。**cache_creation** `_object_`[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)创建信息。 **属性** __ **ephemeral_5m_input_tokens** `_integer_` 创建显式缓存的 Token 数。 **cache_creation_input_tokens** `_integer_` 创建显式缓存的 Token 数。**cache_type** `_string_` 缓存类型，固定为`ephemeral`。

## DashScope

北京地域

新加坡地域

金融云

__

__

HTTP 请求地址：

  * 通义千问大语言模型：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

  * 通义千问VL/Audio模型：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用无需配置 `base_url`。

HTTP 请求地址：

  * 通义千问大语言模型：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

  * 通义千问VL模型：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

Python代码

Java代码

__

__

---

```python
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
```


  * **方式一：**

---

```java
import com.alibaba.dashscope.protocol.Protocol;
Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope-intl.aliyuncs.com/api/v1");
```


  * **方式二：**

---

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";
```


HTTP 请求地址：

  * 通义千问大语言模型：`POST https://dashscope-finance.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

  * 通义千问VL模型：`POST https://dashscope-finance.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

Python代码

Java代码

__

__

---

```python
dashscope.base_http_api_url = 'https://dashscope-finance.aliyuncs.com/api/v1'
```


  * **方式一：**

---

```java
import com.alibaba.dashscope.protocol.Protocol;
Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope-finance.aliyuncs.com/api/v1");
```


  * **方式二：**

---

```java
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {
        Constants.baseHttpApiUrl="https://dashscope-finance.aliyuncs.com/api/v1";
    }
}
```


> 您需要已[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过DashScope SDK进行调用，需要[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk#f3e80b21069aa)。

### 请求体

| 文本输入流式输出图像输入视频输入音频输入联网搜索工具调用异步调用文档理解 --- PythonJavaPHP（HTTP）Node.js（HTTP）C#（HTTP）Go（HTTP）curl --- ---
```python
import os
import dashscope

messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': '你是谁？'}
]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    result_format='message'
    )
print(response)
```
  ---
```java
// 建议dashscope SDK的版本 >= 2.12.0
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
        System.exit(0);
    }
}
```
  ---
```php
<?php

$url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
$apiKey = getenv('DASHSCOPE_API_KEY');

$data = [
    // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    "model" => "qwen-plus",
    "input" => [
        "messages" => [
            [
                "role" => "system",
                "content" => "You are a helpful assistant."
            ],
            [
                "role" => "user",
                "content" => "你是谁？"
            ]
        ]
    ],
    "parameters" => [
        "result_format" => "message"
    ]
];

$jsonData = json_encode($data);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer $apiKey",
    "Content-Type: application/json"
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($httpCode == 200) {
    echo "Response: " . $response;
} else {
    echo "Error: " . $httpCode . " - " . $response;
}

curl_close($ch);
?>
```
  DashScope 未提供 Node.js 环境的 SDK。如需通过 OpenAI Node.js SDK调用，请参考本文的OpenAI章节。 ---
```nodejs
import fetch from 'node-fetch';

const apiKey = process.env.DASHSCOPE_API_KEY;

const data = {
    model: "qwen-plus", // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    input: {
        messages: [
            {
                role: "system",
                content: "You are a helpful assistant."
            },
            {
                role: "user",
                content: "你是谁？"
            }
        ]
    },
    parameters: {
        result_format: "message"
    }
};

fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => {
    console.log(JSON.stringify(data));
})
.catch(error => {
    console.error('Error:', error);
});
```
  ---
```csharp
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
            return;
        }

        // 设置请求 URL 和内容
        string url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
        // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        string jsonContent = @"{
            ""model"": ""qwen-plus"",
            ""input"": {
                ""messages"": [
                    {
                        ""role"": ""system"",
                        ""content"": ""You are a helpful assistant.""
                    },
                    {
                        ""role"": ""user"",
                        ""content"": ""你是谁？""
                    }
                ]
            },
            ""parameters"": {
                ""result_format"": ""message""
            }
        }";

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```
  DashScope 未提供 Go 的 SDK。如需通过 OpenAI Go SDK调用，请参考本文的OpenAI-Go章节。 ---
```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type Input struct {
	Messages []Message `json:"messages"`
}

type Parameters struct {
	ResultFormat string `json:"result_format"`
}

type RequestBody struct {
	Model      string     `json:"model"`
	Input      Input      `json:"input"`
	Parameters Parameters `json:"parameters"`
}

func main() {
	// 创建 HTTP 客户端
	client := &http.Client{}

	// 构建请求体
	requestBody := RequestBody{
		// 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
		Model: "qwen-plus",
		Input: Input{
			Messages: []Message{
				{
					Role:    "system",
					Content: "You are a helpful assistant.",
				},
				{
					Role:    "user",
					Content: "你是谁？",
				},
			},
		},
		Parameters: Parameters{
			ResultFormat: "message",
		},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		log.Fatal(err)
	}

	// 创建 POST 请求
	req, err := http.NewRequest("POST", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal(err)
	}

	// 设置请求头
	// 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey := "sk-xxx"
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	// 读取响应体
	bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	// 打印响应内容
	fmt.Printf("%s\n", bodyText)
}
```
  ---
```curl
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```


> 相关文档：[流式输出](https://help.aliyun.com/zh/model-studio/stream)。

文本生成模型多模态模型 --- PythonJavacurl --- ---
```python
import os
import dashscope

messages = [
    {'role':'system','content':'you are a helpful assistant'},
    {'role': 'user','content': '你是谁？'}
]
responses = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    result_format='message',
    stream=True,
    incremental_output=True
    )
for response in responses:
    print(response)
```
  ---
```java
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import io.reactivex.Flowable;
import java.lang.System;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static void handleGenerationResult(GenerationResult message) {
        System.out.println(JsonUtils.toJson(message));
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(Arrays.asList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .incrementalOutput(true)
                .build();
    }
    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
            streamCallWithMessage(gen, userMsg);
        } catch (ApiException | NoApiKeyException | InputRequiredException  e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```
  ---
```curl
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--header "X-DashScope-SSE: enable" \
--data '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message",
        "incremental_output":true
    }
}'
```
  PythonJavacurl --- ---
```python
import os
from dashscope import MultiModalConversation
import dashscope

# 若使用新加坡地域的模型，请取消下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
            {"text": "图中描绘的是什么景象?"}
        ]
    }
]

responses = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3-vl-plus',  # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages,
    stream=True,
    incremental_output=True
    )

full_content = ""
print("流式输出内容为：")
for response in responses:
    if response.output.choices[0].message.content:
        print(response.output.choices[0].message.content[0]['text'])
        full_content += response.output.choices[0].message.content[0]['text']
print(f"完整内容为：{full_content}")
```
  ---
```java
import java.util.Arrays;
import java.util.Collections;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import io.reactivex.Flowable;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 若使用新加坡地域的模型，请取消下列注释
    //  static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}

    public static void streamCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                        Collections.singletonMap("text", "图中描绘的是什么景象？"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-vl-plus")  // 可按需更换为其它多模态模型，并修改相应的 messages
                .messages(Arrays.asList(userMessage))
                .incrementalOutput(true)
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(item -> {
            try {
                var content = item.getOutput().getChoices().get(0).getMessage().getContent();
                    // 判断content是否存在且不为空
                if (content != null &&  !content.isEmpty()) {
                    System.out.println(content.get(0).get("text"));
                    }
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```
  ---
```curl
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3-vl-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                    {"text": "图中描绘的是什么景象？"}
                ]
            }
        ]
    },
    "parameters": {
        "incremental_output": true
    }
}'
```


> 关于大模型分析图像的更多用法，请参见[视觉理解](https://help.aliyun.com/zh/model-studio/vision)。

PythonJavacurl --- ---
```python
import os
import dashscope

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png"},
            {"text": "这些是什么?"}
        ]
    }
]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-vl-max', # 此处以qwen-vl-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
    )
print(response)
```
  ---
```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"),
                        Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"),
                        Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png"),
                        Collections.singletonMap("text", "这些是什么?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-vl-plus")
                .message(userMessage)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```
  ---
```curl
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-vl-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
                    {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
                    {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png"},
                    {"text": "这些是什么?"}
                ]
            }
        ]
    }
}'
```


> 以下为传入视频帧的示例代码，关于更多用法（如传入视频文件），请参见[视觉理解](https://help.aliyun.com/zh/model-studio/vision#80dbf6ca8fh6s)。

PythonJavacurl --- ---
```python
from http import HTTPStatus
import os
# dashscope版本需要不低于1.20.10
import dashscope

messages = [{"role": "user",
             "content": [
                 {"video":["https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                           "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                           "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                           "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"]},
                 {"text": "描述这个视频的具体过程"}]}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen-vl-max-latest',  # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
)
if response.status_code == HTTPStatus.OK:
    print(response)
else:
    print(response.code)
    print(response.message)
```
  ---
```java
// DashScope SDK版本需要不低于2.16.7
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
public class Main {
    // 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    private static final String MODEL_NAME = "qwen-vl-max-latest";
    public static void videoImageListSample() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMessage = MultiModalMessage.builder()
                .role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "You are a helpful assistant.")))
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("video", Arrays.asList("https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                                "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                                "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                                "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg")),
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model(MODEL_NAME).message(systemMessage)
                .message(userMessage).build();
        MultiModalConversationResult result = conv.call(param);
        System.out.print(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            videoImageListSample();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen-vl-max-latest",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "video": [
              "https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
              "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
              "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
              "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"
            ]
          },
          {
            "text": "描述这个视频的具体过程"
          }
        ]
      }
    ]
  }
}'
```
  音频理解 ---

> 关于大模型分析音频的更多用法，请参见[音频理解-Qwen-Audio](https://help.aliyun.com/zh/model-studio/audio-language-model)。

PythonJavacurl --- ---
```python
import os
import dashscope

messages = [
    {
        "role": "user",
        "content": [
            {"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"},
            {"text": "这段音频在说什么?"}
        ]
    }
]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen2-audio-instruct', # 此处以qwen2-audio-instruct为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
    )
print(response)
```
  ---
```java
import java.util.Arrays;
import java.util.Collections;
import java.lang.System;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"),
                        Collections.singletonMap("text", "这段音频在说什么?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen2-audio-instruct为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen2-audio-instruct")
                .message(userMessage)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```
  ---
```curl
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen2-audio-instruct",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": [
                    {"text": "You are a helpful assistant."}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"},
                    {"text": "这段音频在说什么?"}
                ]
            }
        ]
    }
}'
```
  PythonJavacurl --- ---
```python
import os
import dashscope

messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': '杭州明天天气是什么？'}
    ]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    enable_search=True,
    result_format='message'
    )
print(response)
```
  ---
```java
// 建议dashscope SDK的版本 >= 2.12.0
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("明天杭州什么天气？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .enableSearch(true)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
        System.exit(0);
    }
}
```
  ---
```curl
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "明天杭州天气如何？"
            }
        ]
    },
    "parameters": {
        "enable_search": true,
        "result_format": "message"
    }
}'
```


> 完整的Function Calling 流程代码请参见[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#0f0fcbd808d8o)。

PythonJavacurl --- ---
```python
import os
import dashscope

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                }
            },
            "required": [
                "location"
            ]
        }
    }
]
messages = [{"role": "user", "content": "杭州天气怎么样"}]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-plus',  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    tools=tools,
    result_format='message'
)
print(response)
```
  ---
```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import com.alibaba.dashscope.aigc.conversation.ConversationParam.ResultFormat;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.tools.FunctionDefinition;
import com.alibaba.dashscope.tools.ToolFunction;
import com.alibaba.dashscope.utils.JsonUtils;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.github.victools.jsonschema.generator.Option;
import com.github.victools.jsonschema.generator.OptionPreset;
import com.github.victools.jsonschema.generator.SchemaGenerator;
import com.github.victools.jsonschema.generator.SchemaGeneratorConfig;
import com.github.victools.jsonschema.generator.SchemaGeneratorConfigBuilder;
import com.github.victools.jsonschema.generator.SchemaVersion;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Main {
    public class GetWeatherTool {
        private String location;
        public GetWeatherTool(String location) {
            this.location = location;
        }
        public String call() {
            return location+"今天是晴天";
        }
    }
    public class GetTimeTool {
        public GetTimeTool() {
        }
        public String call() {
            LocalDateTime now = LocalDateTime.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            String currentTime = "当前时间：" + now.format(formatter) + "。";
            return currentTime;
        }
    }
    public static void SelectTool()
            throws NoApiKeyException, ApiException, InputRequiredException {
        SchemaGeneratorConfigBuilder configBuilder =
                new SchemaGeneratorConfigBuilder(SchemaVersion.DRAFT_2020_12, OptionPreset.PLAIN_JSON);
        SchemaGeneratorConfig config = configBuilder.with(Option.EXTRA_OPEN_API_FORMAT_VALUES)
                .without(Option.FLATTENED_ENUMS_FROM_TOSTRING).build();
        SchemaGenerator generator = new SchemaGenerator(config);
        ObjectNode jsonSchema_weather = generator.generateSchema(GetWeatherTool.class);
        ObjectNode jsonSchema_time = generator.generateSchema(GetTimeTool.class);
        FunctionDefinition fdWeather = FunctionDefinition.builder().name("get_current_weather").description("获取指定地区的天气")
                .parameters(JsonUtils.parseString(jsonSchema_weather.toString()).getAsJsonObject()).build();
        FunctionDefinition fdTime = FunctionDefinition.builder().name("get_current_time").description("获取当前时刻的时间")
                .parameters(JsonUtils.parseString(jsonSchema_time.toString()).getAsJsonObject()).build();
        Message systemMsg = Message.builder().role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant. When asked a question, use tools wherever possible.")
                .build();
        Message userMsg = Message.builder().role(Role.USER.getValue()).content("杭州天气").build();
        List<Message> messages = new ArrayList<>();
        messages.addAll(Arrays.asList(systemMsg, userMsg));
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(messages)
                .resultFormat(ResultFormat.MESSAGE)
                .tools(Arrays.asList(
                        ToolFunction.builder().function(fdWeather).build(),
                        ToolFunction.builder().function(fdTime).build()))
                .build();
        Generation gen = new Generation();
        GenerationResult result = gen.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            SelectTool();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(String.format("Exception %s", e.getMessage()));
        }
        System.exit(0);
    }
}
```
  ---
```curl
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-plus",
    "input": {
        "messages": [{
            "role": "user",
            "content": "杭州天气怎么样"
        }]
    },
    "parameters": {
        "result_format": "message",
        "tools": [{
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "当你想知道现在的时间时非常有用。",
                "parameters": {}
            }
        },{
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "当你想查询指定城市的天气时非常有用。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                        }
                    }
                },
                "required": ["location"]
            }
        }]
    }
}'
```
  ---
```python
# 您的Dashscope Python SDK版本需要不低于 1.19.0。
import asyncio
import platform
import os
from dashscope.aigc.generation import AioGeneration

async def main():
    response = await AioGeneration.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[{"role": "user", "content": "你是谁"}],
        result_format="message",
    )
    print(response)

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
```
  PythonJavacurl --- ---
```python
import os
import dashscope

messages = [
        {'role': 'system', 'content': 'you are a helpful assisstant'},
        # 请将 '{FILE_ID}'替换为您实际对话场景所使用的 fileid
        {'role':'system','content':f'fileid://{FILE_ID}'},
        {'role': 'user', 'content': '这篇文章讲了什么'}]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-long",
    messages=messages,
    result_format='message'
)
print(response)
```
  ---
```java
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {

    public static GenerationResult callWithFile() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();

        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("you are a helpful assistant")
                .build();

        Message fileSystemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                // 请将 '{FILE_ID}'替换为您实际对话场景所使用的 file-id
                .content("fileid://{FILE_ID}")
                .build();

        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("这篇文章讲了什么")
                .build();

        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-long")
                .messages(Arrays.asList(systemMsg, fileSystemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();

        return gen.call(param);
    }

    public static void main(String[] args) {
        try {
            GenerationResult result = callWithFile();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("调用 DashScope API 出错: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```


> 请将 {FILE_ID}替换为您实际对话场景所使用的 file-id

---
```curl
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-long",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "system",
                "content": "fileid://{FILE_ID}"
            },
            {
                "role": "user",
                "content": "这篇文章讲了什么？"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

---|---
**model**` _string_` __**（必选）** 模型名称。支持的模型：Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、通义千问Audio、数学模型。**具体模型名称和计费，请参见**[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。
**messages**` _array_` __**（必选）** 传递给大模型的上下文，按对话顺序排列。

> 通过HTTP调用时，请将**messages** 放入 **input** 对象中。

**消息类型** __ System Message****`_object_`（可选）系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在`messages`数组的第一位。

> QwQ模型不建议设置 System Message，QVQ 模型设置 System Message不会生效。

**属性** __ **content**` _string_`**（必选）** 消息内容。**role**` _string_` __**（必选）** 系统消息的角色，固定为`system`。 User Message****`_object_`**（必选）** 用户消息，用于向模型传递问题、指令或上下文等。 **属性** __ **content**` _string 或 array_`**（必选）** 消息内容。若输入只有文本，则为 string 类型；若输入包含图像等多模态数据，或启用显式缓存，则为 array 类型。 **属性** __ **text**` _string_`**（必选）** 输入的文本。**image**` _string_`（可选）指定用于图片理解的图像文件，图像支持以下三种方式传入：

  * 公网 URL：公网可访问的图像链接
  * 图片的 Base64 编码，格式为 `data:image/<format>;base64,<data>`
  * 本地文件：本地文件的绝对路径

适用模型：[Qwen-VL](https://help.aliyun.com/zh/model-studio/vision#f18fc2bb52wxo)、[QVQ](https://help.aliyun.com/zh/model-studio/visual-reasoning#f18fc2bb52wxo)示例值：`{"image":"https://xxxx.jpeg"}`**video**` _array 或 string_`（可选）使用[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)或[QVQ模型](https://help.aliyun.com/zh/model-studio/visual-reasoning)传入的视频。

  * 若传入图像列表，则为` _array_`类型；
  * 若传入视频文件，则为` _string_`类型 _。_

传入本地文件请参见[本地文件（Qwen-VL）](https://help.aliyun.com/zh/model-studio/vision#f18fc2bb52wxo)或[本地文件（QVQ）](https://help.aliyun.com/zh/model-studio/visual-reasoning#f18fc2bb52wxo)。示例值：

  * 图像列表：`{"video":["https://xx1.jpg",...,"https://xxn.jpg"]} `
  * 视频文件：`{"video":"https://xxx.mp4"} `

**fps**` _float_` __ （可选）每秒抽帧数。取值范围为 [0.1, 10]，默认值为2.0。有两个功能：

  * 输入视频文件时，控制抽帧频率，每 fps1​秒抽取一帧。

> 适用于[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)与[QVQ模型](https://help.aliyun.com/zh/model-studio/visual-reasoning)。

  * 告知模型相邻帧之间的时间间隔，帮助其更好地理解视频的时间动态。同时适用于输入视频文件与图像列表时。该功能同时支持视频文件和图像列表输入，适用于事件时间定位或分段内容摘要等场景。

> 支持`Qwen2.5-VL`、`Qwen3-VL`模型与QVQ模型。

示例值如下：

  * 图像列表传入：`{"video":["https://xx1.jpg",...,"https://xxn.jpg"]，"fps":2}`
  * 视频文件传入：`{"video": "https://xx1.mp4"，"fps":2}`

较大的`fps`适合高速运动的场景（如体育赛事、动作电影等），较小的`fps`适合长视频或内容偏静态的场景。

> OpenAI 兼容协议不支持设置该值。视频文件默认每间隔0.5秒抽取一帧，图像列表默认是以每隔0.5秒从视频中抽取出来的。

**audio**` _string_`

> 模型为音频理解时，是必选参数，如模型为qwen2-audio-instruct等。

使用音频理解功能时，传入的音频文件。示例值：`{"audio":"https://xxx.mp3"}`**min_pixels**` _integer_` __ （可选）设定输入图像或视频帧的最小像素阈值。当输入图像或视频帧的像素小于`min_pixels`时，会将其进行放大，直到总像素高于`min_pixels`。

  * **输入图像：**
    * 适用模型：QVQ、Qwen-VL模型支持
    * 取值范围：如下所示 **min_pixels 取值范围** __
      * `Qwen3-VL`：默认值和最小值均为65536
      * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值和最小值均为`4096`
      * `QVQ` 及其他 `Qwen2.5-VL` 模型：默认值和最小值均为`3136`
    * 示例值：`{"image":"https://xxxx.jpg", "min_pixels": 65536}`
  * **输入视频文件或图像列表：**
    * 适用模型：`qwen3-vl-plus`系列模型支持
    * 取值范围：默认值为`65536`，最小值为`4096`
    * 示例值：
      * 输入视频文件时：`{"video":"https://xxxx.mp4","min_pixels": 65536}`
      * 输入图像列表时：`{"video":["https://xx1.jpg",...,"https://xxn.jpg"]，"min_pixels": 65536}`

> OpenAI 兼容协议仅支持在传入图像时设置该参数。

**max_pixels**` _integer_` __ （可选）用于设定输入图像或视频帧的最大像素阈值。当输入图像或视频的像素在`[min_pixels, max_pixels]`区间内时，模型会按原图进行识别。当输入图像像素大于`max_pixels`时，会将图像进行缩小，直到总像素低于`max_pixels`。

  * **输入图像：**
    * 适用模型：QVQ、Qwen-VL 模型支持
    * 取值范围：如下所示 **max_pixels 取值范围** __ `max_pixels`的取值与是否开启`vl_high_resolution_images`参数有关。
      * 当`vl_high_resolution_images`为`False`时：
        * `Qwen3-VL`：默认值为`2621440`，最大值为：`16777216`
        * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815`、`qwen-vl-plus-0710`：默认值为`1310720`，最大值为：`16777216`
        * `QVQ`及其他`Qwen2.5-VL`模型：默认值为`1003520` ，最大值为`12845056`
      * 当`vl_high_resolution_images`为`True`时：
        * `Qwen3-VL`、`qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815`、`qwen-vl-plus-0710`：`max_pixels`无效，输入图像的最大像素固定为`16777216`
        * `QVQ`及其他`Qwen2.5-VL`模型：max_pixels无效，输入图像的最大像素固定为`12845056`
    * 示例值：`{"image":"https://xxxx.jpg", "max_pixels": 8388608}`
  * **输入视频文件或图像列表：**
    * 适用模型：`qwen3-vl-plus`系列模型支持
    * 取值范围：默认值为`655360`，最大值为`2048000`
    * 示例值：
      * 输入视频文件时：`{"video":"https://xxxx.mp4","max_pixels": 655360}`
      * 输入图像列表时：`{"video":["https://xx1.jpg",...,"https://xxn.jpg"]，"max_pixels": 655360}`

> OpenAI 兼容协议仅支持在传入图像时设置该参数。

**total_pixels**` _integer_` __ （可选）用于限制从视频中抽取的所有帧的总像素（单帧图像像素 × 总帧数）。如果视频总像素超过此限制，系统将对视频帧进行缩放，但仍会确保单帧图像的像素值在 `[min_pixels, max_pixels]` 范围内。

  * 适用模型：`qwen3-vl-plus`系列模型支持。
  * 取值说明：默认值和最小值均为`134217728`，该值对应 `131072` 个图像 Token（每 32×32 像素对应 1 个图像 Token）。
  * 示例值：
    * 输入视频文件时：`{"video":"https://xxxx.mp4","total_pixels": 134217728}`
    * 输入图像列表时：`{"video":["https://xx1.jpg",...,"https://xxn.jpg"]，"total_pixels": 134217728}`

对于抽帧数量较多的长视频，可适当降低此值以减少Token消耗和处理时间，但这可能会导致图像细节丢失。**cache_control**` _object_` __**（可选）** 仅支持[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)的模型支持，用于开启显式缓存。 **属性** __ **type** `_string_`**（必选）** 固定为`ephemeral`。 **role**` _string_` __**（必选）** 用户消息的角色，固定为`user`。 Assistant Message `_object_` __ （可选）模型对用户消息的回复。 **属性** __ **content**` _string_` __ （可选）消息内容。仅当助手消息中指定`tool_calls`参数时非必选。**role**` _string_` __**（必选）** 固定为`assistant`。**partial**` _boolean_` __ （可选）是否开启前缀续写。相关文档：[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)。 **支持的模型** __

  * **通义千问 Max 系列**qwen3-max、qwen3-max-2025-09-23、qwen3-max-preview（非思考模式）、qwen-max、qwen-max-latest、qwen-max-2024-09-19及之后的快照模型
  * **通义千问 Plus 系列（非思考模式）**qwen-plus、qwen-plus-latest、qwen-plus-2024-09-19及之后的快照模型
  * **通义千问 Flash 系列（非思考模式）**qwen-flash、qwen-flash-2025-07-28及之后的快照模型
  * **通义千问 Coder 系列**qwen3-coder-plus、qwen3-coder-flash、qwen3-coder-480b-a35b-instruct、qwen3-coder-30b-a3b-instruct、qwen-coder-plus、qwen-coder-plus-latest、qwen-coder-plus-2024-11-06、qwen-coder-turbo、qwen-coder-turbo-latest、qwen-coder-turbo-2024-09-19、qwen2.5-coder-32b-instruct、qwen2.5-coder-14b-instruct、qwen2.5-coder-7b-instruct、qwen2.5-coder-3b-instruct、qwen2.5-coder-1.5b-instruct、qwen2.5-coder-0.5b-instruct
  * **通义千问 VL 系列**
    * **qwen3-vl-plus 系列（非思考模式）** qwen3-vl-plus、qwen3-vl-plus-2025-09-23及之后的快照模型
    * **qwen3-vl-flash 系列（非思考模式）** qwen3-vl-flash、qwen3-vl-flash-2025-10-15及之后的快照模型
    * **qwen-vl-max 系列** qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2024-08-09及之后的快照模型
    * **qwen-vl-plus 系列** qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2024-08-09及之后的快照模型
  * **通义千问 Turbo 系列（非思考模式）**qwen-turbo、qwen-turbo-latest、qwen-turbo-2024-09-19及之后的快照模型
  * **通义千问开源系列** Qwen3 开源模型（非思考模式）、qwen2.5-72b-instruct、qwen2.5-32b-instruct、qwen2.5-14b-instruct、qwen2.5-7b-instruct、qwen2.5-3b-instruct、qwen2.5-1.5b-instruct、qwen2.5-0.5b-instruct、Qwen3-VL开源模型（非思考模式）
  * **通义千问 Math 系列**qwen-math-plus、qwen-math-plus-latest、qwen-math-plus-0919、qwen-math-turbo、qwen-math-turbo-latest、qwen-math-turbo-0919、qwen2.5-math-72b-instruct、qwen2.5-math-7b-instruct、qwen2.5-math-1.5b-instruct

**tool_calls** `_array_` __ （可选）发起 Function Calling 后，返回的工具与入参信息，包含一个或多个对象。由上一轮模型响应的`tool_calls`字段获得。 **属性** __ **id** `_string_` __ 工具响应的ID。**type** `_string_` 工具类型，当前只支持设为`function`。**function** `_object_` 工具与入参信息。 **属性** __ **name** `_string_` 工具名称。**arguments** `_string_` 入参信息，为JSON格式字符串。 **index** `_integer_` 当前工具信息在`tool_calls`数组中的索引。 Tool Message****`_object_`（可选）工具的输出信息。 **属性** __ **content**` _string_` __**（必选）** 工具函数的输出内容，必须为字符串格式。**role**` _string_` __**（必选）** 固定为`tool`。**tool_call_id**` _string_` __**（可选）** 发起 Function Calling 后返回的 id，可以通过`response.output.choices[0].message.tool_calls[$index]["id"]`获取，用于标记 Tool Message 对应的工具。
**temperature**` _float_` __ （可选）采样温度，控制模型生成文本的多样性。temperature越高，生成的文本更多样，反之，生成的文本更确定。取值范围： [0, 2) **temperature 默认值** __

  * Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen-turbo系列（非思考模式）、qwen开源系列、qwen-coder系列、qwen2-audio-instruct、qwen-doc-turbo、qwen-vl-max-2025-08-13、Qwen3-VL（非思考）：0.7；
  * QVQ系列 、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15 : 0.5；
  * qwen-audio-turbo系列：0.00001；
  * qwen-vl系列、qwen2.5-omni-7b、qvq-72b-preview：0.01；
  * qwen-math系列：0；
  * Qwen3（思考模式）、Qwen3-Thinking、Qwen3-Omni-Captioner、QwQ 系列：0.6；
  * qwen3-max-preview（思考模式）、qwen-long系列： 1.0；
  * qwen-plus-character：0.92
  * qwen3-omni-flash系列：0.9
  * Qwen3-VL（思考模式）：0.8

> 通过HTTP调用时，请将 **temperature** 放入 **parameters** 对象中。

> 不建议修改QVQ模型的默认 temperature 值。

**top_p**` _float_` __ （可选）核采样的概率阈值，控制模型生成文本的多样性。top_p越高，生成的文本更多样。反之，生成的文本更确定。取值范围：（0,1.0]。 **top_p 默认值** __ Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen-turbo系列（非思考模式）、qwen开源系列、qwen-coder系列、qwen-long、qwen-doc-turbo、qwq-32b-preview、qwen-audio-turbo系列、qwen-vl-max-2025-08-13、Qwen3-VL（非思考模式）：0.8；qwen-vl-max-2024-11-19、qwen-vl-max-2024-10-30、qwen-vl-max-2024-08-09、qwen2-vl-72b-instruct、qwen-omni-turbo 系列：0.01；qwen-vl-plus系列、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-04-08、qwen-vl-max-2025-04-02、qwen-vl-max-2025-01-25、qwen-vl-max-2024-12-30、qvq-72b-preview、qwen2-vl-2b-instruct、qwen2-vl-7b-instruct、qwen2.5-vl-3b-instruct、qwen2.5-vl-7b-instruct、qwen2.5-vl-32b-instruct、qwen2.5-vl-72b-instruct：0.001；QVQ系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15 、qwen2-audio-instruct：0.5；qwen3-max-preview（思考模式）、qwen-math系列、Qwen3-Omni-Flash系列：1.0；Qwen3（思考模式）、Qwen3-VL（思考模式）、Qwen3-Thinking、QwQ 系列、Qwen3-Omni-Captioner、qwen-plus-character：0.95

> Java SDK中为**topP** _。_ 通过HTTP调用时，请将 **top_p** 放入 **parameters** 对象中。

> 不建议修改QVQ模型的默认 top_p 值。

**top_k**` _integer_` __ （可选）生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。取值需要大于或等于0。 **top_k 默认值** __ QVQ系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15：10；QwQ 系列：40；qwen-math 系列、其余qwen-vl-plus系列、qwen-vl-max-2025-08-13之前的模型、qwen-audio-turbo系列、qwen2.5-omni-7b、qvq-72b-preview：1；Qwen3-Omni-Flash系列：50其余模型均为20；

> Java SDK中为**topK** _。_ 通过HTTP调用时，请将 **top_k** 放入 **parameters** 对象中。

> 不建议修改QVQ模型的默认 top_k 值。

**enable_thinking** `_boolean_` （可选）使用混合思考模型时，是否开启思考模式，适用于 Qwen3 、Qwen3-VL模型。相关文档：[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)可选值：

  * `true`：开启

> 开启后，思考内容将通过`reasoning_content`字段返回。

  * `false`：不开启

不同模型的默认值：[支持的模型](https://help.aliyun.com/zh/model-studio/deep-thinking#78286fdc35hlw)

> Java SDK 为enableThinking；通过HTTP调用时，请将 **enable_thinking** **** 放入 **parameters** 对象中。

**thinking_budget** `_integer_` （可选）思考过程的最大长度。适用于Qwen3-VL、Qwen3 的商业版与开源版模型。相关文档：[限制思考长度](https://help.aliyun.com/zh/model-studio/deep-thinking#e7c0002fe4meu)。默认值为模型最大思维链长度，请参见：[模型列表](https://help.aliyun.com/zh/model-studio/models)

> Java SDK 为 thinkingBudget。通过HTTP调用时，请将 **thinking_budget** **** 放入 **parameters** 对象中。

> 默认值为模型最大思维链长度。

**enable_code_interpreter** `_boolean_` （可选）默认值为 `false`是否开启代码解释器功能。仅适用于思考模式下的 qwen3-max-preview。相关文档：[代码解释器](https://help.aliyun.com/zh/model-studio/qwen-code-interpreter)可选值：

  * `true`：开启
  * `false`：不开启

> 不支持 Java SDK。通过HTTP调用时，请将 **enable_code_interpreter** **** 放入 **parameters** 对象中。

**repetition_penalty**` _float_` __ （可选）模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。没有严格的取值范围，只要大于0即可。 **repetition_penalty 默认值** __

  * qwen-max、qwen-max-latest、qwen-max-2024-09-19、qwen-math系列、qwen-vl-max系列、qvq-72b-preview、qwen2-vl-72b-instruct、qwen-vl-plus-2025-01-02、qwen-vl-plus-2025-05-07、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15、qwen-vl-plus-latest、qwen2.5-vl-3b-instruct、qwen2.5-vl-7b-instruct、qwen2.5-vl-32b-instruct、qwen2.5-vl-72b-instruct、qwen-audio-turbo-latest、qwen-audio-turbo-2024-12-04、QVQ系列、QwQ系列、qwq-32b-preview、Qwen3-VL： 1.0；
  * qwen-coder系列、qwen2.5-1.5b-instruct、qwen2.5-0.5b-instruct、qwen2-1.5b-instruct、qwen2-0.5b-instruct、qwen2-vl-2b-instruct、qwen2-vl-7b-instruct、qwen-vl-plus-2024-08-09、qwen-vl-plus-2023-12-01、qwen2.5-omni-7b、qwen2-audio-instruct：1.1；
  * qwen-vl-plus、qwen-vl-plus-2025-01-25：1.2；
  * 其余模型为1.05。

> Java SDK中为**repetitionPenalty** _。_ 通过HTTP调用时，请将 **repetition_penalty** 放入 **parameters** 对象中。

> 使用qwen-vl-plus_2025-01-25模型进行文字提取时，建议设置repetition_penalty为1.0。

> 不建议修改QVQ模型的默认 repetition_penalty 值。

**presence_penalty**` _float_` __ （可选）控制模型生成文本时的内容重复度。取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。 **presence_penalty 默认值** __ qwen3-max-preview（思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、qwen3-0.6b/1.7b/4b（思考模式）、QVQ系列、qwen-max、qwen-max-latest、qwen-max-latest、qwen-max-2024-09-19、qwen2.5-vl系列、qwen-vl-max系列、qwen-vl-plus、qwen2-vl-72b-instruct、qwen-vl-plus-2025-01-02、Qwen3-VL（非思考）：1.5；qwen-vl-plus-latest、qwen-vl-plus-2025-08-15、qwen-vl-plus-2025-07-10：1.2qwen-vl-plus-2025-01-25：1.0；qwen3-8b/14b/32b/30b-a3b/235b-a22b（思考模式）、qwen-plus/qwen-plus-latest/2025-04-28（思考模式）、qwen-turbo/qwen-turbo/2025-04-28（思考模式）：0.5；其余均为0.0。 **原理介绍** __ 如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。 **示例** __ 提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。

> 使用qwen-vl-plus-2025-01-25模型进行文字提取时，建议设置presence_penalty为1.5。

> 不建议修改QVQ模型的默认presence_penalty值。

> Java SDK不支持设置该参数 _。_ 通过HTTP调用时，请将 **presence_penalty** 放入 **parameters** 对象中。

**vl_high_resolution_images**` _boolean_` __ （可选）默认值为`false`是否将输入图像的像素上限提升至 16384 Token 对应的像素值。相关文档：[处理高分辨率图像](https://help.aliyun.com/zh/model-studio/vision#e7e2db755f9h7)。

  * `vl_high_resolution_images：true`，使用固定分辨率策略，忽略 `max_pixels` 设置，超过此分辨率时会将图像总像素缩小至此上限内。 **点击查看各模型像素上限** __ `vl_high_resolution_images`为`True`时，不同模型像素上限不同：
    * `Qwen3-VL系列`、`qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`模型：`16777216`（每`Token`对应`32*32`像素，即`16384*32*32`）
    * `QVQ系列`、其他`Qwen2.5-VL系列`模型：`12845056`（每`Token`对应`28*28`像素，即 `16384*28*28`）
  * `vl_high_resolution_images`为`false`，实际分辨率由 `max_pixels` 与默认上限共同决定，取二者计算结果的最大值。超过此像素上限时会将图像缩小至此上限内。 **点击查看各模型的默认像素上限** __ `vl_high_resolution_images`为`false`时，不同模型默认像素上限不同：
    * `Qwen3-VL系列`：`2621440`(`2560*32*32`，即默认`Token`上限为`2560`)
    * `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`模型：`1310720`(`1280*32*32`，即默认`Token`上限为`1280`)
    * `QVQ系列`、其他`Qwen2.5-VL系列`模型：`1003520`(`1280*28*28`，即默认`Token`上限为`1280`)

> Java SDK 为 **vlHighResolutionImages** （需要的最低版本为2.20.8**）** _。_ 通过HTTP调用时，请将 **vl_high_resolution_images** 放入 **parameters** 对象中。

**vl_enable_image_hw_output**` _boolean_` __ （可选）默认值为 `false`是否返回图像缩放后的尺寸。模型会对输入的图像进行缩放处理，配置为 True 时会返回图像缩放后的高度和宽度，开启流式输出时，该信息在最后一个数据块（chunk）中返回。支持[Qwen-VL模型](https://help.aliyun.com/zh/model-studio/vision)。

> Java SDK中为 **vlEnableImageHwOutput** ，Java SDK最低版本为2.20.8 _。_ 通过HTTP调用时，请将 **vl_enable_image_hw_output** 放入 **parameters** 对象中。

**max_input_tokens**` _integer_` __ （可选）允许输入的最大 Token 长度。目前仅支持qwen-plus-0728/latest模型。

  * qwen-plus-latest 默认值：129,024

> 后续默认值可能调整至1,000,000。

  * qwen-plus-2025-07-28 默认值：1,000,000

> Java SDK 暂不支持该参数。通过HTTP调用时，请将 **max_input_tokens** 放入 **parameters** 对象中。

**max_tokens**` _integer_` __ （可选）用于限制模型输出的最大 Token 数。若生成内容超过此值，生成将提前停止，且返回的`finish_reason`为`length`。默认值与最大值均为模型的最大输出长度，请参见[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。适用于需控制输出长度的场景，如生成摘要、关键词，或用于降低成本、缩短响应时间。触发 `max_tokens `时，响应的 finish_reason 字段为 `length`。

> `max_tokens`不限制思考模型思维链的长度。

> Java SDK中为**maxTokens** （模型为通义千问VL/Audio时，Java SDK中为**maxLength，** 在 2.18.4 版本之后支持也设置为 maxTokens） _。_ 通过HTTP调用时，请将 **max_tokens** 放入 **parameters** 对象中。

**seed**` _integer_` __ （可选）**** 随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 `seed` 且其他参数不变，模型将尽可能返回相同结果。取值范围：`[0,231−1]`。 **seed 默认值** __ qwen-vl-plus-2025-01-02、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-04-08、qwen-vl-max-2025-04-02、qwen-vl-max-2024-12-30、qvq-72b-preview、qvq-max系列：3407；qwen-vl-max-2025-01-25、qwen-vl-max-2024-11-19、qwen-vl-max-2024-10-30、qwen-vl-max-2024-08-09、qwen-vl-max-2024-02-01、qwen2-vl-72b-instruct、qwen2-vl-2b-instruct、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2025-05-07、qwen-vl-plus-2025-01-25、qwen-vl-plus-2024-08-09、qwen-vl-plus-2023-12-01：无默认值；其余模型均为1234。

> 通过HTTP调用时，请将 **seed** 放入 **parameters** 对象中。

**stream**` _boolean_` __**** （可选） __ 默认值为`false`是否流式输出回复。参数值：

  * false：模型生成完所有内容后一次性返回结果。
  * true：边生成边输出，即每生成一部分内容就立即输出一个片段（chunk）。

> 该参数仅支持Python SDK。通过Java SDK实现流式输出请通过`streamCall`接口调用；通过HTTP实现流式输出请在Header中指定`X-DashScope-SSE`为`enable`。

> Qwen3商业版（思考模式）、Qwen3开源版、QwQ、QVQ只支持流式输出。

**incremental_output**` _boolean_` __ （可选）默认为`false`（Qwen3-Max、Qwen3-VL、[Qwen3 开源版](https://help.aliyun.com/zh/model-studio/models#9d516d17965af)、[QwQ](https://help.aliyun.com/zh/model-studio/deep-thinking) 、[QVQ](https://help.aliyun.com/zh/model-studio/visual-reasoning)模型默认值为 `true`）在流式输出模式下是否开启增量输出。推荐您优先设置为`true`。参数值：

  * false：每次输出为当前已经生成的整个序列，最后一次输出为生成的完整结果。 ---
```plaintext
I
I like
I like apple
I like apple.
```

  * true（推荐）：增量输出，即后续输出内容不包含已输出的内容。您需要实时地逐个读取这些片段以获得完整的结果。 ---
```plaintext
I
like
apple
.
```


> Java SDK中为**incrementalOutput** _。_ 通过HTTP调用时，请将 **incremental_output** 放入 **parameters** 对象中。

> QwQ 模型与思考模式下的 Qwen3 模型只支持设置为 `true`。由于 Qwen3 商业版模型默认值为`false`，您需要在思考模式下手动设置为 `true`。

> Qwen3 开源版模型不支持设置为 `false`。

**response_format**` _object_` （可选） 默认值为`{"type": "text"}`返回内容的格式。可选值：

  * `{"type": "text"}`：输出文字回复；
  * `{"type": "json_object"}`：输出标准格式的JSON字符串。
  * `{"type": "json_schema","json_schema": {...} }`：输出指定格式的JSON字符串。

> 相关文档：[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)。

> 支持的模型参见[支持的模型](https://help.aliyun.com/zh/model-studio/qwen-structured-output#7a8e438e89xeq)。

> 若指定为`{"type": "json_object"}`，需在提示词中明确指示模型输出JSON，如：“请按照json格式输出”，否则会报错。

> Java SDK中为responseFormat _。_ 通过HTTP调用时，请将 **response_format** 放入 **parameters** 对象中。

**属性** __ **type**` _string_` __**（必选）** 返回内容的格式。可选值：

  * `text`：输出文字回复；
  * `json_object`：输出标准格式的JSON字符串；
  * `json_schema`：输出指定格式的JSON字符串。

**json_schema**` _object_` __ 当 type 为 json_schema 时，该字段为必选，用于定义结构化输出的配置。 **属性** __ **name**` _string_` __**（必选）** Schema 的唯一标识名称。仅支持字母（不区分大小写）、数字、下划线和短横线，最长 64 个字符。**description**` _string_` __ （可选）描述 Schema 的用途，帮助模型理解输出的语义上下文。**schema**` _object_` __ （可选）符合 JSON Schema 标准的对象，定义模型输出的数据结构。

> 构建JSON Schema 方法参加：[JSON Schema](https://json-schema.org/)

**strict**` _boolean_`**** （可选）默认值为`false`控制是否强制模型严格遵守 Schema 的所有约束。

  * **true（推荐）** 模型严格遵循字段类型、必填项、格式等所有约束，确保输出 100% 合规。
  * **false（不推荐）** 模型仅大致遵循 Schema，可能生成不符合规范的输出，导致验证失败。


**result_format**` _string_`（可选） __ 默认为`text`（Qwen3-Max、Qwen3-VL、[QwQ](https://help.aliyun.com/zh/model-studio/deep-thinking) 模型、Qwen3 开源模型（除了qwen3-next-80b-a3b-instruct）与 Qwen-Long 模型默认值为 message）返回数据的格式。推荐您优先设置为`message`，可以更方便地进行[多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)。

> 平台后续将统一调整默认值为`message`。

> Java SDK中为**resultFormat** _。_ 通过HTTP调用时，请将 **result_format** 放入 **parameters** 对象中。

> 模型为通义千问VL/QVQ/Audio时，设置`text`不生效。

> Qwen3-Max、Qwen3-VL、思考模式下的 Qwen3 模型只能设置为`message`，由于 Qwen3 商业版模型默认值为`text`，您需要将其设置为`message`。

> 如果您使用 Java SDK 调用Qwen3 开源模型，并且传入了 `text`，依然会以 `message`格式进行返回。

**logprobs** `_boolean_` （可选）默认值为 `false`是否返回输出 Token 的对数概率，可选值：

  * `true`返回
  * `false`不返回

支持以下模型：

  * qwen-plus系列的快照模型（不包含主线模型）
  * qwen-turbo 系列的快照模型（不包含主线模型）
  * Qwen3 开源模型

> 通过HTTP调用时，请将 **logprobs** 放入 **parameters** 对象中。

**top_logprobs** `_integer_` （可选）默认值为0指定在每一步生成时，返回模型最大概率的候选 Token 个数。取值范围：[0,5]仅当 `logprobs` 为 `true` 时生效。

> Java SDK中为**topLogprobs** _。_ 通过HTTP调用时，请将 **top_logprobs** 放入 **parameters** 对象中。

**n**` _integer_` __ （可选） 默认值为1生成响应的个数，取值范围是`1-4`。对于需要生成多个响应的场景（如创意写作、广告文案等），可以设置较大的 n 值。

> 当前仅支持 qwen-plus、 [Qwen3（非思考模式）](https://help.aliyun.com/zh/model-studio/deep-thinking#be9890136awsc)、qwen-plus-character 模型，且在传入 tools 参数时固定为1。

> 设置较大的 n 值不会增加输入 Token 消耗，会增加输出 Token 的消耗。

> 通过HTTP调用时，请将 **n** 放入 **parameters** 对象中。

**stop**` _string 或 array_`（可选） __ 用于指定停止词。当模型生成的文本中出现`stop` 指定的字符串或`token_id`时，生成将立即终止。可传入敏感词以控制模型的输出。

> stop为数组时，不可将`token_id`和字符串同时作为元素输入，比如不可以指定为`["你好",104307]`。

> 通过HTTP调用时，请将 **stop** 放入 **parameters** 对象中。

**tools**` _array_` __ （可选）包含一个或多个工具对象的数组，供模型在 Function Calling 中调用。相关文档：[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)使用 `tools` 时，必须将`result_format`设为`message`。发起 Function Calling，或提交工具执行结果时，都必须设置`tools`参数。 **属性** __ **type**` _string_` __**（必选）** 工具类型，当前仅支持`function`。**function**` _object_` __**（必选）** **属性** __ **name**` _string_` __**（必选）** 工具函数的名称，必须是字母、数字，可以包含下划线和短划线，最大长度为64。**description**` _string_` __**（必选）** 工具函数的描述，供模型选择何时以及如何调用工具函数。**parameters**` _objcet_` __**（必选）** 工具的参数描述，需要是一个合法的JSON Schema。JSON Schema的描述可以见[链接](https://json-schema.org/understanding-json-schema)。如果parameters参数为空，表示function没有入参。

> 通过HTTP调用时，请将 **tools** 放入 **parameters** 对象中。暂时不支持qwen-vl与qwen-audio系列模型。

**tool_choice**` _string 或 object_`（可选）默认值为 `auto`工具选择策略。若需对某类问题强制指定工具调用方式（例如始终使用某工具或禁用所有工具），可设置此参数。

  * `auto`大模型自主选择工具策略；
  * `none`若在特定请求中希望临时禁用工具调用，可设定`tool_choice`参数为`none`；
  * `{"type": "function", "function": {"name": "the_function_to_call"}}`若希望强制调用某个工具，可设定`tool_choice`参数为`{"type": "function", "function": {"name": "the_function_to_call"}}`，其中`the_function_to_call`是指定的工具函数名称。

> 思考模式的模型不支持强制调用某个工具。

> Java SDK中为**toolChoice** _。_ 通过HTTP调用时，请将 **tool_choice** 放入 **parameters** 对象中。

**parallel_tool_calls** `_boolean_` （可选）默认值为 `false`是否开启并行工具调用。可选值：

  * `true`：开启
  * `false`：不开启。

并行工具调用详情请参见：[并行工具调用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#cb6b5c484bt4x)。

> Java SDK中为**parallelToolCalls** _。_ 通过HTTP调用时，请将 **parallel_tool_calls** 放入 **parameters** 对象中。

**enable_search**` _boolean_` __ （可选）**** 默认值为`false`模型在生成文本时是否使用互联网搜索结果进行参考。取值如下：

  * true：启用互联网搜索，模型会将搜索结果作为文本生成过程中的参考信息，但模型会基于其内部逻辑判断是否使用互联网搜索结果。

> 若开启后未联网搜索，可优化提示词，或设置`search_options`中的`forced_search`参数开启强制搜索。

  * false：关闭互联网搜索。

计费信息请参见[计费说明](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599)。

> Java SDK中为**enableSearch** _。_ 通过HTTP调用时，请将 **enable_search** 放入 **parameters** 对象中。

> 启用互联网搜索功能可能会增加 Token 的消耗。

**search_options**` _object_` __ （可选）联网搜索的策略。仅当`enable_search`为`true`时生效。详情参见[联网搜索](https://help.aliyun.com/zh/model-studio/web-search#cbddf5b28bug8)。

> 通过HTTP调用时，请将 **search_options** 放入 **parameters** 对象中。Java SDK中为**searchOptions** 。

**属性** __ **enable_source**` _boolean_`（可选）默认值为`false`在返回结果中是否展示搜索到的信息。参数值：

  * true：展示；
  * false：不展示。

**enable_citation** `_boolean_`（可选）默认值为`false`是否开启[1]或[ref_1]样式的角标标注功能。在`enable_source`为`true`时生效。参数值：

  * true：开启；
  * false：不开启。

**citation_format** `_string_`（可选）默认值为`"[<number>]"`角标样式。在`enable_citation`为`true`时生效。参数值：

  * [<number>]：角标形式为`[1]`；
  * [ref_<number>]：角标形式为`[ref_1]`。

**forced_search** `_boolean_`（可选）默认值为`false`是否强制开启搜索。参数值：

  * true：强制开启；
  * false：不强制开启。

**search_strategy** `_string_`（可选）默认值为`turbo`搜索互联网信息的策略。可选值：

  * `turbo` （默认）: 兼顾响应速度与搜索效果，适用于大多数场景。
  * `max`: 采用更全面的搜索策略，可调用多源搜索引擎，以获取更详尽的搜索结果，但响应时间可能更长。
  * `agent`：可多次调用联网搜索工具与大模型，实现多轮信息检索与内容整合。

> `agent`策略仅适用于 qwen3-max 与 qwen3-max-2025-09-23。

> 启用该策略时，仅支持**返回搜索来源** （`enable_source: true`），其他联网搜索功能不可用。

**enable_search_extension** `_boolean_`（可选）默认值为`false`是否开启特定领域增强。参数值：

  * `true`开启。
  * `false`（默认值）不开启。

**prepend_search_result** `_boolean_`（可选）默认值为`false`在流式输出且`enable_source`为`true`时，可通过`prepend_search_result`配置**第一个返回的数据包** 是否只包含搜索来源信息。可选值：

  * `true`只包含搜索来源信息。
  * `false`（默认值）包含搜索来源信息与大模型回复信息。

> 暂不支持 DashScope Java SDK。

**X-DashScope-DataInspection**` _string_` （可选）在通义千问 API 的内容安全能力基础上，是否进一步识别输入输出内容的违规信息。取值如下：

  * `'{"input":"cip","output":"cip"}'`：进一步识别；
  * 不设置该参数：不进一步识别。

通过 HTTP 调用时请放入请求头：`-H "X-DashScope-DataInspection: {\"input\": \"cip\", \"output\": \"cip\"}"`；通过 Python SDK 调用时请通过`headers`配置：`headers={'X-DashScope-DataInspection': '{"input":"cip","output":"cip"}'}`。详细使用方法请参见[内容审核](https://help.aliyun.com/zh/model-studio/content-security)。

> 不支持通过 Java SDK 设置。

> 不适用于 Qwen-VL、Qwen-Audio 系列模型。

### chat响应对象（流式与非流式输出格式一致）

|  ---
```json
{
  "status_code": 200,
  "request_id": "902fee3b-f7f0-9a8c-96a1-6b4ea25af114",
  "code": "",
  "message": "",
  "output": {
    "text": null,
    "finish_reason": null,
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": "我是阿里云开发的一款超大规模语言模型，我叫通义千问。"
        }
      }
    ]
  },
  "usage": {
    "input_tokens": 22,
    "output_tokens": 17,
    "total_tokens": 39
  }
}
```

---|---
**status_code**` _string_` 本次请求的状态码。200 表示请求成功，否则表示请求失败。

> Java SDK不会返回该参数。调用失败会抛出异常，异常信息为**status_code** 和**message** 的内容。

**request_id**` _string_` 本次调用的唯一标识符。

> Java SDK返回参数为**requestId。**

**code**` _string_` 错误码，调用成功时为空值。

> 只有Python SDK返回该参数。

**output**` _object_` 调用结果信息。 **属性** __ **text**` _string_` 模型生成的回复。当设置输入参数**result_format** 为**text** 时将回复内容返回到该字段。**finish_reason**` _string_` 当设置输入参数**result_format** 为**text** 时该参数不为空。有四种情况：

  * 正在生成时为null；
  * 因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；
  * 因生成长度过长而结束为length；
  * 因发生工具调用为tool_calls。

**choices**` _array_` 模型的输出信息。当result_format为message时返回choices参数。 **属性** __ **finish_reason**` _string_` 有四种情况：

  * 正在生成时为null；
  * 因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；
  * 因生成长度过长而结束为length；
  * 因发生工具调用为tool_calls。

**message**` _object_` 模型输出的消息对象。 **属性** __ **role**` _string_` 输出消息的角色，固定为assistant。**content**` _string 或array_`输出消息的内容。当使用qwen-vl或qwen-audio系列模型时为`array`，其余情况为`string`。

> 如果发起Function Calling，则该值为空。

**属性** __ **text**` _string_` 当使用qwen-vl或qwen-audio系列模型时，输出消息的内容。**image_hw**` _array_` 当Qwen-VL系列模型启用 vl_enable_image_hw_output 参数时，有两种情况：

  * 图像输入：返回图像的高度和高度（数值单位：像素）
  * 视频输入：返回空数组

**reasoning_content** `_string_` 模型的深度思考内容。**tool_calls**` _array_` 若模型需要调用工具，则会生成tool_calls参数。 **属性** __ **function**`object`调用工具的名称，以及输入参数。 **属性** __ **name**` _string_` 调用工具的名称**arguments**` _string_` 需要输入到工具中的参数，为JSON字符串。

> 由于大模型响应有一定随机性，输出的JSON字符串并不总满足于您的函数，建议您在将参数输入函数前进行参数的有效性校验。

**index** `_integer_` 当前**tool_calls** 对象在tool_calls数组中的索引。**id** `_string_` 本次工具响应的ID。**type** `_string_` 工具类型，固定为`function`。 **logprobs**` _object_` 当前 choices 对象的概率信息。 **属性** __ **content** `_array_` 带有对数概率信息的 Token 数组。 **属性** __ **token** `_string_` 当前 Token。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。**logprob** `_float_` 当前 Token 的对数概率。返回值为 null 表示概率值极低。**top_logprobs** `_array_` 当前 Token 位置最可能的若干个 Token 及其对数概率，元素个数与入参的`top_logprobs`保持一致。 **属性** __ **token** `_string_` 当前 Token。**bytes** `_array_` 当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。**logprob** `_float_` 当前 Token 的对数概率。返回值为 null 表示概率值极低。 **search_info**` _object_` 联网搜索到的信息，在设置`search_options`参数后会返回该参数。 **属性** __ **search_results**` _array_` 联网搜索到的结果。 **属性** __ **site_name**` _string_` 搜索结果来源的网站名称。**icon**` _string_` 来源网站的图标URL，如果没有图标则为空字符串。**index**` _integer_` 搜索结果的序号，表示该搜索结果在`search_results`中的索引。**title**` _string_` 搜索结果的标题。**url**` _string_` 搜索结果的链接地址。 **extra_tool_info**` _array_` 开启`enable_search_extension`参数后返回的领域增强信息。 **属性** __ **result**` _string_` 领域增强工具输出信息。**tool**` _string_` 领域增强使用的工具。
**usage**` _map_` 本次chat请求使用的Token信息。 **属性** __ **input_tokens** `_integer_` 用户输入内容转换成Token后的长度。**output_tokens** `_integer_` 模型输出内容转换成Token后的长度。**input_tokens_details** `_integer_` 使用[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)或[QVQ模型](https://help.aliyun.com/zh/model-studio/visual-reasoning)时，输入内容转换成Token后的长度详情。 **属性** __ **text_tokens** `_integer_` 使用[Qwen-VL 模型](https://help.aliyun.com/zh/model-studio/vision)或[QVQ模型](https://help.aliyun.com/zh/model-studio/visual-reasoning)时，为输入的文本转换为Token后的长度。**image_tokens** `_integer_` 输入的图像转换为Token后的长度。**video_tokens** `_integer_` 输入的视频文件或图像列表转换为Token后的长度。 **total_tokens** `_integer_` 当输入为纯文本时返回该字段，为**input_tokens** 与**output_tokens** 之和**。****image_tokens** `_integer_` 输入内容包含`image`时返回该字段。为用户输入图片内容转换成Token后的长度。**video_tokens** `_integer_` 输入内容包含`video`时返回该字段。为用户输入视频内容转换成Token后的长度。**audio_tokens** `_integer_` 输入内容包含`audio`时返回该字段。为用户输入音频内容转换成Token后的长度。**output_tokens_details** `_integer_` 输出内容转换成 Token后的长度详情。 **属性** __ **text_tokens** `_integer_` 输出的文本转换为Token后的长度。**reasoning_tokens** `_integer_` Qwen3 模型思考过程转换为Token后的长度。 **prompt_tokens_details** `_object_` 输入 Token 的细粒度分类。 **属性** __ **cached_tokens** `_integer_` 命中 Cache 的 Token 数。Context Cache 详情请参见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。**cache_creation** `_object_`[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)创建信息。 **属性** __ **ephemeral_5m_input_tokens** `_integer_` 用于创建5分钟有效期显式缓存的 Token 长度。 **cache_creation_input_tokens** `_integer_` 用于创建显式缓存的 Token 长度。**cache_type** `_string_` 使用[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)时，参数值为`ephemeral`，否则该参数不存在。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
