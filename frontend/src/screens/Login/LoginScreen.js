import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { styles } from './LoginStyle';

/**
 * LoginScreen Component
 * @description 서비스 진입 시 가장 먼저 노출되는 로그인 화면
 * @purpose 유저 식별 및 서비스 이용 권한 획득(OAuth)을 위한 엔트리 포인트 역할 수행
 */
const LoginScreen = ({ navigation }) => {

  /**
   * handleKakaoLogin
   * @description 카카오 인증 API를 호출하고 성공 시 유저 데이터 수집
   * @why 유저의 취향 데이터(식사 히스토리 등)를 DB에 고도화하기 위해 유저 식별자(UID)가 반드시 필요
   */
  const handleKakaoLogin = () => {
    // TODO: 백엔드 API 연동 (OAuth2.0 로직 구현 예정)
    console.log('카카오 로그인 시도 중...');
    
    // 로그인 성공을 가정하고 질문 화면으로 이동
    navigation.navigate('Question');
  };

  return (
    <View style={styles.container}>
      {/* 어플리케이션 타이틀 및 브랜딩 영역 */}
      <View style={styles.logoContainer}>
        <Text style={styles.titleText}>메추리 🐦</Text>
        <Text style={styles.subTitleText}>오늘 뭐 먹을지 고민될 땐?</Text>
      </View>

      {/* 소셜 로그인 인터렉션 영역 */}
      <TouchableOpacity 
        style={styles.kakaoButton}
        onPress={handleKakaoLogin}
      >
        <Text style={styles.buttonText}>카카오로 1초 만에 시작하기</Text>
      </TouchableOpacity>
    </View>
  );
};

export default LoginScreen;