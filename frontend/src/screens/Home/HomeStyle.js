import { StyleSheet, Dimensions, Platform } from 'react-native';

const { width } = Dimensions.get('window');

export const styles = StyleSheet.create({
  // 전체 컨테이너
  container: { 
    flex: 1, 
    backgroundColor: '#F8FAFC' 
  },

  // 상단 고정 헤더 바
  headerBar: {
    height: 60,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    backgroundColor: '#FFF',
    borderBottomWidth: 1,
    borderBottomColor: '#F1F5F9',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  headerLogo: {
    fontSize: 22,
    fontWeight: '900',
    color: '#6366F1',
    letterSpacing: -0.5,
  },

  // 스크롤 뷰 내부 컨텐츠 여백
  scrollContent: {
    paddingTop: 10,
    paddingBottom: 100, 
  },

  // 섹션 1: 상단 배너 구역
  headerSection: { 
    padding: 20, 
    backgroundColor: '#FFF', 
    borderBottomLeftRadius: 30, 
    borderBottomRightRadius: 30, 
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    marginBottom: 10,
  },
  welcomeText: { fontSize: 16, color: '#64748B', marginBottom: 10 },
  mainBanner: { 
    backgroundColor: '#6366F1', 
    padding: 25, 
    borderRadius: 20, 
    flexDirection: 'row', 
    alignItems: 'center', 
    justifyContent: 'space-between' 
  },
  bannerTitle: { fontSize: 24, fontWeight: 'bold', color: '#FFF' },
  bannerSub: { fontSize: 14, color: '#E0E7FF', marginTop: 5 },

  // 공통 섹션 스타일
  section: { padding: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: '#1E293B', marginBottom: 15 },
  
  // 섹션 2: 날씨 카드
  weatherCard: { 
    backgroundColor: '#FFF', 
    padding: 20, 
    borderRadius: 20, 
    flexDirection: 'row', 
    alignItems: 'center', 
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
  },
  weatherTextContainer: { marginLeft: 15, flex: 1 },
  weatherText: { fontSize: 15, color: '#475569', lineHeight: 22 },

  // 섹션 3: 주변 식당 리스트
  titleRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  moreText: { color: '#6366F1', fontSize: 14 },
  resCard: { 
    backgroundColor: '#FFF', 
    padding: 15, 
    borderRadius: 15, 
    marginBottom: 10, 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center', 
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  resName: { fontSize: 16, fontWeight: '600', color: '#1E293B' },
  resDetail: { fontSize: 13, color: '#94A3B8', marginTop: 3 },

  // 도보 시간 정보 태그
  timeTag: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    backgroundColor: '#F1F5F9', // 차분한 배경
    paddingHorizontal: 10, 
    paddingVertical: 5, 
    borderRadius: 12,
  },
  timeValue: {
    fontSize: 13,
    fontWeight: '800', // 시간 데이터 강력 강조
    color: '#4F46E5', // 시인성 좋은 컬러
  },

  // 하단 고정 푸터 바
  footerBar: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    height: Platform.OS === 'ios' ? 90 : 70,
    flexDirection: 'row',
    backgroundColor: '#FFF',
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
    paddingBottom: Platform.OS === 'ios' ? 25 : 0,
    elevation: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -3 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  footerTab: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  footerTabText: {
    fontSize: 12,
    marginTop: 4,
    color: '#94A3B8',
  },
  activeTabText: {
    color: '#6366F1',
    fontWeight: '700',
  },
  fixedContent: {
  backgroundColor: '#F8FAFC',
  zIndex: 10,
  flexShrink: 0,
  },
  restaurantListScroll: {
  flex: 1,
  backgroundColor: '#F8FAFC',
  },
});