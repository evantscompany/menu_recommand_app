/**
 * @file App.js
 * @description 애플리케이션의 최상위 엔트리 포인트 및 네비게이션 관제 시스템
 * @property {Component} NavigationContainer - 전체 네비게이션 상태 관리 컨테이너
 * @property {Stack} Stack.Navigator - 화면 전환 스택 관리 엔진
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

/** * @description 개별 화면 컴포넌트 모듈 임포트 
 */
import LoginScreen from './src/screens/Login/LoginScreen';
import QuestionScreen from './src/screens/Question/QuestionScreen';
import ResultScreen from './src/screens/Result/ResultScreen';
import SignUpScreen from './src/screens/Login/SignUpScreen';
import SignInScreen from './src/screens/Login/SignInScreen';


/**
 * @constant {Object} Stack
 * @description Stack Navigation 인스턴스 생성
 */
const Stack = createStackNavigator();

/**
 * @function App
 * @description 애플리케이션 메인 라우팅 정의 및 초기화
 * @returns {JSX.Element} Navigation 구조가 정의된 최상위 컴포넌트
 */
export default function App() {
  
  return (
    <NavigationContainer>
      {/* @config Stack.Navigator
        initialRouteName: 초기 기동 시 렌더링될 라우트 이름
        screenOptions: 글로벌 스크린 스타일 옵션 (Header 비활성화)
      */}
      <Stack.Navigator 
        initialRouteName="Login"
        screenOptions={{ headerShown: false }}
      >
        {/* [Route] 메인 진입 화면 */}
        <Stack.Screen name="Login" component={LoginScreen} />
        
        {/* [Route] 로그인 입력 화면 */}
        <Stack.Screen name="SignIn" component={SignInScreen} />

        {/* [Route] 회원가입 정보 입력 화면 */}
        <Stack.Screen name="SignUp" component={SignUpScreen} />
        
        {/* [Route] 사용자 성향 분석 질문지 화면 */}
        <Stack.Screen name="Question" component={QuestionScreen} />

        {/* [Route] 최종 데이터 기반 추천 결과 화면 */}
        <Stack.Screen name="Result" component={ResultScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}