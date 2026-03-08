import { StyleSheet, Platform } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  profileSection: {
    backgroundColor: '#FFF',
    paddingTop: 40,
    paddingBottom: 30,
    alignItems: 'center',
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  avatarWrapper: {
    position: 'relative',
    marginBottom: 15,
  },
  avatarCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#E0E7FF',
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  cameraBadge: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    backgroundColor: '#6366F1',
    width: 30,
    height: 30,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: '#FFF',
  },
  nickname: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#1E293B',
  },
  userEmail: {
    fontSize: 14,
    color: '#94A3B8',
    marginTop: 5,
  },

  /* 현재 활동 구역 카드 스타일 */
  locationCard: {
    width: '85%',
    backgroundColor: '#F8FAFC',
    borderRadius: 20,
    padding: 20,
    marginTop: 25,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    alignItems: 'center', // [MOD]: 내부 요소들을 가로축 중앙으로 정렬
    alignSelf: 'center',  // [MOD]: 카드 자체를 화면 중앙에 배치
  },
  locationHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center', // [ADD]: 헤더 내용 중앙 정렬
    marginBottom: 8,
    width: '100%',
  },
  locationLabel: {
    fontSize: 14,
    fontWeight: '700',
    color: '#64748B',
    marginLeft: 6,
  },
  locationText: {
    fontSize: 18,
    fontWeight: '800',
    color: '#1E293B',
    marginBottom: 4,
    textAlign: 'center', // [ADD]: 텍스트 중앙 정렬
  },
  locationSub: {
    fontSize: 12,
    color: '#94A3B8',
    textAlign: 'center', // [ADD]: 보조 설명 중앙 정렬
  },

  /* 메뉴 리스트 섹션 */
  menuSection: {
    marginTop: 20,
    paddingHorizontal: 20,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF',
    padding: 18,
    borderRadius: 15,
    marginBottom: 12,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  /* [NEW]: 미구현 메뉴 비활성화 스타일 */
  disabledMenuItem: {
    opacity: 0.5,
    backgroundColor: '#F8FAFC', // 배경을 살짝 더 어둡게
  },
  menuText: {
    flex: 1,
    fontSize: 16,
    color: '#334155',
    marginLeft: 15,
    fontWeight: '500',
  },
  /* [NEW]: 미구현 메뉴 텍스트 색상 */
  disabledMenuText: {
    color: '#CBD5E1',
  },

/* 게시판 느낌을 살린 공지사항 모달 스타일 */
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)', // 배경을 조금 더 어둡게 하여 게시판 강조
    justifyContent: 'center',
    alignItems: 'center',
  },
  noticeModal: {
    width: '85%',
    backgroundColor: '#FFF',
    borderRadius: 15,
    overflow: 'hidden', // 상단 바 둥근 모서리 적용을 위해 필수
    elevation: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
  },
  // 게시판 상단 포인트 바
  noticeTopBar: {
    height: 4,
    backgroundColor: '#6366F1', 
  },
  noticeHeader: {
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#F1F5F9',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center', // [MOD]: 타이틀 가운데 정렬을 위해 추가
    position: 'relative', // 닫기 버튼 배치를 위해 설정
  },
  noticeTitle: {
    fontSize: 18,
    fontWeight: '800',
    color: '#1E293B',
    textAlign: 'center', // [MOD]: 글씨 가운데 정렬
  },
  closeButton: {
    position: 'absolute',
    right: 15,
  },
  noticeContent: {
    padding: 30, // 여백을 넉넉히 주어 문서 느낌 강조
    alignItems: 'center',
    minHeight: 150,
    justifyContent: 'center',
  },
  noticeBody: {
    fontSize: 16,
    color: '#475569',
    lineHeight: 26,
    textAlign: 'center',
    fontWeight: '500',
  },
  // 하단 닫기 버튼 구역 (게시판 하단 버튼 느낌)
  noticeFooter: {
    padding: 15,
    backgroundColor: '#F8FAFC',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
  },
  footerCloseText: {
    fontSize: 14,
    color: '#6366F1',
    fontWeight: '700',
  },
});