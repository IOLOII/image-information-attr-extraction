# 应用开发说明

└── index.py # 入口文件，包含了调用百炼大模型应用，图片信息提取

cp .env.example .env

## 环境变量

- `DASHSCOPE_API_KEY`：百炼的 API-KEY，获取方式请参考：[如何获取](https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key "如何获取")。
- `ALIBABA_CLOUD_ACCESS_KEY_ID`：访问对象存储OSS发起请求，获取方式请参考：[如何获取](https://help.aliyun.com/zh/oss/developer-reference/use-the-accesskey-pair-of-a-ram-user-to-initiate-a-request "如何获取")。
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`：访问对象存储OSS发起请求，获取方式请参考：[如何获取](https://help.aliyun.com/zh/oss/developer-reference/use-the-accesskey-pair-of-a-ram-user-to-initiate-a-request "如何获取")。
- `OSS_ENDPOINT`：对象存储外网访问 Endpoint（地域节点），获取方式请参考：[如何获取](https://help.aliyun.com/zh/oss/user-guide/oss-domain-names "如何获取")。
- `OSS_BUCKET`：对象存储存储桶名。
- `ENABLE_LOGIN`：开启鉴权访问（默认为 `false`）。
- `USER_NAME`：应用程序的用户名（默认为 `""` ENABLE_LOGIN 为 `true` 时需要配置）。
- `USER_PASSWORD`：应用程序的密码（默认为 `""` ENABLE_LOGIN 为 `true` 时需要配置）。
