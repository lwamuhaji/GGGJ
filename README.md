1학년 2학기-대학 기초 SW 입문

파이썬 게임 만들기 프로젝트

- 클라이언트 생성 및 연결
```python
import gnetwork.gclient as gclient

client = gclient.GClient()
client.connect()
```
  
- 서버에 데이터 전송
```python
client.send(data=data)
```
