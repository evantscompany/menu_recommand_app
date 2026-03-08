import { StyleSheet, Dimensions } from 'react-native';

const { width } = Dimensions.get('window');

export const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#F8FAFC' 
  },
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
    marginBottom: 20,
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

  section: { padding: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: '#1E293B', marginBottom: 15 },
  
  // 주변 식당 리스트 스타일
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
  timeTag: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    backgroundColor: '#F1F5F9', 
    paddingHorizontal: 10, 
    paddingVertical: 5, 
    borderRadius: 12,
  },
  timeValue: {
    fontSize: 13,
    fontWeight: '800',
    color: '#4F46E5',
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