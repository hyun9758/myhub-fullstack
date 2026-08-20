# MyHub

MyHub는 소유자가 비밀 코드로 인증해 직접 관리하는 개인 이력서 풀스택 웹 애플리케이션이다.

## Language

**Owner (소유자)**:
비밀 코드로 인증한, 이 이력서의 유일한 관리자. 계정 개념 없이 단일 비밀 코드로만 식별된다.
_Avoid_: 관리자, Admin, 사용자

**Visitor (방문자)**:
로그인 없이 이력서를 읽기 전용으로 열람하는 사람 (채용 담당자, 협업 파트너 등).
_Avoid_: 게스트, 비회원

**Live Editing (라이브 편집)**:
소유자가 로그인한 뒤, 별도 관리자 콘솔이 아니라 이력서 화면 그 자리에서 바로 데이터를 수정하는 방식.
_Avoid_: 인라인 편집, 관리자 모드

**단일 객체형 개체 (Singleton Entity)**:
소유자당 정확히 1개만 존재하며 생성·삭제 없이 조회·수정만 가능한 개체. `profile`, `skills`가 해당한다.
_Avoid_: 단일 레코드

**목록형 개체 (List Entity)**:
0개 이상 존재하며 생성·조회·수정·삭제가 모두 가능한 개체. `education`, `career`가 해당한다.
_Avoid_: 배열, 컬렉션

**자동 정렬 (Auto Sort)**:
목록형 개체의 표시 순서를 사용자가 직접 지정하지 않고, 정해진 기준(시작일 최신순)으로 항상 자동 계산하는 방식. MyHub는 수동 재정렬 기능을 두지 않는다 (ADR-0001).
_Avoid_: 정렬 순서(order), 수동 정렬

**민감 필드 (Sensitive Field)**:
`profile.birth`, `profile.address`, `profile.militaryService`처럼 방문자에게는 숨기고 소유자(편집 모드)에게만 노출하는 필드.
_Avoid_: 비공개 필드

## 관련 문서

- [specs/myhub_prd.md](specs/myhub_prd.md) — 제품 요구사항 정의서
- [specs/analysis/myhub_us.md](specs/analysis/myhub_us.md) — 유저스토리 명세서
- [specs/design/myhub_data_req.md](specs/design/myhub_data_req.md) — 데이터 요구사항(논리 데이터 모델)
- [specs/adr/](specs/adr/) — 되돌리기 어려운 아키텍처 결정과 그 이유
