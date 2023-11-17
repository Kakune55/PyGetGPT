# server API 接口文档  

## 请求格式（json）
| 键       | 类型   | 必选  | 示例 |
|---------|------|-----|-----|
| prompt  | str  | yes | "你好" |
| userkey | str  | yes | "2b3j41b2xh1hz1" |
| history | list | no  | "history":[{"user":"XXXXXX","bot":"XXXXXX"},{"user":"XXXXXX""bot":"XXXXXX"}] |


## 返回格式（json）
| 键 | 类型 | 示例 |
|----|------|------|
| code | int | 200 |
| output | str | "你好" |
| surplus | int | 10000 |
| |