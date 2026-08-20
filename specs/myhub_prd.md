# MyHub PRD

> PRD = Product Requirements Document (제품 요구사항 정의서)

| 항목 | 내용 |
|---|---|
| 문서 ID | `PRD-MYHUB-001` |
| 버전 | v0.4 |
| 작성일 | 2026-08-20 |
| 상태 | 검토완료 |
| 작성자 | ymbaek (초안), 정현수 (v0.4 그릴링) |

## 1. 개요

**배경.** 개인의 이력·연구 실적·프로젝트 이력은 파일 형태의 이력서로 관리될 때 최신 상태를 유지하기 어렵고, 열람자마다 다른 버전을 보게 된다. 소유자가 직접 데이터를 갱신하고 열람자는 항상 최신 이력을 웹에서 확인할 수 있는 단일 창구가 필요하다.

**목적.** Server / Client / DB로 구성된 풀스택 개인 이력서 웹 애플리케이션 `MyHub`의 요구사항을 정의한다. 소유자는 비밀 코드 인증 후 이력서 화면에서 직접 데이터를 CRUD 하고, 열람자는 별도 로그인 없이 이력서를 열람·인쇄할 수 있다.

**대상 사용자.** (1) 채용 담당자·협업 파트너 등 **열람자**(비인증, 읽기 전용 = 방문자 모드), (2) 이력 데이터를 관리하는 **소유자**(비밀 코드 인증 후 읽기/쓰기 = 편집 모드). 소유자는 1인이며 계정 개념 없이 단일 비밀 코드로만 식별한다.

**구현 기반.** 실제 구현은 별도 컨텍스트로 제공되는 **풀스택 스캐폴드 프로젝트의 코드베이스**를 기반으로 한다. 언어·프레임워크·DB 종류·인증 세션 방식 등 상세 기술 스택 결정과 그에 대한 책임은 해당 스캐폴드에 있으며, 본 PRD는 스택 중립적으로 요구사항만 정의한다.

## 2. 범위

**In Scope**
- 이력서 열람 및 섹션별 렌더링 (Profile, Intro, Education, Career, Projects, Publications, Awards, Skills)
- 데이터 스키마 정의서(`myhub_data_schema_def.md`)의 전 항목에 대한 DB CRUD 지원
- 비밀 코드 기반 소유자 인증(로그인/로그아웃)
- 인증 후 이력서 화면 내 라이브 에디팅(인라인 편집)으로 데이터 수정/추가/삭제
- 한국어/영어 언어 전환
- 라이트/다크 테마 선택
- 이력서 전체 인쇄(PDF 저장 포함)
- Server(REST API) / Client(SPA) / DB로 구성된 3계층 구조

**Out of Scope**
- 열람자 계정 가입·로그인 및 다중 사용자(여러 명의 이력서) 지원
- 아이디/비밀번호, 소셜 로그인, 2단계 인증 등 비밀 코드 외의 인증 수단
- 이력서 화면과 분리된 별도 관리자 콘솔(`/admin` 등 전용 편집 페이지)
- 편집 이력·버전 관리, 변경 되돌리기(undo/redo), 동시 편집 충돌 처리
- 기술 스택 선정 및 프로젝트 초기 구성 (스캐폴드 프로젝트가 담당)
- 이력서 템플릿/레이아웃 선택, 외부 서비스(LinkedIn 등) 데이터 자동 연동
- 열람 통계·분석, 댓글·문의 폼 등 커뮤니케이션 기능
- 한국어·영어 외 언어 확장 및 자동 번역
- 상세 UI/UX 및 품질 기준 (구현 단계에서 별도 제공 예정)

## 3. 정보 구조 — 섹션 ID

