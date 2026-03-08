import React, { useState, useEffect } from 'react';
import { View, Text, SafeAreaView, TouchableOpacity, ScrollView, Image, Modal, TouchableWithoutFeedback, Alert } from 'react-native'; // [MOD]: Alert 추가
import { MaterialCommunityIcons } from '@expo/vector-icons';
import * as Location from 'expo-location'; 
import AsyncStorage from '@react-native-async-storage/async-storage'; 
import CommonLoading from '../../components/CommonLoadingScreen'; 
import FooterBar from '../../components/FooterBar';
import { styles } from './MyPageStyle';
import { useImagePicker } from '../../hooks/useImagePicker';

const MyPageScreen = ({ route, navigation }) => {
  const { nickname: pNickname, access_token } = route.params || {};
  
  const [nickname, setNickname] = useState(pNickname || "유저");
  const [loading, setLoading] = useState(false);
  const [currentAddress, setCurrentAddress] = useState("위치 확인 중..."); 
  const [noticeVisible, setNoticeVisible] = useState(false); 
  const { image, pickImage, setImage } = useImagePicker();

  useEffect(() => {
    initUserData(); 
    fetchCurrentLocation(); 
  }, []);

  const initUserData = async () => {
    try {
      let finalNickname = pNickname;
      if (!finalNickname) {
        finalNickname = await AsyncStorage.getItem('userNickname') || "유저";
      } else {
        await AsyncStorage.setItem('userNickname', finalNickname);
      }
      setNickname(finalNickname);
      const savedImage = await AsyncStorage.getItem(`profileImage_${finalNickname}`);
      if (savedImage) setImage(savedImage);
    } catch (e) {
      console.error("데이터 로드 실패:", e);
    }
  };

  const fetchCurrentLocation = async () => {
    try {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setCurrentAddress("위치 권한 미허용");
        return;
      }
      let location = await Location.getCurrentPositionAsync({});
      let reverseGeocode = await Location.reverseGeocodeAsync({
        latitude: location.coords.latitude,
        longitude: location.coords.longitude,
      });
      if (reverseGeocode.length > 0) {
        const { city, district } = reverseGeocode[0];
        setCurrentAddress(`${city || ''} ${district || ''}`);
      }
    } catch (error) {
      setCurrentAddress("지역 정보 확인 불가");
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 100 }}>
        {/* 프로필 및 주소 카드 구역 */}
        <View style={styles.profileSection}>
          <TouchableOpacity 
            onPress={() => {
              Alert.alert(
                "프로필 설정",
                `${nickname}님, 어떤 작업을 하시겠습니까?`,
                [
                  { text: "프로필 사진 변경", onPress: async () => await pickImage() },
                  { text: "로그아웃", onPress: () => navigation.navigate('Login'), style: "destructive" },
                  { text: "취소", style: "cancel" }
                ]
              );
            }} 
            activeOpacity={0.7} 
            style={{ alignItems: 'center', width: '100%' }}
          >
            <View style={styles.avatarWrapper}>
              <View style={styles.avatarCircle}>
                {image ? <Image source={{ uri: image }} style={{ width: 100, height: 100, borderRadius: 50 }} /> 
                       : <MaterialCommunityIcons name="account" size={60} color="#6366F1" />}
              </View>
              <View style={styles.cameraBadge}><MaterialCommunityIcons name="camera" size={16} color="#FFF" /></View>
            </View>
            <Text style={[styles.nickname, { marginTop: 5 }]}>{nickname}님</Text>
          </TouchableOpacity>

          <View style={styles.locationCard}>
            <View style={styles.locationHeader}>
              <MaterialCommunityIcons name="map-marker-radius" size={20} color="#6366F1" />
              <Text style={styles.locationLabel}>현재 활동 구역</Text>
            </View>
            <Text style={styles.locationText}>{currentAddress}</Text>
            <Text style={styles.locationSub}>위 위치를 기반으로 주변 식당을 추천합니다.</Text>
          </View>
        </View>

        {/* 메뉴 리스트 - 알림 기능 복구 완료 */}
        <View style={styles.menuSection}>
          {/* [MOD]: 미구현 항목 시각적 처리 (회색조 및 투명도 적용) */}
          <TouchableOpacity 
            style={[styles.menuItem, styles.disabledMenuItem]} 
            onPress={() => Alert.alert("알림", "서비스 준비 중입니다.")}
          >
            <MaterialCommunityIcons name="heart" size={24} color="#CBD5E1" />
            <Text style={[styles.menuText, styles.disabledMenuText]}>내가 좋아하는 식당(준비중)</Text>
            <MaterialCommunityIcons name="chevron-right" size={24} color="#E2E8F0" />
          </TouchableOpacity>

          <TouchableOpacity 
            style={[styles.menuItem, styles.disabledMenuItem]} 
            onPress={() => Alert.alert("알림", "서비스 준비 중입니다.")}
          >
            <MaterialCommunityIcons name="tune" size={24} color="#CBD5E1" />
            <Text style={[styles.menuText, styles.disabledMenuText]}>입맛 취향 다시 설정(준비중)</Text>
            <MaterialCommunityIcons name="chevron-right" size={24} color="#E2E8F0" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.menuItem} onPress={() => setNoticeVisible(true)}>
            <MaterialCommunityIcons name="bell-outline" size={24} color="#F59E0B" />
            <Text style={styles.menuText}>공지사항</Text>
            <MaterialCommunityIcons name="chevron-right" size={24} color="#CBD5E1" />
          </TouchableOpacity>
        </View>
      </ScrollView>

      {/* 게시판 스타일 커스텀 공지사항 모달 */}
      <Modal
        animationType="fade"
        transparent={true}
        visible={noticeVisible}
        onRequestClose={() => setNoticeVisible(false)}
      >
        <TouchableWithoutFeedback onPress={() => setNoticeVisible(false)}>
          <View style={styles.modalOverlay}>
            <TouchableWithoutFeedback>
              <View style={styles.noticeModal}>
                <View style={styles.noticeTopBar} />
                <View style={styles.noticeHeader}>
                  <Text style={styles.noticeTitle}>공지사항</Text>
                  <TouchableOpacity onPress={() => setNoticeVisible(false)} style={styles.closeButton}>
                    <MaterialCommunityIcons name="close" size={22} color="#94A3B8" />
                  </TouchableOpacity>
                </View>
                <View style={styles.noticeContent}>
                  <Text style={styles.noticeBody}>
                    <Text style={{fontSize: 18, fontWeight: '800', color: '#6366F1'}}>Mechuri Project v0.1 (MVP)</Text>{"\n\n"}
                    현재 메추리는 핵심 기능 검증을 위한{"\n"}
                    <Text style={{fontWeight: '700'}}>최소 기능 제품(MVP)</Text> 단계입니다.{"\n\n"}
                    <Text style={{fontWeight: '700', color: '#1E293B'}}>[ 업데이트 예고 ]</Text>{"\n"}
                    • 실제 주변 식당 데이터 실시간 연동{"\n"}
                    • 초개인화 메뉴 추천 알고리즘 고도화{"\n\n"}
                    <Text style={{fontWeight: '700', color: '#1E293B'}}>[ 시스템 안내 ]</Text>{"\n"}
                    • 데이터 엔진 고도화 및 최적화 작업 중으로{"\n"}
                    일부 환경에서 응답이 지연될 수 있습니다.{"\n\n"}
                    더욱 쾌적하고 맛있는 서비스를 위해{"\n"}
                    끊임없이 개선해 나가겠습니다.
                  </Text>
                </View>
                <TouchableOpacity style={styles.noticeFooter} onPress={() => setNoticeVisible(false)}>
                  <Text style={styles.footerCloseText}>확인</Text>
                </TouchableOpacity>
              </View>
            </TouchableWithoutFeedback>
          </View>
        </TouchableWithoutFeedback>
      </Modal>

      <FooterBar activeTab="MyPage" nickname={nickname} access_token={access_token} />
    </SafeAreaView>
  );
};

export default MyPageScreen;