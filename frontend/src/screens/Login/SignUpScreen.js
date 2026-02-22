import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  Alert,
  KeyboardAvoidingView, // 키보드가 입력창을 가리지 않게
  TouchableWithoutFeedback, // 터치 인식용
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

  /**
   * handleNextStep
   * @description QuestionScreen로 이동하며 데이터를 전달하는 함수
   */
  const handleNextStep = () => {
    // 필수 입력값 확인
    if (!username || !nickname || !email || !password) {
      Alert.alert("알림", "모든 항목을 입력해야 회원가입이 가능합니다.");
      return;
    }

    // 수집된 데이터를 변수에 저장
    const accountData = { 
      username: username, 
      nickname: nickname,
      email: email, 
      password: password 
    };

    // 변수를 Question으로 이동
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
            contentContainerStyle={{ flexGrow: 1 }} // 스크롤 내용이 적어도 전체 화면 높이 유지
            showsVerticalScrollIndicator={false} // 스크롤 바 숨기기
            keyboardShouldPersistTaps="handled" // 입력창 터치 시 키보드 유지
          >
            <View style={styles.content}>
              
              {/* [상단] 헤더 영역 */}
              <View style={styles.headerArea}>
                <TouchableOpacity onPress={() => navigation.goBack()}>
                  <MaterialCommunityIcons name="arrow-left" size={28} color="#FFFFFF" style={{ marginBottom: 20 }} />
                </TouchableOpacity>
                <Text style={styles.titleText}>Sign Up</Text>
                <Text style={styles.subTitleText}>
                  "오늘 뭐 먹지?" 매일 하는 고민,{"\n"}내 취향에 딱 맞는 메뉴로 정해드릴게요.
                </Text>
              </View>

              {/* [중앙] 입력 영역 */}
              <View style={styles.bottomArea}>
                <Text style={styles.inputLabel}>계정 정보 입력</Text>
                
                <TextInput 
                  style={styles.inputField} 
                  placeholder="계정ID" 
                  placeholderTextColor="#94A3B8"
                  value={username}
                  onChangeText={setUsername}
                  autoCapitalize="none"
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