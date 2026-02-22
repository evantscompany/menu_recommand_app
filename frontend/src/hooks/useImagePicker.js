import { useState } from 'react';
import * as ImagePicker from 'expo-image-picker';
import { Alert } from 'react-native';

export const useImagePicker = () => {
  const [image, setImage] = useState(null);

  const pickImage = async () => {
    // 앨범 권한 요청
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    
    if (status !== 'granted') {
      Alert.alert("권한 거부", "사진을 선택하려면 앨범 권한이 필요합니다.");
      return null;
    }

    // 이미지 선택기 실행
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.7, // 서버 업로드를 고려해 화질을 살짝 조정
    });

    if (!result.canceled) {
      const selectedUri = result.assets[0].uri;
      setImage(selectedUri);
      return selectedUri;
    }
    return null;
  };

  return { image, setImage, pickImage };
};