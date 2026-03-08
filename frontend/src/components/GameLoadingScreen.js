import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, SafeAreaView, ActivityIndicator, Animated } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import LottieView from 'lottie-react-native'; 
import { styles } from './GameLoadingStyle'; 

const BALANCE_QUESTIONS = [
  { a: "평생 라면 안 먹기", b: "평생 치킨 안 먹기" },
  { a: "양치질 직후에 귤 먹기", b: "초콜릿 먹고 바로 김치찌개 먹기" },
  { a: "평생 미지근한 콜라만 마시기", b: "평생 눅눅한 감자튀김만 먹기" },
  { a: "민트초코맛 김치찌개 먹기", b: "김치찌개맛 민트초코 먹기" },
  { a: "삼겹살에 쌈장/소금 없이 먹기", b: "회에 초장/간장 없이 먹기" },
  { a: "1년 내내 뜨거운 냉면 먹기", b: "1년 내내 얼음 띄운 국밥 먹기" },
  { a: "고기 없는 제육볶음", b: "떡 없는 떡볶이" },
  { a: "평생 탄산음료 끊기", b: "평생 커피 끊기" },
  { a: "탕수육 평생 소스 없이 먹기", b: "탕수육 평생 남의 소스에 찍어 먹기" },
  { a: "불어터진 면 평생 먹기", b: "덜 익은 생쌀 밥 평생 먹기" },
  { a: "짜장면에 마요네즈 듬뿍 비비기", b: "짬뽕에 슬라이스 치즈 5장 넣기" },
  { a: "평생 단맛 못 느끼기", b: "평생 매운맛 못 느끼기" },
  { a: "평생 숟가락으로만 면 먹기", b: "평생 젓가락으로만 국물 먹기" },
  { a: "국물 아예 없는 라면", b: "면 아예 없는 라면 국물" },
  { a: "소고기 사주는 얄미운 상사", b: "컵라면 사주는 찐친" },
  { a: "밥 먹을 때 물 절대 못 마시기", b: "국물 요리 절대 못 먹기" },
  { a: "눈 감고 아무거나 랜덤으로 먹기", b: "코 막고 제일 좋아하는 음식 먹기" },
  { a: "피자 도우만 5판 먹기", b: "피자 토핑만 긁어서 5판 먹기" },
  { a: "평생 밀가루 완전히 끊기", b: "평생 고기 완전히 끊기" },
  { a: "치킨 먹을 때 치킨무/음료 금지", b: "삼겹살 먹을 때 김치/마늘 금지" },
  { a: "식당에서 음식 나오자마자 엎기", b: "다 먹고 지갑 없는 거 깨닫기" },
  { a: "팥 붕어빵에 간장 찍어 먹기", b: "슈크림 붕어빵에 초장 찍어 먹기" },
  { a: "하루 세 끼 라면만 먹기", b: "하루 세 끼 샐러드만 먹기" },
  { a: "매운 거 먹고 뜨거운 물 마시기", b: "느끼한 거 먹고 미지근한 우유 마시기" },
  { a: "햄버거 빵 없이 패티만 먹기", b: "패티 없이 빵만 먹기" },
  { a: "수육, 국밥 절대 안 먹기", b: "구운 삼겹살 절대 안 먹기" },
  { a: "혼자서 고깃집 4인분 구워 먹기", b: "패밀리 레스토랑에서 혼자 칼질하기" },
  { a: "라면 끓일 때 스프 먼저", b: "라면 끓일 때 면 먼저" },
  { a: "카레에 밥 비벼 먹기", b: "밥에 카레 비벼 먹기" },
  { a: "식사 직후 바로 양치질하기", b: "식사 후 3시간 뒤에 양치질하기" }
];

