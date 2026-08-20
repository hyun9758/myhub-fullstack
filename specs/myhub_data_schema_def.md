# MyHub — 데이터 스키마 정의서

## 데이터 스키마

| 최상위 키 | 필드 구성 |
|---|---|
| `profile` | `photo`, `name{ko,en}`, `nameSuffix{ko,en}`, `badges[]{ko,en}`, `birth`, `address{ko,en}`, `militaryService{ko,en}`, `email`, `mobile`, `affiliation{ko,en}`, `social[]{platform,label,url}` |
| `intro` | `{ko, en}` (한 문단) |
| `education[]` | `degree{ko,en}`, `school{ko,en}`, `major{ko,en}`, `year`, `gpa` |
| `career[]` | `period`, `institution{ko,en}`, `role{ko,en}`, `description{ko,en}` |
| `projects[]` | `category{ko,en}`, `year`, `period`, `execution{ko,en}`, `name{ko,en}`, `role{ko,en}` |
| `publications[]` | `type{ko,en}`(논문/특허), `title{ko,en}`, `venue{ko,en}`, `date` |
| `awards[]` | `title{ko,en}`, `org{ko,en}`, `date` |
| `skills` | `tech[]{ko,en}`, `languages[]{name{ko,en}, level{ko,en}}` |
