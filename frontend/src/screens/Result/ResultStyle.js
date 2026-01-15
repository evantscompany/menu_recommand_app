/**
 * @file ResultStyle.js
 * @description 결과 출력 화면(ResultScreen) 전용 스타일 시트
 */

import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  headerTitle: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 30,
  },
  resultCard: {
    width: '100%',
    backgroundColor: '#F8F9FA',
    borderRadius: 20,
    padding: 30,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E9ECEF',
  },
  subText: {
    fontSize: 15,
    color: '#666',
    marginBottom: 10,
  },
  mainMenu: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF4D4D',
    marginVertical: 15,
  },
  divider: {
    width: '100%',
    height: 1,
    backgroundColor: '#DEE2E6',
    marginVertical: 20,
  },
  infoArea: {
    alignSelf: 'flex-start',
  },
  infoText: {
    fontSize: 16,
    color: '#495057',
    marginBottom: 5,
  },
  homeButton: {
    marginTop: 40,
    backgroundColor: '#FEE500',
    paddingVertical: 15,
    paddingHorizontal: 60,
    borderRadius: 12,
  },
  homeButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#3C1E1E',
  },
});