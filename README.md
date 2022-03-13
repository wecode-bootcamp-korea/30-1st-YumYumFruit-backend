# 냠냠프룻 Proejct

<img src="https://user-images.githubusercontent.com/96276152/158007141-d2c590c8-1e24-405c-80ba-63716ac6a6f8.jpg" width="100" height="100">  

## 프로젝트 소개

- 냠냠제주는 제주 과일을 이용하여 수작업 마말랭을 만드는 커머스 사이트이며, 냠냠제주를 클론코딩한 냠냠프룻입니다.
- 짧은 프로젝트 기간동안 개발에 집중하기 위해 디자인/기획 부분만 클론했습니다.

### 프로젝트 인원

- **프론트엔드: 김혜진, 노유정, 정건희**  
- **백엔드: 박건우, 이예솔, 윤명국**

### 프로젝트 작업기간

2022.02.28 ~ 2022.03.11

### 시연 영상

[시연 영상](https://youtu.be/tMo2KpaQ-MA)

### DB modeling

<img src="https://user-images.githubusercontent.com/96276152/158007694-1f2f1826-f8bb-46ca-ba95-073c8e8a9769.png" width="1200" height="700">

## 적용 기술 및 구현 기능

### 적용 기술

> - Front-End: React.js, sass
> - Back-End: Python, Django web fremework, Bcrypt, MySQL
> - Common: Git, Github

### 구현 기능

#### 회원가입, 로그인 
- 회원가입: 정규표현식을 활용하여 email 및 비밀번호 유효성 체크, 이메일 중복 여부 체크, Bycrypt 활용하여 비밀번호 암호화 후 DB에 저장 (POST) 
- 로그인:Bcrypt 활용하여 비밀번호 복호화하여 체크 후 JWT로 토큰 발급시 만료기간 2일 설정  (POST)

#### 상품 리스트

- 카테고리별 필터링
- 높은 금액순, 낮은 금액순, 이름순, 신상품순 정렬
- 페이지네이션 - 페이지 크기에 맞춰 데이터 리턴

#### 상품 상세 페이지

- 상품정보 (상품명, 원산지, 금액, 썸네일이미지, 포장옵션, 설명, 본문이미지)
- 포장옵션 선택기능
- 주문 및 장바구니 추가시 수량 선택기능

#### 장바구니 페이지

- 상품 추가
- 상품 수량 변경
- 상품 삭제 (단건삭제, 선택삭제, 일괄삭제)
- 사용자 가용적립금 표시
- 상품 구매시 적립되는 적립금 표시
- 배송비 표시
- 총 결제금액 표시 (장바구니 전체 상품, 배송비)


## Reference
- 이 프로젝트는 냠냠제주 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
