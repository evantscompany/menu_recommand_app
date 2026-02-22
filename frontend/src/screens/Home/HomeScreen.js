import React, { useState, useEffect } from 'react';
import { 
  View, Text, TouchableOpacity, ScrollView, SafeAreaView, 
  ActivityIndicator, Alert 
} from 'react-native';
import { MaterialCommunityIcons, FontAwesome5 } from '@expo/vector-icons';
import axios from 'axios';
import { API_ENDPOINTS } from '../../Api/config';
import CommonLoading from '../../components/CommonLoadingScreen';
import FooterBar from '../../components/FooterBar';
import { styles } from './HomeStyle';

const HomeScreen = ({ route, navigation }) => {
  // true: [MOCK_MODE] / false: [REAL_API]
  const MOCK_MODE = true; 

  const [loading, setLoading] = useState(false);
  const [weatherData, setWeatherData] = useState(null);
  const [nearbyRestaurants, setNearbyRestaurants] = useState([]);
  
  // 로그인/회원가입에서 넘어온 유저 세션 정보
  const { access_token, nickname = "닉네임" } = route.params || {};

  useEffect(() => {
    loadHomeData();
  }, []);

const loadHomeData = async () => {
    setLoading(true);

    if (MOCK_MODE) {
      // =========================================================
      // [MOCK_MODE]: 서버 연동 전 UI 및 로직 테스트용 (가짜 데이터)
      // ---------------------------------------------------------
      console.log('[MOCK] 홈 화면 데이터 로딩 중...');
      
      setTimeout(() => {
        setWeatherData({
          display_text: "비도 오는데 뜨끈한 칼국수 어때요?",
          recommended_menu: "칼국수"
        });
        setNearbyRestaurants([
            { id: 1, name: "할머니 칼국수", distance: "350m", walking_time: "5분", category: "한식" },
            { id: 2, name: "면사랑 국수집", distance: "700m", walking_time: "10분", category: "중식" },
            { id: 3, name: "돈까스 하우스", distance: "450m", walking_time: "7분", category: "일식" },
            { id: 4, name: "역삼 김치찜", distance: "200m", walking_time: "3분", category: "한식" },
            { id: 5, name: "파스타 팩토리", distance: "800m", walking_time: "12분", category: "양식" },
            { id: 6, name: "마라탕 명가", distance: "500m", walking_time: "8분", category: "중식" },
            { id: 7, name: "수제버거 킹덤", distance: "1.2km", walking_time: "18분", category: "패스트푸드" },
            { id: 8, name: "샐러드 가든", distance: "300m", walking_time: "4분", category: "샐러드" },
            { id: 9, name: "소고기 국밥집", distance: "600m", walking_time: "9분", category: "한식" },
            { id: 10, name: "초밥 천국", distance: "900m", walking_time: "13분", category: "일식" },
        ]);
                setLoading(false); // 가짜 로딩 종료
      }, 800);
      // =========================================================


    } else {
      // =========================================================
      // [REAL_API]: 실제 백엔드 서버 연동 (나중에 주석 해제하여 사용)
      // ---------------------------------------------------------
      try {
        /* 백엔드 연동 시 아래 주석을 해제하십시오 */
        // const response = await axios.get(API_ENDPOINTS.HOME_DATA, {
        //   headers: { Authorization: `Bearer ${access_token}` }
        // });
        // if (response.status === 200) {
        //   setWeatherData(response.data.weather_recommend);
        //   setNearbyRestaurants(response.data.nearby);
        // }
      } catch (error) {
        console.error("[Home API Error]:", error.response?.data || error);
        Alert.alert("서버 연결 실패 ⚠️", "서버 상태를 확인해주세요.");
      } finally {
        setLoading(false);
      }
      // =========================================================
    }
  };

  return (
    <SafeAreaView style={styles.container}>
    {loading && <CommonLoading message="🐣주변 식당 정보를 불러오는 중입니다..." />}

    {/* [1] 고정 영역: 헤더 바 */}
    <View style={styles.headerBar}>
      <Text style={styles.headerLogo}>Mechuri</Text>
      <TouchableOpacity onPress={() => Alert.alert("설정", "환경설정으로 이동")}>
        <MaterialCommunityIcons name="cog" size={24} color="#475569" />
      </TouchableOpacity>
    </View>

    {/* [2] 고정 영역: 배너 & 날씨 (스크롤 되지 않음) */}
    <View style={styles.fixedContent}>
      {/* 섹션 1: 배너 */}
      <View style={styles.headerSection}>
        <Text style={styles.welcomeText}>{nickname}님, 반가워요! 🐣</Text>
        <TouchableOpacity 
          style={styles.mainBanner}
          onPress={() => navigation.navigate('Result', { access_token })}
        >
          <View>
            <Text style={styles.bannerTitle}>오늘 뭐 먹지?</Text>
            <Text style={styles.bannerSub}>취향과 날씨를 분석한 정밀 추천</Text>
          </View>
          <MaterialCommunityIcons name="chevron-right" size={32} color="#FFF" />
        </TouchableOpacity>
      </View>

      {/* 섹션 2: 날씨 큐레이션 */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>날씨 맞춤 메뉴 ☁️</Text>
        <TouchableOpacity style={styles.weatherCard}>
          <MaterialCommunityIcons name="weather-rainy" size={40} color="#6366F1" />
          <View style={styles.weatherTextContainer}>
            <Text style={styles.weatherText}>{weatherData?.display_text}</Text>
          </View>
        </TouchableOpacity>
      </View>

      {/* 섹션 3: 타이틀 (스크롤 바로 위에 고정) */}
      <View style={[styles.section, { paddingBottom: 10 }]}>
        <View style={styles.titleRow}>
          <Text style={styles.sectionTitle}>지금 내 주변 식당 📍</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Map')}>
            <Text style={styles.moreText}>전체보기</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>

    {/* [3] 스크롤 영역: 식당 리스트만 개별 스크롤 */}
    <ScrollView 
        showsVerticalScrollIndicator={false}
        style={styles.restaurantListScroll}
        contentContainerStyle={{ paddingHorizontal: 20, paddingBottom: 100 }}
        
        alwaysBounceVertical={false} 
        bounces={false} // iOS에서 전체가 끌려 올라오는 현상 방지
        overScrollMode="never" // 안드로이드에서 파란 원 생기며 밀리는 현상 방지
        >

        {nearbyRestaurants.map((res) => (
          <TouchableOpacity 
            key={res.id} 
            style={styles.resCard}
            onPress={() => navigation.navigate('Map', { restaurantName: res.name })}
          >
          <View style={styles.resInfo}>
            <Text style={styles.resName}>{res.name}</Text>
            <Text style={styles.resDetail}>{res.category} · {res.distance}</Text>
          </View>
          <View style={styles.timeTag}>
            <MaterialCommunityIcons name="walk" size={14} color="#4F46E5" style={{ marginRight: 2 }} />
            <Text style={styles.timeValue}>{res.walking_time}</Text>
          </View>
        </TouchableOpacity>
      ))}
    </ScrollView>

      {/* 하단 고정 푸터 (내비게이션 바) */}

      <FooterBar activeTab="Home" nickname={nickname} access_token={access_token} />
      
    </SafeAreaView>
  );
};

export default HomeScreen;