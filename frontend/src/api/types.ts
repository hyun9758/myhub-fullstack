// 이 파일에서는 타입을 "만들지" 않는다.
// 자동 생성된 schema.d.ts 에서 필요한 것을 꺼내 짧은 이름만 붙인다.
import type { paths } from './schema'

export type ProfileResponse =
  paths['/api/profile']['get']['responses'][200]['content']['application/json']

export type Profile = ProfileResponse['profile']

export type AuthStatus =
  paths['/api/auth/session']['get']['responses'][200]['content']['application/json']

export type ProfileUpdate =
  paths['/api/profile']['put']['requestBody']['content']['application/json']