| ID | 섹션 | 앵커/경로 | 저장 위치 | 데이터 없을 때 |
|---|---|---|---|---|
| SEC-01 | Profile | `#profile` | DB `profile` 테이블 | 필수 섹션. 누락 필드만 개별 숨김 |
| SEC-02 | Intro | `#intro` | DB `intro` 테이블 | 섹션 숨김 |
| SEC-03 | Education | `#education` | DB `education` 테이블 | 섹션 숨김 |
| SEC-04 | Career | `#career` | DB `career` 테이블 | 섹션 숨김 |
| SEC-05 | Projects | `#projects` | DB `projects` 테이블 | 섹션 숨김 |
| SEC-06 | Publications | `#publications` | DB `publications` 테이블 | 섹션 숨김 |
| SEC-07 | Awards | `#awards` | DB `awards` 테이블 | 섹션 숨김 |
| SEC-08 | Skills | `#skills` | DB `skills` 테이블 | 섹션 숨김 |
| SEC-09 | 전역 컨트롤 (언어/테마/인쇄) | 네비게이션 고정 영역 | `localStorage` (언어·테마 선택값) | 기본값(ko / 시스템 테마) 적용 |
| SEC-10 | 소유자 인증 (비밀 코드 입력) | 네비게이션 진입점 + 모달/패널 | 비밀 코드는 `.env`, 인증 세션은 클라이언트 세션 저장소 | 방문자 모드에서는 진입점만 노출 |
| SEC-11 | 라이브 편집 모드 | SEC-01~SEC-08 위에 오버레이 (별도 경로 없음) | SEC-01~SEC-08과 동일한 DB 테이블 | 비인증 시 편집 UI 자체를 렌더링하지 않음 |

## 4. 데이터 스키마

- 다국어 필드는 `{ko, en}` 객체로 저장하며, 렌더링 시 현재 선택된 언어 키를 사용한다. 선택 언어 값이 비어 있으면 다른 언어 값으로 대체(fallback)한다.
- 배열형 최상위 키(`education`, `career`, `projects`, `publications`, `awards`)는 각 항목이 고유 `id`와 정렬용 `order` 값을 가지며, DB에서는 독립 테이블(또는 컬렉션)로 관리한다.
- 단일 객체형 키(`profile`, `intro`, `skills`)는 소유자당 1개의 레코드로 관리하며 생성/삭제 없이 조회·수정만 지원한다.
- 날짜성 필드(`year`, `date`, `period`, `birth`)는 문자열로 저장하되 표기 규칙(`YYYY`, `YYYY-MM`, `YYYY-MM ~ YYYY-MM`)을 서버에서 검증한다.
- 클라이언트에는 언어 무관하게 `{ko, en}` 전체를 내려보내며, 언어 선택은 클라이언트에서 처리한다(인쇄 시 현재 언어 기준).

| 키 | 필드 구성 |
|---|---|
| `profile` | `photo`, `name{ko,en}`, `nameSuffix{ko,en}`, `badges[]{ko,en}`, `birth`, `address{ko,en}`, `militaryService{ko,en}`, `email`, `mobile`, `affiliation{ko,en}`, `social[]{platform,label,url}` |
| `intro` | `{ko, en}` (한 문단) |
| `education[]` | `degree{ko,en}`, `school{ko,en}`, `major{ko,en}`, `year`, `gpa` |
| `career[]` | `period`, `institution{ko,en}`, `role{ko,en}`, `description{ko,en}` |
| `projects[]` | `category{ko,en}`, `year`, `period`, `execution{ko,en}`, `name{ko,en}`, `role{ko,en}` |
| `publications[]` | `type{ko,en}`(논문/특허), `title{ko,en}`, `venue{ko,en}`, `date` |
| `awards[]` | `title{ko,en}`, `org{ko,en}`, `date` |
| `skills` | `tech[]{ko,en}`, `languages[]{name{ko,en}, level{ko,en}}` |

## 5. 요구사항 명세

### 5.1 기술 요구사항 (TR)

| ID | 요구사항 |
|---|---|
| TR-01 | Client / Server / DB가 분리된 3계층 구조로 구성한다 |
| TR-02 | Client는 SPA로 구현하고, 섹션 렌더링에 필요한 데이터는 Server API에서만 가져온다 |
| TR-03 | Server는 REST API를 제공하며, 응답 형식은 JSON으로 통일한다 |
| TR-04 | 조회 API는 비인증 공개, 생성/수정/삭제 API는 인증 필수로 라우팅을 분리한다 |
| TR-05 | DB는 스키마의 최상위 키 단위로 테이블/컬렉션을 구성하고 다국어 필드를 함께 저장한다 |
| TR-06 | API 요청/응답 스키마 검증을 서버 계층에서 수행한다 |
| TR-07 | DB 접속 정보·인증 시크릿 등 환경 의존 값은 환경변수로 주입한다 |
| TR-08 | 초기 데이터 시드(seed) 스크립트를 제공해 빈 DB에서도 실행 가능하게 한다 |
| TR-09 | 소유자 인증은 단일 비밀 코드 검증 방식만 구현하며, 코드 값은 `.env`로 주입한다 |
| TR-10 | 비밀 코드 검증은 서버에서만 수행하고, 코드 값은 클라이언트 번들·응답에 포함하지 않는다 |
| TR-11 | 인증 성공 시 만료 시간이 있는 세션/토큰을 발급하고, 로그아웃 시 즉시 무효화한다. 세션 유효기간은 7일로 한다 *(v0.4, 그릴링으로 확정)* |
| TR-12 | 편집 기능은 이력서 화면과 동일한 라우트에서 동작하며, 별도 관리자 콘솔 라우트를 두지 않는다 |
| TR-13 | 언어·프레임워크·DB·세션 구현 방식은 제공되는 풀스택 스캐폴드 프로젝트의 규약을 따른다 |

