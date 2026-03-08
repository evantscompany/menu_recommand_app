import { StyleSheet, Dimensions } from 'react-native';
const { height } = Dimensions.get('window');

export const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { marginTop: 40, paddingHorizontal: 30, height: 100, justifyContent: 'center' },
  headerTitle: { fontSize: 30, fontWeight: '900', color: '#FFFFFF' },
  headerSub: { fontSize: 14, color: '#94A3B8', marginTop: 4 },

  listContainer: { flex: 1, justifyContent: 'center', paddingVertical: 10 },
  
  cardWrapper: { height: '80%', justifyContent: 'center' }, // 높이 조정
  mainCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 35,
    elevation: 10,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 15,
    overflow: 'hidden',
  },

  // [MOD]: 이미지 영역 대체 헤더
  matchHeader: { 
    height: 80, 
    backgroundColor: '#F8FAFC', 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center',
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#F1F5F9'
  },
  rankBadge: { backgroundColor: '#1E293B', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  rankText: { color: '#FFF', fontWeight: 'bold', fontSize: 11 },
  
  matchBadge: { alignItems: 'flex-end' },
  matchLabel: { fontSize: 10, color: '#94A3B8', fontWeight: 'bold' },
  matchValue: { fontSize: 22, color: '#6366F1', fontWeight: '900' },

  infoArea: { flex: 1, padding: 25, justifyContent: 'center' }, // 가독성 위해 flex 부여
  titleRow: { marginBottom: 8 },
  storeName: { fontSize: 26, fontWeight: '900', color: '#1E293B' },
  
  categoryText: { color: '#6366F1', fontWeight: '800', fontSize: 14, marginBottom: 15 },
  addressText: { color: '#64748B', fontSize: 15, lineHeight: 22 },

  interactionArea: { flexDirection: 'row', height: 90, borderTopWidth: 1, borderColor: '#F1F5F9' },
  actionBtn: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  iconCircle: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center', marginBottom: 6 },
  divider: { width: 1, height: '40%', backgroundColor: '#F1F5F9', alignSelf: 'center' },
  
  btnLabelRed: { fontSize: 12, color: '#F87171', fontWeight: 'bold' },
  btnLabelGreen: { fontSize: 12, color: '#22C55E', fontWeight: 'bold' },

  retryBtn: { marginHorizontal: 30, marginBottom: 30, padding: 18, borderRadius: 20, backgroundColor: 'rgba(255,255,255,0.08)', alignItems: 'center' },
  retryText: { color: '#94A3B8', fontWeight: 'bold', fontSize: 14 },
});