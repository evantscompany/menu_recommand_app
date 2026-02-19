import React from 'react';
import { 
  View, 
  Text, 
  TouchableOpacity, 
  SafeAreaView, 
} from 'react-native';

import { styles } from './LoginStyle';
import { MaterialCommunityIcons } from '@expo/vector-icons'; 

const LoginScreen = ({ navigation }) => {

  // 로그인 페이지로 이동
  const handleGoSignIn = () => {
    navigation.navigate('SignIn'); 
  };

  // 회원가입(설문) 페이지로 이동
  const handleGoSignUp = () => {
    navigation.navigate('SignUp'); 
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        
        <View style={styles.headerArea}>
          <View style={styles.iconCircle}>
            <MaterialCommunityIcons name="bird" size={48} color="#6366F1" />
          </View>

          <Text style={styles.titleText}>Mechuri</Text> 
          <Text style={styles.subTitleText}>
            오늘 뭐 먹을지 고민될 땐?{"\n"}당신의 취향을 분석해 드립니다.
          </Text>
        </View>

        <View style={styles.bottomArea}>
          <Text style={styles.inputLabel}>서비스 이용을 위해 로그인이 필요합니다</Text> 
          
          {/* [수정] 메인 로그인 버튼: 인디고 컬러로 변경 */}
          <TouchableOpacity 
            style={styles.mainLoginButton} // [수정] 스타일 명칭 변경
            onPress={handleGoSignIn}
            activeOpacity={0.8}
          >
            <MaterialCommunityIcons name="login" size={24} color="#FFFFFF" style={{ marginRight: 10 }} />
            <Text style={styles.loginButtonText}>로그인하기</Text>
          </TouchableOpacity>

          {/* [수정] 회원가입 버튼: 박스 형태 제거, 텍스트 링크 형태로 변경 */}
          <View style={styles.signUpContainer}>
            <Text style={styles.footerText}>처음이신가요? </Text>
            <TouchableOpacity onPress={handleGoSignUp}>
              <Text style={styles.signUpLinkText}>신규 회원가입</Text>
            </TouchableOpacity>
          </View>
          
          <View style={styles.footerArea}>
             <Text style={styles.footerText}>계속 진행하면 </Text>
             <TouchableOpacity><Text style={styles.linkText}>이용약관</Text></TouchableOpacity>
             <Text style={styles.footerText}>에 동의하게 됩니다.</Text>
          </View>
        </View>

      </View>
    </SafeAreaView>
  );
};

export default LoginScreen;