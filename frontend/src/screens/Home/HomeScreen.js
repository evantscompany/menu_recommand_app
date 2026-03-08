import React, { useState, useEffect } from 'react';
import { 
  View, Text, TouchableOpacity, 
  ScrollView, SafeAreaView, Alert 
} from 'react-native';
import * as Location from 'expo-location';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import apiClient from '../../Api/apiClient'
import CommonLoading from '../../components/CommonLoadingScreen';
import FooterBar from '../../components/FooterBar';
import { styles } from './HomeStyle';

const HomeScreen = ({ route, navigation }) => {
  // MOCK_MODE: true // REAL: false
  const MOCK_MODE = true;

  const [loading, setLoading] = useState(false);
  const [nearbyRestaurants, setNearbyRestaurants] = useState([]);
  
  const [userNickname, setUserNickname] = useState("");
  const { access_token, nickname } = route.params || {};

  useEffect(() => {
    loadHomeData();
    initNickname();
  }, []);

  const initNickname = async () => {
      if (nickname) {
        setUserNickname(nickname);
        await AsyncStorage.setItem('userNickname', nickname);
      } else {
        const storedNickname = await AsyncStorage.getItem('userNickname');
        setUserNickname(storedNickname || "유저"); 
      }
  };

  const loadHomeData = async () => {
      setLoading(true);
      try {
        // 위치 권한 요청 및 현재 좌표 획득
        let { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
          Alert.alert("알림", "위치 권한을 허용해야 주변 식당을 볼 수 있습니다.");
          setLoading(false);
          return;
        }
        let location = await Location.getCurrentPositionAsync({});
        const { latitude, longitude } = location.coords;

        if (access_token) {
          apiClient.defaults.headers.Authorization = `Bearer ${access_token}`;
        }

        // =========================================================
        // [MOCK_MODE]: 주변 식당 데이터 - 서버 연동 전 테스트용
        // ---------------------------------------------------------
        if (MOCK_MODE) {
          setNearbyRestaurants([
            { id: 1, name: "할머니 칼국수(가짜 식당)", distance: "350", walking_time: "5분", category: "한식" },
            { id: 2, name: "면사랑 국수집(가짜 식당)", distance: "700", walking_time: "10분", category: "중식" },
            { id: 3, name: "돈까스 하우스(가짜 식당)", distance: "450", walking_time: "7분", category: "일식" },
            { id: 4, name: "역삼 김치찜(가짜 식당)", distance: "200", walking_time: "3분", category: "한식" },
            { id: 5, name: "파스타 팩토리(가짜 식당)", distance: "800", walking_time: "12분", category: "양식" },
          ]);
        }
        // =========================================================


        // =========================================================
        // [REAL_API]: 주변 식당 데이터 - 실제 백엔드 서버 연동
        // ---------------------------------------------------------
        if (!MOCK_MODE) {
          const response = await apiClient.get(apiClient.urls.NEARBY_RESTAURANTS, {
            params: { lat: latitude, lon: longitude }
          });

          console.log("서버 응답 데이터 확인:", response);
          
          if (response) {
            // 서버 응답(배열)을 상태값에 직접 저장
            setNearbyRestaurants(response);
          }
        }
        // =========================================================
        

      } catch (error) {
        console.error("[NEARBY API Error]:", error.response?.data || error);
        
        // 에러 상황별 분기 처리
        if (error.response?.status === 401) {
          // 토큰이 만료된 경우이는 로그인으로 이동
          Alert.alert("세션 만료", "인증 정보가 만료되었습니다. 다시 로그인해주세요.");
          navigation.navigate('Login');
        } else {
          // 서버 점검이나 단순 네트워크 오류일 때는 현 위치 유지
          Alert.alert(
            "통신 실패", 
            "주변 식당 정보를 가져오지 못했습니다. 네트워크 상태를 확인해주세요."
          );
        }
      } finally {
        setLoading(false);
      }
  };

  return (
    <SafeAreaView style={styles.container}>
      {loading && <CommonLoading message="🐣주변 식당 정보를 불러오는 중입니다..." />}

      {/* [1] 고정 헤더 */}
      <View style={styles.headerBar}>
        <Text style={styles.headerLogo}>Mechuri</Text>
        
        {/*  환경설정 버튼 비활성화 시각 처리 (opacity 추가) */}
        <TouchableOpacity 
          style={{ opacity: 0.5 }}
          onPress={() => Alert.alert("알림", "서비스 준비 중입니다.")}
        >
          {/* 아이콘 색상을 조금 더 연한 회색(#CBD5E1)으로 변경 */}
          <MaterialCommunityIcons name="cog" size={24} color="#CBD5E1" />
        </TouchableOpacity>
      </View>

      <View style={styles.fixedContent}>
        {/* [2] 메인 배너 - 결과 화면으로 이동 */}
        <View style={styles.headerSection}>
          <Text style={styles.welcomeText}>{userNickname}님, 반가워요! 🐣</Text>
          <TouchableOpacity 
            style={styles.mainBanner}
            onPress={() => navigation.navigate('Result', { access_token })}
          >
            <View>
              <Text style={styles.bannerTitle}>오늘 뭐 먹지?</Text>
              <Text style={styles.bannerSub}>개인 취향을 분석한 정밀 추천</Text>
            </View>
            <MaterialCommunityIcons name="chevron-right" size={32} color="#FFF" />
          </TouchableOpacity>
        </View>

        {/* [3] 리스트 타이틀 (고정) */}
        <View style={[styles.section, { paddingBottom: 10 }]}>
          <View style={styles.titleRow}>
            <Text style={styles.sectionTitle}>지금 내 주변 식당 📍</Text>
            <TouchableOpacity onPress={() => navigation.navigate('Map')}>
              <Text style={styles.moreText}>자세히</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      {/* [4] 스크롤 영역: 식당 리스트 */}
      <ScrollView 
        showsVerticalScrollIndicator={false}
        style={styles.restaurantListScroll}
        contentContainerStyle={{ paddingHorizontal: 20, paddingBottom: 100 }}
        alwaysBounceVertical={false} 
        bounces={false} 
        overScrollMode="never" 
      >
        {nearbyRestaurants.map((res) => (
          <TouchableOpacity 
            key={res.id} 
            style={styles.resCard}
            onPress={() => navigation.navigate('Map', { restaurantName: res.name })}
          >
            <View style={styles.resInfo}>
              <Text style={styles.resName}>{res.name}</Text>
              <Text style={styles.resDetail}>{res.category_1} · {res.distance}m</Text>
            </View>
            <View style={styles.timeTag}>
              <MaterialCommunityIcons name="walk" size={14} color="#4F46E5" style={{ marginRight: 2 }} />
              <Text style={styles.timeValue}>{res.walking_time}</Text>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <FooterBar activeTab="Home" nickname={userNickname} access_token={access_token} />
    </SafeAreaView>
  );
};

export default HomeScreen;