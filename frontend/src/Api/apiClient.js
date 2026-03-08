import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import BASE_URL, { API_ENDPOINTS } from './config';

/**
 * 전역 API 통신 클라이언트 (Axios Instance)
 * - 모든 요청에 사용자 토큰(JWT) 자동 주입
 * - API 응답 데이터(response.data) 전처리 수행
 */
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 60000, // 타임아웃 설정
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.urls = API_ENDPOINTS;

/**
 * [Request Interceptor]
 * 요청 송신 전 공통 작업 처리
 */
apiClient.interceptors.request.use(
  async (config) => {
    try {
      // 로컬 스토리지에서 인증 토큰 추출
      const token = await AsyncStorage.getItem('userToken');
      
      if (token) {
        // 인증 헤더에 Bearer 토큰 주입
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('[API Client] 토큰 로드 중 예외 발생:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * [Response Interceptor]
 * 서버 응답 수신 후 후처리 로직
 */
apiClient.interceptors.response.use(
  (response) => {
    // API 응답 본문만 바로 반환 (접근 편의성 향상)
    return response.data;
  },
  (error) => {
    // 서버 에러 핸들링 공통화
    const status = error.response ? error.response.status : null;

    if (status === 401) {
      // 401 Unauthorized: 세션 만료 또는 인증 실패 처리
      console.warn('[API Client] 인증 실패: 세션이 만료되었습니다.');
      // TODO: 필요 시 자동 로그아웃 로직 추가
    } else if (status === 500) {
      console.error('[API Client] 서버 내부 에러 발생 (500)');
    }

    return Promise.reject(error);
  }
);

export default apiClient;