### 5.2 데이터 요구사항 (DR)

| ID | 요구사항 |
|---|---|
| DR-01 | `myhub_data_schema_def.md`의 8개 최상위 키를 모두 저장·제공한다 |
| DR-02 | 배열형 키(education, career, projects, publications, awards)는 항목 단위 Create/Read/Update/Delete를 지원한다 |
| DR-03 | 단일 객체형 키(profile, intro, skills)는 Read/Update를 지원한다 |
| DR-04 | 배열 항목은 고유 ID를 가지며, 표시 순서는 도메인 특성에 따른 자동 정렬(예: education/career는 시작일 최신순)을 따른다. 사용자가 직접 순서를 지정하는 수동 재정렬 기능은 제공하지 않는다 *(v0.4, 그릴링으로 수정 — 원래 "정렬 순서(order) 값 + 순서 변경 가능"이었으나, 이력서 도메인 특성상 날짜 자동 정렬이 자연스럽다는 소유자 의사결정으로 대체)* |
| DR-05 | 다국어 필드는 ko/en 값을 각각 저장하며, 한쪽만 입력된 경우에도 저장 가능하다 |
| DR-06 | 필수 필드(예: profile.name, education.school) 누락 시 저장을 거부하고 오류 사유를 반환한다 |
| DR-07 | `profile.photo`는 외부 이미지 URL 참조 방식으로만 저장한다 (파일 업로드 미지원) *(v0.4, 그릴링으로 확정)* |
| DR-08 | `profile.social[]`의 `url`은 URL 형식을 검증한다 |

### 5.3 UI/UX 요구사항 (UR)

| ID | 요구사항 |
|---|---|
| UR-01 | 이력서는 단일 페이지에 섹션(SEC-01~SEC-08) 순서대로 렌더링한다 |
| UR-02 | 네비게이션에 언어 전환·테마 전환·인쇄 컨트롤을 상시 노출한다 |
| UR-03 | 섹션 목차/앵커 내비게이션으로 각 섹션에 바로 이동할 수 있다 |
| UR-04 | 데이터가 없는 섹션은 빈 영역 대신 섹션 자체를 숨긴다 |
| UR-05 | 라이트/다크 테마 모두에서 텍스트·배경 대비를 확보한다 |
| UR-06 | 인쇄 시 네비게이션·컨트롤 등 화면 전용 요소를 제외한 인쇄 전용 레이아웃을 적용한다 |
| UR-07 | 데스크톱·모바일 화면 폭에 대응하는 반응형 레이아웃을 적용한다 |
| UR-08 | 편집은 이력서 화면을 벗어나지 않고 각 섹션·항목 위에서 인라인으로 수행하며, 저장 결과(성공/실패)를 즉시 알린다 |
| UR-09 | 방문자 모드와 편집 모드는 현재 상태를 시각적으로 구분할 수 있게 표시한다 |
| UR-10 | 비밀 코드 입력은 마스킹 처리하고, 실패 시 사유를 노출하되 코드 값 힌트는 제공하지 않는다 |
| UR-11 | 편집 모드에서도 인쇄 시에는 편집 UI(입력 필드·버튼·모드 표시)를 제외한다 |
| UR-12 | 세부 디자인 가이드(색상·타이포·간격)는 구현 단계 별도 제공 문서를 따른다 |
| UR-13 | `profile.birth`, `profile.address`, `profile.militaryService`는 방문자 모드에서 노출하지 않으며, 소유자 인증(편집 모드) 상태에서만 표시·수정한다 *(v0.4, 그릴링으로 신설 — 민감정보 보호를 위해 방문자 공개 범위에서 제외)* |

### 5.4 기능 요구사항 (FR)

