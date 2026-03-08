/**
 * Mechuri 글로벌 설정 파일 (컨트롤 타워)
 * 접속 환경이 바뀔 때 SERVER_IP만 수정하면 모든 파일에 즉시 적용됩니다.
 */
const BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://192.168.0.11:8000';

export const API_ENDPOINTS = {
  // 인증 관련
  SIGNUP: `api/auth/signup`,
  LOGIN: 'api/auth/login-json',
  
  // 추천 관련
  RECOMMEND: `api/recommend/`,
  FEEDBACK: `api/recommend/feedback`,
  // FEEDBACK: `/api/recommend/feedback/instant`,
  
  // 홈&지도 화면용
  NEARBY_RESTAURANTS: `api/recommend/nearby`,
};

export default BASE_URL;