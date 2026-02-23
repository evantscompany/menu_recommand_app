/**
 * QuestionScreen.js
 */

import React, { useState, useRef } from 'react';
import { 
  View, Text, TouchableOpacity, TextInput, Alert, 
  SafeAreaView, Keyboard, TouchableWithoutFeedback,
  PanResponder
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import apiClient from '../../Api/apiClient';
import { styles } from './QuestionStyle'; 
import { MaterialCommunityIcons } from '@expo/vector-icons'; 
import CommonLoading from '../../components/CommonLoadingScreen';

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
    placeholder: "숫자만 입력 (예: 10000)" 
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
  const [inputText, setInputText] = useState("10000");
  const [loading, setLoading] = useState(false);

  // 누적 드래그 거리를 체크하기 위한 변수
  const dragAccumulator = useRef(0);

  // [드래그 로직] 위아래 스와이프로 금액 조절
  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onMoveShouldSetPanResponder: () => true,
      onPanResponderGrant: () => {
        dragAccumulator.current = 0;
      },
      onPanResponderMove: (evt, gestureState) => {
        // 감도 조절: 12픽셀 이동 시 1,000원씩 변경
        const threshold = 12; 
        const diff = gestureState.dy - dragAccumulator.current;

        if (Math.abs(diff) >= threshold) {
          // 위로 밀면(-dy) 증가, 아래로 밀면(+dy) 감소
          const change = diff < 0 ? 1000 : -1000;
          adjustBudget(change);
          dragAccumulator.current = gestureState.dy;
        }
      },
      onPanResponderRelease: () => {
        dragAccumulator.current = 0;
      }
    })
  ).current;

  // 금액 조절 함수 (천원 단위)
  const adjustBudget = (amount) => {
    setInputText((prev) => {
      const currentBudget = parseInt(prev, 10) || 0;
      const newBudget = Math.max(0, currentBudget + amount);
      return String(newBudget);
    });
  };

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
      
      // 다음 질문으로 넘어갈 때 만원으로 다시 세팅
      setInputText("10000");
    } else {
      // 서버 전송 로직
      submitSurvey(newAnswers);
    }
  };

  const submitSurvey = async (finalAnswers) => {
    const requestData = {
      ...accountData,
      ...finalAnswers,
      allergies: ""
    };

    setLoading(true);
    try {
      // 1단계: 회원가입
      await apiClient.post(apiClient.urls.SIGNUP, requestData);
      
      // 2단계: 자동 로그인
      const loginRes = await apiClient.post(apiClient.urls.LOGIN, {
        username: requestData.username,
        password: requestData.password
      });

      // 3단계: 토큰 수신 및 결과 화면 이동
      if (loginRes && loginRes.access_token) {
        await AsyncStorage.setItem('userToken', loginRes.access_token);
        await AsyncStorage.setItem('userNickname', loginRes.nickname || requestData.nickname);

        apiClient.defaults.headers.Authorization = `Bearer ${loginRes.access_token}`;
        
        Alert.alert("성공", "회원가입 및 취향 분석이 완료되었습니다!");
        navigation.navigate('Result', { 
          userSurvey: requestData, 
          access_token: loginRes.access_token
        });
      }
    } catch (error) {
      console.error("[Network Error]:", error.response?.data || error);
      Alert.alert(
        "가입 실패", 
        error.response?.data?.detail || "이미 존재하는 아이디거나 통신 에러가 발생했습니다.",
        [{ text: "확인", onPress: () => navigation.navigate('SignUp') }]
      );
    } finally {
      setLoading(false);
    }
  };

  const currentQ = questions[currentStep];
  const progressPercent = ((currentStep + 1) / questions.length) * 100;

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <SafeAreaView style={styles.container}>
        {loading && <CommonLoading message="🐣 취향 분석 데이터를 처리 중입니다..." />}
        
        {!loading && (
          <View style={styles.contentContainer}>
            <View style={styles.headerArea}>
              <View style={styles.stepInfoContainer}>
                <Text style={styles.stepText}>Step {currentStep + 1}</Text>
                <Text style={styles.totalStepText}>/ {questions.length}</Text>
              </View>
              <View style={styles.progressBarBg}>
                <View style={[styles.progressBarFill, { width: `${progressPercent}%` }]} />
              </View>
            </View>
            
            <View style={styles.cardWrapper}>
              <View style={styles.cardContainer}>
                <Text style={styles.categoryBadge}>{currentQ.category}</Text>
                <Text style={styles.questionTitle}>{currentQ.question}</Text>

                {currentQ.type === "INPUT" ? (
                  <View style={styles.inputWrapper}>
                    {/* 가로 정렬: 입력창 + 드래그 전용 아이콘 구역 */}
                    <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 30 }}>
                      <TextInput
                        style={[styles.budgetInput, { flex: 1, textAlign: 'center', marginBottom: 0 }]}
                        placeholder={currentQ.placeholder}
                        placeholderTextColor="#94A3B8"
                        keyboardType="numeric"
                        value={inputText}
                        onChangeText={setInputText}
                      />
                      
                      {/* [드래그 전용 아이콘 핸들] 디자인 */}
                      <View 
                        {...panResponder.panHandlers} 
                        style={{ 
                          width: 50, 
                          height: 70,
                          backgroundColor: '#F8FAFC',
                          borderRadius: 15, 
                          marginLeft: 12,
                          justifyContent: 'center', 
                          alignItems: 'center',
                          borderWidth: 1.5,
                          borderColor: '#E2E8F0', 
                          // 그림자(iOS용)
                          shadowColor: "#000",
                          shadowOffset: { width: 0, height: 2 },
                          shadowOpacity: 0.05,
                          shadowRadius: 3,
                          elevation: 2, // 그림자(안드로이드용)
                        }}
                      >
                        {/* 상단 화살표 */}
                        <MaterialCommunityIcons name="chevron-up" size={20} color="#6366F1" style={{ marginBottom: -4 }} />
                        
                        {/* 슬라이더 핸들 느낌의 점 3개 ("드래그" 암시) */}
                        <View style={{ marginVertical: 2 }}>
                            <View style={{ width: 4, height: 4, borderRadius: 2, backgroundColor: '#CBD5E1', marginBottom: 2 }} />
                            <View style={{ width: 4, height: 4, borderRadius: 2, backgroundColor: '#CBD5E1', marginBottom: 2 }} />
                            <View style={{ width: 4, height: 4, borderRadius: 2, backgroundColor: '#CBD5E1' }} />
                        </View>

                        {/* 하단 화살표 */}
                        <MaterialCommunityIcons name="chevron-down" size={20} color="#6366F1" style={{ marginTop: -4 }} />
                      </View>
                    </View>

                    <TouchableOpacity 
                      style={[styles.confirmButton, { width: '100%' }]} 
                      onPress={() => {
                        Keyboard.dismiss();
                        handleAnswer(inputText);
                      }}
                    >
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
    </TouchableWithoutFeedback>
  );
};

export default QuestionScreen;