| ID | 요구사항 |
|---|---|
| FR-01 | 열람자는 로그인 없이 이력서 전체를 열람할 수 있다 |
| FR-02 | 열람자는 섹션별로 이력 데이터를 확인할 수 있다 |
| FR-03 | 사용자는 한국어/영어를 전환할 수 있고, 선택은 재방문 시 유지된다 |
| FR-04 | 사용자는 라이트/다크 테마를 선택할 수 있고, 선택은 재방문 시 유지된다 |
| FR-05 | 사용자는 현재 언어 기준으로 이력서 전체를 인쇄하거나 PDF로 저장할 수 있다 |
| FR-06 | 소유자는 비밀 코드 입력만으로 로그인할 수 있다 (아이디 입력 없음) |
| FR-07 | 인증에 성공하면 현재 보고 있는 이력서 화면이 그대로 라이브 편집 모드로 전환된다 |
| FR-08 | 인증된 소유자는 각 섹션의 데이터를 추가할 수 있다 |
| FR-09 | 인증된 소유자는 각 섹션의 데이터를 수정할 수 있다 |
| FR-10 | 인증된 소유자는 각 섹션의 항목을 삭제할 수 있으며, 삭제 전 브라우저 기본 확인 팝업으로 확인을 거친다 *(v0.4, 그릴링으로 확정)* |
| FR-11 | 인증된 소유자는 배열형 섹션의 항목 표시 순서를 변경할 수 있다 |
| FR-12 | 소유자는 로그아웃할 수 있으며, 로그아웃 시 방문자 모드(읽기 전용)로 복귀한다 |
| FR-13 | 세션 만료 시에도 방문자 모드로 복귀하고 재인증을 안내한다 |
| FR-14 | 비인증 사용자에게는 편집 UI를 노출하지 않으며, 쓰기 API 직접 호출도 서버에서 차단한다 |
| FR-15 | 비밀 코드가 틀리면 인증을 거부하고 방문자 모드를 유지한다 |
| FR-16 | API 오류·네트워크 실패 시 사용자에게 오류 상태를 표시하고, 편집 중이던 입력값은 유지한다 |

### 5.5 배포 요구사항 (DPR)

| ID | 요구사항 |
|---|---|
| DPR-01 | Client / Server를 로컬 개발 환경에서 단일 명령으로 기동할 수 있으며, DB는 외부 Supabase 인스턴스에 연결한다 |
| DPR-02 | 개발·운영 환경 설정을 `.env`로 분리하고, 비밀 코드를 포함한 시크릿은 저장소에 커밋하지 않는다 (`.env.example`만 제공) |
| DPR-03 | 서버 상태 확인용 헬스체크 엔드포인트를 제공한다 |

## 6. 비기능 요구사항 (NFR)

| ID | 요구사항 |
|---|---|
| NFR-01 | 성능: 이력서 첫 화면이 일반 네트워크 환경에서 3초 이내에 렌더링된다 |
| NFR-02 | 성능: 조회 API 응답은 통상 조건에서 500ms 이내로 반환된다 |
| NFR-03 | 보안: 비밀 코드는 `.env`로만 관리하고 소스·DB·클라이언트 번들에 하드코딩하지 않으며, 전송 구간은 HTTPS로 보호한다 |
| NFR-04 | 보안: 인증 토큰/세션은 만료 시간을 두고, 만료 후에는 재인증을 요구한다 |
| NFR-05 | 보안: 쓰기 API는 서버 측에서 인증·입력 검증을 수행하며 클라이언트 검증에 의존하지 않는다 |
| NFR-06 | 호환성: 최신 버전 Chrome·Edge·Safari·Firefox에서 동일하게 동작한다 |
| NFR-07 | 유지보수성: 스키마에 필드가 추가되어도 렌더링·편집 코드 수정 범위가 해당 섹션으로 한정된다 |
| NFR-08 | 안정성: 특정 섹션 데이터 오류가 다른 섹션 렌더링을 중단시키지 않는다 |

## 7. 파일 구조

> 아래 구조는 요구사항을 충족하기 위해 필요한 **구성 요소의 참고 예시**이며, 실제 디렉터리 규약·파일 확장자·모듈 배치는 제공되는 풀스택 스캐폴드 프로젝트를 따른다 (TR-13).

