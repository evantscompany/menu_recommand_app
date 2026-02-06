import { StyleSheet, Dimensions } from 'react-native';
const { height } = Dimensions.get('window');

export const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { marginTop: 40, paddingHorizontal: 30, height: 100, justifyContent: 'center' },
  headerTitle: { fontSize: 30, fontWeight: '900', color: '#FFFFFF' },
  headerSub: { fontSize: 14, color: '#94A3B8', marginTop: 4 },

  // [핵심] 리스트가 차지하는 영역을 화면 높이에 맞춰 유동적으로 조절
  listContainer: { flex: 1, justifyContent: 'center', paddingVertical: 10 },
  
  cardWrapper: { height: '90%', justifyContent: 'center' },
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

  imageArea: { flex: 1.1, backgroundColor: '#F1F5F9', justifyContent: 'center', alignItems: 'center' },
  rankBadge: { position: 'absolute', top: 15, left: 15, backgroundColor: '#1E293B', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  rankText: { color: '#FFF', fontWeight: 'bold', fontSize: 11 },
  placeholderText: { color: '#CBD5E1', fontSize: 12 },

  infoArea: { padding: 20 },
  titleRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 5 },
  storeName: { fontSize: 20, fontWeight: '900', color: '#1E293B', flex: 1, marginRight: 8 },
  rating: { fontSize: 14, color: '#F59E0B', fontWeight: 'bold' },
  categoryText: { color: '#6366F1', fontWeight: '800', fontSize: 13 },
  addressText: { color: '#64748B', marginTop: 10, fontSize: 12 },

  interactionArea: { flexDirection: 'row', height: 80, borderTopWidth: 1, borderColor: '#F1F5F9' },
  actionBtn: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  iconCircle: { width: 40, height: 40, borderRadius: 20, justifyContent: 'center', alignItems: 'center', marginBottom: 4 },
  divider: { width: 1, height: '40%', backgroundColor: '#F1F5F9', alignSelf: 'center' },
  
  btnLabelRed: { fontSize: 11, color: '#F87171', fontWeight: 'bold' },
  btnLabelGreen: { fontSize: 11, color: '#22C55E', fontWeight: 'bold' },

  retryBtn: { marginHorizontal: 30, marginBottom: 30, padding: 18, borderRadius: 20, backgroundColor: 'rgba(255,255,255,0.08)', alignItems: 'center' },
  retryText: { color: '#94A3B8', fontWeight: 'bold', fontSize: 14 },
});