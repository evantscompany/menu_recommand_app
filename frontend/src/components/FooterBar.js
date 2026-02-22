import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Platform, Alert } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const FooterBar = ({ activeTab, nickname, access_token }) => {
  const navigation = useNavigation();

  return (
    <View style={styles.footerBar}>
      <TouchableOpacity 
        style={styles.footerTab} 
        onPress={() => navigation.navigate('Home')}
      >
        <MaterialCommunityIcons name="home" size={26} color={activeTab === 'Home' ? "#6366F1" : "#94A3B8"} />
        <Text style={[styles.footerTabText, activeTab === 'Home' && styles.activeTabText]}>홈</Text>
      </TouchableOpacity>

      <TouchableOpacity 
        style={styles.footerTab} 
        onPress={() => navigation.navigate('Map')}
      >
        <MaterialCommunityIcons 
          name="map-marker-radius" 
          size={26} 
          color={activeTab === 'Map' ? "#6366F1" : "#94A3B8"} // 탭 활성화 상태 체크
        />
        <Text style={[styles.footerTabText, activeTab === 'Map' && styles.activeTabText]}>주변 식당</Text>
      </TouchableOpacity>

      <TouchableOpacity 
        style={styles.footerTab} 
        onPress={() => navigation.navigate('MyPage', { nickname, access_token })}
      >
        <MaterialCommunityIcons name="account" size={26} color={activeTab === 'MyPage' ? "#6366F1" : "#94A3B8"} />
        <Text style={[styles.footerTabText, activeTab === 'MyPage' && styles.activeTabText]}>마이</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  footerBar: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    height: Platform.OS === 'ios' ? 90 : 70,
    flexDirection: 'row',
    backgroundColor: '#FFF',
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
    paddingBottom: Platform.OS === 'ios' ? 25 : 0,
    elevation: 10,
    zIndex: 100,
  },
  footerTab: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  footerTabText: { fontSize: 12, marginTop: 4, color: '#94A3B8' },
  activeTabText: { color: '#6366F1', fontWeight: '700' },
});

export default FooterBar;