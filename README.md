# GGGJ (긴급9조)

1학년 2학기-대학 기초 SW 입문

파이썬 게임 만들기 프로젝트

---
* GGGJ 폴더에 클라이언트 관련 파일 넣을 것
* gnetwork 폴더는 내가 관리함
* 이미지나 기타 리소스는 resources 폴더에 넣을 것
* 그 외 백업용/테스트용 파일은 test 폴더로.


## gnetwork

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
