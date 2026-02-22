import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  // 화면 전체를 덮는 오버레이 컨테이너
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(255, 255, 255, 0.8)', // 반투명 배경으로 뒤쪽 화면이 살짝 보이게 처리
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 999, // 최상단 배치
  },
  // 로딩 박스
  loadingBox: {
    padding: 30,
    borderRadius: 20,
    alignItems: 'center',
  },
  // 로딩 메시지 텍스트
  messageText: {
    marginTop: 15,
    fontSize: 15,
    fontWeight: '600',
    color: '#6366F1', // 브랜드 컬러 적용
    textAlign: 'center',
    lineHeight: 22,
  }
});