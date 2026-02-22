import React, { useState } from 'react';
import { View, Text, SafeAreaView, TouchableOpacity, ScrollView, Alert, Image } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import CommonLoading from '../../components/CommonLoadingScreen'; 
import FooterBar from '../../components/FooterBar';
import { styles } from './MyPageStyle';
import { useImagePicker } from '../../hooks/useImagePicker';

const MyPageScreen = ({ route, navigation }) => {
  const { nickname = "닉네임", access_token } = route.params || {};
  const [loading, setLoading] = useState(false);
  const [showDetail, setShowDetail] = useState(false);
  const { image, pickImage } = useImagePicker();

  const analysisLevel = 4;
  const matchRate = 85;

  const handleProfilePress = () => {
    Alert.alert(
      "프로필 설정",
      `${nickname}님, 어떤 작업을 하시겠습니까?`,
      [
        { text: "프로필 사진 변경", onPress: async () => await pickImage() },
        { 
          text: "로그아웃", 
          onPress: () => navigation.navigate('Login'),
          style: "destructive" 
        },
        { text: "취소", style: "cancel" }
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      {loading && <CommonLoading message="프로필 정보를 불러오는 중입니다..." />}

      {/* 하단 패딩 - 메뉴가 가려지지 않게 */}
      <ScrollView 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        {/* 상단 프로필 구역 */}
        <View style={styles.profileSection}>
          <TouchableOpacity 
            onPress={handleProfilePress} 
            activeOpacity={0.7} 
            style={{ alignItems: 'center', width: '100%' }}
          >
            <View style={styles.avatarWrapper}>
              <View style={styles.avatarCircle}>
                {image ? (
                  <Image source={{ uri: image }} style={{ width: 100, height: 100, borderRadius: 50 }} />
                ) : (
                  <MaterialCommunityIcons name="account" size={60} color="#6366F1" />
                )}
              </View>
              <View style={styles.cameraBadge}>
                <MaterialCommunityIcons name="camera" size={16} color="#FFF" />
              </View>
            </View>
            
            <Text style={styles.nickname}>
              {nickname}님 <MaterialCommunityIcons name="pencil-outline" size={16} color="#94A3B8" />
            </Text>
            <Text style={styles.userEmail}>commander@mechuri.com</Text>
          </TouchableOpacity>

          {/* 활동 통계 섹션 */}
          <View style={styles.statsContainer}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>12</Text>
              <Text style={styles.statLabel}>찜한 식당</Text>
            </View>
            
            <TouchableOpacity 
              style={[styles.statItem, showDetail && styles.activeStatItem]} 
              onPress={() => setShowDetail(!showDetail)}
            >
              <Text style={styles.statValue}>Lv. {analysisLevel}</Text>
              <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                <Text style={styles.statLabel}>메추리 레벨 </Text>
                <MaterialCommunityIcons 
                  name={showDetail ? "chevron-up" : "information-outline"} 
                  size={12} 
                  color={showDetail ? "#6366F1" : "#94A3B8"} 
                />
              </View>
            </TouchableOpacity>
          </View>

          {/* 게이지 바 상세 박스 */}
          {showDetail && (
            <View style={styles.detailBox}>
              <View style={styles.detailHeader}>
                <Text style={styles.detailTitle}>취향 반영률 정밀도</Text>
                <Text style={styles.detailPercent}>{matchRate}%</Text>
              </View>
              <View style={styles.gaugeBackground}>
                <View style={[styles.gaugeFill, { width: `${matchRate}%` }]} />
              </View>
              <Text style={styles.detailDesc}>설문에 더 참여할수록 정밀도가 상승합니다!</Text>
            </View>
          )}
        </View>

        {/* 메뉴 리스트 섹션 */}
        <View style={styles.menuSection}>
          <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert("알림", "서비스 준비 중")}>
            <MaterialCommunityIcons name="heart" size={24} color="#F87171" />
            <Text style={styles.menuText}>찜한 식당 목록</Text>
            <MaterialCommunityIcons name="chevron-right" size={24} color="#CBD5E1" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert("알림", "서비스 준비 중")}>
            <MaterialCommunityIcons name="tune" size={24} color="#6366F1" />
            <Text style={styles.menuText}>내 취향 분석 수정</Text>
            <MaterialCommunityIcons name="chevron-right" size={24} color="#CBD5E1" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert("알림", "서비스 준비 중")}>
            <MaterialCommunityIcons name="bell" size={24} color="#F59E0B" />
            <Text style={styles.menuText}>공지사항</Text>
            <MaterialCommunityIcons name="chevron-right" size={24} color="#CBD5E1" />
          </TouchableOpacity>
        </View>
      </ScrollView>

      {/* 하단 고정 푸터 */}
      <FooterBar activeTab="MyPage" />
    </SafeAreaView>
  );
};

export default MyPageScreen;