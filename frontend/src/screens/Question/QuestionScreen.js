/**
 * QuestionScreen.js
 */

import React, { useState } from 'react';
import { View, Text, TouchableOpacity, TextInput, Alert, ActivityIndicator, SafeAreaView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import apiClient from '../../Api/apiClient';
import { styles } from './QuestionStyle'; 

const questions = [
  { 
    key: "dietary_label", 
    category: "식단 제한", 
    question: "원하는 식단을 고르세요", 
    options: [
      { label: "뭐든 잘 먹음", value: "none" },
      { label: "비건(채식)", value: "vegan" },
      { label: "다이어터", value: "diet" },
      { label: "페스코(해산물)", value: "pesco" },
      { label: "유당 불내증", value: "lactose_free" }
    ] 
  },
  { 
    key: "spicy_threshold", 
    category: "미각 성향", 
    question: "매운 걸 얼마나 잘 드시나요?", 
    options: [
      { label: "1. 진라면 순한맛", value: "1" },
      { label: "2. 신라면", value: "2" },
      { label: "3. 틈새라면", value: "3" },
      { label: "4. 불닭볶음면", value: "4" },
      { label: "5. 핵불닭", value: "5" }
    ] 
  },
  { 
    key: "saltiness_preference", 
    category: "미각 성향", 
    question: "평소 선호하는 간 세기는?", 
    options: [
      { label: "아주 싱겁게", value: "1" },
      { label: "삼삼하게", value: "2" },
      { label: "보통", value: "3" },
      { label: "짭짤하게", value: "4" },
      { label: "짜고 강한 맛", value: "5" }
    ] 
  },
  { 
    key: "lunch_budget_max", 
    category: "경제적 성향", 
    question: "한 끼 지출 가능 예산 상한선", 
    type: "INPUT", 
    placeholder: "숫자만 입력 (예: 12000)" 
  },
  { 
    key: "is_adventurous", 
    category: "탐험 성향", 
    question: "새로운 메뉴 도전을 좋아하시나요?", 
    options: [
      { label: "새로운 맛있는 걸 찾자!", value: "예(True)" },
      { label: "내가 아는 맛이 더 좋아", value: "아니오(False)" }
    ] 
  }
];

const QuestionScreen = ({ route, navigation }) => { 
  // SignUpScreen에서 넘겨받은 계정 정보 수신
  const { accountData } = route.params || {}; 
  
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnswer = async (value) => {
    const currentQuestion = questions[currentStep];
    let finalValue = value;

    // [데이터 변환]
    if (currentQuestion.key === "lunch_budget_max") {
      finalValue = parseInt(value, 10) || 12000; // 숫자(int)로 변환
    } else if (currentQuestion.key === "is_adventurous") {
      finalValue = value.includes("예"); // true/false(bool)로 변환
    } else if (currentQuestion.key === "spicy_threshold" || currentQuestion.key === "saltiness_preference") {
      finalValue = parseInt(value, 10); // 숫자(int)로 변환
    }
    const newAnswers = { ...answers, [currentQuestion.key]: finalValue };
    
    if (currentStep < questions.length - 1) {
      setAnswers(newAnswers);
      setCurrentStep(currentStep + 1);
      setInputText("");
    } else {
      // 서버 전송 로직
      submitSurvey(newAnswers);

    }
  };

  const submitSurvey = async (finalAnswers) => {
    // 백엔드 전송용 통합 데이터 생성 (계정 + 취향)
    const requestData = {
      ...accountData,    // username, email, password, nickname
      ...finalAnswers,   // dietary_label, spicy_threshold 등
      allergies: ""      // 선택사항이므로 일단 빈값 처리
    };

    // // // =========================================================
    // // // [MOCK_MODE]: 서버 연동 전 UI 및 로직 테스트용
    // // ---------------------------------------------------------
    // console.log('[MOCK] 회원가입 통합 데이터:', requestData);
    // Alert.alert("테스트", "설문이 완료되었습니다. 결과 화면으로 이동합니다.");
    // navigation.navigate('Result', { userSurvey: requestData, recommendations: [] });
    // // =========================================================



// =========================================================
    // [REAL_API]: 실제 백엔드 서버 연동 구역 api/auth/signup 회원가입 데이터 전송
    // ---------------------------------------------------------
    setLoading(true);
    try {
      // 1단계: 회원가입
      await apiClient.post(apiClient.urls.SIGNUP, requestData);
      
      // 2단계: 자동 로그인
      const params = new URLSearchParams();
      params.append('username', requestData.username);
      params.append('password', requestData.password);

      // 로그인 전용 규격
      const loginRes = await apiClient.post(apiClient.urls.LOGIN, params.toString(),{
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      // 3단계: 토큰 수신 및 결과 화면 이동
      if (loginRes && loginRes.access_token) {

        // 휴대폰 저장소에 토큰 보관 나중에 다시 켤때 사용
        await AsyncStorage.setItem('userToken', loginRes.access_token);

        // 토큰 즉시 사용
        apiClient.defaults.headers.Authorization = `Bearer ${loginRes.access_token}`;
        
        Alert.alert("성공", "회원가입 및 취향 분석이 완료되었습니다!");
        navigation.navigate('Result', { 
          userSurvey: requestData, 
          access_token: loginRes.access_token 
        });
      }
    } catch (error) {
      console.error("[Network Error]:", error);
      Alert.alert("가입 실패", "이미 존재하는 아이디거나 통신 에러가 발생했습니다.");
    } finally {
      setLoading(false);
    }
    // =========================================================

  };

  // 렌더링 헬퍼 변수
  const currentQ = questions[currentStep];
  const progressPercent = ((currentStep + 1) / questions.length) * 100;

  return (
    <SafeAreaView style={styles.container}>
      {loading ? (
        /* ==================== [Loading View] ==================== */
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#6366F1" />
          <Text style={styles.loadingText}>데이터를 불러오고 있습니다...</Text>
        </View>
      ) : (
        /* ==================== [Main Content] ==================== */
        <View style={styles.contentContainer}>
          
          {/* 1. Header Area (Progress Bar) */}
          <View style={styles.headerArea}>
            <View style={styles.stepInfoContainer}>
              <Text style={styles.stepText}>Step {currentStep + 1}</Text>
              <Text style={styles.totalStepText}>/ {questions.length}</Text>
            </View>
            <View style={styles.progressBarBg}>
              <View style={[styles.progressBarFill, { width: `${progressPercent}%` }]} />
            </View>
          </View>
          
          {/* 2. Card Area (Question UI) */}
          <View style={styles.cardWrapper}>
            <View style={styles.cardContainer}>
              <Text style={styles.categoryBadge}>{currentQ.category}</Text>
              <Text style={styles.questionTitle}>{currentQ.question}</Text>

              {/* 문항 타입별 조건부 렌더링 (Input vs Select) */}
              {currentQ.type === "INPUT" ? (
                <View style={styles.inputWrapper}>
                  <TextInput
                    style={styles.budgetInput}
                    placeholder={currentQ.placeholder}
                    placeholderTextColor="#94A3B8"
                    keyboardType="numeric"
                    value={inputText}
                    onChangeText={setInputText}
                  />
                  <TouchableOpacity style={styles.confirmButton} onPress={() => handleAnswer(inputText)}>
                    <Text style={styles.confirmButtonText}>확인</Text>
                  </TouchableOpacity>
                </View>
              ) : (
                <View style={styles.optionsContainer}>
                  {currentQ.options.map((option, index) => (
                    <TouchableOpacity 
                      key={index} 
                      style={styles.optionButton} 
                      onPress={() => handleAnswer(option.value)}
                    >
                      <Text style={styles.optionText}>{option.label}</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              )}
            </View>
          </View>

        </View>
      )}
    </SafeAreaView>
  );
};

export default QuestionScreen;