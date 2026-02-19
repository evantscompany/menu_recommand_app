import { StyleSheet, Dimensions, Platform } from 'react-native';

// 디바이스 화면 너비 기준으로 반응형 패딩 계산
const { width, height } = Dimensions.get('window');
const cardHeight = height * 0.6; // 화면 높이의 60% 정도로 카드 높이 고정

export const styles = StyleSheet.create({
  // [Container] 전체 화면 스타일 (다크 테마 배경)
  container: {
    flex: 1,
    backgroundColor: '#0F172A', 
  },
  contentContainer: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 20,
    paddingBottom: 40, // 하단 여백 확보
  },
  
  // [Loading State] 로딩 화면 스타일
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0F172A',
  },
  loadingText: {
    marginTop: 24,
    color: '#94A3B8',
    fontSize: 16,
    fontWeight: '600',
    letterSpacing: -0.5,
  },

  // [Header Area] 상단 진행 정보 및 프로그레스 바
  headerArea: {
    marginBottom: 20,
  },
  stepInfoContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginBottom: 12,
  },
  stepText: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: '900',
  },
  totalStepText: {
    color: '#64748B',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 4,
  },
  progressBarBg: {
    height: 6, // 조금 더 슬림하게 변경
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#6366F1', // Primary Brand Color
    borderRadius: 3,
  },

  // [Card Wrapper] 카드를 화면 수직 중앙에 위치시키기 위한 래퍼
  cardWrapper: {
    flex: 1,
    justifyContent: 'center', // 수직 중앙 정렬 (핵심!)
    alignItems: 'center',
  },

  // [Main Card] 질문 카드 스타일 (고정 높이 + 내부 중앙 정렬)
  cardContainer: {
    width: '100%',
    height: cardHeight, // [중요] 모든 질문에서 동일한 높이 유지 (세련미 UP)
    backgroundColor: '#FFFFFF',
    borderRadius: 28, // 더 부드러운 곡률
    paddingHorizontal: 30,
    paddingVertical: 40,
    justifyContent: 'center', // [중요] 카드 내부 콘텐츠 수직 중앙 정렬
    alignItems: 'center', // 가로 중앙 정렬
    // 고급스러운 그림자 효과 (Elevation & Shadow)
    elevation: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.25,
    shadowRadius: 16,
  },
  
  // [Content Elements] 내부 텍스트 및 요소 스타일
  categoryBadge: {
    color: '#6366F1',
    fontWeight: '800',
    fontSize: 13,
    marginBottom: 16,
    textAlign: 'center',
    letterSpacing: 1,
    textTransform: 'uppercase', // 대문자로 변환하여 뱃지 느낌 강조
    backgroundColor: 'rgba(99, 102, 241, 0.1)', // 배경색 추가
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
    overflow: 'hidden',
  },
  questionTitle: {
    fontSize: 26,
    fontWeight: '900',
    color: '#1E293B',
    textAlign: 'center',
    marginBottom: 40, // 질문과 선택지 사이 여백 확보
    lineHeight: 36,
    letterSpacing: -0.5,
  },

  // [Input Type] 주관식 입력 스타일
  inputWrapper: {
    width: '100%',
    alignItems: 'center',
  },
  budgetInput: {
    backgroundColor: '#F1F5F9',
    width: '100%',
    paddingVertical: 22,
    paddingHorizontal: 20,
    borderRadius: 18,
    fontSize: 20,
    color: '#1E293B',
    textAlign: 'center',
    marginBottom: 20,
    fontWeight: 'bold',
  },
  confirmButton: {
    backgroundColor: '#6366F1',
    width: '100%',
    paddingVertical: 18,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 4,
  },
  confirmButtonText: {
    color: '#FFFFFF',
    fontWeight: '800',
    fontSize: 16,
  },

  // [Option Type] 객관식 선택지 스타일
  optionsContainer: {
    width: '100%',
  },
  optionButton: {
    backgroundColor: '#F8FAFC', // 아주 연한 회색 배경
    paddingVertical: 20,
    borderRadius: 18,
    marginBottom: 12,
    borderWidth: 1.5,
    borderColor: '#E2E8F0', // 은은한 테두리
    alignItems: 'center',
    justifyContent: 'center',
  },
  optionText: {
    fontSize: 16,
    color: '#334155',
    fontWeight: '700', // 글씨체 조금 더 두껍게
    letterSpacing: -0.3,
  },
});