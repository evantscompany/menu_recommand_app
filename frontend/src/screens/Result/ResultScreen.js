/**
 * @file ResultScreen.js
 * @description 서버로부터 받은 실제 추천 식당 리스트 렌더링
 */

import React from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { styles } from './ResultStyle'; 

const ResultScreen = ({ route, navigation }) => {
  // QuestionScreen에서 보낸 데이터 수신 (recommendations 추가)
  const { userSurvey, recommendations } = route.params || { userSurvey: {}, recommendations: [] };

  return (
    <View style={styles.container}>
      <Text style={styles.headerTitle}>분석 완료 🎯</Text>
      
      {/* 여러 개의 식당이 올 수 있으므로 ScrollView 사용 권장 */}
      <ScrollView style={{ width: '100%' }} contentContainerStyle={{ alignItems: 'center' }}>
        
        {/* 추천 식당 리스트 렌더링 */}
        {recommendations && recommendations.length > 0 ? (
          recommendations.map((store, index) => (
            <View key={store.store_id || index} style={styles.resultCard}>
              <Text style={styles.subText}>{index + 1}순위 추천</Text>
              <Text style={styles.mainMenu}>🍴 {store.store_name}</Text>
              
              <View style={styles.tagArea}>
                <Text style={styles.categoryTag}>#{store.category}</Text>
                <Text style={styles.categoryTag}>#₩{store.price_level.toLocaleString()}</Text>
              </View>

              <View style={styles.divider} />
              
              <View style={styles.infoArea}>
                <Text style={styles.infoText}>📍 주소: {store.address || '정보 없음'}</Text>
                <Text style={styles.infoText}>📞 번호: {store.phone_number || '정보 없음'}</Text>
                {/* StoreDetail 정보가 포함되어 있다면 아래처럼 표시 가능 */}
                {store.details && (
                   <Text style={styles.infoText}>⭐️ 만족도: {store.details.real_satisfaction_score} / 5.0</Text>
                )}
              </View>
            </View>
          ))
        ) : (
          <View style={styles.resultCard}>
            <Text style={styles.mainMenu}>결과가 없습니다. 😅</Text>
            <Text style={styles.subText}>조건을 조금 더 완만하게 조정해보세요.</Text>
          </View>
        )}

        {/* 유저가 입력한 데이터 확인용 (선택 사항) */}
        <View style={{ marginTop: 20, marginBottom: 40 }}>
           <Text style={{ textAlign: 'center', color: '#666' }}>내가 선택한 조건</Text>
           <Text style={{ color: '#999', fontSize: 12 }}>
             {userSurvey.dietary_restriction} | {userSurvey.spicy_level} | {userSurvey.budget_range}
           </Text>
        </View>

      </ScrollView>

      <TouchableOpacity 
        style={styles.homeButton} 
        onPress={() => navigation.navigate('Question')} // 다시 질문지로 이동
      >
        <Text style={styles.homeButtonText}>다시 하기</Text>
      </TouchableOpacity>
    </View>
  );
};

export default ResultScreen;