const MENU_CATEGORIES = {
  "한식": ["김치찌개", "된장찌개", "제육볶음", "국밥", "비빔밥", "삼겹살", "뚝배기 불고기", "보쌈"],
  "중식": ["짜장면", "짬뽕", "볶음밥", "탕수육", "마라탕", "깐풍기", "마파두부", "고추잡채"],
  "일식": ["돈까스", "초밥", "라멘", "우동", "소바", "덮밥", "텐동", "연어덮밥"],
  "양식": ["크림 파스타", "토마토 파스타", "피자", "스테이크", "수제 햄버거", "리조또", "샐러드", "그라탕"]
};

const shuffleArray = (array) => [...array].sort(() => Math.random() - 0.5);

const GameLoadingScreen = () => {
  const [gameStep, setGameStep] = useState(0);
  const [balanceList, setBalanceList] = useState([]);
  const [balanceIndex, setBalanceIndex] = useState(0);
  const [worldCupCategory, setWorldCupCategory] = useState('');
  const [worldCupItems, setWorldCupItems] = useState([]);
  const [survivor, setSurvivor] = useState('');
  const [challengerIndex, setChallengerIndex] = useState(1);

  const rotateAnim = useRef(new Animated.Value(0)).current;
  const cardScale = useRef(new Animated.Value(1)).current; 
  const cardTranslateA = useRef(new Animated.Value(0)).current; 
  const cardTranslateB = useRef(new Animated.Value(0)).current; 

  useEffect(() => {
    const shuffledQuestions = shuffleArray(BALANCE_QUESTIONS).slice(0, 5);
    setBalanceList(shuffledQuestions);
    const categories = Object.keys(MENU_CATEGORIES);
    const randomCategory = categories[Math.floor(Math.random() * categories.length)];
    const shuffledMenus = shuffleArray(MENU_CATEGORIES[randomCategory]).slice(0, 4);
    
    setWorldCupCategory(randomCategory);
    setWorldCupItems(shuffledMenus);
    setSurvivor(shuffledMenus[0]);

    Animated.loop(
      Animated.sequence([
        Animated.timing(rotateAnim, { toValue: 1, duration: 1000, useNativeDriver: true }),
        Animated.delay(500),
        Animated.timing(rotateAnim, { toValue: 0, duration: 0, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  const spin = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  const handleBalanceSelect = () => {
    if (balanceIndex < balanceList.length - 1) {
      setBalanceIndex(prev => prev + 1);
    } else {
      setGameStep(2); 
    }
  };

  const triggerCardAnimation = (type, nextSurvivor, callback) => {
    cardTranslateA.setValue(0);
    cardTranslateB.setValue(0);
    cardScale.setValue(1);
    Animated.parallel([
      Animated.sequence([
        Animated.timing(cardScale, { toValue: 1.1, duration: 150, useNativeDriver: true }),
        Animated.timing(cardScale, { toValue: 1, duration: 100, useNativeDriver: true }),
      ]),
      Animated.timing(type === 'A' ? cardTranslateB : cardTranslateA, {
        toValue: type === 'A' ? 500 : -500, 
        duration: 250,
        useNativeDriver: true,
      }),
    ]).start(() => {
      callback(); 
      if (type === 'A' ? cardTranslateB : cardTranslateA) {
        (type === 'A' ? cardTranslateB : cardTranslateA).setValue(0); 
      }
    });
  };

  const handleWorldCupSelect = (type, selectedMenu) => {
    const isGameOver = challengerIndex >= 3;
    triggerCardAnimation(type, selectedMenu, () => {
      if (!isGameOver) {
        setSurvivor(selectedMenu);
        setChallengerIndex(prev => prev + 1);
      } else {
        setSurvivor(selectedMenu);
        setGameStep(3); 
      }
    });
  };

  if (balanceList.length === 0) return null;

  return (
    <SafeAreaView style={styles.overlay}>
      <View style={styles.container}>
        {gameStep === -1 && (
          <View style={styles.standardLoadingArea}>
            <ActivityIndicator size="large" color="#6366F1" />
            <Text style={styles.standardLoadingText}>취향과 날씨를{"\n"}정밀 분석 중입니다...🐣</Text>
          </View>
        )}

        {gameStep === 0 && (
          <View style={styles.promptArea}>
            <Animated.View style={{ transform: [{ rotate: spin }] }}>
              <MaterialCommunityIcons name="timer-sand" size={48} color="#6366F1" />
            </Animated.View>
            <Text style={styles.promptTitle}>AI 정밀 분석 중...</Text>
            <Text style={styles.promptSub}>
              맞춤 메뉴를 찾기 위해 약 40초가 소요됩니다.{"\n"}
              기다리시는 동안 가벼운 미니 게임 어떠신가요?
            </Text>
            <View style={styles.btnRow}>
              <TouchableOpacity style={styles.declineBtn} onPress={() => setGameStep(-1)}>
                <Text style={styles.declineBtnText}>그냥 대기할게요</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.acceptBtn} onPress={() => setGameStep(1)}>
                <Text style={styles.acceptBtnText}>미니게임 시작 🎮</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {/* [MOD]: 게임 헤더 디자인 퀄리티 강화 */}
        {(gameStep === 1 || gameStep === 2) && (
          <View style={styles.header}>
            <Text style={styles.subTitle}>메추리 AI 분석 대기 중</Text>
            <View style={styles.titleWrapper}>
              <Text style={styles.miniTag}>미니 게임</Text>
              <Text style={styles.mainTitle}>
                {gameStep === 1 ? "미각 밸런스 게임" : `${worldCupCategory} 월드컵`}
              </Text>
            </View>
          </View>
        )}

        {gameStep === 1 && (
          <View style={styles.gameArea}>
            <Text style={styles.roundText}>Round {balanceIndex + 1} / 5</Text>
            <TouchableOpacity style={styles.cardA} onPress={handleBalanceSelect} activeOpacity={0.7}>
              <Text style={styles.cardText}>{balanceList[balanceIndex].a}</Text>
            </TouchableOpacity>
            <Text style={styles.vsText}>VS</Text>
            <TouchableOpacity style={styles.cardB} onPress={handleBalanceSelect} activeOpacity={0.7}>
              <Text style={styles.cardText}>{balanceList[balanceIndex].b}</Text>
            </TouchableOpacity>
          </View>
        )}

        {gameStep === 2 && (
          <View style={styles.gameArea}>
            <Text style={styles.roundText}>결승전 진출자를 가려라! ({challengerIndex}/3)</Text>
            <Animated.View style={[styles.cardWrapper, { transform: [{ translateX: cardTranslateA }, { scale: (survivor && cardScale) || 1 }] }]}>
              <TouchableOpacity style={styles.cardA} onPress={() => handleWorldCupSelect('A', survivor)} activeOpacity={0.7}>
                <Text style={styles.cardText}>{survivor}</Text>
              </TouchableOpacity>
            </Animated.View>
            <Text style={styles.vsText}>VS</Text>
            <Animated.View style={[styles.cardWrapper, { transform: [{ translateX: cardTranslateB }, { scale: (survivor && cardScale) || 1 }] }]}>
              <TouchableOpacity style={styles.cardB} onPress={() => handleWorldCupSelect('B', worldCupItems[challengerIndex])} activeOpacity={0.7}>
                <Text style={styles.cardText}>{worldCupItems[challengerIndex]}</Text>
              </TouchableOpacity>
            </Animated.View>
          </View>
        )}

        {gameStep === 3 && (
          <View style={styles.resultArea}>
            <View style={styles.menuNameContainer}>
              <LottieView
                source={require('../assets/animations/Confetti.json')}
                autoPlay
                loop
                style={styles.lottieAnimation}
              />
              <Text style={styles.gameResultTitle}>🏆 미니 게임 결과</Text>
              <Text style={styles.resultMenuText}>{survivor}</Text>
            </View>
            <Text style={styles.resultSubText}>
              잠시 후 취향분석 메뉴추천 결과가 나타납니다!
            </Text>
            <ActivityIndicator size="large" color="#6366F1" style={{ marginTop: 30 }} />
          </View>
        )}
      </View>
    </SafeAreaView>
  );
};

export default GameLoadingScreen;