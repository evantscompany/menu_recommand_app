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
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialCommunityIcons } from '@expo/vector-icons'; 

const SignInScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSignIn = async () => {
    if (!username || !password) {
      Alert.alert("알림", "아이디와 비밀번호를 모두 입력해주세요.");
      return;
    }

    // =========================================================
    // [MOCK_MODE]: 서버 연동 전 UI 및 로직 테스트용
    // ---------------------------------------------------------
    console.log('[MOCK] 로그인 시도 데이터:', { username, password });
    Alert.alert("테스트", "로그인 버튼이 정상 작동합니다. (MOCK_MODE)");
    // navigation.replace('Main'); 
    // =========================================================




/* // =========================================================
    // [REAL_API]: 실제 백엔드 서버 연동 구역 api/auth/login 로그인 데이터 전송
    // ---------------------------------------------------------
    // 서버 연동 시 위 [MOCK_MODE]를 주석 처리하고 여기 주석 해제
    try {
      const SERVER_IP = '192.168.0.38'; 
      const PORT = '8000';             
      
      const response = await fetch(`http://${SERVER_IP}:${PORT}/api/auth/login`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify({
          username: username, // 명세서 필드명 준수
          password: password, // 명세서 필드명 준수
        }),
      });

      const result = await response.json();

      if (response.ok) {
        // 성공 시 백엔드에서 준 JWT 토큰 수신
        console.log('[REAL] Login Success. Token:', result.token);
        Alert.alert("성공", "로그인에 성공했습니다.");
        
        // [중요] 로그인 성공 후 메인 화면으로 전환
        // navigation.replace('Main'); 
      } else {
        // ID/PW 불일치 등 서버에서 보낸 에러 메시지 표시
        Alert.alert("오류", result.message || "로그인 정보를 확인해주세요.");
      }
    } catch (error) {
      // 서버가 꺼져있거나 네트워크 연결이 안 될 때
      Alert.alert("연동 에러", "현재 서버와 통신할 수 없습니다.");
      console.error('[REAL] 통신 장애:', error);
    }
    // =========================================================
    */
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={{ flex: 1 }}
      >
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
          <ScrollView contentContainerStyle={{ flexGrow: 1 }} showsVerticalScrollIndicator={false}>
            <View style={styles.content}>
              
              <View style={styles.headerArea}>
                <TouchableOpacity onPress={() => navigation.goBack()}>
                  <MaterialCommunityIcons name="arrow-left" size={28} color="#FFFFFF" style={{ marginBottom: 20 }} />
                </TouchableOpacity>
                <Text style={styles.titleText}>Sign In</Text>
                <Text style={styles.subTitleText}>
                  다시 만나서 반가워요!{"\n"}아이디와 비밀번호를 입력해주세요.
                </Text>
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
                />

                <TextInput 
                  style={styles.inputField} 
                  placeholder="비밀번호" 
                  placeholderTextColor="#94A3B8"
                  secureTextEntry
                  value={password}
                  onChangeText={setPassword}
                  textContentType="password"
                />

                <TouchableOpacity 
                  style={styles.mainLoginButton} 
                  onPress={handleSignIn}
                  activeOpacity={0.8}
                >
                  <Text style={styles.loginButtonText}>로그인하기</Text>
                  <MaterialCommunityIcons name="login" size={24} color="#FFFFFF" style={{ marginLeft: 8 }} />
                </TouchableOpacity>

                {/* 비밀번호 재설정은 추후 고도화 시 추가 예정 */}
              </View>

            </View>
          </ScrollView>
        </TouchableWithoutFeedback>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default SignInScreen;