import { StyleSheet, Dimensions } from 'react-native';

const { width } = Dimensions.get('window');

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A', 
  },
  content: {
    flex: 1,
    paddingHorizontal: 35,
    justifyContent: 'space-between',
    paddingVertical: 60,
  },
  headerArea: {
    marginTop: 60,
    alignItems: 'flex-start',
  },
  iconCircle: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: 'rgba(99, 102, 241, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 25,
  },
  titleText: {
    fontSize: 52,
    fontWeight: '900',
    color: '#FFFFFF',
    letterSpacing: -1.5,
    marginBottom: 15,
  },
  subTitleText: {
    fontSize: 16,
    color: '#94A3B8',
    lineHeight: 26,
    fontWeight: '500',
    textAlign: 'left',
  },
  bottomArea: {
    width: '100%',
    paddingBottom: 20,
  },
  inputLabel: {
    color: '#64748B',
    fontSize: 13,
    marginBottom: 15,
    fontWeight: '600',
    paddingLeft: 4,
  },

  // 통합 메인 버튼 스타일 (로그인, 가입완료 등 공용)
  mainLoginButton: {
    backgroundColor: '#6366F1', 
    flexDirection: 'row',
    width: '100%',
    height: 58,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
    marginBottom: 20, 
    // 그림자 효과
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  loginButtonText: {
    color: '#FFFFFF',
    fontSize: 17,
    fontWeight: 'bold',
  },

  // 입력창 스타일
  inputField: {
    width: '100%',
    height: 58,
    backgroundColor: '#1E293B',
    borderRadius: 18,
    paddingHorizontal: 20,
    fontSize: 16,
    color: '#FFFFFF',
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#334155',
  },

  // 하단 링크 영역
  signUpContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  signUpLinkText: {
    color: '#6366F1',
    fontSize: 15,
    fontWeight: 'bold',
    textDecorationLine: 'underline',
  },
  
  footerArea: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  footerText: {
    color: '#475569',
    fontSize: 13,
  },
  linkText: {
    color: '#6366F1',
    fontSize: 13,
    fontWeight: 'bold',
    textDecorationLine: 'underline',
  },
});