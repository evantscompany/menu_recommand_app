import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Dimensions, FlatList, SafeAreaView, Alert, ActivityIndicator } from 'react-native';
import { styles } from './ResultStyle'; 
import FontAwesome from '@expo/vector-icons/FontAwesome';
import apiClient from '../../Api/apiClient';

// [MOD]: 기존 CommonLoading 대신 새로 만든 미니게임 로딩 컴포넌트 임포트
import GameLoadingScreen from '../../components/GameLoadingScreen';

const { width } = Dimensions.get('window');
const CARD_WIDTH = width * 0.72; 
const CARD_MARGIN = 10; 
const SNAP_INTERVAL = CARD_WIDTH + (CARD_MARGIN * 2); 

const ResultScreen = ({ route, navigation }) => {
  // [State] 추천 결과 데이터 관리
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  // QuestionScreen에서 전달받은 기본 데이터 (서버 통신 시 활용)
  const { userSurvey, access_token, nickname } = route.params || {};
  const userToken = access_token;

  // 화면 진입 시 추천 결과 조회
  useEffect(() => {
    fetchRecommendations();
  }, []);

  /**
   * [GET] 추천 결과 조회 로직
   */
  const fetchRecommendations = async () => {

    /*
    // =========================================================
    // [MOCK_MODE]: 서버 연동 전 테스트용 (전달받은 데이터 그대로 사용)
    // ---------------------------------------------------------
    setLoading(true); // 로딩 시뮬레이션 시작
    
    setTimeout(() => {
      const mockData = [
        {
          menu_name: "매콤 치즈 부대찌개",
          category: "한식",
          price: 10000,
          match_rate: 85,
          description: "비 오는 날씨와 유저님의 매운맛 선호도가 일치합니다.",
          details: { rating: 4.8 }
        },
        {
          menu_name: "바삭한 돈카츠",
          category: "일식",
          price: 12000,
          match_rate: 72,
          description: "최근 일식 카테고리 방문 빈도가 높으시네요!",
          details: { rating: 4.5 }
        }
      ];

      setRecommendations(mockData);
      setLoading(false);
      console.log('[MOCK] 결과 화면 가짜 데이터 로드 완료');
    }, 2000); 
    // =========================================================
    */

    // =========================================================
    // [REAL_API]: 실제 서버 연동 구역  [GET] /api/recommendations 메뉴 추천 결과 받기
    // ---------------------------------------------------------

    setLoading(true);
    try {
      const data = await apiClient.post(apiClient.urls.RECOMMEND,{
        dietary_restriction: userSurvey?.dietary_label || "none",
        spicy_level: String(userSurvey?.spicy_threshold || "3"),
        budget_range: String(userSurvey?.lunch_budget_max || "12000"),
        salty_level: String(userSurvey?.saltiness_preference || "3"),
        exploration_style: userSurvey?.is_adventurous ? "adventurous" : "stable",
        city: "Seoul"
      });

      console.log('--------------------------');
      console.log('[DEBUG] 백엔드 응답 데이터:', JSON.stringify(data, null, 2));
      console.log('--------------------------');

      if (data) {
        setRecommendations(data);
      }
    } catch (error) {
      console.error('추천 조회 실패:', error);
      Alert.alert("연동 에러", "추천 결과를 가져오지 못했습니다.");
    } finally {
      setLoading(false);
    }
    // ========================================================= 

  };

  /**
   * [POST] 유저 피드백 전송 핸들러
   */
  const handleFeedback = async (item, type) => {
    // =========================================================
    // [REAL_API]: [POST] /api/feedback 실제 서버 연동 구역 /api/feedback 유저 피드백 전송
    // ---------------------------------------------------------
    try {
      await apiClient.post(apiClient.urls.FEEDBACK,{
        menu_name: item.menu_name,
        feedback_type: type,
        category: item.category || "일반",
        score: item.match_rate || 0
      });

      Alert.alert("알림", "피드백이 저장되었습니다.");
    } catch (error) {
      console.error('피드백 전송 실패:', error);
      Alert.alert("오류", "피드백 전송 중 문제가 발생했습니다.");
    }
  };

  const renderItem = ({ item, index }) => {
    return (
      <View style={[styles.cardWrapper, { width: CARD_WIDTH, marginHorizontal: CARD_MARGIN }]}>
        <View style={styles.mainCard}>
          {/* [MOD]: 이미지 영역 제거 후 상단 매칭률 헤더로 변경 */}
          <View style={styles.matchHeader}>
            <View style={styles.rankBadge}>
              <Text style={styles.rankText}>{index + 1}위</Text>
            </View>
            <View style={styles.matchBadge}>
              <Text style={styles.matchLabel}>매칭률</Text>
              <Text style={styles.matchValue}>{item.match_rate}%</Text>
            </View>
          </View>

          <View style={styles.infoArea}>
            <View style={styles.titleRow}>
              <Text style={styles.storeName} numberOfLines={1}>{item.menu_name}</Text>
            </View>
            <Text style={styles.categoryText}>#{item.category}  #평균 {item.price}원</Text>
            <Text style={styles.addressText} numberOfLines={3}>
              {item.description}
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

            <TouchableOpacity 
              style={styles.actionBtn}
              onPress={() => {
                Alert.alert(
                  "식당 찾기", 
                  `주변에 '${item.menu_name}' 맛집을 보러 갈까요?`,
                  [
                    { text: "취소", style: "cancel" },
                    { text: "이동", onPress: () => navigation.navigate('Map', { searchQuery: item.menu_name }) }
                  ]
                );
              }}
            >
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
      {/* [MOD]: 로딩 상태일 때 미니게임 컴포넌트 렌더링 */}
      {loading && <GameLoadingScreen />}

      <View style={styles.header}>
        <Text style={styles.headerTitle}>{nickname || '메추리'} 추천</Text>
        <Text style={styles.headerSub}>AI가 분석한 최적의 메뉴입니다.</Text>
      </View>

      <View style={styles.listContainer}>
        {!loading && (
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

      <TouchableOpacity style={styles.retryBtn} onPress={() => navigation.navigate('Home',{
        access_token: userToken, 
        nickname: userSurvey?.nickname || nickname
      })}>
        <Text style={styles.retryText}>홈으로</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
};

export default ResultScreen;