```
myhub/
├── client/
│   ├── public/
│   ├── src/
│   │   ├── main.[js|ts]
│   │   ├── App.[jsx|tsx]
│   │   ├── api/
│   │   │   └── client.[js|ts]
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── NavBar.[jsx|tsx]
│   │   │   │   └── SectionNav.[jsx|tsx]
│   │   │   ├── controls/
│   │   │   │   ├── LanguageToggle.[jsx|tsx]
│   │   │   │   ├── ThemeToggle.[jsx|tsx]
│   │   │   │   ├── PrintButton.[jsx|tsx]
│   │   │   │   └── OwnerAuthButton.[jsx|tsx]
│   │   │   ├── auth/
│   │   │   │   └── SecretCodeDialog.[jsx|tsx]
│   │   │   ├── editing/
│   │   │   │   ├── EditableField.[jsx|tsx]
│   │   │   │   ├── EditableList.[jsx|tsx]
│   │   │   │   └── EditModeBadge.[jsx|tsx]
│   │   │   └── sections/
│   │   │       ├── Profile.[jsx|tsx]
│   │   │       ├── Intro.[jsx|tsx]
│   │   │       ├── Education.[jsx|tsx]
│   │   │       ├── Career.[jsx|tsx]
│   │   │       ├── Projects.[jsx|tsx]
│   │   │       ├── Publications.[jsx|tsx]
│   │   │       ├── Awards.[jsx|tsx]
│   │   │       └── Skills.[jsx|tsx]
│   │   ├── pages/
│   │   │   └── ResumePage.[jsx|tsx]   # 열람/편집 단일 화면
│   │   ├── context/
│   │   │   ├── LanguageContext.[js|ts]
│   │   │   ├── ThemeContext.[js|ts]
│   │   │   └── AuthContext.[js|ts]    # 방문자/편집 모드 상태
│   │   └── styles/
│   │       ├── theme.css
│   │       └── print.css
│   └── package.json
├── server/
│   ├── src/
│   │   ├── index.[js|ts]
│   │   ├── routes/
│   │   │   ├── auth.routes.[js|ts]
│   │   │   ├── profile.routes.[js|ts]
│   │   │   ├── intro.routes.[js|ts]
│   │   │   ├── education.routes.[js|ts]
│   │   │   ├── career.routes.[js|ts]
│   │   │   ├── projects.routes.[js|ts]
│   │   │   ├── publications.routes.[js|ts]
│   │   │   ├── awards.routes.[js|ts]
│   │   │   └── skills.routes.[js|ts]
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   ├── middleware/
│   │   │   ├── auth.[js|ts]          # 세션 검증 + 쓰기 라우트 보호
│   │   │   ├── validate.[js|ts]
│   │   │   └── error.[js|ts]
│   │   └── config/
│   │       └── db.[js|ts]
│   ├── migrations/
│   ├── seeds/
│   │   └── initial-resume.json
│   └── package.json
├── docs/
│   ├── myhub_fullstack_prd.md
│   ├── myhub_fullstack_data_schema_def.md
│   ├── app_context_fullstack.md
│   └── myhub_usg_list.md
├── .env.example                      # OWNER_SECRET_CODE, SESSION_SECRET, Supabase 접속 정보 등
└── README.md
```

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|---|---|---|
| 2026-08-20 | v0.4 | 요구사항 그릴링([specs/analysis/myhub_us.md](analysis/myhub_us.md)) 결과 반영: DR-04 수동 순서 요구사항 삭제(자동 정렬로 대체), DR-07 사진 저장 방식을 URL 참조로 확정, TR-11 세션 유효기간 7일로 확정, FR-10 삭제 확인 방식 확정, UR-13(민감정보 방문자 비공개) 신설. 이번 그릴링 사이클의 구현 범위는 profile/education/career/skills 4개 도메인으로 한정(나머지는 8장에서 별도 진행) |
| 2026-08-09 | v0.3 | 섹션 3의 '데이터 소스'를 '저장 위치'로 변경(API 표기 삭제), 요구사항 표의 '상태' 컬럼 제거, FR의 USG 참조 삭제, DPR-01을 외부 Supabase 기준으로 수정하고 DPR-03~05 삭제, NFR-06/08/11 삭제 후 재번호, '헤더' 표현을 '네비게이션'으로 통일 |
| 2026-08-09 | v0.2 | 소유자 인증을 비밀 코드(`.env`) 방식으로 확정, 별도 관리자 콘솔 제거 후 라이브 에디팅 모드로 대체, 로그아웃 시 방문자 모드 복귀 명시, 구현 기반을 풀스택 스캐폴드 프로젝트로 규정 (TR-09~13, UR-08~11, FR-06~16, NFR-03, SEC-10/11) |
| 2026-08-09 | v0.1 | 최초 작성 |
