import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Dimensions, FlatList, SafeAreaView, Alert, ActivityIndicator } from 'react-native';
import { styles } from './ResultStyle'; 
import FontAwesome from '@expo/vector-icons/FontAwesome';
import axios from 'axios';
import apiClient from '../../Api/ApiClient';
import CommonLoading from '../../components/CommonLoadingScreen';

const { width } = Dimensions.get('window');
const CARD_WIDTH = width * 0.72; 
const CARD_MARGIN = 10; 
const SNAP_INTERVAL = CARD_WIDTH + (CARD_MARGIN * 2); 

const ResultScreen = ({ route, navigation }) => {
  // [State] 추천 결과 데이터 관리
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  // QuestionScreen에서 전달받은 기본 데이터 (서버 통신 시 활용)
  const { userSurvey, access_token } = route.params || {};
  const userToken = access_token;

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
    setLoading(true); // 로딩 시뮬레이션 시작
    
    setTimeout(() => {
      const mockData = [
        {
          menu_name: "매콤 치즈 부대찌개",
          category: "한식",
          description: "비 오는 날씨와 유저님의 매운맛 선호도가 일치합니다.",
          address: "서울 강남구 역삼동 123-4",
          details: { rating: "4.8" }
        },
        {
          menu_name: "바삭한 돈카츠",
          category: "일식",
          description: "최근 일식 카테고리 방문 빈도가 높으시네요!",
          address: "서울 강남구 논현동 56-7",
          details: { rating: "4.5" }
        },
        {
          menu_name: "연어 포케",
          category: "샐러드",
          description: "가벼운 한 끼를 원하실 때 추천드리는 메뉴입니다.",
          address: "서울 서초구 서초동 88-9",
          details: { rating: "4.2" }
        }
      ];

      setRecommendations(mockData);
      setLoading(false);
      console.log('[MOCK] 결과 화면 가짜 데이터 로드 완료');
    }, 1000); // 1초 뒤 데이터 출력
    // =========================================================



    // // =========================================================
    // // [REAL_API]: 실제 서버 연동 구역  [GET] /api/recommendations 메뉴 추천 결과 받기
    // // ---------------------------------------------------------

    // setLoading(true);
    // try {
    //   const data = await apiClient.post(API_ENDPOINTS.RECOMMEND, {
    //     dietary_restriction: userSurvey?.dietary_label || "none",
    //     spicy_level: String(userSurvey?.spicy_threshold || "3"),
    //     budget_range: String(userSurvey?.lunch_budget_max || "12000"),
    //     salty_level: String(userSurvey?.saltiness_preference || "3"),
    //     exploration_style: userSurvey?.is_adventurous ? "adventurous" : "stable",
    //     city: "Seoul"
    //   });

    //   if (data) {
    //     setRecommendations(data);
    //   }
    // } catch (error) {
    //   console.error('추천 조회 실패:', error);
    //   Alert.alert("연동 에러", "추천 결과를 가져오지 못했습니다.");
    // } finally {
    //   setLoading(false);
    // }
    // // ========================================================= */

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



    // // =========================================================
    // // [REAL_API]: [POST] /api/feedback 실제 서버 연동 구역 /api/feedback 유저 피드백 전송
    // // ---------------------------------------------------------
    // try {
    //   await apiClient.post(API_ENDPOINTS.FEEDBACK, {
    //     menu_name: item.menu_name || item.name,
    //     feedback_type: type,
    //     category: item.category || "일반",
    //     score: item.match_rate || 0
    //   });

    //   Alert.alert("알림", "피드백이 저장되었습니다.");
    // } catch (error) {
    //   console.error('피드백 전송 실패:', error);
    //   Alert.alert("오류", "피드백 전송 중 문제가 발생했습니다.");
    // }
    // // =========================================================
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
      {loading && <CommonLoading message={"취향과 날씨를\n정밀 분석 중입니다...🐣"} />}

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

      <TouchableOpacity style={styles.retryBtn} onPress={() => navigation.navigate('Home')}>
        <Text style={styles.retryText}>다시 추천받기</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
};

export default ResultScreen;