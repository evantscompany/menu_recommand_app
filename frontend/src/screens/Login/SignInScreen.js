// 로그인

import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  Alert,
  KeyboardAvoidingView, 
  TouchableWithoutFeedback, 
  Keyboard,
  Platform,
  ScrollView
} from 'react-native';

import { styles } from './LoginStyle';
import apiClient from '../../Api/apiClient'
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialCommunityIcons } from '@expo/vector-icons'; 
import AsyncStorage from '@react-native-async-storage/async-storage'; // 수정: 필수 저장소 모듈 추가
import CommonLoadingScreen from '../../components/CommonLoadingScreen'; // 추가: 공통 로딩 컴포넌트

const SignInScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false); // 추가: 로딩 상태 관리

  const handleSignIn = async () => {
    // 추가: 로딩 중일 경우 중복 클릭 방지
    if (isLoading) return;

    // 수정: 자동 띄어쓰기 입력 방지를 위해 trim() 적용
    const trimId = username.trim();
    const trimPw = password.trim();

    if (!trimId || !trimPw) {
      Alert.alert("알림", "아이디와 비밀번호를 모두 입력해주세요.");
      return;
    }

    // // // =========================================================
    // // // [MOCK_MODE]: 서버 연동 전 UI 및 로직 테스트용
    // // // ---------------------------------------------------------
    // console.log('[MOCK] 로그인 시도 데이터:', { username: trimId, password: trimPw });
    // Alert.alert("테스트", "로그인 버튼이 정상 작동합니다. (MOCK_MODE)");
    // navigation.replace('Home'); 
    // // =========================================================



    // =========================================================
    // [REAL_API]: 실제 백엔드 서버 연동 구역 
    // ---------------------------------------------------------
    try {
      setIsLoading(true); // 추가: 통신 시작 시 로딩 활성화

      const response = await apiClient.post(apiClient.urls.LOGIN, { 
        username: trimId, 
        password: trimPw 
      });

      if (response && response.access_token) {
        await AsyncStorage.setItem('userToken', response.access_token);
        await AsyncStorage.setItem('userNickname', response.nickname); 

        apiClient.defaults.headers.Authorization = `Bearer ${response.access_token}`;

        navigation.replace('Home', { access_token: response.access_token }); 
      }
    } catch (error) {
      setIsLoading(false); // 추가: 실패 시 버튼 다시 활성화를 위해 로딩 해제
      console.error("[Login Error]:", error.response?.data || error);
      
      const errorDetail = error.response?.data?.detail;
      Alert.alert(
        "로그인 실패", 
        errorDetail === "아이디 또는 비밀번호가 틀렸습니다." 
          ? errorDetail 
          : "아이디 또는 비밀번호를 다시 확인해주세요."
      );
    }
    // =========================================================
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* 추가: 로딩 상태일 때 화면을 덮어 연타 및 조작 방지 */}
      {isLoading && <CommonLoadingScreen message="로그인중...🐣" />}

      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={{ flex: 1 }}
      >
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
          <ScrollView 
            contentContainerStyle={{ flexGrow: 1 }}
            showsVerticalScrollIndicator={false}
          >
            <View style={styles.content}>
              
              <View style={styles.headerArea}>
                <TouchableOpacity onPress={() => navigation.goBack()} disabled={isLoading}>
                  <MaterialCommunityIcons name="arrow-left" size={28} color="#FFFFFF" style={{ marginBottom: 20 }} />
                </TouchableOpacity>
                <Text style={styles.titleText}>Mechuri</Text>
                <Text style={styles.subTitleText}>당신의 오늘 점심을 책임집니다</Text>
              </View>

              <View style={styles.bottomArea}>
                <Text style={styles.inputLabel}>로그인 정보 입력</Text>
                
                <TextInput 
                  style={styles.inputField} 
                  placeholder="아이디" 
                  placeholderTextColor="#94A3B8"
                  value={username}
                  onChangeText={setUsername}
                  autoCapitalize="none"
                  autoCorrect={false}
                  editable={!isLoading} // 추가: 로딩 중 입력 수정 방지
                />

                <TextInput 
                  style={styles.inputField} 
                  placeholder="비밀번호" 
                  placeholderTextColor="#94A3B8"
                  secureTextEntry
                  value={password}
                  onChangeText={setPassword}
                  textContentType="password"
                  autoCapitalize="none" // 수정: 비밀번호 첫 글자 대문자 자동변환 방지
                  autoCorrect={false} // 수정: 스마트폰 자동완성 방지
                  editable={!isLoading} // 추가: 로딩 중 입력 수정 방지
                />

                <TouchableOpacity 
                  style={[styles.mainLoginButton, isLoading && { opacity: 0.7 }]} // 추가: 로딩 중 시각적 비활성화 표시
                  onPress={handleSignIn}
                  activeOpacity={0.8}
                  disabled={isLoading} // 추가: 로딩 중 버튼 클릭 차단
                >
                  <Text style={styles.loginButtonText}>
                    {isLoading ? "로그인 중" : "로그인하기"}
                  </Text>
                  <MaterialCommunityIcons 
                    name={isLoading ? "dots-horizontal" : "login"} 
                    size={24} 
                    color="#FFFFFF" 
                    style={{ marginLeft: 8 }} 
                  />
                </TouchableOpacity>

                <View style={styles.signUpContainer}>
                  <Text style={styles.footerText}>아직 회원이 아니신가요? </Text>
                  <TouchableOpacity onPress={() => navigation.navigate('SignUp')} disabled={isLoading}>
                    <Text style={styles.signUpLinkText}>회원가입</Text>
                  </TouchableOpacity>
                </View>
                
              </View>

            </View>
          </ScrollView>
        </TouchableWithoutFeedback>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default SignInScreen;