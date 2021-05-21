# yeonguham-server
연구함 서버

postgresql arrayfield vs django m2m

원래 arrayfield로 해결할 수 있을 것 같았던 게 disease나 tag 같은 거 하면 좋겠다고 생각했었는데 disease는 없어졌고 아래 링크 읽어보니 circular dependency 문제도 있고 filtering에 쓸 때는 m2m이 나은 것 같아서 일단 arrayfield는 사용을 안 해놨어요. choices는 써놓았습니다 

[stackoverflow answer](https://stackoverflow.com/questions/27048400/django-postgres-arrayfield-vs-one-to-many-relationship)
