/**
 * @file QuestionStyle.js
 * @description QuestionScreen 전용 외부 스타일 시트
 */

import { StyleSheet, Platform } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
    paddingHorizontal: 20,
    justifyContent: 'center',
  },
  progressContainer: {
    marginBottom: 20,
    alignItems: 'center',
  },
  progressText: {
    fontSize: 16,
    color: '#868E96',
    fontWeight: '700',
  },
  categoryText: {
    textAlign: 'center',
    color: '#007AFF',
    fontWeight: 'bold',
    marginBottom: 5,
  },
  questionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#212529',
    textAlign: 'center',
    marginBottom: 40,
  },
  /* [ADD] 예산 입력창 전용 스타일 */
  inputWrapper: {
    width: '100%',
    alignItems: 'center',
    // 웹 브라우저 상호작용 우선순위 확보
    zIndex: 999, 
  },
  budgetInput: {
    backgroundColor: '#FFFFFF',
    width: '90%',
    padding: 18,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#007AFF',
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
    // 웹 브라우저용 포커스 아웃라인 제거
    ...Platform.select({
      web: {
        outlineStyle: 'none',
      },
    }),
  },
  /* [MOD] 확인 버튼 전용 스타일 */
  confirmButton: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
    width: '90%',
  },
  confirmButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
  /* 기존 옵션 버튼 스타일 */
  optionButton: {
    backgroundColor: '#FFFFFF',
    paddingVertical: 18,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#DEE2E6',
    alignItems: 'center',
  },
  optionText: {
    fontSize: 17,
    color: '#495057',
    fontWeight: '500',
  },
});