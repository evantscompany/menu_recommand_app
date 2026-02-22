/**
 * Mechuri 글로벌 설정 파일 (컨트롤 타워)
 * 접속 환경이 바뀔 때 SERVER_IP만 수정하면 모든 파일에 즉시 적용됩니다.
 */
const SERVER_IP = '192.168.0.38'; 
const PORT = '8000';
const BASE_URL = `http://${SERVER_IP}:${PORT}`;

export const API_ENDPOINTS = {
  // 인증 관련
  SIGNUP: `${BASE_URL}/api/auth/signup`,
  LOGIN: `${BASE_URL}/api/auth/login`,
  
  // 추천 관련
  RECOMMEND: `${BASE_URL}/recommend/`,
  FEEDBACK: `${BASE_URL}/api/recommendations/feedback/instant`,
  
  // 홈 화면용 (추후 백엔드 준비 시 활성화)
  // WEATHER_RECOMMEND: `${BASE_URL}/api/v1/home/weather-recommend`,
  // NEARBY_RESTAURANTS: `${BASE_URL}/api/v1/restaurants/nearby`,
};

export default BASE_URL;