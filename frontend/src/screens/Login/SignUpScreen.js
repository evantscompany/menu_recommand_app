// 회원가입

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
import { SafeAreaView } from 'react-native-safe-area-context'
import { MaterialCommunityIcons } from '@expo/vector-icons'; 

const SignUpScreen = ({ navigation }) => {
  // 인적사항 수집을 위한 State
  const [username, setUsername] = useState('');
  const [nickname, setNickname] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState(''); // 수정: 비밀번호 확인용 State 추가

  /**
   * handleNextStep
   * @description QuestionScreen로 이동하며 데이터를 전달하는 함수
   */
  const handleNextStep = () => {
    // 필수 입력값 확인
    if (!username || !nickname || !email || !password || !confirmPassword) {
      Alert.alert("알림", "모든 항목을 입력해야 회원가입이 가능합니다.");
      return;
    }

    // 수정: 비밀번호 오타 방지 일치 여부 확인
    if (password !== confirmPassword) {
      Alert.alert("알림", "비밀번호가 일치하지 않습니다.");
      return;
    }

    // 수집된 데이터를 변수에 저장 (수정: 스마트폰 자동 띄어쓰기 방지를 위해 trim() 적용)
    const accountData = { 
      username: username.trim(), 
      nickname: nickname.trim(),
      email: email.trim(), 
      password: password.trim() 
    };

    navigation.navigate('Question', { accountData }); 
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={{ flex: 1 }}
      >
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>

          <ScrollView 
            contentContainerStyle={{ flexGrow: 1 }} 
            showsVerticalScrollIndicator={false} 
            keyboardShouldPersistTaps="handled" 
          >
            <View style={styles.content}>
              
              <View style={styles.headerArea}>
                <TouchableOpacity onPress={() => navigation.goBack()}>
                  <MaterialCommunityIcons name="arrow-left" size={28} color="#FFFFFF" style={{ marginBottom: 20 }} />
                </TouchableOpacity>
                <Text style={styles.titleText}>Sign Up</Text>
                <Text style={styles.subTitleText}>
                  "오늘 뭐 먹지?" 매일 하는 고민,{"\n"}내 취향에 딱 맞는 메뉴로 정해드릴게요.
                </Text>
              </View>

              <View style={styles.bottomArea}>
                <Text style={styles.inputLabel}>계정 정보 입력</Text>
                
                <TextInput 
                  style={styles.inputField} 
                  placeholder="계정ID" 
                  placeholderTextColor="#94A3B8"
                  value={username}
                  onChangeText={setUsername}
                  autoCapitalize="none"
                  autoCorrect={false}
                  returnKeyType="next"
                />

                <TextInput 
                  style={styles.inputField} 
                  placeholder="닉네임" 
                  placeholderTextColor="#94A3B8"
                  value={nickname}
                  onChangeText={setNickname}
                  returnKeyType="next"
                />
                
                <TextInput 
                  style={styles.inputField} 
                  placeholder="이메일 주소" 
                  placeholderTextColor="#94A3B8"
                  keyboardType="email-address"
                  value={email}
                  onChangeText={setEmail}
                  autoCapitalize="none"
                  autoCorrect={false}
                  textContentType="emailAddress"
                  returnKeyType="next"
                />

                <TextInput 
                  style={styles.inputField} 
                  placeholder="비밀번호 (8자 이상)" 
                  placeholderTextColor="#94A3B8"
                  secureTextEntry
                  value={password}
                  onChangeText={setPassword}
                  returnKeyType="next"
                />

                {/* 수정: 비밀번호 확인 입력창 추가 */}
                <TextInput 
                  style={styles.inputField} 
                  placeholder="비밀번호 확인" 
                  placeholderTextColor="#94A3B8"
                  secureTextEntry
                  value={confirmPassword}
                  onChangeText={setConfirmPassword}
                  autoCapitalize="none"
                  autoCorrect={false}
                  returnKeyType="done"
                />

                <TouchableOpacity 
                  style={styles.mainLoginButton} 
                  onPress={handleNextStep}
                  activeOpacity={0.8}
                >
                  <Text style={styles.loginButtonText}>내 취향 분석하기</Text>
                  <MaterialCommunityIcons name="chevron-right" size={24} color="#FFFFFF" />
                </TouchableOpacity>
              </View>

            </View>
          </ScrollView>
        </TouchableWithoutFeedback>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default SignUpScreen;