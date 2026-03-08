import { StyleSheet, Dimensions, Platform } from 'react-native';

const { width, height } = Dimensions.get('window');

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF', // 앱 기본 배경색을 순백색으로 통일
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
  },
  // 헤더 디자인 개선 (그림자 제거, 라인 추가로 깔끔하게)
  header: {
    height: 60,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#F1F5F9', // 아주 연한 회색 라인
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1E293B', // 다크 그레이
  },
  backButton: {
    width: 36,
    height: 36,
    borderRadius: 12,
    backgroundColor: '#F8FAFC', // 연한 회색 배경
    justifyContent: 'center',
    alignItems: 'center',
  },
  mapContainer: {
    flex: 1,
  },
  map: {
    width: '100%',
    height: '100%',
  },
  
  // ------------------------------------------------------------
  // MOCK - [서비스 준비 중 오버레이 스타일] (기존 주석 유지)
  // ------------------------------------------------------------
  // overlay: {
  //   ...StyleSheet.absoluteFillObject,
  //   backgroundColor: 'rgba(15, 23, 42, 0.4)', // 어두운 반투명 배경
  //   justifyContent: 'center',
  //   alignItems: 'center',
  //   paddingHorizontal: 30,
  // },
  // overlayContent: {
  //   width: '100%',
  //   backgroundColor: '#FFFFFF',
  //   paddingVertical: 40,
  //   borderRadius: 28, // 둥근 모서리 강조
  //   alignItems: 'center',
  //   ...Platform.select({
  //     ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 10 }, shadowOpacity: 0.1, shadowRadius: 20 },
  //     android: { elevation: 10 },
  //   }),
  // },
  // overlayTitle: { fontSize: 22, fontWeight: '800', color: '#0F172A', marginTop: 20, marginBottom: 8 },
  // overlayText: { fontSize: 15, color: '#64748B', textAlign: 'center', lineHeight: 22 },
  // ------------------------------------------------------------

  // 커스텀 마커 디자인 강화 ( Indigo 컬러 포인트 )
  customMarker: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  markerDot: {
    width: 14,
    height: 14,
    backgroundColor: '#6366F1', // Indigo (메인 컬러)
    borderRadius: 7,
    borderWidth: 2.5,
    borderColor: '#FFFFFF', // 흰색 테두리
  },
  markerHalo: {
    position: 'absolute',
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: 'rgba(99, 102, 241, 0.15)', // 연한 Indigo 후광
    borderWidth: 1,
    borderColor: 'rgba(99, 102, 241, 0.3)',
  },
  loadingText: {
    marginTop: 20,
    fontSize: 15,
    fontWeight: '500',
    color: '#94A3B8', // 연한 그레이
  },

  // 식당 전용 마커 스타일
