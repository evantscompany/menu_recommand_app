import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Dimensions, FlatList, SafeAreaView, Alert, ActivityIndicator } from 'react-native';
import { styles } from './ResultStyle'; 
import FontAwesome from '@expo/vector-icons/FontAwesome';
import axios from 'axios'; 

const { width } = Dimensions.get('window');
const CARD_WIDTH = width * 0.72; 
const CARD_MARGIN = 10; 
const SNAP_INTERVAL = CARD_WIDTH + (CARD_MARGIN * 2); 

const ResultScreen = ({ route, navigation }) => {
  // [State] 추천 결과 데이터 관리
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  // QuestionScreen에서 전달받은 기본 데이터 (서버 통신 시 활용)
  const { userSurvey } = route.params || {};

  // 화면 진입 시 추천 결과 조회
  useEffect(() => {
    fetchRecommendations();
  }, []);

  /**
   * [GET] 추천 결과 조회 로직
   */
  const fetchRecommendations = async () => {
    // =========================================================
    // [MOCK_MODE]: 서버 연동 전 테스트용 (전달받은 데이터 그대로 사용)
    // ---------------------------------------------------------
    const { recommendations: initialData } = route.params || { recommendations: [] };
    setRecommendations(initialData);
    // =========================================================

    /* // =========================================================
    // [REAL_API]: 실제 서버 연동 구역  [GET] /api/recommendations 메뉴 추천 결과 받기
    // ---------------------------------------------------------
    setLoading(true);
    try {
      const SERVER_IP = '192.168.0.38'; 
      const PORT = '8000';
      
      const response = await axios.get(`http://${SERVER_IP}:${PORT}/api/recommendations`, {
        params: { user_id: userSurvey?.username || 'guest' } // 명세 기반 파라미터
      });

      if (response.data) {
        setRecommendations(response.data);
      }
    } catch (error) {
      console.error('[REAL] 추천 조회 실패:', error);
      Alert.alert("연동 에러", "추천 결과를 가져오지 못했습니다.");
    } finally {
      setLoading(false);
    }
    // ========================================================= */
  };

  /**
   * [POST] 유저 피드백 전송 핸들러
   */
  const handleFeedback = async (item, type) => {


    // =========================================================
    // [MOCK_MODE]: 피드백 전송 테스트용
    // ---------------------------------------------------------
    console.log(`[MOCK] 피드백: ${item.menu_name}, 타입: ${type}`);
    Alert.alert("알림", `${type === 'like' ? '좋아요' : '별로야'}가 반영되었습니다. (MOCK)`);
    // =========================================================



    /* // =========================================================
    // [REAL_API]: [POST] /api/feedback 실제 서버 연동 구역 /api/feedback 유저 피드백 전송
    // ---------------------------------------------------------
    try {
      const SERVER_IP = '192.168.0.38';
      const PORT = '8000';

      const response = await axios.post(`http://${SERVER_IP}:${PORT}/api/feedback`, {
        user_id: userSurvey?.username || 'guest', // 현재 유저 ID
        menu_name: item.menu_name,                // 메뉴 이름
        feedback_type: type,                      // "like" 또는 "dislike"
        category: item.category,                  // 메뉴 카테고리
        score: item.match_rate || 0               // 추천 점수 (0~100)
      });

      if (response.status === 200 || response.status === 201) {
        Alert.alert("알림", "피드백이 서버에 저장되었습니다.");
      }
    } catch (error) {
      console.error('[REAL] 피드백 전송 실패:', error);
      Alert.alert("오류", "피드백 전송 중 문제가 발생했습니다.");
    }
    // ========================================================= */
  };

  const renderItem = ({ item, index }) => {
    return (
      <View style={[styles.cardWrapper, { width: CARD_WIDTH, marginHorizontal: CARD_MARGIN }]}>
        <View style={styles.mainCard}>
          <View style={styles.imageArea}>
            <View style={styles.rankBadge}>
              <Text style={styles.rankText}>{index + 1}위</Text>
            </View>
            <Text style={styles.placeholderText}>📸 메뉴 이미지</Text>
          </View>

          <View style={styles.infoArea}>
            <View style={styles.titleRow}>
              <Text style={styles.storeName} numberOfLines={1}>{item.menu_name || item.store_name}</Text>
              <Text style={styles.rating}>⭐ {item.details?.real_satisfaction_score || item.details?.rating || '4.5'}</Text>
            </View>
            <Text style={styles.categoryText}>#{item.category}</Text>
            <Text style={styles.addressText} numberOfLines={1}>
              {item.description ? `✨ ${item.description}` : `📍 ${item.address}`}
            </Text>
          </View>

          <View style={styles.interactionArea}>
            <TouchableOpacity style={styles.actionBtn} onPress={() => handleFeedback(item, 'dislike')}>
              <View style={[styles.iconCircle, { backgroundColor: '#FFF1F1' }]}>
                <FontAwesome name="thumbs-down" size={24} color="#F87171" />
              </View>
              <Text style={styles.btnLabelRed}>별로야</Text>
            </TouchableOpacity>
            
            <View style={styles.divider} />

            <TouchableOpacity style={styles.actionBtn} onPress={() => handleFeedback(item, 'like')}>
              <View style={[styles.iconCircle, { backgroundColor: '#F0FDF4' }]}>
                <FontAwesome name="thumbs-up" size={24} color="#22C55E" />
              </View>
              <Text style={styles.btnLabelGreen}>좋아요</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>이거 어때?</Text>
        <Text style={styles.headerSub}>당신의 취향을 분석한 결과입니다.</Text>
      </View>

      <View style={styles.listContainer}>
        {loading ? (
          <ActivityIndicator size="large" color="#6366F1" />
        ) : (
          <FlatList
            data={recommendations}
            renderItem={renderItem}
            keyExtractor={(item, index) => index.toString()}
            horizontal
            showsHorizontalScrollIndicator={false}
            snapToInterval={SNAP_INTERVAL}
            decelerationRate="fast"
            contentContainerStyle={{
              paddingHorizontal: (width - CARD_WIDTH) / 2 - CARD_MARGIN
            }}
          />
        )}
      </View>

      <TouchableOpacity style={styles.retryBtn} onPress={() => navigation.popToTop()}>
        <Text style={styles.retryText}>다시 추천받기</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
};

export default ResultScreen;