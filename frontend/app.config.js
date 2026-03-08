import 'dotenv/config';

export default {
  expo: {
    name: "Mechuri",
    slug: "mechuri",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "light",
    platforms: ['ios', 'android'],
    splash: {
      image: "./assets/splash.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    ios: {
      supportsTablet: true,
      bundleIdentifier: "com.anonymous.frontend",
      config: {
        googleMapsApiKey: process.env.EXPO_PUBLIC_GOOGLE_MAPS_API_KEY
      },
      infoPlist: {
        "KAKAO_APP_KEY": process.env.EXPO_PUBLIC_KAKAO_APP_KEY,
        "LSApplicationQueriesSchemes": ["kakaokompassauth", "kakaolink", "kakaotalk"],
        "NSLocationWhenInUseUsageDescription": "사용자 주변의 맛집 정보를 지도에 표시하기 위해 현재 위치 권한이 필요합니다."
      }
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/adaptive-icon.png",
        backgroundColor: "#ffffff"
      },
      package: "com.anonymous.frontend",
      config: {
        googleMaps: {
          apiKey: process.env.EXPO_PUBLIC_GOOGLE_MAPS_API_KEY
        }
      },
      permissions: ["ACCESS_COARSE_LOCATION", "ACCESS_FINE_LOCATION", "FOREGROUND_SERVICE"],
      metaData: {
        "com.kakao.sdk.AppKey": process.env.EXPO_PUBLIC_KAKAO_APP_KEY
      }
    },
    web: {
      favicon: "./assets/favicon.png"
    },
    extra: {
          eas: {
            projectId: "82477313-cc5c-4762-8951-50936b644dec"
          }
    },
    updates: {
      url: "https://u.expo.dev/82477313-cc5c-4762-8951-50936b644dec"
    },
    runtimeVersion: "1.0.0"
  }
};