// MapStyle.js 내 styles 객체 수정 영역

  // (기존 내 위치 마커 유지)
  customMarker: { alignItems: 'center', justifyContent: 'center' },
  markerDot: { width: 14, height: 14, backgroundColor: '#6366F1', borderRadius: 7, borderWidth: 2.5, borderColor: '#FFFFFF' },
  markerHalo: { position: 'absolute', width: 30, height: 30, borderRadius: 15, backgroundColor: 'rgba(99, 102, 241, 0.15)', borderWidth: 1, borderColor: 'rgba(99, 102, 241, 0.3)' },
  
  // ============================================================
  // 식당 전용 마커
  // ============================================================
  
  // 1. 핀 전체 구조와 그림자를 담당하는 컨테이너
  pinContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  // 2. 아이콘이 박힌 상단 원형 부분
  pinCircle: {
    width: 32,
    height: 32,
    backgroundColor: '#F43F5E',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#FFFFFF',
    zIndex: 2, // 팁보다 위에 노출
  },
  // 3. 하단 뾰족한 삼각형 부분
  pinTip: {
    width: 12,
    height: 12,
    backgroundColor: '#F43F5E',
    borderLeftWidth: 2,
    borderBottomWidth: 2,
    borderColor: '#FFFFFF',
    transform: [{ rotate: '-45deg' }], 
    marginTop: -6,
    zIndex: 1,
  },
  
  loadingText: { marginTop: 20, fontSize: 15, fontWeight: '500', color: '#94A3B8' },


  // ============================================================
  // [ 바텀 시트 레이아웃 - 식당 정보 카드 ]
  // ============================================================
  bottomSheet: {
    position: 'absolute',
    bottom: 0, // 애니메이션 처리를 위해 0으로 고정
    left: 0,
    right: 0,
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: Platform.OS === 'ios' ? 75 : 55, // 기기별 하단 여백 최적화
    minHeight: 180,
    elevation: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -10 },
    shadowOpacity: 0.1,
    shadowRadius: 15,
  },
  sheetHandle: {
    width: 40,
    height: 4,
    backgroundColor: '#E2E8F0',
    borderRadius: 2,
    alignSelf: 'center',
    marginBottom: 20,
  },
  sheetHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  sheetName: {
    fontSize: 22,
    fontWeight: '800',
    color: '#0F172A',
    letterSpacing: -0.5,
  },
  tagRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    marginTop: 8,
  },
  categoryTag: {
    backgroundColor: '#F1F5F9',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  tagText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#64748B',
  },
  sheetActionRow: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 8,
  },
  kakaoButton: {
    flex: 1,
    height: 52,
    backgroundColor: '#FEE500', // 카카오 브랜드 컬러
    borderRadius: 14,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
  },
  kakaoButtonText: {
    color: '#3C1E1E',
    fontWeight: '700',
    fontSize: 15,
  },
  closeButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#F8FAFC',
    justifyContent: 'center',
    alignItems: 'center',
  },

  markerContainer: {
    backgroundColor: '#FFF',
    padding: 8,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#6366F1',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  selectedMarker: {
    backgroundColor: '#6366F1',
    borderColor: '#FFF',
    transform: [{ scale: 1.1 }], // 선택 시 약간 확대
  },

});

// ============================================================
// [ 지도 커스텀 스타일 ]
// ============================================================
export const cleanMapStyle = [
  {
    "featureType": "all",
    "elementType": "labels.text.fill",
    "stylers": [{ "color": "#475569" }] 
  },
  // 1. 도로 명칭(성대로 등) 및 모든 라벨 제거
  {
    "featureType": "road",
    "elementType": "labels.text",
    "stylers": [{ "visibility": "off" }] 
  },
  // 2. 관심 지점(POI) 아이콘 및 라벨 제거
  {
    "featureType": "poi",
    "stylers": [{ "visibility": "off" }] 
  },
  // 3. 지형(바닥) 설정 - 가장 밝은 연그레이로 베이스 처리
  {
    "featureType": "landscape",
    "elementType": "geometry.fill",
    "stylers": [{ "color": "#F8FAFC" }] 
  },
  // 4. 건물(Man-made) 설정 - 지형보다 어둡게 설정하여 확실히 구분
  {
    "featureType": "landscape.man_made",
    "elementType": "geometry.fill",
    "stylers": [{ "color": "#E2E8F0" }] 
  },
  // 5. 건물 테두리 - 선을 명확히 그어 경계선 확정
  {
    "featureType": "landscape.man_made",
    "elementType": "geometry.stroke",
    "stylers": [{ "color": "#CBD5E1" }, { "visibility": "on" }] 
  },
  // 6. 도로 디자인 - 건물/지형과 대비되도록 구성
  {
    "featureType": "road.highway",
    "elementType": "geometry.fill",
    "stylers": [{ "color": "#FFFFFF" }] 
  },
  {
    "featureType": "road.arterial",
    "elementType": "geometry.fill",
    "stylers": [{ "color": "#FFFFFF" }] 
  },
  {
    "featureType": "road.local",
    "elementType": "geometry.fill",
    "stylers": [{ "color": "#FFFFFF" }] 
  },
  // 7. 물 디자인 - 연한 블루 그레이로 모던함 유지
  {
    "featureType": "water",
    "elementType": "geometry.fill",
    "stylers": [{ "color": "#E2E8F0" }] 
  },
  // 8. 기타 대중교통 요소 제거
  {
    "featureType": "transit",
    "stylers": [{ "visibility": "off" }] 
  }
];