import React, { useState, useEffect, useRef } from 'react';
import { 
  View, Text, TouchableOpacity, SafeAreaView, 
  ActivityIndicator, StatusBar , Animated,
  Alert
} from 'react-native';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps'; 
import * as Location from 'expo-location';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import FooterBar from '../../components/FooterBar';
import { styles, cleanMapStyle } from './MapStyle';
import apiClient from '../../Api/apiClient';

const MapScreen = ({ navigation, route }) => {
  // MOCK 모드 스위치 (true: MOCK / false: 실제 서버 연동)
  const MOCK_MODE = true; 

  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(true);

  // 식당 데이터 및 지도 카메라 위치 상태 추가
  const [restaurants, setRestaurants] = useState([]);
  const [mapRegion, setMapRegion] = useState(null);

  // 선택된 식당 및 애니메이션 상태 관리
  const [selectedRes, setSelectedRes] = useState(null);
  const slideAnim = useRef(new Animated.Value(300)).current; // 초기 위치: 바닥 아래

  // 홈 화면에서 클릭해서 넘어온 식당 이름 받기
  const { access_token, nickname, restaurantName } = route.params || {};

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setLoading(false);
        return;
      }
      let userLocation = await Location.getCurrentPositionAsync({});
      const currentCoords = userLocation.coords;
      setLocation(currentCoords);
      
      // 내 위치 확인 후 식당 데이터 로드
      loadRestaurantData(currentCoords);
    })();
  }, []);

  // 바텀 시트 제어 함수
  const showSheet = (res) => {
    setSelectedRes(res);
    Animated.spring(slideAnim, {
      toValue: 0,
      useNativeDriver: true,
      bounciness: 5,
    }).start();
  };

  const hideSheet = () => {
    Animated.timing(slideAnim, {
      toValue: 300,
      duration: 200,
      useNativeDriver: true,
    }).start(() => setSelectedRes(null));
  };


  const loadRestaurantData = async (coords) => {
    // =========================================================
    // [MOCK_MODE]: 주변 식당 데이터 - 서버 연동 전 테스트용
    // ---------------------------------------------------------
    if (MOCK_MODE) {
      // 내 현재 위치를 기준으로 가짜 식당 배치
      const mockData = [
        { id: 1, name: "할머니 칼국수(가짜 식당)", latitude: coords.latitude + 0.0015, longitude: coords.longitude + 0.0015, category: "한식" },
        { id: 2, name: "면사랑 국수집(가짜 식당)", latitude: coords.latitude - 0.0020, longitude: coords.longitude + 0.0010, category: "중식" },
        { id: 3, name: "돈까스 하우스(가짜 식당)", latitude: coords.latitude + 0.0010, longitude: coords.longitude - 0.0020, category: "일식" },
        { id: 4, name: "역삼 김치찜(가짜 식당)", latitude: coords.latitude - 0.0015, longitude: coords.longitude - 0.0015, category: "한식" },
        { id: 5, name: "파스타 팩토리(가짜 식당)", latitude: coords.latitude + 0.0025, longitude: coords.longitude + 0.0005, category: "양식" },
      ];
      setRestaurants(mockData);

      // 홈에서 특정 식당을 클릭하고 왔다면 그 식당 위치로 카메라 포커싱, 아니면 내 위치 포커싱 --for MOCK
      const target = restaurantName ? mockData.find(r => r.name === restaurantName) : null;
      setMapRegion({
        latitude: target ? target.latitude : coords.latitude,
        longitude: target ? target.longitude : coords.longitude,
        latitudeDelta: 0.005,
        longitudeDelta: 0.005,
      });
      setLoading(false);
    }
    // =========================================================

    // =========================================================
    // [REAL_API]: 주변 식당 데이터 - 실제 백엔드 서버 연동
    // ---------------------------------------------------------
    if (!MOCK_MODE) {
      try {
        // config.js에 등록한 url을 가져다 씁니다 (apiClient.urls 사용)
        const realData = await apiClient.get(apiClient.urls.NEARBY_RESTAURANTS, {
          params: {
            lat: coords.latitude,
            lng: coords.longitude
          }
        });

        // apiClient에서 response.data를 이미 리턴했으므로 바로 사용
        setRestaurants(realData)

        // 홈에서 특정 식당을 클릭하고 왔다면 그 식당 위치로 카메라 포커싱, 아니면 내 위치 포커싱 -- for REAL
        const target = restaurantName ? realData.find(r => r.name === restaurantName) : null;
        setMapRegion({
          latitude: target ? target.latitude : coords.latitude,
          longitude: target ? target.longitude : coords.longitude,
          latitudeDelta: 0.005,
          longitudeDelta: 0.005,
        });
      } catch (error) {
        console.error("식당 데이터 수신 실패:", error);
      } finally {
        setLoading(false);
      }
    }
    // =========================================================
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#6366F1" />
        <Text style={styles.loadingText}>위치 정보를 수신하고 있습니다</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      
      {/* 1. 헤더 영역 */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <MaterialCommunityIcons name="chevron-left" size={28} color="#0F172A" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>주변 식당</Text>
        <View style={{ width: 40 }} /> 
      </View>

      {/* 2. 지도 및 마커 영역 */}
      <View style={styles.mapContainer}>
        <MapView
          provider={PROVIDER_GOOGLE}
          style={styles.map}
          customMapStyle={cleanMapStyle}
          region={mapRegion} // initialRegion 대신 region을 사용하여 동적 이동 처리
          showsUserLocation={false} 
        >
          {/* 내 위치 마커 (파란색) */}
          {location && (
            <Marker coordinate={{ latitude: location.latitude, longitude: location.longitude }} zIndex={10}>
              <View style={styles.customMarker}>
                <View style={styles.markerHalo} />
                <View style={styles.markerDot} />
              </View>
            </Marker>
          )}

          {/* 식당 위치 마커들 (빨간색) */}
          {restaurants.map((res) => (
            <Marker 
              key={res.id} 
              coordinate={{ latitude: res.latitude, longitude: res.longitude }}
              zIndex={5}
              // 핀 포인트 설정. 핀의 뾰족한 끝(맨 아래 중앙)을 좌표에 맞춤.
              anchor={{ x: 0.5, y: 1.0 }} 

              onPress={() => showSheet(res)}
            >
              {/* 새로운 핀 마커 구조 적용 */}
              <View style={styles.pinContainer}>
                {/* 상단 원형 아이콘 */}
                <View style={styles.pinCircle}>
                  <MaterialCommunityIcons name="silverware-fork-knife" size={16} color="#FFFFFF" />
                </View>
                {/* 하단 뾰족한 팁 */}
                <View style={styles.pinTip} />
              </View>
            </Marker>
          ))}
        </MapView>

        {/* 선택 식당 바텀 시트 레이아웃 */}
        {selectedRes && (
          <Animated.View 
            style={[
              styles.bottomSheet,
              { transform: [{ translateY: slideAnim }] }
            ]}
          >
            <View style={styles.sheetHandle} />
            
            <View style={styles.sheetHeader}>
              <View style={{ flex: 1 }}>
                <Text style={styles.sheetName}>{selectedRes.name}</Text>
                <View style={styles.tagRow}>
                  <View style={styles.categoryTag}>
                    <Text style={styles.tagText}>{selectedRes.category}</Text>
                  </View>
                  {/* 데이터가 부족하므로 '추천 메뉴' 등 가짜 태그로 UI 보강 가능 */}
                  <View style={styles.categoryTag}>
                    <Text style={styles.tagText}>인기맛집</Text>
                  </View>
                </View>
              </View>
              
              <TouchableOpacity style={styles.closeButton} onPress={hideSheet}>
                <MaterialCommunityIcons name="close" size={20} color="#94A3B8" />
              </TouchableOpacity>
            </View>

            <View style={styles.sheetActionRow}>
              <TouchableOpacity 
                style={styles.kakaoButton}
                onPress={() => Alert.alert("서비스 준비중", "카카오 연동 후 카카오맵으로 연결됩니다.")}
              >
                <MaterialCommunityIcons name="map-marker-path" size={18} color="#3C1E1E" />
                <Text style={styles.kakaoButtonText}>카카오 길찾기</Text>
                <MaterialCommunityIcons name="open-in-new" size={14} color="#3C1E1E" style={{ marginLeft: 4 }} />
              </TouchableOpacity>
            </View>
          </Animated.View>
        )}

        {/* ============================================================ */}
        {/* [ 서비스 준비 중 오버레이 ] - 푸시할 때만 주석 해제 */}
        {/* ============================================================ */}
        {/* <View style={styles.overlay}>
          <View style={styles.overlayContent}>
            <MaterialCommunityIcons name="alert-decagram" size={40} color="#6366F1" />
            <Text style={styles.overlayTitle}>서비스 준비 중</Text>
            <Text style={styles.overlayText}>
              보다 정확한 맛집 지도를 위해{"\n"}데이터를 정밀 분석 중입니다.
            </Text>
          </View>
        </View> */}
        {/* ============================================================ */}
        
      </View>

      <FooterBar activeTab="Map" nickname={nickname} access_token={access_token} />
    </SafeAreaView>
  );
};

export default MapScreen;