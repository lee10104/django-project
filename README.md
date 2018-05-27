# 넣고 싶은 기능 막 넣어보는 프로젝트

1. 메인 화면
  * 테마: [startbootstrap-agency](https://github.com/blackrockdigital/startbootstrap-agency/)

2. 사진관
  * url: /album/~~~
  * 좋아하는 사진 저장해놓고 관람하기(?)
  * 로그인 해야만 사진 등록/삭제 가능
  * TODO
    * 없는 앨범 페이지에는 들어갈 수 없도록 하기
    * 프론트 하기 덜 귀찮아지면 액자 아래에 사진 목록을 작게 만들어보기

3. 조아라 최신작품 목록
  * url: /new\_novels
  * 조아라 최신 소설 보여주기
  * 소설 커버, 이름, 작가, 설명, 링크 등 표시
  * 보기 싫은 애는 뮤트 가능
  * 로그인 해야만 사용 가능
  * TODO
    * 제목/소개글에 있는 단어 검색해서 한꺼번에 뮤트하기
    * 소설이 너무 많을 때 pagination 하기
    * 아예 url을 장르 별로 나눠버리자

4. 크롤링
  * celery 사용
  * 1시간마다 조아라에서 로맨스판타지, 판타지, 패러디 카테고리의 소설들을 최신 순으로 5페이지까지 크롤링해 저장
  * TODO
    * 5페이지까지 크롤링하는 것이 아니라, 이전에 저장했던 부분까지 크롤링하는 방법으로 바꾸기
    * 코드 리팩토링

5. 기타
  * TODO
    * fabric 세팅하기
    * https
    * requirements.txt
    * 404 페이지
