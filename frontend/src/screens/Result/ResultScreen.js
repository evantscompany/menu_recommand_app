/**
 * @file ResultScreen.js
 * @description 사용자 성향 분석 데이터 수신 및 최종 결과 렌더링
 */

import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
// [MOD] 외부 스타일 시트 참조 방식으로 변경
import { styles } from './ResultStyle'; 

/**
 * @function ResultScreen
 * @param {Object} route - 네비게이션 파라미터 수신
 */
const ResultScreen = ({ route, navigation }) => {
  // QuestionScreen으로부터 전달받은 5대 성향 데이터
  const { userSurvey } = route.params || { userSurvey: {} };

  return (
    <View style={styles.container}>
      <Text style={styles.headerTitle}>분석 완료 🐦</Text>
      
      <View style={styles.resultCard}>
        <Text style={styles.subText}>오늘의 추천은?</Text>
        
        {/* ============================================================
            [BACKEND LOGIC START]
            아래 영역은 추후 API 서버로부터 응답받은 실제 메뉴 데이터로 대체됩니다.
            ============================================================ */}
        
        {/* [DELETE_CANDIDATE] DB 연동 시 아래 하드코딩된 '매콤 제육볶음' 텍스트는 삭제됩니다. */}
        <Text style={styles.mainMenu}>🔥 매콤 제육볶음</Text>
        
        {/* ============================================================
            [BACKEND LOGIC END]
            ============================================================ */}

        <View style={styles.divider} />
        
        <View style={styles.infoArea}>
          {/* 유저가 선택한 원천 데이터(Source Data) 시각화 */}
          <Text style={styles.infoText}>📍 식단: {userSurvey.dietary_restriction || '미지정'}</Text>
          <Text style={styles.infoText}>🌶️ 맵기: {userSurvey.spicy_level || '0단계'}</Text>
          {/* [FIX] 입력받은 예산 상한선을 직관적으로 표시 */}
          <Text style={styles.infoText}>💰 예산: {userSurvey.budget_range || '제한 없음'}</Text>
          <Text style={styles.infoText}>🧂 간: {userSurvey.salty_level || '보통'}</Text>
          <Text style={styles.infoText}>🧭 스타일: {userSurvey.exploration_style || '안정형'}</Text>
        </View>
      </View>

      <TouchableOpacity 
        style={styles.homeButton} 
        onPress={() => navigation.navigate('Login')}
      >
        <Text style={styles.homeButtonText}>다시 하기</Text>
      </TouchableOpacity>
    </View>
  );
};

export default ResultScreen;