/**
 * @file QuestionScreen.js
 * @description 사용자 취향 분석 데이터 수집용 설문 컴포넌트
 */

import React, { useState } from 'react';
import { View, Text, TouchableOpacity, TextInput } from 'react-native';
import { styles } from './QuestionStyle'; 

const questions = [
  { 
    key: "dietary_restriction", 
    category: "식단 제한", 
    question: "원하는 식단이 있으십니까?", 
    options: ["뭐든 잘 먹음", "비건(채식주의)", "다이어터(저칼로리)", "육류 제외(해산물파)","유당불내증(NO유제품)"] 
  },
  { 
    key: "spicy_level", 
    category: "미각 성향(Taste)", 
    question: "매운맛 선호도 (1:순함 ~ 5:매움)", 
    options: ["1(아기예요)", "2(신라면)", "3(불닭볶음면)", "4(엽떡오리지널)", "5(핵불닭)"] 
  },
  { 
    key: "salty_level", 
    category: "미각 성향(Taste)", 
    question: "평소 선호하는 간의 세기는?", 
    options: ["많이 싱겁게", "싱겁게", "보통", "조금 짜게", "많이 짜게"] 
  },
  { 
    key: "budget_range", 
    category: "경제적 성향", 
    question: "한 끼 지출 가능 예산 상한선", 
    type: "INPUT", 
    placeholder: "직접 숫자로 입력하십시오"
  },
  { 
    key: "exploration_style", 
    category: "탐험 성향", 
    question: "선호하시는 음식점 스타일은?", 
    options: ["안정형(익숙한 맛)", "모험형(새로운 도전)"] 
  }
];

const QuestionScreen = ({ navigation }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [inputText, setInputText] = useState(""); 

  const handleAnswer = (value) => {
    const cleanValue = value ? value.toString().trim() : "";
    if (cleanValue === "") return;

    const currentQuestion = questions[currentStep];
    const finalValue = currentQuestion.type === "INPUT" ? `${cleanValue}원 이하` : cleanValue;
    
    const newAnswers = { ...answers, [currentQuestion.key]: finalValue };
    setAnswers(newAnswers);

    if (currentStep < questions.length - 1) {
      setCurrentStep(currentStep + 1);
      setInputText(""); 
    } else {
      navigation.navigate('Result', { userSurvey: newAnswers });
    }
  };

  const currentQ = questions[currentStep];

  return (
    <View style={styles.container}>
      <View style={styles.progressContainer}>
        <Text style={styles.progressText}>{currentStep + 1} / {questions.length}</Text>
      </View>
      
      <Text style={styles.categoryText}>{currentQ.category}</Text>
      <Text style={styles.questionTitle}>{currentQ.question}</Text>

      {/* [LOGIC] 질문 타입에 따른 조건부 렌더링 - 스타일 참조 방식 통일 */}
      {currentQ.type === "INPUT" ? (
        <View style={styles.inputWrapper}>
          <TextInput
            style={styles.budgetInput}
            placeholder={currentQ.placeholder}
            keyboardType="numeric"
            value={inputText}
            onChangeText={setInputText}
            autoFocus={true}
          />
          <TouchableOpacity 
            style={[styles.optionButton, styles.confirmButton]}
            onPress={() => handleAnswer(inputText)}
          >
            <Text style={[styles.optionText, styles.confirmButtonText]}>확인</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View>
          {currentQ.options.map((option, index) => (
            <TouchableOpacity 
              key={`${currentStep}-${index}`} 
              style={styles.optionButton} 
              onPress={() => handleAnswer(option)}
            >
              <Text style={styles.optionText}>{option}</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}
    </View>
  );
};

export default QuestionScreen;