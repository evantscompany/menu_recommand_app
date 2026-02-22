import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, SafeAreaView, ActivityIndicator, StatusBar } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import * as Location from 'expo-location';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import FooterBar from '../../components/FooterBar';
import { styles, cleanMapStyle } from './MapStyle';

const MapScreen = ({ navigation, route }) => {
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(true);

  const { access_token, nickname } = route.params || {};

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setLoading(false);
        return;
      }
      let userLocation = await Location.getCurrentPositionAsync({});
      setLocation(userLocation.coords);
      setLoading(false);
    })();
  }, []);

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
      
      {/* 개선된 커스텀 헤더 */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <MaterialCommunityIcons name="chevron-left" size={28} color="#0F172A" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>주변 식당 탐색</Text>
        <View style={{ width: 40 }} /> 
      </View>

      {/* 단순화된 지도 영역 */}
      <View style={styles.mapContainer}>
        <MapView
          style={styles.map}
          customMapStyle={cleanMapStyle}
          initialRegion={{
            latitude: location ? location.latitude : 37.4979,
            longitude: location ? location.longitude : 127.0276,
            latitudeDelta: 0.005,
            longitudeDelta: 0.005,
          }}
          showsUserLocation={false} // 커스텀 마커
        >
          {location && (
            <Marker coordinate={{ latitude: location.latitude, longitude: location.longitude }}>
              {/* 커스텀 마커 */}
              <View style={styles.customMarker}>
                <View style={styles.markerHalo} />
                <View style={styles.markerDot} />
              </View>
            </Marker>
          )}
        </MapView>
      </View>

      <FooterBar activeTab="Map" nickname={nickname} access_token={access_token} />
    </SafeAreaView>
  );
};

export default MapScreen;